from abc import ABC, abstractmethod
from tkinter import Canvas
import re
import json


def is_color(text):
    return bool(re.match(r'#[0-9A-Fa-f]{6}', text))


class BaseDrawSettings:
    __slots__ = [
        'border_width',
        'border_color',
        'fill_color'
    ]

    def __init__(self, bw=1, bc='#000000', fc='#FFFFFF'):
        self.border_width = bw
        self.border_color = bc
        self.fill_color = fc

    @staticmethod
    def from_dict(data):
        assert all(v in data for v in ['bw', 'bc', 'fc'])
        assert is_color(data['bc'])
        assert is_color(data['fc'])
        assert type(data['bw']) is int
        return BaseDrawSettings(**data)

    @abstractmethod
    def to_dict(self):
        return {
            'bw': self.border_width,
            'bc': self.border_color,
            'fc': self.fill_color
        }


class BaseFigure(ABC):

    __slots__ = ['figure_type']

    def __init__(self, tag):
        self.figure_type = tag

    @abstractmethod
    def contains(self, x, y):
        pass

    @abstractmethod
    def move(self, dx, dy):
        pass

    @abstractmethod
    def draw(self, canvas: Canvas):
        pass

    @staticmethod
    @abstractmethod
    def tag():
        pass

    @abstractmethod
    def to_str(self):
        pass

    @staticmethod
    @abstractmethod
    def from_str(text):
        pass


class RectBoundedFigure(BaseFigure, ABC):
    __slots__ = [
        'x0', 'y0',
        'x1', 'y1',
        'draw_settings'
    ]

    def __init__(self, tag, x0, y0, x1, y1, draw_settings):
        super().__init__(tag)
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.draw_settings = draw_settings

    def contains(self, x, y):
        return (
                min(self.x0, self.x1) <= x <= max(self.x0, self.x1) and
                min(self.y0, self.y1) <= y <= max(self.y0, self.y1)
        )

    def move(self, dx, dy):
        self.x0 += dx
        self.y0 += dy
        self.x1 += dx
        self.y1 += dy

    @classmethod
    def from_str(cls, text):
        data = json.loads(text)
        assert all(k in ['x0', 'x1', 'y0', 'y1', 'ds'] for k in data.keys())
        assert all(v in data and type(data[v]) is int for v in ['x0', 'x1', 'y0', 'y1'])
        ds = data.get('ds', None)
        return cls(
            data['x0'], data['y0'],
            data['x1'], data['y1'],
            ds and BaseDrawSettings.from_dict(ds)
        )

    def to_str(self):
        data_str = json.dumps({
            'x0': self.x0,
            'y0': self.y0,
            'x1': self.x1,
            'y1': self.y1,
            'ds': self.draw_settings.to_dict()
        })
        return f'{self.tag()}: {data_str}'


class RectFigure(RectBoundedFigure):

    def __init__(self, x0, y0, x1, y1, draw_settings=None):
        super().__init__(RectFigure.tag(), x0, y0, x1, y1, draw_settings or BaseDrawSettings())

    @staticmethod
    def tag():
        return 'rect'

    def draw(self, canvas: Canvas):
        return canvas.create_rectangle(
            self.x0, self.y0, self.x1, self.y1,
            width=self.draw_settings.border_width,
            fill=self.draw_settings.fill_color,
            outline=self.draw_settings.border_color
        )


class OvalFigure(RectBoundedFigure):

    def __init__(self, x0, y0, x1, y1, draw_settings=None):
        super().__init__(OvalFigure.tag(), x0, y0, x1, y1, draw_settings or BaseDrawSettings())

    @staticmethod
    def tag():
        return 'oval'

    def draw(self, canvas: Canvas):
        return canvas.create_oval(
            self.x0, self.y0, self.x1, self.y1,
            width=self.draw_settings.border_width,
            fill=self.draw_settings.fill_color,
            outline=self.draw_settings.border_color
        )


def parse(text):
    lines = text.split('\n')
    supported_figures = [RectFigure, OvalFigure]
    parse_options = dict((fig.tag(), fig.from_str) for fig in supported_figures)
    ret = []
    tags = '|'.join(parse_options.keys())
    reg_parser = re.compile(rf'(?P<tag>(?:{tags}))\s*:\s*(?P<text>.+)$')
    for line_idx, line in enumerate(lines):
        if not line.split():
            continue
        match = reg_parser.match(line)
        if not match:
            ret.append((line_idx, None))
            continue
        info = match.groupdict()
        try:
            ret.append((line_idx, parse_options[info['tag']](info['text'])))
        except:
            ret.append((line_idx, None))
    return ret
