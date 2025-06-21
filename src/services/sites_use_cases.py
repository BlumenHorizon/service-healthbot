from datetime import timedelta
from typing import Sequence

from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from src import config
from src.db.database import async_session
from src.db.models import SiteToCheck
from src.labels import InlineLabel
from src.repos.sites import SiteRepo


async def get_sites() -> Sequence[SiteToCheck]:
    async with async_session() as db:
        return await SiteRepo(db=db).get_all()


async def delete_site(site_id: int) -> bool:
    async with async_session() as db:
        return await SiteRepo(db=db).delete_by_id(site_id=site_id)


async def create_site(site_url: str, expected_status_code: int) -> SiteToCheck:
    async with async_session() as db:
        return await SiteRepo(db=db).create(
            site_url=site_url, expected_status_code=expected_status_code
        )


async def notify_restored(
    site_id: int, downtime: timedelta, context: ContextTypes.DEFAULT_TYPE
) -> None:
    minutes = int(downtime.total_seconds() // 60)

    async with async_session() as db:
        site_url = await SiteRepo(db=db).get_url_by_id(site_id=site_id)

    message = (
        f"<b>✅ {InlineLabel.ALERT_SITE_RESTORED}</b>\n\n"
        f'🌐 <b>Сайт:</b> <a href="{site_url}">{site_url}</a>\n'
        f"⏳ <b>Час простою:</b> <code>{minutes} хвилин</code>\n\n"
    )

    for chat_id in config.ALLOWED_CHAT_IDS:
        await context.bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,  # чтобы ссылка не показывала превью
        )
