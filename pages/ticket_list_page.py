import re

from playwright.sync_api import Dialog, Locator, Page, expect

from constants.locators import TicketListLocators as locators
from pages.base_page import BasePage
from pages.ticket_detail_dialog import TicketDetailDialog


class TicketListPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.panel = page.locator(locators.PANEL)
        self.rows = page.locator(locators.ROWS)
        self.tbody = page.locator(locators.TBODY)
        self.search_input = page.get_by_placeholder(locators.SEARCH_PLACEHOLDER)
        self.priority_filter = page.get_by_label(locators.PRIORITY_FILTER_LABEL)
        self.pagination_top = page.locator(locators.PAGINATION_TOP)
        self.pagination_bottom = page.locator(locators.PAGINATION_BOTTOM)
        self.created_header = page.locator(locators.CREATED_HEADER)
        self.sort_icon = page.locator(locators.SORT_ICON)
        self.tooltip_trigger = self.created_header.locator(locators.TOOLTIP_TRIGGER)
        self.tooltip_content = self.created_header.locator(locators.TOOLTIP_CONTENT)
        self.select_all_checkbox = page.get_by_role("checkbox", name=locators.SELECT_ALL_CHECKBOX)
        self.row_checkboxes = self.rows.locator(locators.ROW_CHECKBOX)
        self.bulk_action_bar = page.locator(locators.BULK_ACTION_BAR)
        self.bulk_complete_button = page.get_by_role("button", name=locators.BULK_COMPLETE_BUTTON)
        self.empty_create_button = self.tbody.get_by_role(
            "button", name=locators.EMPTY_CREATE_BUTTON, exact=True
        )
        self.preview_frame = page.frame_locator(locators.PREVIEW_IFRAME)
        self.open_manual_button = page.get_by_role("button", name=locators.OPEN_MANUAL_BUTTON)
        self.print_preview_button = page.get_by_role("button", name=locators.PRINT_PREVIEW_BUTTON)
        self.reassign_button = page.get_by_role("button", name=locators.REASSIGN_BUTTON)
        self.reassign_result = page.locator(locators.REASSIGN_RESULT)

    # ---------- row helpers ----------
    def row(self, subject: str) -> Locator:
        """Mỗi dòng đều có nút 詳細/削除/⋮ riêng (Bẫy #1) → luôn scope theo dòng."""
        return self.rows.filter(has_text=subject)

    def get_row_texts(self) -> list[str]:
        return self.rows.all_inner_texts()

    def get_created_dates(self) -> list[str]:
        date_cells = self.rows.get_by_role("cell").filter(
            has_text=re.compile(locators.CREATED_DATE_CELL_PATTERN)
        )
        return date_cells.all_inner_texts()

    # ---------- actions ----------
    def search_by_enter(self, keyword: str) -> None:
        self.fill(self.search_input, keyword)
        self.search_input.press("Enter")

    def filter_by_priority(self, priority: str) -> None:
        self.priority_filter.select_option(priority)

    def click_next_page(self) -> None:
        self.click(self.pagination_top.get_by_role("button", name=locators.NEXT_BUTTON))

    def click_created_header(self) -> None:
        self.click(self.created_header)

    def hover_created_help_icon(self) -> None:
        self.tooltip_trigger.hover()

    def check_select_all(self) -> None:
        self.select_all_checkbox.check()

    def check_rows(self, subjects: list[str]) -> None:
        for subject in subjects:
            self.row(subject).locator(locators.ROW_CHECKBOX).check()

    def open_detail(self, subject: str) -> TicketDetailDialog:
        self.click(self.row(subject).get_by_role("button", name=locators.DETAIL_BUTTON, exact=True))
        return TicketDetailDialog(self.page)

    def delete_row_and_accept(self, subject: str) -> None:
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.click(self.row(subject).get_by_role("button", name=locators.DELETE_BUTTON, exact=True))

    def complete_by_kebab(self, subject: str) -> None:
        row = self.row(subject)
        self.click(row.get_by_role("button", name=locators.KEBAB_BUTTON))
        self.click(row.get_by_role("button", name=locators.KEBAB_DONE_ITEM))

    def reassign(self, name: str) -> None:
        self.page.once("dialog", lambda dialog: dialog.accept(name))
        self.click(self.reassign_button)

    def bulk_complete_and_accept(self) -> list[str]:
        """Bấm 一括対応完了: accept confirm rồi alert, trả về message của các dialog theo thứ tự."""
        messages: list[str] = []

        def handle(dialog: Dialog) -> None:
            messages.append(dialog.message)
            dialog.accept()

        self.page.on("dialog", handle)
        try:
            self.click(self.bulk_complete_button)
        finally:
            self.page.remove_listener("dialog", handle)
        return messages

    def apply_status_in_preview(self, status: str) -> None:
        self.preview_frame.locator(locators.FRAME_STATUS_SELECT).select_option(status)
        self.click(self.preview_frame.get_by_role("button", name=locators.FRAME_APPLY_BUTTON))

    def open_print_preview(self) -> Page:
        with self.page.expect_popup() as popup_info:
            self.click(self.print_preview_button)
        return popup_info.value

    def open_manual(self) -> Page:
        with self.page.context.expect_page() as page_info:
            self.click(self.open_manual_button)
        return page_info.value

    # ---------- assertions ----------
    def expect_displayed(self) -> None:
        self.expect_visible(self.panel)

    def expect_row_count(self, count: int) -> None:
        expect(self.rows).to_have_count(count)

    def expect_subjects(self, subjects: list[str]) -> None:
        expect(self.rows).to_have_count(len(subjects))
        for subject in subjects:
            self.expect_visible(self.row(subject))

    def expect_all_rows_have_priority(self, priority: str, count: int) -> None:
        expect(self.rows).to_have_count(count)
        expect(self.rows.filter(has=self.page.get_by_role("cell", name=priority, exact=True))).to_have_count(count)

    def expect_row_status(self, subject: str, status: str) -> None:
        expect(self.row(subject).get_by_role("cell", name=status, exact=True)).to_be_visible()

    def expect_row_absent(self, subject: str) -> None:
        expect(self.row(subject)).to_have_count(0)

    def expect_kebab_menu_closed(self, subject: str) -> None:
        self.expect_hidden(self.row(subject).locator(locators.KEBAB_MENU))

    def expect_prev_enabled(self) -> None:
        expect(self.pagination_top.get_by_role("button", name=locators.PREV_BUTTON)).to_be_enabled()

    def expect_sort_icon(self, icon_name: str) -> None:
        expect(self.sort_icon).to_have_text(icon_name)

    def expect_tooltip(self, text: str) -> None:
        expect(self.tooltip_content).to_be_visible()
        expect(self.tooltip_content).to_have_text(text)

    def expect_all_rows_checked(self, count: int) -> None:
        expect(self.row_checkboxes).to_have_count(count)
        expect(self.rows.locator(locators.ROW_CHECKBOX_UNCHECKED)).to_have_count(0)

    def expect_bulk_action_bar_visible(self) -> None:
        self.expect_visible(self.bulk_action_bar)

    def expect_empty_state(self, message: str) -> None:
        """Phân trang bị ẩn hoàn toàn khi ≤ 1 trang (Bẫy #3) → assert hidden, không assert disabled."""
        expect(self.tbody).to_contain_text(message)
        self.expect_visible(self.empty_create_button)
        self.expect_hidden(self.pagination_top)
        self.expect_hidden(self.pagination_bottom)

    def expect_reassign_result(self, text: str) -> None:
        expect(self.reassign_result).to_have_text(text)

    def expect_preview_result(self, text: str) -> None:
        expect(self.preview_frame.locator(locators.FRAME_RESULT)).to_have_text(text)

    def expect_row_texts(self, texts: list[str]) -> None:
        expect(self.rows).to_have_text(texts, use_inner_text=True)

    @staticmethod
    def expect_popup_contains(popup: Page, text: str) -> None:
        expect(popup.locator(locators.POPUP_BODY)).to_contain_text(text)

    @staticmethod
    def expect_page_url(target: Page, pattern: re.Pattern) -> None:
        expect(target).to_have_url(pattern)
