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
    fighter=Fighter(clarity=Dice(2),
                    endurance=Dice(2),
                    faith=Dice(2),
                    grace=Dice(2),
                    valor=Dice(2)),
    inventory=Inventory(capacity=26),
)

orc = Actor(
    char="2",
    color=(63, 127, 63),
    name="Goblin",
    ai_cls=HostileEnemy,
    fighter=Fighter(might=2),
    inventory=Inventory(capacity=0),
)
troll = Actor(
    char="3",
    color=(0, 127, 0),
    name="Orc",
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

potion_of_valor = Item(
    char="!",
    color=(127,0,255),
    name="Potion of Valor",
    consumable=consumable.ValorPotion()
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