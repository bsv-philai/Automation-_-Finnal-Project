import allure

from constants.messages import MSG_STATUS_UPDATED
from constants.test_data import SECOND_PAGE_COUNT, STATUS_DONE, TARGET_TICKET_SUBJECT
from helpers import description_md

SORT_ICON_DESC = "arrow_downward"


@allure.feature("チケット一覧")
@allure.story("GD02.1-Click")
@allure.link("https://bsv-nhungnguyen.github.io/bai_tap_17082026.html", name="bai_tap_17082026")
@description_md(
    "Test cases GD02.1-02, GD02.1-04, GD02.1-16 in file "
    "Automation _ Finnal Project — シート: Testcases (Category: GD02.1-Click)"
)
class TestGD02_1_Click:

    @allure.title("GD02.1-02: Click 次へ shows page 2 with 2 tickets")
    @description_md(
        """
- **前提条件**: 1ページの表示件数が10件（デフォルト）
- **テスト手順**: 1. 「次へ」ボタンを押下する
- **期待する結果**: 2ページ目（残り2件）が表示され、「前へ」ボタンが活性化する
        """
    )
    def test_ticket_list_click_next_shows_page_two(self, ticket_list):
        ticket_list.click_next_page()
        ticket_list.expect_row_count(SECOND_PAGE_COUNT)
        ticket_list.expect_prev_enabled()
        with allure.step("[PASSED] Page 2 shows 2 tickets and 前へ is enabled"):
            pass

    @allure.title("GD02.1-04: Click 作成日 header twice sorts descending")
    @description_md(
        """
- **前提条件**: 「作成日」列見出しを1回押下済み
- **テスト手順**: 1. 「作成日」列見出しをもう一度押下する
- **期待する結果**: 作成日の降順に並び替わり、ソートアイコンが下向き矢印になる
        """
    )
    def test_ticket_list_click_created_header_twice_sorts_descending(self, ticket_list):
        with allure.step("前提条件: Click 作成日 header once (ascending)"):
            ticket_list.click_created_header()
        ticket_list.click_created_header()
        ticket_list.expect_sort_icon(SORT_ICON_DESC)
        dates = ticket_list.get_created_dates()
        assert dates == sorted(dates, reverse=True), f"Created dates are not descending: {dates}"
        with allure.step("[PASSED] Tickets sorted by 作成日 descending with down arrow icon"):
            pass

    @allure.title("GD02.1-16: Select 完了にする in kebab menu updates the row status")
    @description_md(
        """
- **前提条件**: チケット一覧画面を表示中
- **テスト手順**:
  1. 任意の行の「⋮」ボタンを押下する
  2. 表示されたメニューから「完了にする」を選択する
- **期待する結果**: メニューが閉じ、該当行のステータスが「完了」に変わる。トースト通知が表示される
        """
    )
    def test_ticket_list_kebab_complete_changes_status_to_done(self, ticket_list):
        ticket_list.complete_by_kebab(TARGET_TICKET_SUBJECT)
        ticket_list.expect_kebab_menu_closed(TARGET_TICKET_SUBJECT)
        ticket_list.expect_row_status(TARGET_TICKET_SUBJECT, STATUS_DONE)
        ticket_list.expect_toast(MSG_STATUS_UPDATED)
        with allure.step("[PASSED] Kebab menu closed, status changed to 完了 and toast displayed"):
            pass
