from flask_sqlalchemy import SQLAlchemy
from enum import Enum

db = SQLAlchemy()

class PlayerClass(Enum):
    WARRIOR = 'Воин'
    ROGUE = 'Разбойник'
    MAGE = 'Маг'

class PlayerRace(Enum):
    HUMAN = 'Человек'
    ORC = 'Орк'
    ELF = 'Эльф'
    FOREST_ELF = 'Лесной Эльф'
    CHUPACABRA = 'Чупакабра'

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    race = db.Column(db.String(50), nullable=False)
    player_class = db.Column(db.String(50), nullable=False)
    level = db.Column(db.Integer, default=1)
    health = db.Column(db.Integer, default=100)
    energy = db.Column(db.Integer, nullable=True)
    mana = db.Column(db.Integer, nullable=True)
    gold = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Player {self.name}, Race: {self.race}, Class: {self.player_class}>"
