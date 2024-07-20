import time

from pages.base_page import BasePage
import allure
from playwright.sync_api import Page, Locator




class MyLoansPage(BasePage):

    SELECTED_BOOK_NAME_HEADER = '//div[2]/span/h1'
    RETURN_NOW_BUTTON_TEXT = "Return now"
    BORROWED_BOOKS_LIST = '//span[@class="book"]'
    MY_LOANS_HEADER_TEXT = '//h1[@class = "details-title"]'
    READ_BUTTON_TEXT = "Read"
    RETURN_BOOK_TEXT = "Return book"

    def __init__(self, page : Page):
        super().__init__(page)
        self.logger.debug("MyLoansPage initialized")
        self.borrow_book_from_carousel_button: Locator = self.page.locator('#slick-slide00').get_by_role("link", name="Borrow")
        self.borrowed_books_list: Locator = self.page.locator(self.BORROWED_BOOKS_LIST)


    @allure.step("Navigate to My Loans page")
    def navigate_to_my_loans_page(self):
        my_loans_path = f"{self.base_url}/account/loans"
        self.page.goto(my_loans_path)

    @allure.step("Check if the carousel exists on the page")
    def is_carousel_exist(self):
        return  self.borrow_book_from_carousel_button.is_visible()

    @allure.step("Borrow a book from the carousel")
    def borrow_book_from_carousel(self):
        self.borrow_book_from_carousel_button.click()

    @allure.step("Get selected book header (from books page)")
    def get_selected_book_header(self):
        return self.text(self.SELECTED_BOOK_NAME_HEADER)

    @allure.step("After borrowing a book check 'Return Now' button")
    def check_return_now_button(self):
        return self.text('button', selector_type='role', name=self.RETURN_NOW_BUTTON_TEXT)

    @allure.step("Get borrowed books list")
    def get_borrowed_books_list(self):
        self.logger.info(f"list count: {self.borrowed_books_list.count()}")
        return self.borrowed_books_list

    @allure.step("Return now borrowed book")
    def return_now_borrowed_book(self):
        self.click(self.RETURN_NOW_BUTTON_TEXT)

    @allure.step("Get My Loans Page text")
    def get_my_loans_header(self):
        return self.text(self.MY_LOANS_HEADER_TEXT)

    @allure.step("Read borrowed book")
    def read_book(self):
        self.click(selector='button', selector_type='role', name = self.READ_BUTTON_TEXT, index=0)

    @allure.step("Return (first) book")
    def return_book(self):
        self.click("button",selector_type="role", name=self.RETURN_BOOK_TEXT)

