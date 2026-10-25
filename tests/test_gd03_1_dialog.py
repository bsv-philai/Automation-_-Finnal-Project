import allure

from constants.messages import MSG_BULK_COMPLETED, MSG_REASSIGNED, MSG_TICKET_DELETED
from constants.test_data import BULK_TARGET_SUBJECTS, REASSIGN_NAME, STATUS_DONE, TARGET_TICKET_SUBJECT
from helpers import description_md


@allure.feature("チケット一覧")
@allure.story("GD03.1-Dialog")
@allure.link("https://bsv-nhungnguyen.github.io/bai_tap_17082026.html", name="bai_tap_17082026")
@description_md(
    "Test cases GD03.1-01, GD03.1-02, GD03.1-06 in file "
    "Automation _ Finnal Project — シート: Testcases (Category: GD03.1-Dialog)"
)
class TestGD03_1_Dialog:

    @allure.title("GD03.1-01: Delete ticket and accept confirm removes the row")
    @description_md(
        """
- **前提条件**: チケット一覧画面を表示中
- **テスト手順**:
  1. 任意の行の「削除」ボタンを押下する
  2. 確認ダイアログ（confirm）で「OK」を押下する
- **期待する結果**: 該当行が一覧から削除され、トースト通知「チケットを削除しました。」が表示される
        """
    )
    def test_ticket_list_delete_accept_confirm_removes_row(self, ticket_list):
        ticket_list.delete_row_and_accept(TARGET_TICKET_SUBJECT)
        ticket_list.expect_row_absent(TARGET_TICKET_SUBJECT)
        ticket_list.expect_toast(MSG_TICKET_DELETED)
        with allure.step("[PASSED] Row deleted and toast displayed"):
            pass

    @allure.title("GD03.1-02: Enter a name in reassign prompt shows the new assignee")
    @description_md(
        """
- **前提条件**: チケット一覧画面を表示中
- **テスト手順**:
  1. 「担当者を再割り当てする」ボタンを押下する
  2. promptダイアログに任意の名前を入力してOKを押下する
- **期待する結果**: 入力した名前が画面上の再割り当て結果として反映される
        """
    )
    def test_ticket_list_reassign_prompt_shows_new_assignee(self, ticket_list):
        ticket_list.reassign(REASSIGN_NAME)
        ticket_list.expect_reassign_result(MSG_REASSIGNED.format(name=REASSIGN_NAME))
        with allure.step("[PASSED] Reassign result shows the entered name"):
            pass

    @allure.title("GD03.1-06: Accept bulk complete confirm changes status and shows alert")
    @description_md(
        """
- **前提条件**: 一括対応完了の確認ダイアログを表示中
- **テスト手順**: 1. 確認ダイアログで「OK」を押下する
- **期待する結果**: 選択した全件のステータスが「完了」に変わり、件数を通知するalertダイアログが表示される
        """
    )
    def test_ticket_list_bulk_complete_accept_changes_status_to_done(self, ticket_list):
        with allure.step("前提条件: Check 2 rows to enable bulk complete"):
            ticket_list.check_rows(BULK_TARGET_SUBJECTS)
        messages = ticket_list.bulk_complete_and_accept()
        expected_alert = MSG_BULK_COMPLETED.format(count=len(BULK_TARGET_SUBJECTS))
        for subject in BULK_TARGET_SUBJECTS:
            ticket_list.expect_row_status(subject, STATUS_DONE)
        assert len(messages) == 2, f"Expected confirm and alert dialogs, got {messages}"
        assert messages[-1] == expected_alert, f"Alert message is '{messages[-1]}', expected '{expected_alert}'"
        with allure.step("[PASSED] Selected tickets changed to 完了 and alert shows the count"):
            pass
