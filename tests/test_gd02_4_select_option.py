import allure

from constants.test_data import HIGH_PRIORITY_COUNT, PRIORITY_HIGH
from helpers import description_md


@allure.feature("チケット一覧")
@allure.story("GD02.4-SelectOption")
@allure.link("https://bsv-nhungnguyen.github.io/bai_tap_17082026.html", name="bai_tap_17082026")
@description_md(
    "Test cases GD02.4-02 in file "
    "Automation _ Finnal Project — シート: Testcases (Category: GD02.4-SelectOption)"
)
class TestGD02_4_SelectOption:

    @allure.title("GD02.4-02: Select priority 高 shows only 5 high-priority tickets")
    @description_md(
        """
- **前提条件**: チケット一覧画面を表示中
- **テスト手順**: 1. 優先度プルダウンで「高」を選択する
- **期待する結果**: 優先度が「高」のチケットのみ表示される（5件）
        """
    )
    def test_ticket_list_select_priority_high_shows_only_high(self, ticket_list):
        ticket_list.filter_by_priority(PRIORITY_HIGH)
        ticket_list.expect_all_rows_have_priority(PRIORITY_HIGH, HIGH_PRIORITY_COUNT)
        with allure.step("[PASSED] Only 5 tickets with priority 高 are displayed"):
            pass
