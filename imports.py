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

from database.db import DB_CONFIG

from dto.game_dto import *
from dto.army_dto import ArmyDto
from dto.warrior_dto import WarriorDto
from dto.archer_dto import ArcherDto
from dto.varvar_dto import VarvarDto

from models import *
from controllers import *
import crud