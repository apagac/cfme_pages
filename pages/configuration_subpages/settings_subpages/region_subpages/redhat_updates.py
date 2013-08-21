class RedhatUpdates(Base):
    _edit_registration_button_locator = (By.CSS_SELECTOR, \
        "")
    _http_proxy_locator = ()

    def click_on_edit_registration(self):
        self.selenium.find_element(*self._edit_registration_button_locator).click()
        self._wait_for_results_refresh()
        return RedhatUpdates.EditRegistration(self.testsetup)

    def click_on_http_proxy(self):
        self.selenium.find_element(*self._http_proxy_locator).click()
        return RedhatUpdates.HTTPProxy(self.testsetup)

    class HTTPProxy(Base):
        _address_locator = ()
        _user_id_locator = ()
        _password_locator = ()

        def fill_data(self,
                      address="",
                      user_id="",
                      password=""):
            #address
            self.selenium.find_element(*self._address_locator).send_keys(address)
            #user id
            self.selenium.find_element(*self._user_id_locator).send_keys(user_id)
            #password
            self.selenium.find_element(*self._password_locator).send_keys(password)


    class EditRegistration(Base):
        _register_with_locator = (By.CSS_SELECTOR, \
            "")

        def register_with_rhsm(self):
            self.select_dropdown("Red Hat Subscription Management", \
                *self._register_with_locator)
            self._wait_for_results_refresh()
            return RedhatUpdates.RegisterRHSM(self.testsetup)

        def register_with_satelite5(self):
            self.select_dropdown("Red Hat Satellite 5", \
                *self._register_with_locator)
            self._wait_for_results_refresh()
            return RedhatUpdates.RegisterSatellite5(self.testsetup)

        def register_with_satellite6(self):
            self.select_dropdown("Red Hat Satellite 6", \
                *self._register_with_locator)
            self._wait_for_results_refresh()
            return RedhatUpdates.RegisterSatellite6(self.testsetup)


    class RegisterRHSM(Base):
        _address_locator = (By.CSS_SELECTOR, \
            "")
        _default_button_locator = (By.CSS_SELECTOR, \
            "")
        _login_locator = ()
        _password_locator = ()
        _validate_credentials_button_locator = ()
        _reset_button_locator = ()
        _cancel_button_locator = ()
        _save_button_locator = ()

        def fill_data(self,
                      address="",
                      login="",
                      password="",
                      default=False):
            if default:
                #default button
                self.selenium.find_element(*self._default_button_locator).click()
            else:
                #address
                self.selenium.find_element(*self._address_locator).send_keys(address)
            #login
            self.selenium.find_element(*self._login_locator).send_keys(login)
            #password
            self.selenium.find_element(*self._password_locator).send_keys(password)

        def click_on_validate_credentials(self):
            self.selenium.find_element(*self._validate_credentials_button_locator).click()

        def click_on_reset(self):
            pass

        def click_on_cancel(self):
            pass

        def click_on_save(self):
            self.selenium.find_element(*self._save_button_locator).click()
            self._wait_for_results_refresh()
            return RedhatUpdates.Registered(self.testsetup)


    class RegisterSatellite5(Base):
        pass

    class RegisterSatellite6(Base):
        pass

    class Registered(Base):
        _refresh_list_button_locator = ()
        _check_for_updates_button_locator = ()
        _register_button_locator = ()
        _apply_cfme_update_button_locator = ()
        _edit_registration_button_locator = ()
