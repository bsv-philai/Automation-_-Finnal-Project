import allure

from constants.messages import PRINT_PREVIEW_TICKET_COUNT
from constants.test_data import ADMIN_TICKET_TOTAL, MANUAL_URL_PATTERN
from helpers import description_md


@allure.feature("チケット一覧")
@allure.story("GD03.3-TabWindow")
@allure.link("https://bsv-nhungnguyen.github.io/bai_tap_17082026.html", name="bai_tap_17082026")
@description_md(
    "Test cases GD03.3-01, GD03.3-04 in file "
    "Automation _ Finnal Project — シート: Testcases (Category: GD03.3-TabWindow)"
)
class TestGD03_3_TabWindow:

    @allure.title("GD03.3-01: Open print preview window shows target ticket count")
    @description_md(
        """
- **前提条件**: チケット一覧画面を表示中
- **テスト手順**: 1. 「印刷プレビューを開く（新しいウィンドウ）」ボタンを押下する
- **期待する結果**: 新しいポップアップウィンドウが開き、印刷プレビュー内容（対象チケット数）が表示される
        """
    )
    def test_ticket_list_open_print_preview_shows_ticket_count(self, ticket_list):
        popup = ticket_list.open_print_preview()
        ticket_list.expect_popup_contains(popup, PRINT_PREVIEW_TICKET_COUNT.format(count=ADMIN_TICKET_TOTAL))
        with allure.step("[PASSED] Print preview popup shows 対象チケット数：12件"):
            pass

    @allure.title("GD03.3-04: Open external manual in a new tab")
    @description_md(
        """
- **前提条件**: チケット一覧画面を表示中
- **テスト手順**: 1. 「外部マニュアルを開く（新しいタブ）」ボタンを押下する
- **期待する結果**: 新しいタブが開き、外部サイトが表示される
        """
    )
    def test_ticket_list_open_manual_opens_new_tab(self, ticket_list):
        new_tab = ticket_list.open_manual()
        ticket_list.expect_page_url(new_tab, MANUAL_URL_PATTERN)
        with allure.step("[PASSED] External manual site opened in a new tab"):
            pass
