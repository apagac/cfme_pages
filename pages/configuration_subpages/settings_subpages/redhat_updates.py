from pages.base import Base
from pages.page import Page
from selenium.webdriver.common.by import By

class RedhatUpdates(Base):
    _edit_registration_button_locator = (By.CSS_SELECTOR, \
      "button#settings_rhn_edit")
    _register_with_locator = (By.CSS_SELECTOR, "select#register_to")
    _address_locator = (By.CSS_SELECTOR, "input#server_url")
    _login_locator = (By.CSS_SELECTOR, "input#customer_userid")
    _password_locator = (By.CSS_SELECTOR, "input#customer_password")
    _save_button_locator = (By.CSS_SELECTOR, "img[title='Save Changes']")
    _cancel_button_locator = (By.CSS_SELECTOR, "img[title='Cancel']")

    _cfme_version_locator = (By.CSS_SELECTOR, "div#form_div > table > tbody \
            > tr:nth-of-type(2) > td:nth-of-type(6)")
    _all_appliances_locator = (By.CSS_SELECTOR, "div#form_div > table > tbody \
            > tr:nth-of-type(2)")
    _appliance_checkbox_locator = (By.CSS_SELECTOR, "input#listcheckbox")
    _apply_cfme_updates_button = (By.CSS_SELECTOR, "button#rhn_update_button_on_1")

    #def __init__(self, testsetup, item_class = RedhatUpdates.ApplianceItem):
    #    Page.__init__(self, testsetup)
    #    self.item_class = item_class

    def select_service(self, service):
        if service == "rhsm":
            self.select_dropdown("Red Hat Subscription Management", \
              *self._register_with_locator)
        elif service == "sat5":
            self.select_dropdown("RHN Satellite v5", \
              *self._register_with_locator)
        elif service == "sat6":
            self.select_dropdown("RHN Satellite v6", \
              *self._register_with_locator)
        self._wait_for_results_refresh()

    def edit_registration(self, url, credentials):
        #click on edit registration
        self.selenium.find_element(*self._edit_registration_button_locator).click()
        self._wait_for_results_refresh()
        #register with provider
        self.select_service(credentials)
        #fill data
        self.fill_field_by_locator(url, \
          *self._address_locator)
        self.fill_field_by_locator(credentials["username"], \
          *self._login_locator)
        self.fill_field_by_locator(credentials["password"], \
          *self._password_locator)

    def edit_registration_and_save(self, url, credentials):
        self.edit_registration(url, credentials)
        self._wait_for_visible_element(*self._save_button_locator)
        #click on save
        self.selenium.find_element(*self._save_button_locator).click()
        self._wait_for_results_refresh()
        return RedhatUpdates.Registered(self.testsetup)

    def edit_registration_and_cancel(self, url, credentials):
        self.edit_registration(url, credentials)
        self._wait_for_visible_element(*self._cancel_button_locator)
        #click on cancel
        self.selenium.find_element(*self._cancel_button_locator).click()
        self._wait_for_results_refresh()
        return RedhatUpdates.Cancelled(self.testsetup)

    #def get_appliance_versions(self, cfme_data):
    #    return cfme_data.data["redhat_updates"]["appliances"]

    #def get_appliance_current_version(self):
    #    return cfme_data.data["redhat_updates"]["current_version"]

    @property
    def all_appliances(self):
        #return [self.item_class(self.testsetup, appliance)
        return [RedhatUpdates.ApplianceItem(self.testsetup, appliance)
                for appliance in self.selenium.find_elements(*self._all_appliances_locator)]

    def are_old_versions_before_update(self):
        #cfme_data
        #versions_from_cfme_data = self.get_appliance_versions()
        #for appliance in self.all_appliances:
        #version_from_page = self.selenium.find_element(*self._cfme_version_locator).text
        #here we can use compare version function from rpm package
        #return version_from_page == version_from_cfme_data
        pass

    def is_current_version_after_update(self, current_version):
        #current_version_from_cfme_data = self.get_appliance_current_version()
        for appliance in self.all_appliances:
            if appliance.version != current_version:
                return False
        return True

    def apply_updates(self):
        self.selenium.find_element(*self._appliance_checkbox_locator).click()
        self._wait_for_visible_element(*self._apply_cfme_updates_button)
        self.selenium.find_element(*self._apply_cfme_updates_button).click()
        self._wait_for_results_refresh()

    class ApplianceItem(Base):
        #_name_locator = (By.CSS_SELECTOR, "td:nth-of-type(2)")
        #_zone_locator = (By.CSS_SELECTOR, "td:nth-of-type(3)")
        #_status_locator = (By.CSS_SELECTOR, "td:nth-of-type(4)")
        _last_checked_locator = (By.CSS_SELECTOR, "td:nth-of-type(5)")
        _version_locator = (By.CSS_SELECTOR, "td:nth-of-type(6)")
        _updates_available_locator = (By.CSS_SELECTOR, "td:nth-of-type(7)")


        #@property
        #def name(self):
        #    return self.selenium.find_element(*self._name_locator).text

        #@property
        #def zone(self):
        #    return self.selenium.find_element(*self._zone_locator).text

        #@property
        #def status(self):
        #    return self.selenium.find_element(*self._status_locator).text

        @property
        def last_checked(self):
            return self.selenium.find_element(*self._last_checked_locator).text

        @property
        def version(self):
            return self.selenium.find_element(*self._version_locator).text

        @property
        def updates_available(self):
            return self.selenium.find_element(*self._updates_available_locator).text \
                    == "Yes"

    class Registered(Base):
        _refresh_list_button_locator = ()
        _check_for_updates_button_locator = ()
        _register_button_locator = ()
        _apply_cfme_update_button_locator = ()
        _edit_registration_button_locator = ()

    class Cancelled(Base):
        pass
