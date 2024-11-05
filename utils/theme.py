import random

from ATMusic.utils.database import get_theme

themes = [
    "dante1",
    "dante12",
    "dante3",
    "dante4",
    "dante5",
    "dante6",
    "dante7",
    "dante8",
]


async def check_theme(chat_id: int):
    _theme = await get_theme(chat_id, "theme")
    if not _theme:
        theme = random.choice(themes)
    else:
        theme = _theme["theme"]
        if theme == "Random":
            theme = random.choice(themes)
    return theme
