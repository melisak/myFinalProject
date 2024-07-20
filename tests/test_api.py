from datetime import datetime

from smart_assertions import soft_assert, verify_expectations

from tests.conftest import *

USERNAME = "melisa_kadosh"

allure.title("Test Functionality via API")


@allure.description("Test Functionality via API")
class Test_API:
    @log_function
    @allure.step("Test get list api")
    @pytest.mark.api
    def test_get_lists(self, api_auth):
        response = api_auth.get(f'/people/{USERNAME}/lists.json')
        assert response.status == 200, f"Expected status code 200, but got {response.status}"

        list_data = response.json()

        if list_data["size"] == 0:
            logger.info("No Lists!")
        else:
            for list_item in list_data["entries"]:
                logger.info(f"\nlist_item: {list_item}")
        return list_data

    @log_function
    @allure.step("Test create list api")
    @pytest.mark.api
    def test_create_empty_list(self, api_auth):

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        params = {
            "name": f"Test List {timestamp}",

            "description": "This is an empty list with no books added yet."
        }

        response = api_auth.post(f'/people/{USERNAME}/lists.json', data=params)
        response_data = response.json()
        soft_assert(response.status == 200, f"Expected status code 200, but got {response.status}")
        soft_assert(response_data["key"] is not None)
        list_key = response_data['key']
        logger.info(f"List created with key: {list_key}")
        verify_expectations()
        return list_key

    @log_function
    @allure.step("Test create list with books api")
    @pytest.mark.api
    def test_create_list_with_books(self, api_auth):

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        # Perform an authenticated request to create an empty list
        params = {
            "name": f"Test List {timestamp}",
            "description": "This is list with 2 books ",
            "seeds": ["OL19994651W",
                      "OL2700489W"]
        }

        response = api_auth.post(f'/people/{USERNAME}/lists.json', data=params)
        response_data = response.json()
        soft_assert(response.status == 200,
                    f"test_create_list_with_books: Expected status code 200, but got {response.status}")
        soft_assert(response_data["key"] is not None)
        verify_expectations()
        list_key = response_data['key']
        logger.info(f"List created with key: {list_key}")
        return list_key

    @log_function
    @allure.step("Test delete list api - creates a list and deletes it")
    @pytest.mark.api
    def test_delete_a_list(self, api_auth):
        # Create a new list to ensure we hve a list
        list_key = self.test_create_empty_list(api_auth)
        response = api_auth.post(f'{list_key}/delete.json')
        assert response.status == 200, f"test_delete_a_list() : Expected status code 200, but got {response.status}"
        logger.info(f"List {list_key} deleted successfully.")

    @log_function
    @allure.step("Test delete api - delete a specific list")
    @pytest.mark.api
    def test_delete_all_lists(self, api_auth):
        list_data = self.test_get_lists(api_auth)

        if list_data["size"] == 0:
            logger.info("No lists To delete!")
        else:

            for list_item in list_data["entries"]:
                response = api_auth.post(f'{list_item['url']}/delete.json')
                soft_assert(response.status == 200,
                            f"test_delete_a_list() : Expected status code 200, but got {response.status}")
                logger.info(f"List {list_item['url']} deleted successfully.")

            verify_expectations()
