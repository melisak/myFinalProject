from tests.conftest import *
import pytest_check as check  # Use check for Soft Assertions:


@pytest.fixture(params=[
    ("invalid_user1@gmail.com", "invalid_pass1"),
    ("invalid_user2@hotmail.com", "invalid_pass2"),
    ("invalid_user@gmail.com", ""),  # Case with empty password
    ("melisak@gmail.com", "invalid_pass"),  # valid username
])
def invalid_credentials(request):
    return request.param


@pytest.mark.ui
@allure.title("Test Login Functionality")
@allure.description("Verify user log operations (valid and Invalid)")
class TestLogin:

    @pytest.mark.ui
    @allure.step("Invalid login step")
    def test_01_invalid_login(self, login_page, invalid_credentials):
        username, password = invalid_credentials

        with allure.step(f"Attempt login with username: {username} and password: {password}"):
            login_page.navigate_to_login_page()
            login_page.sign_in(username, password)
            print(username, password)
            error_message = login_page.invalid_login_message()
            check.is_not_none(error_message, "Error message should be displayed for invalid login.")

    @pytest.mark.ui
    @allure.step("Valid login test")
    def test_02_valid_login(self, login_page):
        login_page.navigate_to_login_page()
        login_page.sign_in()
        print(login_page.is_logged_in())
        assert login_page.is_logged_in() == True, "Login Failed, My Account icon was not found on the page."
        login_page.logout()


    @pytest.mark.ui
    @allure.step("Log-Out test")
    def test_03_logout(self, login_page):
        login_page.navigate_to_login_page()
        login_page.sign_in()
        print(login_page.is_logged_in())
        login_page.logout()
        assert login_page.is_logged_in() == False, "Logout Failed."


