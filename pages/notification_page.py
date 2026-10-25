from playwright.sync_api import Page, expect

from constants.locators import NotificationLocators as locators
from pages.base_page import BasePage


class NotificationPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.panel = page.locator(locators.PANEL)
        self.rows = page.locator(locators.ROWS)

    def expect_row_count(self, count: int) -> None:
        self.expect_visible(self.panel)
        expect(self.rows).to_have_count(count)
