import allure
import pytest
from playwright.sync_api import sync_playwright, BrowserContext

from pages.base_page import BasePage
from pages.my_books_page import MyBooksPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.privacy_settings_page import PrivacySettingsPage
from pages.my_loans_page import MyLoansPage
from pages.search_bar import SearchBar
from logger_setup import *

AUTH_STATE_FILE = "auth_state.json"
API_URL = "https://openlibrary.org"
S3_ACCESS_KEY = "a9trHRxGimbB6lrb"
S3_SECRET_KEY = "gaOosvUmgOjlPyzl"
API_PARAMS = dict(access=S3_ACCESS_KEY, secret=S3_SECRET_KEY)
HEADERS = {"Content-Type": "application/json"}

setup_logging()
logger = get_logger(__name__)
# Define the log directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
#VIEWPORT_SIZE = {"width": 1920, "height": 1080}
VIEWPORT_SIZE = {"width": 1366, "height": 768}


# Global variables to track initialization
_playwright = None
_browser = None


@log_fixture
@pytest.fixture(scope="session")
def playwright_instance():
    global _playwright
    if _playwright is None:
        logger.info("Initializing Playwright instance")
        _playwright = sync_playwright().start()
    yield _playwright
    _playwright.stop()
    logger.info("Playwright closed")
    _playwright = None


@log_fixture
@pytest.fixture(scope="session")
def browser_instance(playwright_instance):
    global _browser
    if _browser is None:
        logger.info("Launching browser")

    browser_type = BasePage.get_data_from_xml("BROWSER_TYPE").lower()
    slow_motion = int(BasePage.get_data_from_xml("SLOW_MO"))

    if browser_type == "chrome":
        _browser = playwright_instance.chromium.launch(headless=False, channel="chrome", slow_mo=slow_motion)
    elif browser_type == "edge":
        _browser = playwright_instance.chromium.launch(headless=False, channel="msedge", slow_mo=slow_motion)
    elif browser_type == "firefox":
        _browser = playwright_instance.firefox.launch(headless=False, slow_mo=slow_motion)
    else:
        raise ValueError(f"Unsupported browser type: {browser_type}")

    yield _browser
    _browser.close()
    logger.info("Browser closed")
    _browser = None


@log_fixture
@pytest.fixture(scope="session")
def context(browser_instance) -> BrowserContext:
    logger.info("Creating new browser context")

    # Load storage state if it exists
    if os.path.exists(AUTH_STATE_FILE):
        context = browser_instance.new_context(viewport=VIEWPORT_SIZE, storage_state=AUTH_STATE_FILE)
    else:
        context = browser_instance.new_context(
            viewport=VIEWPORT_SIZE)  # Create new context if loading state fails

    # Start tracing before tests
    trace_file_path = os.path.join(LOG_DIR, "trace.zip")
    context.tracing.start(snapshots=True, screenshots=True, sources=True)

    yield context
    # time.sleep(5)  # Ensure the page is not immediately closed at the end of the test
    context.tracing.stop(path=trace_file_path)
    context.storage_state(path=AUTH_STATE_FILE)
    context.close()
    logger.info("Browser context closed")


@log_fixture
@pytest.fixture(scope="function")
def page(context):
    logger.info("Creating new page")
    page = context.new_page()
    yield page
    page.close()
    logger.info("Page closed")


@log_fixture
@pytest.fixture(scope="session")
def request_context(playwright_instance):
    request_context = playwright_instance.request.new_context(base_url=API_URL)
    yield request_context
    request_context.dispose()
    logger.info("Page closed")


@log_fixture
@pytest.fixture(scope="session")
def api_auth(playwright_instance):
    # Create a request context for authentication
    auth_context = playwright_instance.request.new_context(base_url="https://openlibrary.org")

    # Perform the login request
    response = auth_context.post('/account/login.json', data=API_PARAMS)
    # Check if login was successful
    assert response.status == 200, f"Login failed with status {response.status}"

    # Extract the session ID from the set-cookie header
    session_cookie = response.headers['set-cookie']
    logger.debug(session_cookie)
    if session_cookie is None:
        raise Exception("Login failed, no session cookie returned")
    session_id = session_cookie.split(';')[0]  # Get the session ID part

    # Create a new request context with the session cookie set in the headers
    authenticated_context = playwright_instance.request.new_context(
        base_url="https://openlibrary.org",
        extra_http_headers={"Cookie": session_id}
    )

    yield authenticated_context
    authenticated_context.dispose()


@log_fixture
@pytest.fixture(scope="function")
def home_page(page):
    return HomePage(page)


@log_fixture
@pytest.fixture(scope="function")
def my_books_page(page):
    return MyBooksPage(page)


@log_fixture
@pytest.fixture(scope="function")
def search_bar(page):
    return SearchBar(page)


@log_fixture
@pytest.fixture(scope="function")
def login_page(page):
    return LoginPage(page)


@log_fixture
@pytest.fixture(scope="function")
def privacy_settings_page(page):
    return PrivacySettingsPage(page)


@log_fixture
@pytest.fixture(scope="function")
def my_loans_page(page):
    return MyLoansPage(page)


@log_fixture
@pytest.fixture(scope="function")
def logged_in_context(context, login_page):
    # Use storage state to determine if we are already logged in
    logger.debug("Starting logged_in_context fixture")
    context_storage = context.storage_state()
    cookies = context_storage['cookies']
    logged_in = any(cookie['name'] == 'sessionid' for cookie in cookies)

    if not logged_in:
        login_page.navigate_to_login_page()
        login_page.sign_in(login_page.username, login_page.password)
        # Save the state after logging in
        context.storage_state(path=AUTH_STATE_FILE)

    yield context
    # Perform logout
    login_page.logout()
    logger.debug("Logged out and cleaned up context")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Check if the test is marked as api and skip taking screenshots
    if 'api' in item.keywords:
        return

    if report.when == "call":
        markers = [marker.name for marker in item.iter_markers()]
        allure.dynamic.description(f"Markers: {', '.join(markers)}")
        if report.failed:
            try:
                page = item.funcargs.get("page")
                if page is not None:
                    image_path = os.path.join(LOG_DIR, f"{item.name}.png")
                    page.screenshot(path=image_path, full_page=True)
                    allure.attach.file(image_path, attachment_type=allure.attachment_type.PNG)
                else:
                    logger.warn("Warning: page fixture not found, cannot take screenshot")
            except Exception as e:
                logger.error(f"Failed to take screenshot: {str(e)}")


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before returning the exit status to the system.
    """

    if os.path.exists(AUTH_STATE_FILE):
        os.remove(AUTH_STATE_FILE)
        logger.info(f"Removed {AUTH_STATE_FILE}")
