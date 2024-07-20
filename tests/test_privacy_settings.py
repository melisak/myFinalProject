from tests.conftest import *

@pytest.mark.ui
@allure.title("Test 'Privacy Settings' Page")
@allure.description("Test 'Privacy Settings' Pag")
class TestPrivacySettings:

    @allure.step("Test 'Privacy Settings Page & Toggle the privacy mode")
    def test_01_toggle_privacy_mode(self, privacy_settings_page, logged_in_context):
        privacy_settings_page.navigate_to_privacy_settings_page()
        assert privacy_settings_page.get_privacy_settings_text() == "Privacy & Content Moderation Settings"
        initial_state = privacy_settings_page.is_privacy_mode_enabled()
        privacy_settings_page.toggle_privacy_mode()
        final_state = privacy_settings_page.is_privacy_mode_enabled()
        assert initial_state != final_state, "Privacy mode should have been toggled"

    @allure.step("Test toggle 'Safe Mode'")
    def test_02_toggle_safe_mode(self, privacy_settings_page, logged_in_context):
        privacy_settings_page.navigate_to_privacy_settings_page()
        initial_state = privacy_settings_page.is_safe_mode_enabled()
        privacy_settings_page.toggle_safe_mode()
        final_state = privacy_settings_page.is_safe_mode_enabled()
        assert initial_state != final_state, "Safe_mode mode should have been toggled"

    @allure.step("Test enable 'Privacy Mode'")
    def test_03_enable_privacy(self, privacy_settings_page, logged_in_context):
        privacy_settings_page.navigate_to_privacy_settings_page()
        privacy_settings_page.enable_privacy_mode()
        assert privacy_settings_page.is_privacy_mode_enabled() == True

    @allure.step("Test enable 'safe Mode'")
    def test_04_enable_safe_mode(self, privacy_settings_page, logged_in_context):
        privacy_settings_page.navigate_to_privacy_settings_page()
        privacy_settings_page.enable_safe_mode()
        assert privacy_settings_page.is_safe_mode_enabled() == True

    @allure.step("Test enable 'Privacy Mode'")
    def test_05_disable_privacy(self, privacy_settings_page, logged_in_context):
        privacy_settings_page.navigate_to_privacy_settings_page()
        privacy_settings_page.disable_privacy_mode()
        assert privacy_settings_page.is_privacy_mode_enabled() == False

    @allure.step("Test enable 'safe Mode'")
    def test_06_disable_safe_mode(self, privacy_settings_page, logged_in_context):
        privacy_settings_page.navigate_to_privacy_settings_page()
        privacy_settings_page.disable_safe_mode()
        assert privacy_settings_page.is_safe_mode_enabled() == False

    @allure.step("enable privacy settings and save - ")
    def test_07_enable_privacy_settings_and_save(self, privacy_settings_page, logged_in_context):
        privacy_settings_page.navigate_to_privacy_settings_page()
        privacy_settings_page.enable_privacy_mode()
        privacy_settings_page.enable_safe_mode()
        privacy_settings_page.save_privacy_settings()
        privacy_settings_page.navigate_to_privacy_settings_page()
        assert privacy_settings_page.is_privacy_mode_enabled() == True and privacy_settings_page.is_safe_mode_enabled() == True

    @allure.step("disable privacy settings and save")
    def test_08_disable_privacy_settings_and_save(self, privacy_settings_page, logged_in_context):
        privacy_settings_page.navigate_to_privacy_settings_page()
        privacy_settings_page.disable_privacy_mode()
        privacy_settings_page.disable_safe_mode()
        privacy_settings_page.save_privacy_settings()
        privacy_settings_page.navigate_to_privacy_settings_page()
        assert privacy_settings_page.is_privacy_mode_enabled() == False and privacy_settings_page.is_safe_mode_enabled() == False

    @allure.step("Test toggle privacy mode and cancel")
    def test_09_toggle_privacy_mode_and_cancel(self, privacy_settings_page, logged_in_context):
        privacy_settings_page.navigate_to_privacy_settings_page()
        initial_state = privacy_settings_page.is_privacy_mode_enabled()
        privacy_settings_page.toggle_privacy_mode()
        privacy_settings_page.click_cancel_link()
        privacy_settings_page.navigate_to_privacy_settings_page()
        final_state = privacy_settings_page.is_privacy_mode_enabled()
        assert initial_state == final_state

    @allure.step("Test toggle safe mode and cancel")
    def test_10_toggle_safe_mode_and_cancel(self, privacy_settings_page, logged_in_context):
        privacy_settings_page.navigate_to_privacy_settings_page()
        initial_state = privacy_settings_page.is_safe_mode_enabled()
        privacy_settings_page.toggle_safe_mode()
        privacy_settings_page.click_cancel_link()
        privacy_settings_page.navigate_to_privacy_settings_page()
        final_state = privacy_settings_page.is_safe_mode_enabled()
        assert initial_state == final_state


