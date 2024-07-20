import time

from tests.conftest import *

@pytest.fixture(params=[7, 100, 3])
def goals(request):
    return request.param

GOAL = 5
@pytest.mark.ui
@allure.title("Test 'My Books' Page Yearly Reading Goal")
@allure.description("Set Yearly Reading Goal")
class TestMyBooks:

    @pytest.mark.ui
    @allure.step("Set yearly goal")
    def test_01_set_yearly_reading_goal(self, my_books_page, logged_in_context):
        my_books_page.navigate_to_my_books_page()
        my_books_page.set_reading_goal(GOAL)
        assert my_books_page.is_goal_set() == True

    @pytest.mark.ui
    @allure.step("Get user name")
    def test_02_get_user_name(self, my_books_page, logged_in_context):
        my_books_page.navigate_to_my_books_page()
        expected_user_name = "melisa_kadosh"
        actual_user_name = my_books_page.get_username()
        with allure.step("Verify the user name"):
            assert actual_user_name == expected_user_name, f"Expected '{expected_user_name}', but got '{actual_user_name}'"

    @pytest.mark.ui
    @allure.step("Set or Update reading goals")
    def test_03_set_or_update_reading_goal(self, my_books_page, logged_in_context, goals):
        my_books_page.navigate_to_my_books_page()
        goal = goals
        if my_books_page.is_goal_set():
            logger.info(f"Updating the goal to new goal {goal}")
        else:
            logger.info(f"No Goal is set - test is adding a new goal {goal}")
        my_books_page.set_reading_goal(goal)
        assert my_books_page.is_goal_set() == True

    @pytest.mark.ui
    @allure.step("Unset the reading Goal")
    def test_04_clear_reading_goal(self, my_books_page, logged_in_context):
        my_books_page.navigate_to_my_books_page()
        my_books_page.set_reading_goal(0)
        assert my_books_page.is_goal_set() == False

    @pytest.mark.ui
    @allure.step("Redirect to Privacy Settings")
    def test_05_click_privacy_setting(self, my_books_page, logged_in_context ):
        my_books_page.navigate_to_my_books_page()
        my_books_page.click_privacy_settings()
        assert my_books_page.get_privacy_settings_header() == "Privacy & Content Moderation Settings"

    @pytest.mark.ui
    @allure.step("Redirect to My Loans")
    def test_06_click_my_loans(self, my_books_page, logged_in_context):
        my_books_page.navigate_to_my_books_page()
        time.sleep(2)
        my_books_page.click_my_loans_link()
        print(my_books_page.get_my_loans_header())
        assert my_books_page.get_my_loans_header() == "Books You're Waiting For"






