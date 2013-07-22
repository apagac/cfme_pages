'''
@author: Unknown
'''
# -*- coding: utf-8 -*-

import pytest
from unittestzero import Assert

@pytest.mark.nondestructive #IGNORE:E1101
@pytest.mark.usefixtures("maximized", "db_setup_for_test_infrastructure_clusters")
def test_cluster(home_page_logged_in):
    home_pg = home_page_logged_in
    clusters_pg = home_pg.header.site_navigation_menu(
            "Infrastructure").sub_navigation_menu("Clusters").click()
    Assert.true(clusters_pg.is_the_current_page)
    detail_pg = clusters_pg.click_cluster("scripted_cluster")
    print detail_pg.name, detail_pg.provider, \
            detail_pg.datacenter, detail_pg.host_count

