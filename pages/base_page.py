import random
import string

import allure
from playwright.sync_api import Locator, Page, expect

from constants.locators import BaseLocators as locators


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    @allure.step("Click")
    def click(self, target: Locator) -> None:
        target.click()

    @allure.step("Fill")
    def fill(self, target: Locator, value: str) -> None:
        target.fill(value)

    @allure.step("Expect visible")
    def expect_visible(self, target: Locator) -> None:
        expect(target).to_be_visible()

    @allure.step("Expect hidden")
    def expect_hidden(self, target: Locator) -> None:
        expect(target).to_be_hidden()

    @allure.step("Expect toast: {message}")
    def expect_toast(self, message: str) -> None:
        expect(self.page.locator(locators.TOAST).filter(has_text=message)).to_be_visible()

    @staticmethod
    def random_chars(length: int) -> str:
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))
