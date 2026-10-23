from abc import ABC, abstractmethod
from dataclasses import dataclass

import pyray as rl

from ..core import Color, DrawAPI, Project


@dataclass
class Actor:
    x: int = 0
    y: int = 0


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def undo(self) -> None:
        raise NotImplementedError


class MoveCommand(Command):
    def __init__(self, actor: Actor, dx: int = 0, dy: int = 0) -> None:
        self.actor: Actor = actor
        self.dx: int = dx
        self.dy: int = dy

    def execute(self) -> None:
        self.actor.x += self.dx
        self.actor.y += self.dy

    def undo(self) -> None:
        self.actor.x -= self.dx
        self.actor.y -= self.dy


MOVE_SPEED: int = 50

EXECUTED_COMMANDS_BUFFER_SIZE: int = 20


class CommandPatternProject(Project):
    def __init__(self) -> None:
        self.command_queue: list[Command] = []
        self.executed_commands: list[Command] = []
        self.player: Actor = Actor()

    def on_update(self, delta_time: float) -> None:
        if rl.is_key_pressed(rl.KeyboardKey.KEY_W):
            self.command_queue.append(MoveCommand(self.player, dy=-MOVE_SPEED))
        if rl.is_key_pressed(rl.KeyboardKey.KEY_S):
            self.command_queue.append(MoveCommand(self.player, dy=MOVE_SPEED))
        if rl.is_key_pressed(rl.KeyboardKey.KEY_A):
            self.command_queue.append(MoveCommand(self.player, dx=-MOVE_SPEED))
        if rl.is_key_pressed(rl.KeyboardKey.KEY_D):
            self.command_queue.append(MoveCommand(self.player, dx=MOVE_SPEED))

        if rl.is_key_pressed(rl.KeyboardKey.KEY_Z) and len(self.executed_commands) > 0:
            self.command_queue.clear()
            command: Command = self.executed_commands.pop()
            command.undo()

        if len(self.executed_commands) > EXECUTED_COMMANDS_BUFFER_SIZE:
            self.executed_commands.pop(0)

    def on_fixed_update(self, interval: float) -> None:
        if len(self.command_queue) == 0:
            return

        for cmd in self.command_queue:
            cmd.execute()
            self.executed_commands.append(cmd)

        self.command_queue.clear()

    def on_draw(self, drawer: DrawAPI) -> None:
        drawer.fill()
        drawer.draw_circle(self.player.x, self.player.y, 10.0, Color(0, 0, 255, 255))
