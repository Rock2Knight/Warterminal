from tortoise.models import Model
from tortoise import fields

class UnitType(Model):
    # Тип юнита
    id = fields.IntField(primary_key=True)
    radius_dmg = fields.FloatField()
    name = fields.CharField(max_length=255)
    crit_coef = fields.FloatField()

    def __str__(self):
        return self.name


class Army(Model):
    # Армия
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    count = fields.IntField()
    is_fail = fields.BooleanField(default=False)

    def __str__(self):
        return self.name


class Unit(Model):
    # Юнит
    id = fields.IntField(primary_key=True)
    typeunit =  fields.ForeignKeyField('models.UnitType', related_names='units')  # Тип игрока
    army = fields.ForeignKeyField('models.Army', related_names='units')  # Войско
    health = fields.FloatField(default=100.00)
    damage = fields.FloatField(default=10.00)
    defense = fields.FloatField(default=50.00)
    x_coord = fields.FloatField()
    y_coord = fields.FloatField()