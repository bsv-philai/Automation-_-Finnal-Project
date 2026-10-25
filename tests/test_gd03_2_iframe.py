import allure

from constants.messages import MSG_FRAME_APPLIED
from constants.test_data import STATUS_DONE
from helpers import description_md


@allure.feature("チケット一覧")
@allure.story("GD03.2-Iframe")
@allure.link("https://bsv-nhungnguyen.github.io/bai_tap_17082026.html", name="bai_tap_17082026")
@description_md(
    "Test cases GD03.2-01 in file "
    "Automation _ Finnal Project — シート: Testcases (Category: GD03.2-Iframe)"
)
class TestGD03_2_Iframe:

    @allure.title("GD03.2-01: Apply status in iframe shows result only inside the iframe")
    @description_md(
        """
- **前提条件**: チケット一覧画面を表示中
- **テスト手順**:
  1. 埋め込みプレビュー内のプルダウンでステータスを選択する
  2. 埋め込みプレビュー内の「適用」ボタンを押下する
- **期待する結果**: iframe内にのみ結果メッセージが表示され、親ページの一覧には影響しない
        """
    )
    def test_preview_iframe_apply_status_does_not_affect_parent(self, ticket_list):
        rows_before = ticket_list.get_row_texts()
        ticket_list.apply_status_in_preview(STATUS_DONE)
        ticket_list.expect_preview_result(MSG_FRAME_APPLIED.format(status=STATUS_DONE))
        ticket_list.expect_row_texts(rows_before)
        with allure.step("[PASSED] Result shown in iframe and parent ticket list unchanged"):
            pass
