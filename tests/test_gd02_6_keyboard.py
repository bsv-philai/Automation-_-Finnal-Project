import allure

from constants.test_data import SEARCH_KEYWORD_LOGIN, SEARCH_LOGIN_RESULT_SUBJECTS
from helpers import description_md


@allure.feature("チケット一覧")
@allure.story("GD02.6-Keyboard")
@allure.link("https://bsv-nhungnguyen.github.io/bai_tap_17082026.html", name="bai_tap_17082026")
@description_md(
    "Test cases GD02.6-02 in file "
    "Automation _ Finnal Project — シート: Testcases (Category: GD02.6-Keyboard)"
)
class TestGD02_6_Keyboard:

    @allure.title("GD02.6-02: Press Enter in search box filters like the 検索 button")
    @description_md(
        """
- **前提条件**: チケット一覧画面を表示中
- **テスト手順**:
  1. 検索欄に「ログイン」と入力する
  2. Enterキーを押下する
- **期待する結果**: 「検索」ボタン押下時と同じ結果が表示される
        """
    )
    def test_ticket_list_search_with_enter_shows_matching_tickets(self, ticket_list):
        ticket_list.search_by_enter(SEARCH_KEYWORD_LOGIN)
        ticket_list.expect_subjects(SEARCH_LOGIN_RESULT_SUBJECTS)
        with allure.step("[PASSED] Enter key shows the same 1 matching ticket as the 検索 button"):
            pass
