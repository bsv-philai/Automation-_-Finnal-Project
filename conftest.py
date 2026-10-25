import os
from datetime import datetime
from pathlib import Path

import allure
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Browser, Page

from constants.test_data import TARGET_TICKET_SUBJECT
from pages.header_component import HeaderComponent
from pages.login_page import LoginPage
from pages.notification_page import NotificationPage
from pages.settings_page import SettingsPage
from pages.ticket_detail_dialog import TicketDetailDialog
from pages.ticket_list_page import TicketListPage

load_dotenv()

APP_URL = os.environ["APP_URL"]
ADMIN_ID = os.environ["ADMIN_ID"]
ADMIN_PASSWORD = os.environ["ADMIN_PASSWORD"]
GUEST_ID = os.environ["GUEST_ID"]
GUEST_PASSWORD = os.environ["GUEST_PASSWORD"]
HEADED = os.getenv("HEADED", "false").lower() == "true"

ROOT_DIR = Path(__file__).parent
SCREENSHOT_DIR = ROOT_DIR / "screenshots"
VIDEO_DIR = ROOT_DIR / "videos"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


def _test_outcome(node: pytest.Item) -> str:
    report = getattr(node, "rep_call", None) or getattr(node, "rep_setup", None)
    if report is None:
        return "failed"
    return report.outcome


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    return {**browser_type_launch_args, "headless": not HEADED}


@pytest.fixture
def app_page(request: pytest.FixtureRequest, browser: Browser):
    """Page riêng cho mỗi test: chụp screenshot (pass + fail), đính kèm video khi fail."""
    context = browser.new_context(record_video_dir=str(VIDEO_DIR))
    page = context.new_page()
    yield page

    outcome = _test_outcome(request.node)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    SCREENSHOT_DIR.mkdir(exist_ok=True)
    screenshot_path = SCREENSHOT_DIR / f"{request.node.name}_{outcome}_{timestamp}.png"
    if outcome != "skipped":
        page.screenshot(path=str(screenshot_path), full_page=True)
        allure.attach.file(
            str(screenshot_path), name=f"screenshot_{outcome}", attachment_type=allure.attachment_type.PNG
        )

    # Gồm cả video của popup / tab mới mở trong test
    videos = [opened.video for opened in context.pages if opened.video]
    context.close()
    for index, video in enumerate(videos):
        if outcome == "failed":
            allure.attach.file(video.path(), name=f"video_{index}", attachment_type=allure.attachment_type.WEBM)
        else:
            video.delete()


@pytest.fixture
def access_to_login_screen(app_page: Page) -> Page:
    LoginPage(app_page).open(APP_URL)
    return app_page


@pytest.fixture
def access_to_home_screen(access_to_login_screen: Page) -> Page:
    LoginPage(access_to_login_screen).login(ADMIN_ID, ADMIN_PASSWORD)
    return access_to_login_screen


@pytest.fixture
def access_to_home_screen_as_guest(access_to_login_screen: Page) -> Page:
    LoginPage(access_to_login_screen).login(GUEST_ID, GUEST_PASSWORD)
    return access_to_login_screen


@pytest.fixture
def admin_credentials() -> tuple[str, str]:
    return ADMIN_ID, ADMIN_PASSWORD


@pytest.fixture
def login_page(access_to_login_screen: Page) -> LoginPage:
    return LoginPage(access_to_login_screen)


@pytest.fixture
def header_on_login_screen(access_to_login_screen: Page) -> HeaderComponent:
    return HeaderComponent(access_to_login_screen)


@pytest.fixture
def ticket_list_on_login_screen(access_to_login_screen: Page) -> TicketListPage:
    return TicketListPage(access_to_login_screen)


@pytest.fixture
def header(access_to_home_screen: Page) -> HeaderComponent:
    return HeaderComponent(access_to_home_screen)


@pytest.fixture
def ticket_list(access_to_home_screen: Page) -> TicketListPage:
    return TicketListPage(access_to_home_screen)


@pytest.fixture
def ticket_list_as_guest(access_to_home_screen_as_guest: Page) -> TicketListPage:
    return TicketListPage(access_to_home_screen_as_guest)


@pytest.fixture
def ticket_detail_dialog(ticket_list: TicketListPage) -> TicketDetailDialog:
    dialog = ticket_list.open_detail(TARGET_TICKET_SUBJECT)
    dialog.expect_opened()
    return dialog


@pytest.fixture
def notification_page(header: HeaderComponent) -> NotificationPage:
    return header.go_to_notifications()


@pytest.fixture
def settings_page(header: HeaderComponent) -> SettingsPage:
    return header.go_to_settings()
