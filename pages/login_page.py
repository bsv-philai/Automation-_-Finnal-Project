from playwright.sync_api import Page, expect

from constants.locators import LoginLocators as locators
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.section = page.locator(locators.LOGIN_SECTION)
        self.id_input = page.get_by_label(locators.ID_LABEL, exact=True)
        self.password_input = page.get_by_label(locators.PASSWORD_LABEL, exact=True)
        self.login_button = page.get_by_role("button", name=locators.LOGIN_BUTTON, exact=True)
        self.error_message = page.locator(locators.ERROR_MESSAGE)

    def open(self, url: str) -> None:
        self.page.goto(url)

    def login(self, user_id: str, password: str) -> None:
        self.fill(self.id_input, user_id)
        self.fill(self.password_input, password)
        self.click(self.login_button)

    def expect_displayed(self) -> None:
        self.expect_visible(self.section)
        self.expect_visible(self.id_input)
        self.expect_visible(self.password_input)
        self.expect_visible(self.login_button)

    def expect_error(self, message: str) -> None:
        expect(self.error_message).to_have_text(message)
