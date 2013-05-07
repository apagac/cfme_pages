#!/usr/bin/env python

# -*- coding: utf-8 -*-

import pytest
import time
from unittestzero import Assert

NAME = "RHEV-M (10.16.120.71)"

@pytest.mark.nondestructive  # IGNORE:E1101
class TestISODatastores:
    def test_iso_datastores(self, mozwebqa, home_page_logged_in):
        home_pg = home_page_logged_in
        pxe_pg = home_pg.header.site_navigation_menu("Infrastructure").sub_navigation_menu("PXE").click()
        Assert.true(pxe_pg.is_the_current_page)

        pxe_pg.accordion_region.accordion_by_name("ISO Datastores").click()
        pxe_pg.accordion_region.current_content.click()

        time.sleep(1)

        pxe_pg.center_buttons.configuration_button.click()
        add_pg = pxe_pg.click_on_add_iso_datastore()
        add_pg.select_management_system(NAME)

        time.sleep(2)

        result_pg = add_pg.click_on_add()
        flash_message = 'ISO Datastore "%s" was added' % NAME
        Assert.true(result_pg.flash.message == flash_message, "Flash message: %s" % result_pg.flash.message)
        datastore_name = result_pg.datastore_name()
        Assert.true(NAME == datastore_name, "Actual name of datastore is: %s" % datastore_name)

