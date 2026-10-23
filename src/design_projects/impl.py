import pyray as rl

from .core import Color


class RaylibWindow:
    def open(self, width: int, height: int, title: str) -> None:
        rl.init_window(width, height, title)

    def is_open(self) -> bool:
        return not rl.window_should_close()

    def close(self) -> None:
        rl.close_window()


class RaylibRenderer:
    def begin_frame(self) -> None:
        rl.begin_drawing()

    def end_frame(self) -> None:
        rl.end_drawing()


class RaylibDrawAPI:
    def fill(self, color: Color | None = None) -> None:
        if color is None:
            color = Color(0, 0, 0, 255)
        rl.clear_background(tuple(color))  # type: ignore

    def draw_circle(self, x: int, y: int, r: float, color: Color) -> None:
        rl.draw_circle(x, y, r, tuple(color))  # type: ignore

    def draw_rect(self, x: int, y: int, w: int, h: int, color: Color) -> None:
        rl.draw_rectangle(x, y, w, h, tuple(color))  # type: ignore

    def draw_text(
        self, text: str, x: int, y: int, font_size: int = 20, color: Color | None = None
    ) -> None:
        if color is None:
            color = Color(255, 255, 255, 255)
        rl.draw_text(text, x, y, font_size, tuple(color))  # type: ignore
