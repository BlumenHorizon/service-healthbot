from datetime import datetime

from loguru._logger import Logger
from telegram.ext import ContextTypes

from src.caching import redis_client
from src.db.models import SiteHistory
from src.services.sites_use_cases import notify_restored

REDIS_KEY_PREFIX = "site_down_since"


async def track_site_down(site_id: int, down_since: datetime, logger: Logger) -> None:
    """
    Track when a site goes down by storing the downtime start timestamp in Redis.

    If the site is already being tracked as down, no action is taken.

    Args:
        site_id (int): The unique identifier of the site.
        down_since (datetime): The timestamp when the site was detected as down.

    Returns:
        None
    """
    redis_key = f"{REDIS_KEY_PREFIX}:{site_id}"
    is_tracked = await redis_client.exists(redis_key)
    if not is_tracked:
        await redis_client.set(redis_key, down_since.isoformat())
        logger.warning(f"🚨 Site {site_id} is DOWN. Start tracking at {down_since}")  # type: ignore[no-untyped-call]
    else:
        logger.info(f"📉 Site {site_id} is still down. No action taken.")  # type: ignore[no-untyped-call]


async def handle_site_restored(
    site_id: int, up_time: datetime, context: ContextTypes.DEFAULT_TYPE, logger: Logger
) -> None:
    """
    Handle the event when a site is restored after downtime.

    Retrieves the downtime start from Redis, calculates the total downtime duration,
    logs the information, notifies users, and cleans up the Redis tracking key.

    Args:
        site_id (int): The unique identifier of the site.
        up_time (datetime): The timestamp when the site was detected as up.
        context (ContextTypes.DEFAULT_TYPE): Telegram bot context used for sending notifications.

    Returns:
        None
    """
    redis_key = f"{REDIS_KEY_PREFIX}:{site_id}"
    down_since_str = await redis_client.get(redis_key)
    if down_since_str:
        await redis_client.delete(redis_key)
        try:
            down_since = datetime.fromisoformat(down_since_str)
            downtime_duration = up_time - down_since
            logger.info(
                f"✅ Site {site_id} is UP again. Was down for {downtime_duration} (since {down_since})"  # type: ignore[no-untyped-call]
            )
            await notify_restored(
                site_id=site_id,
                downtime=downtime_duration,
                context=context,
            )
        except Exception as e:
            logger.exception(f"❌ Failed to calculate downtime for site {site_id}: {e}")  # type: ignore[no-untyped-call]
    else:
        logger.debug(
            f"🔄 Site {site_id} is up and was not marked as down. No redis key."  # type: ignore[no-untyped-call]
        )


async def process_site_uptime_status(
    history: SiteHistory, context: ContextTypes.DEFAULT_TYPE, logger: Logger
) -> None:
    """
    Process the uptime status of a site based on its history record.

    If the site is down, start tracking the downtime.
    If the site is restored, handle the restoration process including notifying relevant users.

    Args:
        history (SiteHistory): The site history record containing the current status and timestamps.
        context (ContextTypes.DEFAULT_TYPE): The context from the Telegram bot handler, used for sending notifications.

    Returns:
        None
    """
    site_id = history.site.id
    if not history.is_alive:
        await track_site_down(site_id, history.created_at, logger)
    else:
        await handle_site_restored(site_id, history.created_at, context, logger)
