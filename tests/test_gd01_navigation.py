import allure

from constants.test_data import ADMIN_NOTIFICATION_TOTAL
from helpers import description_md


@allure.feature("画面遷移")
@allure.story("GD01-Navigation")
@allure.link("https://bsv-nhungnguyen.github.io/bai_tap_17082026.html", name="bai_tap_17082026")
@description_md(
    "Test cases GD01_002, GD01_004 in file "
    "Automation _ Finnal Project — シート: Testcases (Category: GD01-Navigation)"
)
class TestGD01_Navigation:

    @allure.title("GD01_002: Open the page shows the login screen")
    @description_md(
        """
- **前提条件**: ブラウザでページを開く
- **テスト手順**: 1. ページを開く
- **期待する結果**: ログイン画面が表示される（ID・パスワード入力欄、ログインボタン）
        """
    )
    def test_login_screen_open_page_shows_login_form(self, login_page):
        login_page.expect_displayed()
        with allure.step("[PASSED] Login screen with ID, password and login button is displayed"):
            pass

    @allure.title("GD01_004: Click 通知 tab shows notification list with 3 items")
    @description_md(
        """
- **前提条件**: admin/admin123でログイン済み
- **テスト手順**: 1. ヘッダーの「通知」タブを押下する
- **期待する結果**: 通知一覧画面に遷移し、3件の通知が表示される
        """
    )
    def test_header_click_notification_tab_shows_three_notifications(self, header):
        notification_page = header.go_to_notifications()
        notification_page.expect_row_count(ADMIN_NOTIFICATION_TOTAL)
        with allure.step("[PASSED] Notification list displays 3 notifications"):
            pass
