from __future__ import annotations
from typing import TYPE_CHECKING
from components.base_component import BaseComponent
from input_handlers import GameOverEventHandler
from render_order import RenderOrder

if TYPE_CHECKING:
    from entity import Actor

class Fighter(BaseComponent):
    entity: Actor
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

        if self.entity is not self.engine.player and self._might > 0:
            self.entity.char = str(self._might)
            # TODO: find a way to graphically represent Might of 10 or higher
        if self._might == 0 and self.entity.ai:
            self.die()

    def reduce_die(self, die) -> None:
        if die is None:
            return

        if die.chain[die.index] <= 2:
            self.die()
        else:
            die.downgrade()

    def die(self) -> None:
        if self.engine.player is self.entity:
            death_message = "You died!"
            self.engine.event_handler = GameOverEventHandler(self.engine)
        else:
            death_message = f"The {self.entity.name} dies."

        self.entity.char = "%"
        self.entity.color = (191, 0, 0)
        self.entity.blocks_movement = False
        self.entity.ai = None
        self.entity.name = f"remains of {self.entity.name}"
        self.entity.render_order = RenderOrder.CORPSE

        print(death_message)