import textwrap
from typing import Callable

import allure


def description_md(text: str) -> Callable:
    """Bọc allure.description, dedent để markdown thụt lề trong source vẫn hiển thị sạch."""
    return allure.description(textwrap.dedent(text).strip())
