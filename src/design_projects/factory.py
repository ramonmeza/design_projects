from enum import IntEnum, auto

from .core import DrawAPI, Project, Renderer, Window


class Backends(IntEnum):
    RAYLIB = 0


class Projects(IntEnum):
    UPDATE_SYSTEM = 0
    COMMAND_PATTERN = auto()


def create_draw_api(backend: Backends = Backends.RAYLIB) -> DrawAPI:
    match backend:
        case Backends.RAYLIB:
            from .impl import RaylibDrawAPI

            return RaylibDrawAPI()
        case _:
            raise NotImplementedError


def create_project(project: Projects) -> Project:
    match project:
        case Projects.UPDATE_SYSTEM:
            from .projects.update_system_project import UpdateSystemProject

            return UpdateSystemProject()

        case Projects.COMMAND_PATTERN:
            from .projects.command_pattern_project import CommandPatternProject

            return CommandPatternProject()

        case _:
            raise NotImplementedError


def create_renderer(backend: Backends = Backends.RAYLIB) -> Renderer:
    match backend:
        case Backends.RAYLIB:
            from .impl import RaylibRenderer

            return RaylibRenderer()
        case _:
            raise NotImplementedError


def create_window(backend: Backends = Backends.RAYLIB) -> Window:
    match backend:
        case Backends.RAYLIB:
            from .impl import RaylibWindow

            return RaylibWindow()
        case _:
            raise NotImplementedError
