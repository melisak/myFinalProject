from tests.conftest import *


@pytest.fixture(params=["dismiss", "accept"])
def dialog_status(request):
    return request.param


@pytest.mark.ui
@allure.title("Test 'My Loans' Page")
@allure.description("Test 'My Loans' Page")
class TestMyLoans:

    # The following tests test borrowing books from the carousel.
    # but sometimes the carousel is not present in the page, In this case these tests will be skipped:
    @allure.step("Borrow a book from carousel, or skip the test if carousel is absent")
    @pytest.mark.ui
    def borrow_a_book(self, my_loans_page, return_to_loans=True):
        my_loans_page.navigate_to_my_loans_page()
        if not my_loans_page.is_carousel_exist():
            pytest.skip("Carousel is not present on the page.")
        my_loans_page.borrow_book_from_carousel()
        if return_to_loans:
            my_loans_page.navigate_to_my_loans_page()

    @pytest.mark.ui
    @allure.step("Borrow a book and verify the 'Return now' button appear")
    def test_01_borrow_a_book_from_carousel(self, my_loans_page, logged_in_context):
        self.borrow_a_book(my_loans_page, False)
        assert my_loans_page.check_return_now_button() == "Return now"
        my_loans_page.navigate_to_my_loans_page()

    @pytest.mark.ui
    @allure.step("Test 'My Loans Page - Borrowed books list")
    def test_02_check_my_borrowed_books(self, my_loans_page, logged_in_context):
        my_loans_page.navigate_to_my_loans_page()
        total_books = my_loans_page.borrowed_books_list.count()
        print(f"\nTotal Books: {total_books}")
        for i in range(total_books):
            print("Book: " + my_loans_page.borrowed_books_list.nth(i).text_content())

    @pytest.mark.ui
    @allure.step("Test 'My Loans Page - borrow a book and verify it is in the borrowed list")
    def test_03_borrow_a_books_and_verify_borrowed(self, my_loans_page, logged_in_context):
        self.borrow_a_book(my_loans_page, True)
        total_books = my_loans_page.get_borrowed_books_list().count()
        assert total_books != 0

    @pytest.mark.ui
    @allure.step("Test 'My Loans Page - borrow a book and immediately return it")
    def test_04_return_now_borrowed_book(self, my_loans_page, logged_in_context):
        self.borrow_a_book(my_loans_page, True)
        assert my_loans_page.get_my_loans_header() == "Books You're Waiting For"

    @pytest.mark.ui
    @allure.step("Read a book from 'My Loans' Page")
    def test_05_borrow_a_book_and_read(self, my_loans_page, logged_in_context):
        self.borrow_a_book(my_loans_page, True)
        my_loans_page.read_book()
        with allure.step("Verify 'Return now' button appears in reading mode"):
            assert my_loans_page.check_return_now_button() == "Return now"
        my_loans_page.navigate_to_my_loans_page()

    @pytest.mark.ui
    @allure.step("Return a book from 'My Loans' Page according to dialog_status: - dismiss or accept the return")
    def test_06_return_book(self, my_loans_page, logged_in_context, dialog_status):
        with allure.step(f"click return a book and then {dialog_status}"):
            # prepare to dismiss \ accept the popup:
            my_loans_page.set_dialog_handler(dialog_status)
            self.borrow_a_book(my_loans_page, True)
            total_books_before = my_loans_page.get_borrowed_books_list().count()
            print(f"\ntotal books before: {total_books_before}")
            my_loans_page.return_book()
            total_books_after = my_loans_page.get_borrowed_books_list().count()
            print(f"\ntotal books after: {total_books_after}")
            if dialog_status == "dismiss":
                assert total_books_before == total_books_after
            else:
                assert total_books_before - 1 == total_books_after
            my_loans_page.navigate_to_my_loans_page()
