import allure

from constants.messages import MSG_FILE_TYPE_UNSUPPORTED
from constants.test_data import UPLOAD_EXE_NAME, UPLOAD_PNG_NAME, UPLOAD_PNG_PREVIEW, UPLOAD_PNG_SIZE
from helpers import description_md

MIME_PNG = "image/png"
MIME_EXE = "application/x-msdownload"
EXE_SIZE = 1024


@allure.feature("チケット詳細ダイアログ")
@allure.story("GD02.7-FileUpload")
@allure.link("https://bsv-nhungnguyen.github.io/bai_tap_17082026.html", name="bai_tap_17082026")
@description_md(
    "Test cases GD02.7-01, GD02.7-04 in file "
    "Automation _ Finnal Project — シート: Testcases (Category: GD02.7-FileUpload)"
)
class TestGD02_7_FileUpload:

    @allure.title("GD02.7-01: Upload 1MB png shows file name, size and delete icon")
    @description_md(
        """
- **前提条件**: 詳細ダイアログを表示中
- **テスト手順**: 1. ドロップゾーンに.pngファイル（1MB程度）をアップロードする
- **期待する結果**: ファイル名とサイズがプレビュー表示され、削除アイコンが表示される
        """
    )
    def test_ticket_detail_upload_png_shows_preview(self, ticket_detail_dialog):
        ticket_detail_dialog.upload_file(UPLOAD_PNG_NAME, MIME_PNG, UPLOAD_PNG_SIZE)
        ticket_detail_dialog.expect_file_preview(UPLOAD_PNG_PREVIEW)
        with allure.step("[PASSED] File name, size and delete icon are displayed"):
            pass

    @allure.title("GD02.7-04: Upload .exe shows unsupported file type error")
    @description_md(
        """
- **前提条件**: 詳細ダイアログを表示中
- **テスト手順**: 1. ドロップゾーンに.exeファイルをアップロードする
- **期待する結果**: 「対応していないファイル形式です。」というエラーが表示され、プレビューされない
        """
    )
    def test_ticket_detail_upload_exe_shows_type_error(self, ticket_detail_dialog):
        ticket_detail_dialog.upload_file(UPLOAD_EXE_NAME, MIME_EXE, EXE_SIZE)
        ticket_detail_dialog.expect_file_error(MSG_FILE_TYPE_UNSUPPORTED)
        with allure.step("[PASSED] Unsupported file type error displayed without preview"):
            pass
