# Automation Rules — Final Project (bai_tap_17082026)

Bộ quy tắc code automation cho trang luyện tập **"Bài tập 17.08.2026"** (サポートチケット管理).
Đọc hết file này trước khi viết test đầu tiên.

## Cấu trúc project

```text
project-root/
├── pages/             # Page Object Model — mỗi màn hình / component 1 file
├── helpers.py         # Tiện ích dùng chung (description_md)
├── tests/             # Mỗi Category trong sheet testcase là 1 file test
├── constants/         # locators.py / messages.py / test_data.py
├── conftest.py        # Fixture pytest (login admin/guest, page object, hook chụp screenshot)
├── pytest.ini         # Cấu hình chạy pytest
└── .env               # APP_URL + tài khoản admin / guest
```

Mapping file test ↔ Category:

| Category (cột B) | File test | Class test |
|---|---|---|
| GD01-Navigation | `tests/test_gd01_navigation.py` | `TestGD01_Navigation` |
| GD02.1-Click | `tests/test_gd02_1_click.py` | `TestGD02_1_Click` |
| GD02.2-Check | `tests/test_gd02_2_check.py` | `TestGD02_2_Check` |
| GD02.3-Fill | `tests/test_gd02_3_fill.py` | `TestGD02_3_Fill` |
| GD02.4-SelectOption | `tests/test_gd02_4_select_option.py` | `TestGD02_4_SelectOption` |
| GD02.5-Hover | `tests/test_gd02_5_hover.py` | `TestGD02_5_Hover` |
| GD02.6-Keyboard | `tests/test_gd02_6_keyboard.py` | `TestGD02_6_Keyboard` |
| GD02.7-FileUpload | `tests/test_gd02_7_file_upload.py` | `TestGD02_7_FileUpload` |
| GD02.8-Assertion | `tests/test_gd02_8_assertion.py` | `TestGD02_8_Assertion` |
| GD03.1-Dialog | `tests/test_gd03_1_dialog.py` | `TestGD03_1_Dialog` |
| GD03.2-Iframe | `tests/test_gd03_2_iframe.py` | `TestGD03_2_Iframe` |
| GD03.3-TabWindow | `tests/test_gd03_3_tab_window.py` | `TestGD03_3_TabWindow` |
| Others | `tests/test_others.py` | `TestOthers` |

**Không** chia file theo 大項目 (cột D) vì ở nhiều dòng cột này không khớp với màn hình thực tế.
Hãy chọn page object dựa vào 小項目 + テスト手順.

---

## Quy ước code

- Python 3.11+; có type hint cho mọi method public.
- Mỗi file 1 class; tên file là tên class viết theo snake_case.
- Hằng số khai báo ở cấp module, viết UPPER_CASE.
- Không dùng `except:` trống — bắt exception cụ thể hoặc dùng `except Exception`.
- Xoá import không dùng; sắp xếp import theo thứ tự stdlib → third-party → local.
- Không lặp logic — tách thành helper method khi một thao tác được dùng lại ở nhiều test hoặc POM.
- **Không bao giờ** hardcode tài khoản trong test, page object, script hay tài liệu; đọc từ `.env`
  (`ADMIN_ID`, `ADMIN_PASSWORD`, `GUEST_ID`, `GUEST_PASSWORD`).

---

## Chiến lược locator (thứ tự ưu tiên)

Trang **không có `data-testid`**. Dùng theo thứ tự sau:

1. **Role + tên hiển thị** — `get_by_role("button", name="ログイン")`.
2. **Label / placeholder** — `get_by_label(...)` / `get_by_placeholder(...)`.
3. **id** — `page.locator("#...")`.
4. **class (kiểu BEM)** — ví dụ `.btn-detail`, `.row-checkbox`.

`get_by_text` / `filter(has_text=...)` chỉ dùng để **scope** (chọn 1 dòng hoặc 1 container), không
dùng làm locator chính cho control.

**Cấm**: XPath theo vị trí (`div[3]/div[2]...`) — chỉ cần đổi layout là gãy.
**Tránh** `nth()` / `.first`, trừ khi UI cố tình lặp phần tử và test nhắm đúng một phần tử cụ thể;
khi dùng phải ghi comment ngắn giải thích lý do.

**Locator đặt trong `constants/locators.py`, không đặt trong page class.** Mỗi page class có
một locator class tương ứng, import với tên `locators`, mỗi dòng kèm comment tiếng Nhật ngắn mô tả
phần tử UI:

