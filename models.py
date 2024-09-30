from tortoise.models import Model
from tortoise import fields

from loaders.model_loader import ModelLoader


class Army(ModelLoader):
    # Армия
    name = fields.CharField(max_length=255)
    count = fields.IntField()
    is_fail = fields.BooleanField(default=False)
    fight_with_id = fields.IntField(null=True, default=None)

    def __str__(self):
        return self.name


class AbstractUnit(ModelLoader):
    # Абстрактный воин
    army = fields.ForeignKeyField('models.Army', related_names='units')  # Войско
    health = fields.FloatField(default=100.00, null=True)
    damage = fields.FloatField(default=10.00, null=True)
    defense = fields.FloatField(default=50.00, null=True)
    x_coord = fields.FloatField(null=True)
    y_coord = fields.FloatField(null=True)

    class Meta:
        abstract = True


class Warrior(AbstractUnit):
    # Воин
    radius_dmg = fields.IntField(default=10, null=True)
    base_speed = fields.IntField(default=2, null=True)
    dmg_coef = fields.FloatField(default=1.5, null=True)


class Archer(AbstractUnit):
    # Лучник
    radius_dmg = fields.IntField(default=10, null=True)
    base_speed = fields.IntField(default=2, null=True)
    dmg_coef = fields.FloatField(default=1.5, null=True)


class Varvar(AbstractUnit):
    # Варвар
    radius_dmg = fields.IntField(default=8, null=True)
    base_speed = fields.IntField(default=2, null=True)
    dmg_coef = fields.FloatField(default=2.5, null=True)