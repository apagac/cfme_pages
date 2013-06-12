#!/usr/bin/env python

# -*- coding: utf-8 -*-

import pytest
import time
from unittestzero import Assert

@pytest.mark.usefixtures("maximized")
@pytest.mark.nondestructive #IGNORE:E1101
class TestCluster:
    def test_cluster(self, mozwebqa, home_page_logged_in):
        home_pg = home_page_logged_in
        clusters_pg = home_pg.header.site_navigation_menu("Infrastructure").sub_navigation_menu("Clusters").click()
        Assert.true(clusters_pg.is_the_current_page)
        detail_pg = clusters_pg.click_cluster("iscsi in iscsi")
        print detail_pg.name, detail_pg.management_system, detail_pg.datacenter, detail_pg.host_count

