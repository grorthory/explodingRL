from __future__ import annotations
from typing import Optional, Tuple, TYPE_CHECKING
import color
import exceptions
if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity, Item


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

class PickupAction(Action):
    """Pickup an item and add it to the inventory, if there is room for it."""

    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        actor_location_x = self.entity.x
        actor_location_y = self.entity.y
        inventory = self.entity.inventory

        for item in self.engine.game_map.items:
            if actor_location_x == item.x and actor_location_y == item.y:
                if len(inventory.items) >= inventory.capacity:
                    raise exceptions.Impossible("Your inventory is full.")

                self.engine.game_map.entities.remove(item)
                item.parent = self.entity.inventory
                inventory.items.append(item)

                self.engine.message_log.add_message(f"You picked up the {item.name}!")
                return

        raise exceptions.Impossible("There is nothing here to pick up.")


class ItemAction(Action):
    def __init__(
        self, entity: Actor, item: Item, target_xy: Optional[Tuple[int, int]] = None
    ):
        super().__init__(entity)
        self.item = item
        if not target_xy:
            target_xy = entity.x, entity.y
        self.target_xy = target_xy

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.target_xy)

    def perform(self) -> None:
        """Invoke the items ability, this action will be given to provide context."""
        self.item.consumable.activate(self)

class DropItem(ItemAction):
    def perform(self) -> None:
        self.entity.inventory.drop(self.item)

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
            raise exceptions.Impossible("Nothing to attack.")

        attacker = self.entity
        player = self.engine.player

        atk_detail = ""
        def_detail = ""

        # --- 1. CALCULATE ATTACKER MIGHT ---
        if attacker is player:
            # Overkill threshold: Enemy Might x2
            threshold = target.fighter.might + target.fighter.might
            val, new_luck, history = attacker.fighter.die.luckyroll(attacker.fighter.luck, threshold)
            attacker.fighter.luck = new_luck
            attack_might = val
            atk_detail = f"[{' + '.join(history)}]"
        else:
            attack_might = attacker.fighter.might

        # --- 2. CALCULATE DEFENDER MIGHT ---
        if target is player:
            # Overkill threshold: Attacker Might x2
            threshold = attacker.fighter.might + attacker.fighter.might
            val, new_luck, history = target.fighter.die.luckyroll(target.fighter.luck, threshold)
            target.fighter.luck = new_luck
            target_might = val
            def_detail = f"[{' + '.join(history)}]"
        else:
            target_might = target.fighter.might

        # --- 3. PREPARE DISPLAY STRINGS ---
        # We build these here so they can be used for both ties and wins
        atk_str = f"{attacker.name.capitalize()} ({attack_might}{atk_detail})"
        def_str = f"{target.name} ({target_might}{def_detail})"

        # --- 4. RESOLVE CLASH ---
        result = attack_might - target_might
        attack_color = color.player_atk if attacker is player else color.enemy_atk

        if result == 0:
            # Now ties include the full history strings!
            self.engine.message_log.add_message(
                f"{atk_str} ties against {def_str}.", color.white
            )
            return

        # Determine winner/loser for non-ties
        if result > 0:
            winner_name = attacker.name
            loser = target
            margin = result
        else:
            winner_name = target.name
            loser = attacker
            margin = abs(result)

        # Final victory message
        self.engine.message_log.add_message(
            f"{atk_str} vs {def_str}: {winner_name.capitalize()} wins by {margin}!",
            attack_color
        )

        loser.fighter.take_damage(margin)

class MovementAction(ActionWithDirection):

    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            # Destination is out of bounds.
            raise exceptions.Impossible("That way is blocked.")
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            # Destination is blocked by a tile.
            raise exceptions.Impossible("That way is blocked.")
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            # Destination is blocked by an entity.
            raise exceptions.Impossible("That way is blocked.")
        self.entity.move(self.dx, self.dy)

class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()