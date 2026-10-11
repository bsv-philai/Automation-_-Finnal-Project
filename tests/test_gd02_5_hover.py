import allure

from constants.messages import TOOLTIP_CREATED_DATE
from helpers import description_md


@allure.feature("チケット一覧")
@allure.story("GD02.5-Hover")
@allure.link("https://bsv-nhungnguyen.github.io/bai_tap_17082026.html", name="bai_tap_17082026")
@description_md(
    "Test cases GD02.5-001 in file "
    "Automation _ Finnal Project — シート: Testcases (Category: GD02.5-Hover)"
)
class TestGD02_5_Hover:

    @allure.title("GD02.5-001: Hover help icon of 作成日 shows tooltip")
    @description_md(
        """
- **前提条件**: チケット一覧画面を表示中
- **テスト手順**: 1. 「作成日」列見出し横のヘルプアイコン（?）にカーソルを合わせる
- **期待する結果**: 「チケットが作成された日付を表示します」という説明テキストが表示される
        """
    )
    def test_ticket_list_hover_created_help_icon_shows_tooltip(self, ticket_list):
        ticket_list.hover_created_help_icon()
        ticket_list.expect_tooltip(TOOLTIP_CREATED_DATE)
        with allure.step("[PASSED] Tooltip text for 作成日 is displayed"):
            pass
