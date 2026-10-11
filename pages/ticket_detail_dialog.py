import os

from playwright.sync_api import Page, expect

from constants.locators import TicketDetailLocators as locators
from pages.base_page import BasePage


class TicketDetailDialog(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.dialog = page.get_by_role("dialog", name=locators.DIALOG)
        self.file_input = page.locator(locators.FILE_INPUT)
        self.file_preview = page.locator(locators.FILE_PREVIEW)
        self.file_name = page.locator(locators.FILE_NAME)
        self.remove_file_button = self.dialog.get_by_role("button", name=locators.REMOVE_FILE_BUTTON)
        self.file_error = page.locator(locators.FILE_ERROR)

    def upload_file(self, name: str, mime_type: str, size: int) -> None:
        """Input file bị display:none (Bẫy #2) → set_input_files với buffer tạo trong code."""
        self.file_input.set_input_files(files=[{
            "name": name, "mimeType": mime_type, "buffer": os.urandom(size),
        }])

    def expect_opened(self) -> None:
        self.expect_visible(self.dialog)

    def expect_file_preview(self, text: str) -> None:
        expect(self.file_name).to_have_text(text)
        self.expect_visible(self.remove_file_button)

    def expect_file_error(self, message: str) -> None:
        expect(self.file_error).to_have_text(message)
        self.expect_hidden(self.file_preview)
