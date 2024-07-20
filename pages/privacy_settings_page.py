from pages.base_page import BasePage
import allure
from playwright.sync_api import Page, Locator


class PrivacySettingsPage(BasePage):

    PRIVACY_SETTINGS_HEADER = '//h1'
    PRIVACY_YES_CSS = '#r0'
    PRIVACY_NO_CSS = '#r1'
    SAFE_MODE_YES_CSS = '#r2'
    SAFE_MODE_NO_CSS = '#r3'
    SAVE_BUTTON = '//button[@title="Save"]'
    CANCEL_LINK = '//a[@class="smaller attn"]'

    def __init__(self, page : Page):
        super().__init__(page)
        self.logger.info("PrivacySettingsPage initialized")
        self.privacy_no: Locator = self.page.locator(self.PRIVACY_NO_CSS)
        self.safe_mode_yes: Locator = self.page.locator(self.SAFE_MODE_YES_CSS)
        self.safe_mode_no: Locator = self.page.locator(self.SAFE_MODE_NO_CSS)
        self.privacy_yes: Locator = self.page.locator(self.PRIVACY_YES_CSS)

    @allure.step("Navigate to my books page")
    def navigate_to_privacy_settings_page(self):
        privacy_settings_path = f"{self.base_url}/account/privacy"
        self.page.goto(privacy_settings_path)

    @allure.step("Get the Privacy Settings Page text")
    def get_privacy_settings_text(self):
        return self.text(self.PRIVACY_SETTINGS_HEADER)

    @allure.step("toggle the privacy mode")
    def toggle_privacy_mode(self):
        if self.privacy_yes.is_checked():
            self.privacy_no.check()
        else:
            self.privacy_yes.check()

    @allure.step("toggle the safe mode")
    def toggle_safe_mode(self):
        if self.safe_mode_yes.is_checked():
            self.safe_mode_no.check()
        else:
            self.safe_mode_yes.check()

    @allure.step("enable the privacy mode")
    def enable_privacy_mode(self):
        if not self.is_privacy_mode_enabled():
            self.privacy_yes.check()

    @allure.step("enable the safe mode")
    def enable_safe_mode(self):
        if not self.is_safe_mode_enabled():
            self.safe_mode_yes.check()

    @allure.step("disable the privacy mode")
    def disable_privacy_mode(self):
        if self.is_privacy_mode_enabled():
            self.privacy_no.check()

    @allure.step("disable the safe mode")
    def disable_safe_mode(self):
        if self.is_safe_mode_enabled():
            self.safe_mode_no.check()

    @allure.step("check if the privacy mode is enabled")
    def is_privacy_mode_enabled(self):
        return self.privacy_yes.is_checked()

    @allure.step("check if the safe mode is enabled")
    def is_safe_mode_enabled(self):
        return self.safe_mode_yes.is_checked()

    @allure.step("Save privacy settings")
    def save_privacy_settings(self):
        self.click(self.SAVE_BUTTON)

    @allure.step("Cancel changes in the privacy settings")
    def click_cancel_link(self):
        self.click(self.CANCEL_LINK)
