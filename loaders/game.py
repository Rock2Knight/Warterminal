from loguru import logger

from loaders.model_loader import ModelLoader

class GameLoader(ModelLoader):

    @classmethod
    async def create(cls, **kwargs):
        pass
        
    @classmethod
    async def update(cls, **kwargs):
        match kwargs['method']:
            case 'put':
                pass
            case 'patch':
                pass

    @classmethod
    async def delete(cls, **kwargs):
        pass