import os
from contextlib import asynccontextmanager

import certifi
from fastapi import FastAPI

os.environ.setdefault("SSL_CERT_FILE", certifi.where())
os.environ.setdefault("REQUESTS_CA_BUNDLE", certifi.where())

from browser_scraper.api.router import job_manager, router
from browser_scraper.providers.claro import ClaroProvider
from browser_scraper.providers.copel import CopelProvider
from browser_scraper.providers.countfly import CountflyProvider
from browser_scraper.providers.registry import registry
from browser_scraper.providers.sanepar import SaneparProvider


def _register_providers() -> None:
    registry.register(CopelProvider())
    registry.register(ClaroProvider())
    registry.register(SaneparProvider())
    registry.register(CountflyProvider())


@asynccontextmanager
async def lifespan(app: FastAPI):
    _register_providers()
    yield
    await job_manager.cancel_all()


app = FastAPI(title="Browser Scraper", version="0.1.0", lifespan=lifespan)
app.include_router(router)
