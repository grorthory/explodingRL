from components.ai import HostileEnemy
from components.fighter import Fighter
from entity import Actor
from dice import Dice

player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    fighter=Fighter(clarity=Dice(5),
                    endurance=Dice(5),
                    faith=Dice(5),
                    grace=Dice(5),
                    valor=Dice(5)),
)

orc = Actor(
    char="3",
    color=(63, 127, 63),
    name="Orc",
    ai_cls=HostileEnemy,
    fighter=Fighter(might=3),
)
troll = Actor(
    char="5",
    color=(0, 127, 0),
    name="Troll",
    ai_cls=HostileEnemy,
    fighter=Fighter(might=5),
)