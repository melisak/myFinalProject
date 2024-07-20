from pages.base_page import BasePage
import allure
from playwright.sync_api import Page
from pages.login_page import LoginPage

class HomePage(BasePage):

    WELCOME_HEADING_TEXT = 'Welcome to Open Library'
    LOG_IN_HEADING_TEXT = 'Log In'
    LOGIN_BUTTON = '//a[@class ="btn"]'
    MY_BOOKS_LINK = "//a[text()='My Books']"

    def __init__(self, page : Page):
        super().__init__(page)
        self.logger.info("HomePage initialized")
        self.login = LoginPage(page)


    @allure.step("Navigate to the homepage")
    def navigate_to_home_page(self):
        self.page.goto(self.base_url)

    @allure.step("Get the welcome text")
    def get_welcome_text(self):
        return self.text('heading',selector_type='role', name=self.WELCOME_HEADING_TEXT)


    @allure.step("Get the Login text")
    def get_login_text(self):
        return self.text('heading', selector_type='role', name=self.LOG_IN_HEADING_TEXT)


    @allure.step("Home Page - Click the Login button")
    def click_login(self):
        self.click(self.LOGIN_BUTTON)
        return self.login

    @allure.step("Home Page - Click my books link")
    def click_my_books_link(self):
        self.click(self.MY_BOOKS_LINK, index=0)




