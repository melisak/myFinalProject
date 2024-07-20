from tests.conftest import *

@pytest.mark.ui
@allure.title("Test Home page Functionality")
@allure.description("Verify that user can navigate to different places from home page")
class TestHomePage:

    @pytest.mark.ui
    @allure.step("click login step")
    def test_01_click_login_button(self, home_page):
        home_page.navigate_to_home_page()
        print(f"\n{home_page.get_welcome_text()}")
        assert home_page.get_welcome_text() == 'Welcome to Open Library'
        home_page.click_login()
        print(home_page.get_login_text())
        assert home_page.get_login_text() == 'Log In'

    @pytest.mark.ui
    @allure.step("click 'My Books' link should lead to login page when you are not logged in")
    def test_02_my_books_link(self, home_page):
        home_page.navigate_to_home_page()
        home_page.click_my_books_link()

        assert home_page.get_login_text() == 'Log In'




