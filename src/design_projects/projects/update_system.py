from ..config import TICK_RATE
from ..core import DrawAPI, Project


class UpdateSystemProject(Project):
    def __init__(self) -> None:
        self.current_tick: int = 0
        self.current_frame: int = 0
        self.fps: int = 0

    def on_update(self, delta_time: float) -> None:
        if delta_time > 0.0:
            self.fps = int(1 / delta_time)

        self.current_frame += 1

    def on_fixed_update(self, interval: float) -> None:
        self.current_tick += 1

    def on_draw(self, drawer: DrawAPI) -> None:
        drawer.fill()
        ui_text: str = "\n".join(
            [
                f"Tick Rate: {TICK_RATE}Hz",
                f"Tick: {self.current_tick}",
                f"FPS: {self.fps}",
                f"Frame: {self.current_frame}",
            ]
        )
        drawer.draw_text(ui_text, 10, 10)
