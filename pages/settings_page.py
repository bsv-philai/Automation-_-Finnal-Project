import allure
from playwright.sync_api import Page, expect

from constants.locators import SettingsLocators as locators
from pages.base_page import BasePage


class SettingsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.panel = page.locator(locators.PANEL)
        self.signature = page.get_by_placeholder(locators.SIGNATURE_PLACEHOLDER)
        self.signature_counter = page.locator(locators.SIGNATURE_COUNTER)

    @allure.step("Type signature")
    def type_signature(self, text: str) -> None:
        """Gõ từng phím để mô phỏng người dùng (maxlength chỉ chặn khi gõ phím)."""
        self.signature.press_sequentially(text)

    @allure.step("Get signature length")
    def get_signature_length(self) -> int:
        return len(self.signature.input_value())

    @allure.step("Expect signature counter: {text}")
    def expect_signature_counter(self, text: str) -> None:
        expect(self.signature_counter).to_have_text(text)
