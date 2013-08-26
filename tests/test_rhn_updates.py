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
    #@pytest.fixture(params=['rhsm', 'sat5', 'sat6'])
    def update_methods(self, services, cfme_data):
        return cfme_data.data['redhat_updates'][services]

    def test_rhn_updates(self, cnf_configuration_pg, services, cfme_data):
        Assert.true(cnf_configuration_pg.is_the_current_page)
        #updates_data = cfme_data.data["redhat_updates"]["rhsm"]
        updates_data = self.update_methods(services, cfme_data)
        updates_pg = cnf_configuration_pg.click_on_redhat_updates()
        cancelled_pg = updates_pg.edit_registration_and_cancel(**updates_data)
        flash_message = "Edit of Customer Information was cancelled"
        Assert.equal(cancelled_pg.flash.message, flash_message, cancelled_pg.flash.message)
