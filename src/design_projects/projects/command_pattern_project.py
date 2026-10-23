from ..core import DrawAPI, Project


class CommandPatternProject(Project):
    def on_update(self, delta_time: float) -> None:
        pass

    def on_fixed_update(self, interval: float) -> None:
        pass

    def on_draw(self, drawer: DrawAPI) -> None:
        pass
