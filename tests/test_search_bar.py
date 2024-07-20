

from tests.conftest import *

@pytest.fixture(params=[
    ("Gone with The wind"),
    ("Armagedon"),
    ("Harry Potter"),
])
def books(request):
    return request.param


@pytest.mark.ui
@allure.title("Test Search Bar - ")
@allure.description("test the search bar that appears on every page")
class TestSearchBar:



    def test_01_search_a_book(self, search_bar, logged_in_context, books):
        book=books
        search_bar.search_a_book(book)
        count = search_bar.get_results_count()
        print(f"\nFound: {count} hits")
        assert count > 0


