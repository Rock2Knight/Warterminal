import sys
import asyncio
print(sys.path)

import models
from . import army as army_crud

async def get_army():
    test_army = Army(
        id=3,
        name="Aliance",
        count=6,
        is_fail=False,
        fight_with_id=None
    )
    real_army = await army_crud.get_army_by_id(3)
    print(real_army)
    #assert test_army == real_army

async def main():
    await get_army()

if __name__ == "__main__":
    asyncio.run(main())