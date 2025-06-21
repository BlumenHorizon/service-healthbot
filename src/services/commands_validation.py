from html import escape

from pydantic import ValidationError
from telegram import Message
from telegram.constants import ParseMode

from src.labels import MenuLabel
from src.schemas.sites import SiteCreateSchema


async def send_validation_errors(message: Message, errors: list[str]) -> None:
    await message.reply_text(
        f"⚠️ <b>Помилка валідації</b>\n\n" + "\n".join(errors),
        parse_mode="HTML",
    )


def validate_args_count(
    args: list[str] | None,
    creation_schema: type[SiteCreateSchema],
) -> bool:
    return args is not None and len(args) == len(creation_schema.model_fields)


async def send_args_error(
    message: Message,
    creation_schema: type[SiteCreateSchema],
) -> None:
    required_fields = ", ".join(f"*`{name}`*" for name in creation_schema.model_fields)
    await message.reply_text(
        f"⚠️ *{MenuLabel.BAD_REQUEST}*\nНеобхідні параметри: {required_fields}",
        parse_mode=ParseMode.MARKDOWN_V2,
    )


def validate_site_data(args: list[str]) -> tuple[SiteCreateSchema | None, list[str]]:
    site_url, expected_status_code = args
    try:
        site = SiteCreateSchema(
            url=site_url,  # type: ignore[arg-type]
            expected_status_code=expected_status_code,  # type: ignore[arg-type]
        )
        return site, []
    except ValidationError as e:
        errors = [
            f"• <b>{err['loc'][0]}</b>: {escape(err['msg'])}" for err in e.errors()
        ]
        return None, errors
