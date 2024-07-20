from pages.base_page import BasePage
import allure
from playwright.sync_api import Page, Locator


class SearchBar(BasePage):
    SEARCH_BAR_LOCATOR = "//input[@type='text']"
    SEARCH_RESULTS_LOCATOR = '//div[@class="search-results-stats"]'

    def __init__(self, page: Page):
        super().__init__(page)
        self.search_bar_locator: Locator = self.page.locator(self.SEARCH_BAR_LOCATOR)
        self.search_bar_results: Locator = self.page.locator(self.SEARCH_RESULTS_LOCATOR)

    @allure.step("Search a book")
    def search_a_book(self, book: str):
        self.fill(self.SEARCH_BAR_LOCATOR, text=book, index=0)
        self.search_bar_locator.press("Enter")

    @allure.step("Get number of results")
    def get_results_count(self):
        text = self.text(self.SEARCH_RESULTS_LOCATOR)
        self.logger.info(f"parsing {text}")
        results_count = self.extract_results_count(text)
        return results_count
