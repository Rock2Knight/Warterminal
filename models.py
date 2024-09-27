from tortoise.models import Model
from tortoise import fields


class Army(Model):
    # Армия
    #id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    count = fields.IntField()
    is_fail = fields.BooleanField(default=False)
    fight_with_id = fields.IntField(null=True, default=None)

    def __str__(self):
        return self.name


class AbstractUnit(Model):
    # Абстрактный воин
    #id = fields.IntField(primary_key=True)
    army = fields.ForeignKeyField('models.Army', related_names='units')  # Войско
    health = fields.FloatField(default=100.00)
    damage = fields.FloatField(default=10.00)
    defense = fields.FloatField(default=50.00)
    x_coord = fields.FloatField()
    y_coord = fields.FloatField()

    class Meta:
        abstract = True


class Warrior(AbstractUnit):
    # Воин
    radius_dmg = fields.IntField(default=10)
    base_speed = fields.IntField(default=2)
    dmg_coef = fields.FloatField(default=1.5)


class Archer(AbstractUnit):
    # Лучник
    radius_dmg = fields.IntField(default=10)
    base_speed = fields.IntField(default=2)
    dmg_coef = fields.FloatField(default=1.5)


class Varvar(AbstractUnit):
    # Варвар
    radius_dmg = fields.IntField(default=8)
    base_speed = fields.IntField(default=2)
    dmg_coef = fields.FloatField(default=2.5)