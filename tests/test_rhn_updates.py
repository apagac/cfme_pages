# -*- coding: utf-8 -*-

import pytest
from unittestzero import Assert

@pytest.mark.nondestructive
@pytest.mark.usefixtures("maximized")
@pytest.mark.parametrize("services", [
  "rhsm",
  "sat5",
  "sat6"])
class TestUpdates:
    def update_methods(self, services, cfme_data):
        return cfme_data.data['redhat_updates'][services]

    #We can use the cfme_data and credentials files, but don't have to
    #probably delete them from unit test, move to cfme_tests
    #TODO this is almost unit test
    def test_rhn_updates(self, cnf_configuration_pg, services, cfme_data):
        Assert.true(cnf_configuration_pg.is_the_current_page)
        updates_data = self.update_methods(services, cfme_data)
        creds_data = cnf_configuration_pg.testsetup.credentials[updates_data["credentials"]]
        updates_pg = cnf_configuration_pg.click_on_redhat_updates()
        cancelled_pg = updates_pg.edit_registration_and_cancel(updates_data["url"], creds_data)
        flash_message = "Edit of Customer Information was cancelled"
        Assert.equal(cancelled_pg.flash.message, flash_message, cancelled_pg.flash.message)

@pytest.mark.nondestructive
@pytest.mark.usefixtures("maximized")
class TestDestructiveUpdates:
    #TODO destructive, move to cfme_tests
    def test_register_rhn(self, cnf_configuration_pg, cfme_data):
        Assert.true(cnf_configuration_pg.is_the_current_page)
        updates_data = cfme_data.data['redhat_updates']["rhsm"]
        creds_data = cnf_configuration_pg.testsetup.credentials[updates_data["credentials"]]
        updates_pg = cnf_configuration_pg.click_on_redhat_updates()
        registered_pg = updates_pg.edit_registration_and_save(updates_data["url"], creds_data)
        flash_message = "Customer Information successfully saved"
        Assert.equal(registered_pg.flash.message, flash_message, registered_pg.flash.message)

    #TODO to run after destructive, move to cfme_tests
    def test_compare_versions(self, cnf_configuration_pg, cfme_data):
        Assert.true(cnf_configuration_pg.is_the_current_page)
        updates_pg = cnf_configuration_pg.click_on_redhat_updates()
        error_message = "Appliance versions are not the same"
        Assert.true(updates_pg.compare_versions, error_message)

    #TODO destructive, move to cfme_tests
    def test_apply_updates(self):
        pass
