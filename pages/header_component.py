import allure
from playwright.sync_api import Page, expect

from constants.locators import HeaderLocators as locators
from pages.base_page import BasePage
from pages.notification_page import NotificationPage
from pages.settings_page import SettingsPage


class HeaderComponent(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.main_section = page.locator(locators.MAIN_SECTION)
        self.user_name = page.locator(locators.USER_NAME)
        self.tab_notifications = page.locator(locators.TAB_NOTIFICATIONS)
        self.tab_settings = page.locator(locators.TAB_SETTINGS)

    @allure.step("Go to notifications tab")
    def go_to_notifications(self) -> NotificationPage:
        self.click(self.tab_notifications)
        return NotificationPage(self.page)

    @allure.step("Go to settings tab")
    def go_to_settings(self) -> SettingsPage:
        self.click(self.tab_settings)
        return SettingsPage(self.page)

    @allure.step("Expect logged in as {user_name}")
    def expect_logged_in_as(self, user_name: str) -> None:
        self.expect_visible(self.main_section)
        expect(self.user_name).to_have_text(user_name)

    @allure.step("Expect main section hidden")
    def expect_main_hidden(self) -> None:
        self.expect_hidden(self.main_section)
