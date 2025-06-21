class MenuLabel:
    CHECK_STATUS = "Перевірити статус"
    SITE_LIST = "Список сайтів"
    CHOOSE_OPTION = "Оберіть опцію:"
    UNAUTHORIZED = "Ви не авторизовані для виокристання цього бота."
    START = "Use /start to begin."
    BAD_REQUEST = "Bad request"

    @staticmethod
    def remove_site(site_url: str) -> str:
        return f"Прибрати {site_url}"


class InlineLabel:
    ALERT_SITE_RESTORED = "🔔 Сайт знову доступний"
    SITE_STATUS = "Статус сайтів:\n"
    SITES_NOT_FROUD = "Жодного статусу ще не зібрано."
    SITE_LIST = "Список сайтів:\n"
    NO_SITES_FOUND = "Сайтів ще немає."
    SITE_REMOVED = f"Сайт було видалено."
    UPDATED_SITES = "Оновлений список сайтів:\n"
    SITES_NOT_FOUND = "Сайти не знайдено."
    ALERT_SITES_UNACCESSIBLE = "⚠️ УВАГА! Наступні сайти недоступні:\n"
