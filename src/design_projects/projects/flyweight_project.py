from __future__ import annotations

from importlib.resources import files
from random import randint
from typing import ClassVar, Protocol, Self, cast

import pyray as rl

from ..config import WINDOW_HEIGHT, WINDOW_WIDTH
from ..core import Color, DrawAPI, Project

PER_SPAWN: int = 10
TEXTURE_PATH: str = str(
    files("design_projects").joinpath("assets", "textures", "cool.png")
)


class Tree(Protocol):
    def __init__(self, x: int, y: int, texture_path: str) -> None: ...
    def unload(self) -> None: ...

    x: int
    y: int
    texture: rl.Texture


class TreeHeavyImpl(Tree):
    """
    Each instance of TreeHeavyImpl manages it's own texture's life-cycle and
    position.
    """

    def __init__(self, x: int, y: int, texture_path: str) -> None:
        self.x: int = x
        self.y: int = y
        self.texture = rl.load_texture(texture_path)  # type: ignore

    def unload(self) -> None:
        rl.unload_texture(self.texture)  # type: ignore


class TreeLightImpl(Tree):
    """
    Each instance of TreeLightImpl only knows it's own position. It uses a class
    variable to hold the single texture shared between instances.
    """

    _texture: ClassVar[rl.Texture | None] = None
    _num_instances: int = 0

    def __new__(cls, x: int, y: int, texture_path: str) -> Self:
        if cls._texture is None:
            cls._texture = rl.load_texture(texture_path)

        instance: Self = super().__new__(cls)
        cls._num_instances += 1
        return instance

    def __init__(self, x: int, y: int, texture_path: str) -> None:
        self.x: int = x
        self.y: int = y
        self.texture: rl.Texture = cast(rl.Texture, TreeLightImpl._texture)

    def unload(self) -> None:
        TreeLightImpl._num_instances -= 1

        if TreeLightImpl._texture is None or TreeLightImpl._num_instances > 0:
            return

        rl.unload_texture(TreeLightImpl._texture)  # type: ignore


class FlyweightProject(Project):
    def __init__(self) -> None:
        self.fps: float = 0.0
        self.current_tree_impl: type[Tree] = TreeHeavyImpl
        self.trees: list[Tree] = []
        self.ui_text: str = ""

    def on_update(self, delta_time: float) -> None:
        self.update_fps_counter(delta_time)

        if rl.is_key_down(rl.KeyboardKey.KEY_EQUAL):
            self.spawn_tree()
        elif rl.is_key_down(rl.KeyboardKey.KEY_MINUS):
            self.despawn_tree()

        if rl.is_key_pressed(rl.KeyboardKey.KEY_SPACE):
            self.clear_trees()
            self.change_tree_impl()

        self.update_ui_text()

    def update_fps_counter(self, delta_time: float) -> None:
        if delta_time == 0.0:
            return
        self.fps = 1 / delta_time

    def spawn_tree(self) -> None:
        for _ in range(PER_SPAWN):
            x: int = randint(0, WINDOW_WIDTH)
            y: int = randint(0, WINDOW_HEIGHT)
            tree: Tree = self.current_tree_impl(x, y, TEXTURE_PATH)
            self.trees.append(tree)

    def despawn_tree(self) -> None:
        if len(self.trees) == 0:
            return

        tree: Tree = self.trees.pop()
        tree.unload()

    def clear_trees(self) -> None:
        for tree in self.trees:
            tree.unload()
        self.trees.clear()

    def change_tree_impl(self) -> None:
        if self.current_tree_impl is TreeHeavyImpl:
            self.current_tree_impl = TreeLightImpl
        elif self.current_tree_impl is TreeLightImpl:
            self.current_tree_impl = TreeHeavyImpl

    def update_ui_text(self) -> None:
        self.ui_text = "\n".join(
            [
                f"FPS: {self.fps:.0f}",
                f"Num Cool Guys: {len(self.trees)}",
                f"Cool Guy Type: {self.current_tree_impl.__name__}",
                "",
                "CONTROLS",
                "+ to add Cool Guys",
                "- to remove Cool Guys",
                "SPACE to change Cool Guy type",
            ]
        )

    def on_draw(self, drawer: DrawAPI) -> None:
        drawer.fill()
        self.draw_trees(drawer)
        self.draw_ui(drawer)

    def draw_trees(self, drawer: DrawAPI) -> None:
        for tree in self.trees:
            rl.draw_texture(tree.texture, tree.x, tree.y, (255, 255, 255, 255))  # type: ignore

    def draw_ui(self, drawer: DrawAPI) -> None:
        font_size: int = 16
        x: int = 10
        y: int = 10
        padding = 5
        size = rl.measure_text_ex(rl.get_font_default(), self.ui_text, font_size, 1.0)  # type: ignore

        drawer.draw_rect(
            x,
            y,
            int(size.x + padding * 2),
            int(size.y + padding * 2),
            Color(120, 120, 120, 240),
        )
        drawer.draw_text(
            self.ui_text, x + padding, y + padding, font_size, Color(g=255)
        )

    def on_fixed_update(self, interval: float) -> None:
        pass
