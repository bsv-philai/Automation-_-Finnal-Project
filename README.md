# baitap-auto-final

Repo automation cho **Final Project — Bài tập 17.08.2026** (trang luyện tập "サポートチケット管理").

- Trang bài tập: <https://bsv-nhungnguyen.github.io/bai_tap_17082026.html>
- Bộ testcase: `Automation _ Finnal Project - Testcases.csv` (88 case, bản gốc trên sheet: `bai_tap_17082026_testcases.tsv`)
- Rule bài tập: `Automation _ Finnal Project - Rules.csv`
- Quy tắc code: [automation_rules_final_project.md](automation_rules_final_project.md) — **đọc trước khi code**

## 1. Tổng quan bài tập

- Bài tập **CÁ NHÂN**, không chia nhóm/cặp. Mỗi người tự thao tác trên trang `bai_tap_17082026.html`.
- Thời gian: **3 tuần** làm bài + **1 tuần** Nhung review feedback.
- Trang **không có `data-testid`** — mô phỏng dự án thực tế, phải tự tìm locator theo đúng thứ tự
  ưu tiên (xem mục 4 của rules).
- Một số hành vi tưởng là bug nhưng là **chủ đích** của trang luyện tập (statistics không tự cập
  nhật, pagination bị ẩn thay vì disable, filter làm mất chọn checkbox...). Đọc kỹ rules trước khi
  báo lỗi.

## 2. Setup lần đầu

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
playwright install

cp .env.example .env
# Điền APP_URL / tài khoản admin / tài khoản guest vào .env

