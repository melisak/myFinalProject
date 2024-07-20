from pages.base_page import BasePage
import allure
from playwright.sync_api import Page, Locator


class LoginPage(BasePage):
    ACCOUNT_ICON_ALT_TEXT = 'My account'
    USERNAME_LOCATOR = '//input[@id="username"]'
    PASSWORD_LOCATOR = '//input[@id="password"]'
    BUTTON_LOCATOR = '//button[@type="submit"]'
    LOG_OUT_TEXT = 'Log Out'
    INVALID_LOGIN_LOCATOR = '//div[@class="note"]'

    def __init__(self, page: Page):
        super().__init__(page)
        self.logger.info("LoginPage initialized")

        self.my_account_button = self.page.get_by_role('img', name=self.ACCOUNT_ICON_ALT_TEXT)
        self.log_in_text_locator: Locator = self.page.get_by_text("You are already logged into Open Library")

    def navigate_to_login_page(self):
        self.page.goto(f"{self.base_url}/account/login")

    @allure.step("Sign in using provided username and password - or defaults logins credentials if not provided")
    def sign_in(self, username=None, password=None):
        if self.is_logged_in():
            self.logout()
        self.logger.info("Starting sign_in process")
        self.navigate_to_login_page()
        username = username or self.username
        password = password or self.password
        self.fill(self.USERNAME_LOCATOR, username)
        self.fill(self.PASSWORD_LOCATOR, password)
        self.click(self.BUTTON_LOCATOR)
        self.logger.debug("Finished sign_in process")

    @allure.step("Verify login")
    def is_logged_in(self):
        result = self.log_in_text_locator.is_visible() or self.my_account_button.is_visible()
        self.logger.info(f"Is logged in: {result}")
        return result

    def invalid_login_message(self):
        return self.text(self.INVALID_LOGIN_LOCATOR)

    def logout(self):
        self.click(selector='img', selector_type='role', name=self.ACCOUNT_ICON_ALT_TEXT)
        self.click(self.LOG_OUT_TEXT, selector_type='text', index=0)