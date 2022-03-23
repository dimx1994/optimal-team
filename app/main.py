import logging

import uvicorn
from fastapi import FastAPI

from app.db.data_importer import import_data
from app.db.models import create_all_waiting_postgres
from app.routes import router

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s"
)


async def on_start_up() -> None:
    pass


async def on_shutdown() -> None:
    pass


create_all_waiting_postgres()
import_data()


app = FastAPI(docs_url="/docs", on_startup=[on_start_up], on_shutdown=[on_shutdown])
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
