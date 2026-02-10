

from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity


class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.
        `self.engine` is the scope this action is being performed in.
        `self.entity` is the object performing the action.
        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self) -> None:
        raise SystemExit()

class WaitAction(Action):
    def perform(self) -> None:
        pass

class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Returns this actions destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return the blocking entity at this actions destination.."""
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError()

class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            return  # No entity to attack.
        attacker = self.entity
        player = self.engine.player

        # Determine the Might values for the clash
        if attacker is player:
            attack_might = attacker.fighter.valor.roll()
            target_might = target.fighter.might
        elif target is player:
            attack_might = attacker.fighter.might
            target_might = target.fighter.valor.roll()
        else:
            # NPC vs NPC (if applicable)
            attack_might = attacker.fighter.might
            target_might = target.fighter.might

        result = attack_might - target_might

        # Handle outcome
        if result == 0:
            print(
                f"{attacker.name.capitalize()} ({attack_might}) ties its clash against {target.name} ({target_might}).")
            return

        # Identify winner and loser
        if result > 0:
            winner, loser = attacker, target
            margin = result
        else:
            winner, loser = target, attacker
            margin = abs(result)

        # Describe damage.
        if loser is player:
            damage_desc = "damaging their Valor"
        else:
            damage_desc = f"dealing {margin} damage"

        print(f"{winner.name.capitalize()} ({max(attack_might, target_might)}) wins the clash against "
              f"{loser.name} ({min(attack_might, target_might)}), {damage_desc}.")

        # Apply damage to loser
        if loser is player:
            loser.fighter.reduce_die(loser.fighter.valor)
        else:
            loser.fighter.might -= margin

class MovementAction(ActionWithDirection):

    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds.
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Destination is blocked by a tile.
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return  # Destination is blocked by an entity.
        self.entity.move(self.dx, self.dy)

class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()