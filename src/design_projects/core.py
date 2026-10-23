from __future__ import annotations

from collections.abc import Generator
from dataclasses import dataclass
from typing import Protocol


@dataclass
class Color:
    r: int = 0
    g: int = 0
    b: int = 0
    a: int = 255

    def __iter__(self) -> Generator[int]:
        yield self.r
        yield self.g
        yield self.b
        yield self.a


class Window(Protocol):
    def open(self, width: int, height: int, title: str) -> None: ...
    def is_open(self) -> bool: ...
    def close(self) -> None: ...


class Renderer(Protocol):
    def begin_frame(self) -> None: ...
    def end_frame(self) -> None: ...


class DrawAPI(Protocol):
    def fill(self, color: Color | None = None) -> None: ...
    def draw_rect(self, x: int, y: int, w: int, h: int, color: Color) -> None: ...
    def draw_text(
        self, text: str, x: int, y: int, font_size: int = 20, color: Color | None = None
    ) -> None: ...


class Project(Protocol):
    def on_update(self, delta_time: float) -> None: ...
    def on_fixed_update(self, interval: float) -> None: ...
    def on_draw(self, drawer: DrawAPI) -> None: ...
