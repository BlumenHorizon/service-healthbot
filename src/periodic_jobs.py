from loguru import logger
from telegram.ext import ContextTypes

from src.db.database import async_session
from src.repos.sites import SiteRepo
from src.services.sites_periodic_jobs import (
    process_site_uptime_status,
)


async def check_sites_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    log = logger.bind(topic="check_sites_job")
    log.info("⏱ Starting check_sites_job...")

    async with async_session() as db:
        site_repo = SiteRepo(db=db)
        sites_history = await site_repo.fetch_statuses()

        for history in sites_history:
            await process_site_uptime_status(history, context, logger=log)  # type: ignore[arg-type]

    log.info("✅ Finished check_sites_job.")
