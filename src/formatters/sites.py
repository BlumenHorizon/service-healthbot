from typing import Sequence

from src.db.models import SiteHistory
from src.labels import InlineLabel
from src.services.datetime_utils import datetime_string_conversion


def compose_dropped_sites_message(down_sites: Sequence[SiteHistory]) -> str:
    """
    Compose a status message listing monitored sites with their uptime status.

    For each site in the provided sequence, appends a line with a status icon,
    the site URL, and the last check timestamp formatted as a string.

    Args:
        down_sites (Sequence[SiteHistory]): List or sequence of SiteHistory objects representing
            the latest status of each monitored site.

    Returns:
        str: A formatted multi-line string indicating the status of each site,
             including check timestamps and status icons (✅ for up, ❌ for down).
    """
    alert_message = InlineLabel.SITE_STATUS
    for site_history in down_sites:
        site_status = "✅" if site_history.is_alive else "❌"
        alert_message += (
            f"- {site_status} ({site_history.site.url}) "
            f"(Перевірено в: {datetime_string_conversion(site_history.created_at)})\n"
        )
    return alert_message
