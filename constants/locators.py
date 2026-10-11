"""Locator cho từng màn hình. Mỗi page class import class tương ứng với tên `locators`."""


class BaseLocators:
    TOAST = "#toast_container .toast"  # トースト通知


class LoginLocators:
    LOGIN_SECTION = "#login_section"  # ログイン画面のセクション
    ID_LABEL = "ID"  # ID入力欄のラベル
    PASSWORD_LABEL = "パスワード"  # パスワード入力欄のラベル
    LOGIN_BUTTON = "ログイン"  # ログインボタン
    ERROR_MESSAGE = "#login_error"  # ログインエラーメッセージ


class HeaderLocators:
    MAIN_SECTION = "#main_section"  # ログイン後のメイン画面
    USER_NAME = "#header_username"  # ヘッダー右上のユーザー名
    TAB_NOTIFICATIONS = "#nav_tab_notifications"  # ヘッダーの「通知」タブ
    TAB_SETTINGS = "#nav_tab_settings"  # ヘッダーの「設定」タブ


class TicketListLocators:
    PANEL = "#panel_tickets"  # チケット一覧パネル
    ROWS = "#ticket_tbody tr"  # 一覧テーブルの行
    TBODY = "#ticket_tbody"  # 一覧テーブルの本体（空状態メッセージを含む）
    SEARCH_PLACEHOLDER = "件名または担当者で検索"  # キーワード検索欄
    PRIORITY_FILTER_LABEL = "優先度で絞り込み"  # 優先度プルダウン
    PAGINATION_TOP = "#pagination_top"  # 一覧上部のページネーション
    PAGINATION_BOTTOM = "#pagination_bottom"  # 一覧下部のページネーション
    NEXT_BUTTON = "次へ"  # ページネーションの次へボタン（コンテナスコープで使用）
    PREV_BUTTON = "前へ"  # ページネーションの前へボタン（コンテナスコープで使用）
    CREATED_HEADER = "#th_created"  # 「作成日」列見出し（ソート）
    SORT_ICON = "#sort_icon"  # 作成日列のソートアイコン
    CREATED_DATE_CELL_PATTERN = r"^\d{4}-\d{2}-\d{2}$"  # 作成日セル（行スコープで使用）
    TOOLTIP_TRIGGER = ".tooltip-wrap"  # 作成日列見出しのヘルプアイコン
    TOOLTIP_CONTENT = ".tooltip-content"  # ヘルプアイコンのツールチップ
    SELECT_ALL_CHECKBOX = "全て選択"  # 全選択チェックボックス（実体のinput）
    ROW_CHECKBOX = ".row-checkbox"  # 行のチェックボックス（実体のinput）
    ROW_CHECKBOX_UNCHECKED = ".row-checkbox:not(:checked)"  # 未チェックの行チェックボックス
    BULK_ACTION_BAR = "#bulk_action_bar"  # 一括操作バー
    BULK_COMPLETE_BUTTON = "選択した項目を一括対応完了にする"  # 一括対応完了ボタン
    DETAIL_BUTTON = "詳細"  # 行内の詳細ボタン（行スコープで使用）
    DELETE_BUTTON = "削除"  # 行内の削除ボタン（行スコープで使用）
    KEBAB_BUTTON = "その他の操作"  # 行内のケバブ（⋮）ボタン（行スコープで使用）
    KEBAB_MENU = ".kebab-menu"  # ケバブメニュー（行スコープで使用）
    KEBAB_DONE_ITEM = "完了にする"  # ケバブメニューの「完了にする」
    EMPTY_CREATE_BUTTON = "＋新規チケット作成"  # 空状態の新規チケット作成ボタン
    PREVIEW_IFRAME = "#preview_iframe"  # 埋め込みプレビューのiframe
    FRAME_STATUS_SELECT = "#frame_status"  # iframe内のステータスプルダウン
    FRAME_APPLY_BUTTON = "適用"  # iframe内の適用ボタン
    FRAME_RESULT = "#frame_result"  # iframe内の結果メッセージ
    OPEN_MANUAL_BUTTON = "外部マニュアルを開く（新しいタブ）"  # 外部マニュアルボタン
    PRINT_PREVIEW_BUTTON = "印刷プレビューを開く（新しいウィンドウ）"  # 印刷プレビューボタン
    REASSIGN_BUTTON = "担当者を再割り当てする"  # 担当者再割り当てボタン
    REASSIGN_RESULT = "#reassign_result"  # 再割り当て結果の表示欄
    POPUP_BODY = "body"  # 印刷プレビュー（ポップアップ）の本文


class TicketDetailLocators:
    DIALOG = "チケット詳細"  # 詳細ダイアログ
    FILE_INPUT = "#detail_file_input"  # 添付ファイルのinput（display:none）
    FILE_PREVIEW = "#detail_file_preview"  # 添付ファイルのプレビュー
    FILE_NAME = "#detail_file_name"  # プレビューのファイル名とサイズ
    REMOVE_FILE_BUTTON = "ファイルを削除"  # プレビューの削除アイコン
    FILE_ERROR = "#detail_file_error"  # 添付ファイルのエラーメッセージ


class NotificationLocators:
    PANEL = "#panel_notifications"  # 通知一覧パネル
    ROWS = "#notification_tbody tr"  # 通知テーブルの行


class SettingsLocators:
    PANEL = "#panel_settings"  # 設定パネル
    SIGNATURE_PLACEHOLDER = "返信メールに付与する署名を入力"  # 署名欄
    SIGNATURE_COUNTER = "#signature_counter"  # 署名の文字数カウンター
