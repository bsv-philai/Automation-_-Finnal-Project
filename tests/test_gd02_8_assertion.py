import allure

from constants.messages import MSG_LOGIN_FAILED, MSG_TICKET_LIST_EMPTY
from constants.test_data import INVALID_PASSWORD
from helpers import description_md


@allure.feature("表示確認")
@allure.story("GD02.8-Assertion")
@allure.link("https://bsv-nhungnguyen.github.io/bai_tap_17082026.html", name="bai_tap_17082026")
@description_md(
    "Test cases GD02.8-04, GD02.8-07 in file "
    "Automation _ Finnal Project — シート: Testcases (Category: GD02.8-Assertion)"
)
class TestGD02_8_Assertion:

    @allure.title("GD02.8-04: Login with wrong password shows error and stays on login screen")
    @description_md(
        """
- **前提条件**: ログイン画面を表示中
- **テスト手順**:
  1. IDに「admin」を入力する
  2. パスワードに「wrongpass」を入力する
  3. 「ログイン」ボタンを押下する
- **期待する結果**: 「IDまたはパスワードが正しくありません。」というエラーメッセージが表示され、画面遷移しない
        """
    )
    def test_login_wrong_password_shows_error(self, login_page, header_on_login_screen, admin_credentials):
        admin_id, _ = admin_credentials
        login_page.login(admin_id, INVALID_PASSWORD)
        login_page.expect_error(MSG_LOGIN_FAILED)
        login_page.expect_displayed()
        header_on_login_screen.expect_main_hidden()
        with allure.step("[PASSED] Error message displayed and login screen remains"):
            pass

    @allure.title("GD02.8-07: Guest ticket list shows empty state without pagination")
    @description_md(
        """
- **前提条件**: guestでログイン済み
- **テスト手順**: 1. チケット一覧画面の表示を確認する
- **期待する結果**: チケットが0件で「登録されているチケットはありません。」というメッセージと「＋新規チケット作成」ボタンが表示される。ページネーションは表示されない
        """
    )
    def test_ticket_list_guest_default_shows_empty_state(self, ticket_list_as_guest):
        ticket_list_as_guest.expect_empty_state(MSG_TICKET_LIST_EMPTY)
        with allure.step("[PASSED] Empty message and create button displayed, pagination hidden"):
            pass
