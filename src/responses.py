from typing import (
    Any,
    Callable,
    Coroutine,
    NotRequired,
    TypedDict,
    TypeVar,
)

from telegram import Update
from telegram.ext import ContextTypes

from src.db.models import SiteToCheck

R = TypeVar("R")
CallableCommand = Callable[[Update, ContextTypes.DEFAULT_TYPE], Coroutine[Any, Any, R]]


class FetchedSiteStatusResponse(TypedDict):
    is_alive: bool
    site: SiteToCheck
    error: NotRequired[str]
