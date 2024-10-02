import random
import sys
import json
import asyncio
import math
import time
from contextlib import asynccontextmanager

from logging import StreamHandler
from loguru import logger

from pydantic import BaseModel
from fastapi import FastAPI
from tortoise.exceptions import IntegrityError
from tortoise.transactions import atomic
from tortoise import Tortoise, run_async
from tortoise.contrib.fastapi import register_tortoise

from fastapi import HTTPException, Response, status

from database.db import DB_CONFIG

from access.archer import access_archer
from access.army import access_army
from access.game import access_game
from access.warrior import access_warrior
from access.varvar import access_varvar

from dto.base_schema import Point
from dto.game_dto import *
from dto.army_dto import ArmyDto
from dto.warrior_dto import WarriorDto
from dto.archer_dto import ArcherDto
from dto.varvar_dto import VarvarDto

from views.fight import Fight

from models import *
#from controllers import *
import crud