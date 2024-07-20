import time

from pages.base_page import BasePage
import allure
from playwright.sync_api import Page, Locator
from pages.privacy_settings_page import PrivacySettingsPage
from pages.my_loans_page import MyLoansPage


class MyBooksPage(BasePage):
    EDIT_GOAL_LINK = '//a[@class="edit-reading-goal-link"]'
    GOAL_FIELD = '//*[@id="yearly-goal-modal-1"]/form/input[@type="number"]'
    SUBMIT_GOAL_BUTTON = '//*[@id="yearly-goal-modal-1"]/form/button'
    SET_READING_GOAL_BUTTON = '//span/a[@class="set-reading-goal-link"]'
    NEW_GOAL_FIELD = '//input[@type="number"]'
    SUBMIT_NEW_GOAL_BUTTON = '//button[contains(@class, "reading-goal-submit-button")]'
    PRIVACY_SETTINGS_BUTTON = '//a[@href="/account/privacy"]'
    PRIVACY_SETTINGS_HEADER = '//h1'
    USER_NAME_LOCATOR = '//h2[@class="account-username"]'
    MY_LOANS_HEADER_TEXT = '//h1[@class = "details-title"]'
    MY_LOANS_LINK = '//h2/a[@name="loans"]'

    def __init__(self, page: Page):

        super().__init__(page)
        self.logger.info("MyBooksPage initialized")
        self.privacy_settings_page = PrivacySettingsPage(page)
        self.my_loans_page = MyLoansPage(page)
        self.goal_field: Locator = self.page.locator(self.GOAL_FIELD)
        self.user_name_locator: Locator = self.page.locator(self.USER_NAME_LOCATOR)
        self.edit_goal_link: Locator = self.page.locator(self.EDIT_GOAL_LINK)

    @allure.step("Check if a new reading goal is set: if we have an Edit option")
    def is_goal_set(self):
        return self.edit_goal_link.is_visible()

    @allure.step("Set Reading Goal")
    def set_reading_goal(self, goal):
        if self.is_goal_set():
            self.update_goal(goal)
        elif goal != 0:
            self.create_goal(goal)

    @allure.step("Update Reading Goal")
    def update_goal(self, goal):
        self.click(self.EDIT_GOAL_LINK)
        self.click(self.GOAL_FIELD)
        self.goal_field.clear()
        self.fill(self.GOAL_FIELD, str(goal))
        self.click(self.SUBMIT_GOAL_BUTTON)

    @allure.step("Create Reading Goal")
    def create_goal(self, goal):
        self.click(self.SET_READING_GOAL_BUTTON)
        self.fill(self.NEW_GOAL_FIELD, str(goal))
        self.click(self.SUBMIT_NEW_GOAL_BUTTON)

    @allure.step("Home Page - Get the user name")
    def get_username(self):
        full_text = self.text(self.USER_NAME_LOCATOR)
        user_name = full_text.split(' ')[0]
        return user_name

    @allure.step("Navigate to my books page")
    def navigate_to_my_books_page(self):
        username = self.get_username()
        my_books_path = f"{self.base_url}/people/{username}/books"
        self.page.goto(my_books_path)

    @allure.step("Home Page - Click the Privacy Settings Button")
    def click_privacy_settings(self):
        self.click(self.PRIVACY_SETTINGS_BUTTON)
        return self.privacy_settings_page

    @allure.step("Get the Privacy Settings Page text")
    def get_privacy_settings_header(self):
        return self.text(self.PRIVACY_SETTINGS_HEADER)

    def click_my_loans_link(self):
        self.logger.info(self.text(self.MY_LOANS_LINK))
        self.click(self.MY_LOANS_LINK)
        return self.my_loans_page

    @allure.step("Get My Loans Page text")
    def get_my_loans_header(self):
        return self.text(self.MY_LOANS_HEADER_TEXT)
