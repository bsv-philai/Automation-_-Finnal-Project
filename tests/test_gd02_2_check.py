import allure

from constants.test_data import DEFAULT_PAGE_SIZE
from helpers import description_md


@allure.feature("チケット一覧")
@allure.story("GD02.2-Check")
@allure.link("https://bsv-nhungnguyen.github.io/bai_tap_17082026.html", name="bai_tap_17082026")
@description_md(
    "Test cases GD02.2-001 in file "
    "Automation _ Finnal Project — シート: Testcases (Category: GD02.2-Check)"
)
class TestGD02_2_Check:

    @allure.title("GD02.2-001: Check select-all checks every row and shows bulk action bar")
    @description_md(
        """
- **前提条件**: チケット一覧画面を表示中
- **テスト手順**: 1. テーブルヘッダーの全選択チェックボックスを押下する
- **期待する結果**: 表示中の全行のチェックボックスがチェックされ、一括操作バーが表示される
        """
    )
    def test_ticket_list_check_select_all_checks_all_rows(self, ticket_list):
        ticket_list.check_select_all()
        ticket_list.expect_all_rows_checked(DEFAULT_PAGE_SIZE)
        ticket_list.expect_bulk_action_bar_visible()
        with allure.step("[PASSED] All displayed rows checked and bulk action bar visible"):
            pass
