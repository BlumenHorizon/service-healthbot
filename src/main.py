from dotenv import load_dotenv
from telegram.ext import Application, CallbackQueryHandler, CommandHandler

from src import commands, config
from src.handlers.buttons import monolith_button
from src.handlers.error import handle_error
from src.logger import configure_logger
from src.periodic_jobs import check_sites_job

load_dotenv(override=True)


async def post_init(application: Application) -> None:  # type: ignore[type-arg]
    await application.bot.set_my_commands(
        [
            ("start", "Start the bot"),
            ("help", "Show help info"),
            ("add", "Add a site (url, status code)"),
        ]
    )


def main() -> None:
    configure_logger()
    application = (
        Application.builder().post_init(post_init).token(config.BOT_TOKEN).build()
    )
    application.add_error_handler(handle_error)
    job_queue = application.job_queue
    if job_queue:
        job_queue.run_repeating(
            check_sites_job,
            interval=600,
            first=10,
        )  # Run every 10 minutes
    else:
        raise RuntimeError(
            "JobQueue requires the extra dependency 'apscheduler'. "
            "Install with: poetry add 'python-telegram-bot[job-queue]'"
        )

    application.add_handler(CommandHandler("start", commands.start))
    application.add_handler(CommandHandler("help", commands.help_command))
    application.add_handler(CommandHandler("add", commands.add_command))
    application.add_handler(CallbackQueryHandler(monolith_button))

    application.run_polling()


if __name__ == "__main__":
    main()
