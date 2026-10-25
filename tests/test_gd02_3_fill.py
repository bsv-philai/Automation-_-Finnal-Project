import allure

from constants.messages import SIGNATURE_COUNTER_MAX, USER_NAME_ADMIN
from constants.test_data import SIGNATURE_MAX_LENGTH
from helpers import description_md


@allure.feature("入力")
@allure.story("GD02.3-Fill")
@allure.link("https://bsv-nhungnguyen.github.io/bai_tap_17082026.html", name="bai_tap_17082026")
@description_md(
    "Test cases GD02.3-001, GD02.3-007 in file "
    "Automation _ Finnal Project — シート: Testcases (Category: GD02.3-Fill)"
)
class TestGD02_3_Fill:

    @allure.title("GD02.3-001: Typing over 100 chars in signature stops at 100/100文字")
    @description_md(
        """
- **前提条件**: 設定画面を表示中
- **テスト手順**: 1. 署名欄に100文字を超えるテキストを入力しようとする
- **期待する結果**: 最大100文字までしか入力できず、カウンター表示が「100/100文字」で止まる
        """
    )
    def test_settings_type_signature_over_limit_stops_at_max(self, settings_page):
        settings_page.type_signature(settings_page.random_chars(length=SIGNATURE_MAX_LENGTH + 1))
        length = settings_page.get_signature_length()
        assert length == SIGNATURE_MAX_LENGTH, f"Signature length is {length}, expected {SIGNATURE_MAX_LENGTH}"
        settings_page.expect_signature_counter(SIGNATURE_COUNTER_MAX)
        with allure.step("[PASSED] Signature limited to 100 chars and counter shows 100/100文字"):
            pass

    @allure.title("GD02.3-007: Login with valid admin account shows ticket list")
    @description_md(
        """
- **前提条件**: ログイン画面を表示中
- **テスト手順**:
  1. IDに「admin」を入力する
  2. パスワードに「admin123」を入力する
  3. 「ログイン」ボタンを押下する
- **期待する結果**: チケット一覧画面に遷移し、ヘッダーにログインユーザー名が表示される
        """
    )
    def test_login_valid_admin_shows_ticket_list(
        self, login_page, header_on_login_screen, ticket_list_on_login_screen, admin_credentials
    ):
        login_page.login(*admin_credentials)
        ticket_list_on_login_screen.expect_displayed()
        header_on_login_screen.expect_logged_in_as(USER_NAME_ADMIN)
        with allure.step("[PASSED] Ticket list displayed with admin user name in header"):
            pass
