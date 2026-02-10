from __future__ import annotations
from typing import TYPE_CHECKING
import color
from components.base_component import BaseComponent
from input_handlers import GameOverEventHandler
from render_order import RenderOrder

if TYPE_CHECKING:
    from entity import Actor

class Fighter(BaseComponent):
    parent: Actor
    def __init__(self, might: int = None, clarity=None, endurance=None, faith=None, grace=None, valor=None):
        self.max_might = might
        self._might = might
        self.clarity = clarity
        self.endurance = endurance
        self.faith = faith
        self.grace = grace
        self.valor = valor

    @property
    def might(self) -> int:
        return self._might

    @might.setter
    def might(self, value: int) -> None:
        self._might = max(0, min(value, self.max_might))

        if self.parent is not self.engine.player and self._might > 0:
            self.parent.char = str(self._might)
            # TODO: find a way to graphically represent Might of 10 or higher
        if self._might == 0 and self.parent.ai:
            self.die()

    def reduce_die(self, die) -> None:
        if die is None:
            return

        if die.chain[die.index] <= 2:
            self.die()
        else:
            die.downgrade()

    def die(self) -> None:
        if self.engine.player is self.parent:
            death_message = "You die..."
            death_message_color = color.player_die
            self.engine.event_handler = GameOverEventHandler(self.engine)
        else:
            death_message = f"The {self.parent.name} dies."
            death_message_color = color.enemy_die

        self.parent.char = "%"
        self.parent.color = (191, 0, 0)
        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.name = f"remains of {self.parent.name}"
        self.parent.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(death_message, death_message_color)