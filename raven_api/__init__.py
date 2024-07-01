from contextlib import asynccontextmanager
import tomllib
from typing import AsyncGenerator
from litestar import Litestar
from .common.models import Config, DOCUMENT_MODELS
from .util import *
from redis.asyncio import Redis
from litestar.channels import ChannelsPlugin
from litestar.channels.backends.redis import RedisChannelsPubSubBackend
from litestar.di import Provide
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from litestar.datastructures import State
from litestar.logging import LoggingConfig
from .controllers import API_ROUTER


with open("./config.toml", "rb") as config_file:
    CONFIG = Config(**tomllib.load(config_file))

REDIS = Redis(host=CONFIG.storage.redis.url)

app_logs = LoggingConfig(
    root={"level": CONFIG.logging.level, "handlers": ["console"]},
    formatters={"standard": {"format": CONFIG.logging.format}},
)


@asynccontextmanager
async def app_lifecycle(app: Litestar) -> AsyncGenerator[None, None]:
    app.logger.info("Initializing lifecycle...")
    plugins = PluginLoader(CONFIG, app.logger)
    async with plugins.resolve_lifecycle() as lifecycle:
        mongo_client = AsyncIOMotorClient(CONFIG.storage.mongo.url)
        await init_beanie(
            database=mongo_client.get_database(CONFIG.storage.mongo.database),
            document_models=DOCUMENT_MODELS,
        )
        context = Context(
            CONFIG,
            plugins,
            REDIS,
            mongo_client.get_database(CONFIG.storage.mongo.database),
        )
        app.state["context"] = context
        yield


app = Litestar(
    route_handlers=[API_ROUTER],
    lifespan=[app_lifecycle],
    plugins=[
        ChannelsPlugin(
            RedisChannelsPubSubBackend(redis=REDIS),
            arbitrary_channels_allowed=True,
            create_ws_route_handlers=True,
            ws_handler_base_path="/api/events",
        )
    ],
    state=State({}),
    dependencies={
        "session": Provide(provide_session),
        "context": Provide(provide_context),
        "config": Provide(provide_config),
        "lifecycle": Provide(provide_lifcycle),
        "plugins": Provide(provide_plugins),
    },
    middleware=[CookieSessionManager],
    logging_config=app_logs,
)