```python
# constants/locators.py
class TicketListLocators:
    SEARCH_PLACEHOLDER = "..."          # キーワード検索欄
    ROW_CHECKBOX       = ".row-checkbox"  # 行のチェックボックス（実体のinput）
    DETAIL_BUTTON      = "詳細"           # 行内の詳細ボタン（行スコープで使用）

# pages/ticket_list_page.py
from constants.locators import TicketListLocators as locators
```

### Quy trình tìm locator

1. **Mở đúng màn hình** qua fixture (admin hoặc guest tuỳ case).
2. **Kiểm tra tính duy nhất** — `locator.count() == 1` **trong phạm vi scope** của nó (dòng /
   dialog / drawer / container phân trang). Trên trang này nhiều nhãn bị lặp (xem Bẫy #1).
3. **Kiểm tra trạng thái** — phần tử hiển thị và enable đúng lúc test cần.
4. **Chỉ inspect phần DOM liên quan** — chỉ lấy container cần thiết; không commit HTML cả trang.
5. **Không dùng `.first` để chữa cháy** — hãy scope lại.

---

## Bẫy riêng của trang

Các hành vi dưới đây là **cố ý** của trang luyện tập. Không báo bug; hãy xử lý trong POM.

### Bẫy #1 — Nút bị lặp & checkbox bị ẩn

- Mỗi dòng đều có "詳細" / "削除" / "⋮" riêng; "前へ" / "次へ" xuất hiện **cả trên và dưới** bảng.
  Luôn scope theo dòng hoặc container:

  ```python
  row = page.locator("tbody tr").filter(has_text=subject)
  row.get_by_role("button", name="詳細").click()
  ```

- Checkbox thật (`<input>`) bị set `opacity:0` và nằm dưới icon `.cb-box`. Click vào icon **không có
  tác dụng** — phải `check()` / `click()` trực tiếp vào `<input>` và assert bằng
  `expect(input).to_be_checked()`. Nếu Playwright báo có phần tử khác chặn click (intercepts pointer
  events), dùng `check(force=True)` và ghi comment tham chiếu tới bẫy này.

### Bẫy #2 — File & bất đồng bộ

- Input file bị `display:none` → dùng `set_input_files`. Không click để mở hộp thoại chọn file
  của OS. Tạo file test ngay trong code (không commit file nhị phân lên git):

  ```python
  file_input.set_input_files(files=[{
      "name": "sample.png", "mimeType": "image/png", "buffer": os.urandom(1 * 1024 * 1024),
  }])
  ```

- Tiêu đề cột "作成日" có icon sort (`arrow_upward` / `arrow_downward`) và tooltip bị lẫn vào text
  → **không** assert tiêu đề bằng `to_have_text` theo innerText. Hãy assert phần tử icon và/hoặc
  thứ tự thực tế của các giá trị trong cột 作成日.
- Màn "統計" **không** tự cập nhật khi chuyển tab — phải bấm "再集計する" rồi mới assert số mới.
  `GD02.1-19` phải assert giá trị **cũ** trước, sau đó bấm nút, rồi mới assert giá trị mới.

### Bẫy #3 — Quản lý trạng thái

- Đổi bất kỳ filter nào (mức độ ưu tiên, từ khoá...) sẽ **bỏ chọn các dòng** và ẩn thanh thao tác
  hàng loạt. Nếu test cần trạng thái đang chọn thì phải chọn lại sau khi filter.
- Phân trang (前へ/次へ/số trang) bị **xoá khỏi trang** chứ không bị disable khi chỉ có ≤ 1 trang
  → assert `to_have_count(0)` / `to_be_hidden()`, không bao giờ dùng `to_be_disabled()`.
- Mỗi lần đăng nhập, **data được khởi tạo lại theo từng tài khoản** (đổi admin ⇄ guest cũng reset
  filter và trạng thái chọn). Mỗi test tự login lại là đủ để đảm bảo độc lập.

### Bẫy #4 — get-or-create (通知)

Gom toàn bộ luồng vào 1 method trong POM, dùng lại làm bước setup:

```python
def ensure_notification_exists(self, title: str, content: str) -> None:
    """Tìm theo tiêu đề; chỉ tạo mới bằng nút ở empty-state khi không tìm thấy."""
    self.search(title)
    if self.is_empty_result_visible():
        self.click_create_from_empty_state()   # nút "＋通知を作成する" ngay dưới message 0 件
        self.fill_create_form(title, content)
        self.submit_create()
```

### Dialog của trình duyệt, cửa sổ mới, iframe

- Playwright **tự động đóng (dismiss)** dialog nếu chưa đăng ký handler. Luôn đăng ký **trước khi**
  click:

  ```python
  page.once("dialog", lambda d: d.accept())               # confirm → OK
  page.once("dialog", lambda d: d.dismiss())              # confirm → キャンセル
  page.once("dialog", lambda d: d.accept(new_assignee))   # prompt
  ```

  `GD03.1-06` sinh ra **confirm rồi đến alert** — dùng `page.on("dialog", ...)` để thu thập message,
  sau đó assert nội dung alert.
- Cửa sổ / tab mới: `with page.expect_popup() as popup_info:` (hoặc `context.expect_page()`), rồi
  assert trên `popup_info.value`.
- iframe: dùng `page.frame_locator(...)`; đồng thời assert danh sách ở trang cha không thay đổi.
- Toast tự biến mất (~3 giây): `expect(toast).to_be_hidden(timeout=5000)` — không dùng `sleep`.
- Ô nhập giới hạn ký tự (`GD02.3-001`): gõ bằng `press_sequentially(self.random_chars(101))` để mô
  phỏng người dùng gõ phím, sau đó assert độ dài giá trị là 100 và bộ đếm hiển thị `100/100文字`.

---

## Quy ước đặt tên

| Đối tượng | Pattern | Ví dụ |
|---|---|---|
| Test method | `test_<subject>_<condition>_<expected>` | `test_ticket_list_click_next_shows_page_two` |
| `@allure.title` | `<ID>: <mô tả ngắn bằng tiếng Anh>` | `"GD02.1-02: Click 次へ shows page 2 with 2 tickets"` |
| ID trong title | **Giữ nguyên như cột C** (không pad lại số) | `GD01_003`, `GD02.1-02`, `GD02.3-001`, `Others_05` |
| Fixture | cụm danh từ snake_case | `ticket_list`, `access_to_home_screen_as_guest` |
| Class test | `Test` + Category, đổi `.`/`-` thành `_` | `TestGD02_1_Click` |
| Page class | PascalCase + hậu tố `Page` / `Dialog` / `Drawer` / `Component` | `TicketCreateDrawer` |
| Hằng số | SCREAMING_SNAKE_CASE | `MSG_TICKET_DELETED` |
| Assertion message | Câu tiếng Anh ngắn, bắt đầu bằng chủ thể | `"Bulk action bar is not visible"` |

ID được giữ nguyên để cột 関数名 trên sheet và title trong Allure đối chiếu được 1:1
(`run_and_open_allure_report.sh` tìm test theo `@allure.title`).

---

## Quy tắc `@description_md`

Mọi test **method** và test **class** đều phải có `@description_md(...)`, import từ `helpers`:

```python
from helpers import description_md
```

`description_md` bọc `allure.description(textwrap.dedent(text))` — nội dung có thể thụt lề trong
source cho dễ đọc, Allure vẫn nhận markdown sạch. **Không** dùng `@allure.description(...)` thô.

### Cấp class

```python
@description_md(
    "Test cases GD02.1-01 – GD02.1-22 in file "
    "Automation _ Finnal Project — シート: Testcases (Category: GD02.1-Click)"
)
class TestGD02_1_Click:
    ...
```

### Cấp method — mapping cột

| Trường trong `@description_md` | Cột CSV |
|---|---|
| `前提条件` | 前提条件 (cột F) |
| `テスト手順` | テスト手順 (cột G) |
| `期待する結果` | 期待する結果 (cột H) |

```python
@description_md(
    """
- **前提条件**: 1ページの表示件数が10件（デフォルト）
- **テスト手順**: 1. 「次へ」ボタンを押下する
- **期待する結果**: 2ページ目（残り2件）が表示され、「前へ」ボタンが活性化する
    """
)
```

Thủ tục / kết quả nhiều dòng thì dùng bullet con thụt lề:

```python
@description_md(
    """
- **前提条件**: チケット一覧画面を表示中
- **テスト手順**:
  1. 任意の行の「削除」ボタンを押下する
  2. 確認ダイアログ（confirm）で「OK」を押下する
- **期待する結果**: 該当行が一覧から削除され、トースト通知「チケットを削除しました。」が表示される
    """
)
```

---

## Nguyên tắc thiết kế test

- **Độc lập** — mỗi test phải chạy được một mình. Các 前提条件 như "「作成日」列見出しを1回押下済み",
  "行を2件チェック済み", "通知を6件以上作成した状態", "ドロワーのStep2を表示中" phải được **dựng trong
  chính test / fixture**, không được dựa vào việc test khác đã chạy trước.
- **Đúng tài khoản** — 前提条件 ghi `guest` thì dùng fixture guest; còn lại dùng admin.
- **Mỗi test một mục tiêu kiểm tra** — 1 kỳ vọng / test (nếu kết quả mong đợi liệt kê nhiều điểm
  của cùng một trạng thái, ví dụ "message + nút + không có phân trang", vẫn tính là 1 test).
- **Không sleep cứng** — dùng wait tường minh của Playwright / timeout của `expect(...)`.
- **Bằng chứng screenshot + video** — conftest tự đính kèm screenshot (pass + fail) và video (fail).
- **Không dùng `@allure.severity`**. Nếu muốn thể hiện 区分 / 重要度 trong report thì dùng
  `@allure.tag("正常系", "高")` (không bắt buộc).

### Bắt buộc kết thúc bằng step `[PASSED]`

```python
with allure.step("[PASSED] <tóm tắt ngắn>"):
    pass
```

### Không tự động hoá được / spec chưa rõ → skip tường minh

Vẫn tạo hàm, skip ngay lập tức, **không** đoán hành vi:

```python
@allure.title("Others_03: Operate while the real network is disconnected")
def test_ticket_list_real_network_disconnected_shows_error(self, ticket_list):
    pytest.skip(
        "Manual only for Others_03: requires disconnecting the real PC network (実ネットワーク), "
        "which cannot be reproduced reliably by browser emulation"
    )
```

Lý do skip phải ghi rõ ID testcase và nêu **tại sao** (cần môi trường thật / spec chưa rõ).
Áp dụng cho: `Others_01` – `Others_14`, `GD02.7-02`, `GD03.3-03`, và — nếu chưa được reviewer làm
rõ — `GD01_001`, `GD02.1-12`, `GD02.6-01`, `GD03.3-02`.

### Độ chặt của assertion

- Assert **đúng nguyên văn** theo spec (toast, thông báo lỗi, empty-state, text bộ đếm).
- **Không** nới assertion bằng `or`.
- Chỉ dùng `or` khi chính spec ghi nhận nhiều kết quả đều hợp lệ.
- Nếu app lệch so với spec thì test phải **fail**; ghi NG + chi tiết vào 備考.

### Dữ liệu ngẫu nhiên cho test độ dài

Dùng helper của `BasePage` thay vì chuỗi lặp cứng:

```python
# Sai
self.fill(locators.SIGNATURE, "A" * 101)

# Đúng
self.fill(locators.SIGNATURE, self.random_chars(length=101))
```

---

## Quy tắc cấu trúc POM

- `BasePage` chứa các helper chung (`click`, `fill`, `expect_visible`, `random_chars`, ...).
- POM của từng màn hình kế thừa `BasePage` và chỉ expose các thao tác nghiệp vụ:
  `LoginPage`, `HeaderComponent`, `TicketListPage`, `TicketDetailDialog`, `TicketCreateDrawer`,
  `NotificationPage`, `StatisticsPage`, `SettingsPage`.
- Assertion dùng `expect()` đặt trong method POM tên `expect_*`.
- Hàm kiểm tra boolean (`is_*`) trả về `bool` và được `assert` trong test — tự chúng không raise.
- Xử lý dialog, bắt popup, tạo file upload đặt trong POM, không đặt trong thân test.
- Fixture trong `conftest.py` tạo page object; test không tự khởi tạo page class.
- Không có locator thô trong thân test.

---

## Fixture

| Fixture | Mục đích |
|---|---|
| `access_to_login_screen` | Mở `APP_URL` ở màn hình đăng nhập. |
| `access_to_home_screen` | Đăng nhập bằng **admin** → チケット一覧 (12 ticket, 3 通知). |
| `access_to_home_screen_as_guest` | Đăng nhập bằng **guest** → チケット一覧 rỗng. |
| `ticket_list`, `notification_page`, `statistics_page`, `settings_page`, ... | Tạo page object trên nền các fixture login; chuyển màn qua tab ở header khi cần. |

App là single page — các màn con được mở qua tab ở header, không phải qua URL. Giữ phần điều hướng
trong fixture / method POM; test không tự dựng trạng thái trình duyệt.

---

## Hằng số và message

Không hardcode chuỗi UI trong test. Khởi tạo `constants/messages.py` với các text lấy từ sheet:

```python
MSG_LOGIN_FAILED            = "IDまたはパスワードが正しくありません。"
MSG_TICKET_DELETED          = "チケットを削除しました。"
MSG_NOTIFICATION_CREATED    = "通知を作成しました。"
MSG_SETTINGS_SAVED          = "設定を保存しました。"
MSG_TICKET_SEARCH_EMPTY     = "該当するチケットがありません"
MSG_NOTIFICATION_NOT_FOUND  = "検索条件に一致する通知が見つかりません"
MSG_TICKET_LIST_EMPTY       = "登録されているチケットはありません。"
MSG_NOTIFICATION_LIST_EMPTY = "通知はまだありません。"
MSG_FILE_TOO_LARGE          = "ファイルサイズが大きすぎます。"
MSG_FILE_TYPE_UNSUPPORTED   = "対応していないファイル形式です。"
TOOLTIP_CREATED_DATE        = "チケットが作成された日付を表示します"
SIGNATURE_COUNTER_MAX       = "100/100文字"
USER_NAME_ADMIN             = "田中 太郎（管理者）"
USER_NAME_GUEST             = "鈴木 花子（新規ユーザー）"
```

Các số liệu mong đợi đặt trong `constants/test_data.py` (ví dụ `ADMIN_TICKET_TOTAL = 12`,
`DEFAULT_PAGE_SIZE = 10`, `HIGH_PRIORITY_COUNT = 5`, `STATUS_OPEN_COUNT = 5`,
`ADMIN_NOTIFICATION_TOTAL = 3`).

---

## Ghi kết quả vào sheet

| Cột | Giá trị |
|---|---|
| 関数名 | Tên test method (`test_...`) |
| スターテス | `chưa làm` / `đang làm` / `hoàn thành` |
| 結果 | `OK` / `NG` (tìm hiểu nguyên nhân trước khi ghi NG) |
| 確認日 / 確認者 | Ngày chạy / tên mình |
| 備考 | NG: bước tái hiện + kết quả mong đợi + kết quả thực tế. Skip: lý do skip. |

---

## CI / Report

- `HEADED` trong `.env`: `true` = có giao diện (chạy local), `false` / không khai báo = headless (CI).
- Kết quả Allure → `allure-results/`, report → `allure-report/`.
- Screenshot → `screenshots/<test_name>_<outcome>_<timestamp>.png`.
- Chạy `bash run_and_open_allure_report.sh` ở local để chạy test, generate và mở Allure report.
- Workflow GitHub Actions (`.github/workflows/e2e.yml`) chạy headless, lấy tài khoản từ
  **secrets** của repository và upload Allure report làm artifact.
- Không commit HTML dump, screenshot, storage state, cookie, file mẫu để upload hay thông tin tài khoản.

---

## Nộp bài

1. Tạo MR vào nhánh `develop`, assignee **Nhung**; làm tới đâu commit / tạo branch tới đó.
2. Tích hợp Allure report vào source.
3. CI/CD chạy được trên GitHub.
4. Các cột trên sheet được cập nhật khớp với code trong MR.

---

## Thêm test mới (checklist)

1. Tìm file test theo **Category** (bảng ở đầu file).
2. Class có `@allure.feature`, `@allure.story`, `@allure.url`, `@description_md`.
3. Mỗi test: `@allure.title("<ID>: <mô tả>")` với ID giữ nguyên từ cột C, kèm
   `@description_md` gồm 前提条件 / テスト手順 / 期待する結果.
4. Chọn đúng fixture tài khoản (guest hay admin) và dựng 前提条件 trong test/fixture.
5. Đọc mục "Bẫy riêng của trang" cho màn hình mình đang làm.
6. Thân test chỉ gọi method POM; message lấy từ `constants/messages.py`.
7. Kết thúc bằng `with allure.step("[PASSED] ...")`, hoặc `pytest.skip(...)` kèm ID + lý do.
8. Chạy thực tế, sau đó điền 関数名 / スターテス / 結果 / 確認日 / 確認者 / 備考 vào sheet.

### File test mẫu

```python
import allure

from constants.messages import MSG_TICKET_DELETED
from helpers import description_md


@allure.feature("チケット一覧")
@allure.story("GD03.1-Dialog")
@allure.url("https://bsv-nhungnguyen.github.io/bai_tap_17082026.html")
@description_md(
    "Test cases GD03.1-01 – GD03.1-06 in file "
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
        subject = ticket_list.get_first_row_subject()
        ticket_list.delete_row_and_accept(subject)
        assert not ticket_list.is_row_visible(subject), f"Row '{subject}' is still visible"
        ticket_list.expect_toast(MSG_TICKET_DELETED)
        with allure.step("[PASSED] Row deleted and toast displayed"):
            pass
```