pytest tests/test_gd02_3_fill.py -k login -v
```

`.env` cần có (giá trị lấy ở mục 3 "Thông tin môi trường" trong file Rules):

```dotenv
APP_URL=https://bsv-nhungnguyen.github.io/bai_tap_17082026.html
ADMIN_ID=
ADMIN_PASSWORD=
GUEST_ID=
GUEST_PASSWORD=
HEADED=true
```

| Tài khoản | Dùng khi | Ghi chú |
|---|---|---|
| admin | Mặc định cho hầu hết case | Có sẵn data: 12 チケット, 3 通知 |
| guest | Case có 前提条件 ghi "guestでログイン済み" | Không có data — kiểm tra trạng thái mặc định (empty state) |

Nhóm case "デフォルトアカウント（guestユーザー）" **bắt buộc** dùng guest. Mỗi lần đăng nhập, data được
khởi tạo lại theo từng tài khoản → mỗi test tự login lại là đủ để độc lập.

Nếu case login (`GD02.3-007` admin, `GD02.3-004` guest) pass nghĩa là setup đúng.

## 3. Cách làm & cách ghi kết quả

Với mỗi case trong sheet Testcases:

1. Chọn case muốn làm.
2. Viết script Playwright và **chạy thử thực tế** để xác nhận.
3. Điền tên hàm vào cột **関数名** (VD: `test_ticket_list_next_page_shows_remaining_tickets`).
4. Điền tiến độ vào **スターテス**: `chưa làm` / `đang làm` / `hoàn thành`.
5. Điền **結果**: `OK` / `NG`. Nếu NG → tìm hiểu nguyên nhân trước khi ghi.
6. Điền **確認日** (ngày chạy) và **確認者** (tên mình).
7. Nếu NG → ghi vào **備考**: bước tái hiện, kết quả mong đợi, kết quả thực tế.

Case không tự động hoá được (xem mục 5) vẫn tạo hàm + `pytest.skip(...)`, ghi tên hàm vào 関数名
và lý do vào 備考.

## 4. Cấu trúc thư mục (đề xuất)

```
baitap_auto_final/
├── README_final_project.md            # File này
├── automation_rules_final_project.md  # Quy tắc code - ĐỌC TRƯỚC KHI CODE
├── conftest.py                        # Fixtures: login admin/guest, page objects, screenshot hook
├── helpers.py                         # description_md decorator
├── constants/
│   ├── locators.py                    # 1 class locator / màn hình
│   ├── messages.py                    # Toast, error, empty-state message
│   └── test_data.py                   # Số liệu mong đợi (12 ticket, 5 件 高...)
├── pages/
│   ├── base_page.py                   # BasePage - click/fill/expect + random data
│   ├── login_page.py                  # ログイン画面
│   ├── header_component.py            # ヘッダー (tab, user menu, logout)
│   ├── ticket_list_page.py            # チケット一覧 (filter, sort, paging, bulk, kebab)
│   ├── ticket_detail_dialog.py        # チケット詳細ダイアログ (edit, file upload)
│   ├── ticket_create_drawer.py        # 新規チケット作成ドロワー (Step1/Step2)
│   ├── notification_page.py           # 通知 (search, get-or-create)
│   ├── statistics_page.py             # 統計 (再集計)
│   └── settings_page.py               # 設定 (signature, toggle)
├── tests/                             # 1 file / Category của sheet
│   ├── test_gd01_navigation.py
│   ├── test_gd02_1_click.py
│   ├── test_gd02_2_check.py
│   ├── test_gd02_3_fill.py
│   ├── test_gd02_4_select_option.py
│   ├── test_gd02_5_hover.py
│   ├── test_gd02_6_keyboard.py
│   ├── test_gd02_7_file_upload.py
│   ├── test_gd02_8_assertion.py
│   ├── test_gd03_1_dialog.py
│   ├── test_gd03_2_iframe.py
│   ├── test_gd03_3_tab_window.py
│   └── test_others.py                 # Toàn bộ Others_* (đa số skip - manual)
├── .github/workflows/e2e.yml          # CI chạy test + upload Allure report
├── .env.example
├── requirements.txt
└── pytest.ini
```

> Test file chia theo **Category** (cột B), không theo 大項目 (cột D). Cột 大項目 trong sheet bị lệch
> so với nội dung (VD: `GD03.1-02` prompt nằm dưới "ログイン画面", `GD02.4-01` nằm dưới "OS・環境依存"),
> nên khi chọn page object hãy dựa vào **小項目 + テスト手順**, không dựa vào 大項目.

## 5. Phân loại 88 testcase

| Category | Số case | ID | Ghi chú |
|---|---:|---|---|
| GD01-Navigation | 6 | GD01_001 – 006 | `GD01_001` (back/forward "仕様どおり") spec chưa rõ |
| GD02.1-Click | 22 | GD02.1-01 – 22 | `GD02.1-12` (double submit) cần xác nhận spec |
| GD02.2-Check | 2 | GD02.2-001 – 002 | Bẫy checkbox `opacity:0` |
| GD02.3-Fill | 7 | GD02.3-001 – 007 | Login, search, counter 100 ký tự |
| GD02.4-SelectOption | 3 | GD02.4-01 – 03 | Filter làm mất chọn checkbox |
| GD02.5-Hover | 1 | GD02.5-001 | Tooltip cột 作成日 |
| GD02.6-Keyboard | 2 | GD02.6-01 – 02 | `GD02.6-01` (toàn bộ thao tác bằng phím) mơ hồ |
| GD02.7-FileUpload | 4 | GD02.7-01 – 04 | `GD02.7-02` (OS dialog) → manual |
| GD02.8-Assertion | 16 | GD02.8-01 – 16 | Nhiều case empty-state của guest |
| GD03.1-Dialog | 6 | GD03.1-01 – 06 | confirm / prompt / alert |
| GD03.2-Iframe | 1 | GD03.2-01 | `frame_locator` |
| GD03.3-TabWindow | 4 | GD03.3-01 – 04 | `GD03.3-02`, `GD03.3-03` → manual / spec chưa rõ |
| Others | 14 | Others_01 – 14 | **Manual** (OS, mạng thật, thiết bị thật, crash...) |
| **Tổng** | **88** | | |

**Không tự động hoá được → tạo hàm + `pytest.skip` kèm lý do:**

- `Others_01` – `Others_14`: đòi hỏi thiết bị/OS/mạng/trình duyệt **thật** (đổi giờ OS, rút mạng,
  sleep máy, kill browser, in thật, nhiều user đồng thời...). Playwright có thể *giả lập* một phần
  (viewport, `context.set_offline`, `page.clock`) nhưng không thoả "実端末/実ネットワーク" → chỉ
  làm nếu đã thống nhất với Nhung.
- `GD02.7-02`: hộp thoại chọn file của OS không tự động hoá được (Rules #6).
- `GD03.3-03`: thao tác trên site bên ngoài thật — nằm ngoài phạm vi app.
- `GD03.3-02`, `GD01_001`, `GD02.6-01`, `GD02.1-12`: kết quả mong đợi ghi "仕様に従って/仕様どおり"
  mà không mô tả spec → skip với lý do "spec incomplete" hoặc hỏi lại trước khi làm.

## 6. Pattern bắt buộc phải luyện

- **get-or-create** ở màn 通知: gom thành 1 hàm `ensure_notification_exists(title, content)` trong
  `NotificationPage` — search → nếu 0 件 thì bấm "＋通知を作成する" ngay dưới message → tạo mới;
  nếu đã có thì không làm gì. Dùng lại hàm này cho setup các case cần ≥6 通知 (`GD02.1-10`).
- **Dialog của browser** (confirm/prompt/alert): đăng ký handler **trước** khi click.
- **Bất đồng bộ có chủ đích** ở 統計: phải bấm "再集計する" thì số mới cập nhật.

Chi tiết + code mẫu: xem mục "Page-specific Traps" trong rules.

## 7. Report

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

Hoặc chạy + mở report một bước:

```bash
bash run_and_open_allure_report.sh      # nhập keyword, VD: GD02.1-02, GD03.1-01
```

Screenshot (pass + fail) và video (fail) tự đính kèm Allure qua hook trong `conftest.py`.

## 8. Nộp bài

1. Tạo **MR vào nhánh `develop`**, assignee **Nhung**. Làm tới đâu commit/tạo branch tới đó.
2. Tích hợp **Allure report** vào source (nếu được).
3. Tạo **CI/CD trên GitHub Actions** để chạy test trực tiếp trên GitHub
   (headless, secrets: `APP_URL`, `ADMIN_ID`, `ADMIN_PASSWORD`, `GUEST_ID`, `GUEST_PASSWORD`;
   upload `allure-report` làm artifact).
4. Cập nhật sheet Testcases (関数名 / スターテス / 結果 / 確認日 / 確認者 / 備考) khớp với code trong MR.

## 9. Câu hỏi & báo lỗi

- Thắc mắc về rule/testcase: comment trực tiếp trên sheet hoặc hỏi Nhung qua kênh liên hệ của lớp.
- Trước khi báo bug: đối chiếu với Rules #5 – #8 (bẫy có chủ đích).

## 10. Lưu ý

- File `.env` **không commit**. Không hardcode tài khoản trong test, page object hay tài liệu.
- Không commit HTML dump, screenshot, file test upload (tạo file upload trong code/`tmp_path`).
