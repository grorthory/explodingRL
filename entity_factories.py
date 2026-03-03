from components.ai import HostileEnemy
from components import consumable
from components.fighter import Fighter
from components.inventory import Inventory
from entity import Actor, Item
from dice import Dice

player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    fighter=Fighter(die=Dice(0), die_max=Dice(0), luck = 1),
    inventory=Inventory(capacity=26),
)

rat = Actor(
    char="2",
    color=(63, 127, 63),
    name="Rat",
    ai_cls=HostileEnemy,
    fighter=Fighter(might=2),
    inventory=Inventory(capacity=0),
)

goblin = Actor(
    char="3",
    color=(63, 127, 63),
    name="Goblin",
    ai_cls=HostileEnemy,
    fighter=Fighter(might=3),
    inventory=Inventory(capacity=0),
)

confusion_scroll = Item(
    char="~",
    color=(207, 63, 255),
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)

potion_of_might = Item(
    char="!",
    color=(127,0,255),
    name="Potion of Might",
    consumable=consumable.MightPotion()
)

darkbolt_scroll=Item(
    char = "~",
    color=(255, 255, 0),
    name="Scroll of Darkbolt",
    consumable=consumable.DarkBoltScroll(damage=8, maximum_range=5),
)

fireball_scroll = Item(
    char="~",
    color=(255, 0, 0),
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)