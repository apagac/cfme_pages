from pages.base import Base
from selenium.webdriver.common.by import By

class RedhatUpdates(Base):
    #_edit_registration_button_locator = (By.CSS_SELECTOR, \
    #    "")
    #_http_proxy_locator = ()

    def click_on_edit_registration(self):
        self.selenium.find_element(*self._edit_registration_button_locator).click()
        self._wait_for_results_refresh()
        return RedhatUpdates.EditRegistration(self.testsetup)

    def click_on_http_proxy(self):
        self.selenium.find_element(*self._http_proxy_locator).click()
        return RedhatUpdates.HTTPProxy(self.testsetup)

    #LOCATORS
    _edit_registration_button_locator = (By.CSS_SELECTOR, \
      "button#settings_rhn_edit")
    _register_with_locator = (By.CSS_SELECTOR, "select#register_to")
    _address_locator = (By.CSS_SELECTOR, "input#server_url")
    _login_locator = (By.CSS_SELECTOR, "input#customer_userid")
    _password_locator = (By.CSS_SELECTOR, "input#customer_password")
    _save_button_locator = (By.CSS_SELECTOR, "img[title='Save Changes']")
    _cancel_button_locator = (By.CSS_SELECTOR, "img[title='Cancel']")

    def select_service(self, services):
        if services == "rhsm":
            self.select_dropdown("Red Hat Subscription Management", \
              *self._register_with_locator)
        elif services == "sat5":
            self.select_dropdown("RHN Satellite v5", \
              *self._register_with_locator)
        elif services == "sat6":
            self.select_dropdown("RHN Satellite v6", \
              *self._register_with_locator)
        self._wait_for_results_refresh()

    def edit_registration(self, services, **rh_updates_data):
        #click on edit registration
        self.selenium.find_element(*self._edit_registration_button_locator).click()
        self._wait_for_results_refresh()
        #register with provider
        self.select_service(services)
        #fill data
        self.fill_field_by_locator(rh_updates_data["url"], \
          *self._address_locator)
        credentials = self.testsetup.credentials[services]
        self.fill_field_by_locator(credentials["username"], \
          *self._login_locator)
        self.fill_field_by_locator(credentials["password"], \
          *self._password_locator)

    def edit_registration_and_save(self, services, **rh_updates_data):
        self.edit_registration(services, **rh_updates_data)
        self._wait_for_visible_element(*self._save_button_locator)
        #click on save
        self.selenium.find_element(*self._save_button_locator).click()
        self._wait_for_results_refresh()
        return RedhatUpdates.Registered(self.testsetup)

    def edit_registration_and_cancel(self, services, **rh_updates_data):
        self.edit_registration(services, **rh_updates_data)
        self._wait_for_visible_element(*self._cancel_button_locator)
        #click on cancel
        self.selenium.find_element(*self._cancel_button_locator).click()
        self._wait_for_results_refresh()
        return RedhatUpdates.Cancelled(self.testsetup)

    class HTTPProxy(Base):
        _address_locator = ()
        _user_id_locator = ()
        _password_locator = ()

        def fill_data(self, rh_updates_data):
            #address
            self.selenium.find_element(*self._address_locator).send_keys(
                rh_updates_data["http_proxy"]["url"])
            #user id
            self.selenium.find_element(*self._user_id_locator).send_keys(
                rh_updates_data["http_proxy"]["username"])
            #password
            self.selenium.find_element(*self._password_locator).send_keys(
                rh_updates_data["http_proxy"]["password"])

    class Registered(Base):
        _refresh_list_button_locator = ()
        _check_for_updates_button_locator = ()
        _register_button_locator = ()
        _apply_cfme_update_button_locator = ()
        _edit_registration_button_locator = ()

    class Cancelled(Base):
        pass
