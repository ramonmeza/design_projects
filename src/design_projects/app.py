import pyray as rl

from .config import TICK_RATE, WINDOW_HEIGHT, WINDOW_WIDTH
from .core import DrawAPI, Project, Renderer, Window
from .factory import (
    Projects,
    create_draw_api,
    create_project,
    create_renderer,
    create_window,
)
from .utils import capitalize_each_word


class App:
    def __init__(self, project: Projects) -> None:
        self.window: Window = create_window()
        self.renderer: Renderer = create_renderer()
        self.draw_api: DrawAPI = create_draw_api()
        self.project_name: str = capitalize_each_word(project.name.replace("_", " "))
        self.current_project: Project = create_project(project)
        self.fixed_update_interval: float = 1.0 / TICK_RATE
        self.fixed_update_stopwatch: float = 0.0

    def startup(self) -> None:
        project_name: str = self.project_name
        self.window.open(WINDOW_WIDTH, WINDOW_HEIGHT, project_name)

    def shutdown(self) -> None:
        self.window.close()

    def update(self) -> None:
        delta_time: float = rl.get_frame_time()
        self.fixed_update_stopwatch += delta_time

        while self.fixed_update_stopwatch >= self.fixed_update_interval:
            self.current_project.on_fixed_update(self.fixed_update_interval)
            self.fixed_update_stopwatch -= self.fixed_update_interval

        self.current_project.on_update(delta_time)

    def render(self) -> None:
        self.renderer.begin_frame()
        self.current_project.on_draw(self.draw_api)
        self.renderer.end_frame()

    def run(self) -> None:
        self.startup()
        try:
            while self.window.is_open():
                self.update()
                self.render()
        finally:
            self.shutdown()
