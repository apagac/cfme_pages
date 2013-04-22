# -*- coding: utf-8 -*-

from pages.base import Base
from selenium.webdriver.common.by import By
from pages.regions.paginator import PaginatorMixin
from selenium.webdriver.common.action_chains import ActionChains
import re

class Infrastructure(Base):
    @property
    def submenus(self):
        return {"management_system": lambda: Infrastructure.ManagementSystems,
                "pxe": lambda: Infrastructure.PXE
                }
        
    class ManagementSystems(Base, PaginatorMixin):
        _page_title = 'CloudForms Management Engine: Management Systems'
        _configuration_button_locator = (By.CSS_SELECTOR, "div.dhx_toolbar_btn[title='Configuration']")
        _discover_management_systems_locator = (By.CSS_SELECTOR, "table.buttons_cont tr[title='Discover Management Systems']")
        _edit_management_systems_locator = (By.CSS_SELECTOR, "table.buttons_cont tr[title='Select a single Management System to edit']")

        _add_new_management_system_locator = (By.CSS_SELECTOR, "tr.tr_btn[title='Add a New Management System']")
        _management_system_name_locator = (By.CSS_SELECTOR, "input#name")
        _management_system_host_name_locator = (By.CSS_SELECTOR, "input#hostname")
        _management_system_ip_address_locator = (By.CSS_SELECTOR, "input#ipaddress")
        _management_system_type_locator = (By.CSS_SELECTOR, "select#server_emstype")
        _management_system_user_id_locator = (By.CSS_SELECTOR, "input#default_userid")
        _management_system_password_locator = (By.CSS_SELECTOR, "input#default_password")
        _management_system_verify_password_locator = (By.CSS_SELECTOR, "input#default_verify")
        _management_system_add_new_locator = (By.CSS_SELECTOR, "img.button[title='Add this Add this Management System']")

        @property
        def quadicon_region(self):
            from pages.regions.quadicons import Quadicons
            return Quadicons(self.testsetup)
        
        @property
        def taskbar(self):
            from pages.regions.taskbar.taskbar import Taskbar
            return Taskbar(self.testsetup)

        @property
        def center_buttons(self):
            from pages.regions.taskbar.center import CenterButtons
            return CenterButtons(self.testsetup)
        
        @property
        def configuration_button(self):
            return self.selenium.find_element(*self._configuration_button_locator)

        def select_management_system(self, management_system_name):
            self.quadicon_region.get_quadicon_by_title(management_system_name).mark_checkbox()

        def click_on_discover_management_systems(self):
            from selenium.webdriver.common.action_chains import ActionChains
            config_button = self.selenium.find_element(*self._configuration_button_locator)
            discover_button = self.selenium.find_element(*self._discover_management_systems_locator)
            ActionChains(self.selenium).click(self.configuration_button).click(discover_button).perform()
            return Infrastructure.ManagementSystemsDiscovery(self.testsetup)

        def click_on_edit_management_systems(self):
            edit_button = self.selenium.find_element(*self._edit_management_systems_locator)
            ActionChains(self.selenium).click(self.configuration_button).click(edit_button).perform()
            return Infrastructure.ManagementSystemsEdit(self.testsetup)

        def management_system_click_on_add(self):
            self.selenium.find_element(*self._management_system_add_new_locator).click()
            self._wait_for_results_refresh()
            return Infrastructure.ManagementSystems(self.testsetup)

        def select_management_system_type(self, management_system_type):
            self.select_dropdown(management_system_type, *self._management_system_type_locator)
            self._wait_for_results_refresh()
            return Infrastructure.ManagementSystems(self.testsetup)

        def new_management_system_fill_data(self, name, hostname, ip_address, user_id, password):
            #name
            self.selenium.find_element(*self._management_system_name_locator).send_keys(name or "test_name")
            #host name
            self.selenium.find_element(*self._management_system_host_name_locator).send_keys(hostname or "test_hostname")
            #ip address
            self.selenium.find_element(*self._management_system_ip_address_locator).send_keys(ip_address or "127.0.0.1")
            #user id
            self.selenium.find_element(*self._management_system_user_id_locator).send_keys(user_id or "test_user")
            #password
            self.selenium.find_element(*self._management_system_password_locator).send_keys(password or "test_password")
            #verify password
            self.selenium.find_element(*self._management_system_verify_password_locator).send_keys(password or "test_password")
    
    class ManagementSystemsDiscovery(Base):
        _page_title = 'CloudForms Management Engine: Management Systems'
        _start_button_locator = (By.CSS_SELECTOR, "input[name='start']")
        _cancel_button_locator = (By.CSS_SELECTOR, "input[name='cancel']")
        _management_system_type_locator = {
            "virtualcenter" : (By.CSS_SELECTOR, "input[name='discover_type_virtualcenter']"),
            "rhevm"         : (By.CSS_SELECTOR, "input[name='discover_type_rhevm']")
        }

        _from_first_locator = (By.CSS_SELECTOR, "input[name='from_first']")
        _from_second_locator = (By.CSS_SELECTOR, "input[name='from_second']")
        _from_third_locator = (By.CSS_SELECTOR, "input[name='from_third']")
        _from_fourth_locator = (By.CSS_SELECTOR, "input[name='from_fourth']")
        
        _to_fourth_locator = (By.CSS_SELECTOR, "input[name='to_fourth']")

        def is_selected(self, checkbox_locator):
            return self.selenium.find_element(*checkbox_locator).is_selected()
        
        def toggle_checkbox(self, checkbox_locator):
            self.selenium.find_element(*checkbox_locator).click()
        
        def mark_checkbox(self, checkbox_locator):
            if not self.is_selected(checkbox_locator):
                self.toggle_checkbox(checkbox_locator)
        
        def unmark_checkbox(self, checkbox_locator):
            if self.is_selected(checkbox_locator):
                self.toggle_checkbox(checkbox_locator)

        def click_on_start(self):
            self.selenium.find_element(*self._start_button_locator).click()
            return Infrastructure.ManagementSystems(self.testsetup)
        
        def click_on_cancel(self):
            self.selenium.find_element(*self._cancel_button_locator).click()
            return Infrastructure.ManagementSystems(self.testsetup)
        
        def discover_systems(self, management_system_type, from_address, to_address):
            self.mark_checkbox(self._management_system_type_locator[management_system_type])
            from_ip = from_address.split('.')
            to_ip = to_address.split('.')
            self.selenium.find_element(*self._from_first_locator).send_keys(from_ip[0])
            self.selenium.find_element(*self._from_second_locator).send_keys(from_ip[1])
            self.selenium.find_element(*self._from_third_locator).send_keys(from_ip[2])
            self.selenium.find_element(*self._from_fourth_locator).send_keys(from_ip[3])
            self.selenium.find_element(*self._to_fourth_locator).send_keys(to_ip[3])
            return self.click_on_start()

    class ManagementSystemsEdit(Base):
        _page_title = 'CloudForms Management Engine: Management Systems'
        _save_button_locator = (By.CSS_SELECTOR, "ul#form_buttons > li > img[title='Save Changes']")
        _cancel_button_locator = (By.CSS_SELECTOR, "ul#form_buttons > li > img[title='Cancel']")
        _name_edit_field_locator = (By.ID, "name")
        _hostname_edit_field_locator = (By.ID, "hostname")
        _ipaddress_edit_field_locator = (By.ID, "ipaddress")
        _server_zone_edit_field_locator = (By.ID, "server_zone")
        _host_default_vnc_port_start_edit_field_locator = (By.ID, "host_default_vnc_port_start")
        _host_default_vnc_port_end_edit_field_locator = (By.ID, "host_default_vnc_port_end")
        _default_userid_edit_field_locator = (By.ID, "default_userid")
        _default_password_edit_field_locator = (By.ID, "default_password")
        _default_verify_edit_field_locator = (By.ID, "default_verify")

        @property
        def name(self):
            return self.get_element(*self._name_edit_field_locator)

        @property
        def hostname(self):
            return self.get_element(*self._hostname_edit_field_locator)

        @property
        def ipaddress(self):
            return self.get_element(*self._ipaddress_edit_field_locator)

        @property
        def server_zone(self):
            return self.get_element(*self._server_zone_edit_field_locator)

        @property
        def host_default_vnc_port_start(self):
            return self.get_element(*self._host_default_vnc_port_start_edit_field_locator)

        @property
        def host_default_vnc_port_end(self):
            return self.get_element(*self._host_default_vnc_port_end_edit_field_locator)

        @property
        def default_userid(self):
            return self.get_element(*self._default_userid_edit_field_locator)

        @property
        def default_password(self):
            return self.get_element(*self._default_password_edit_field_locator)

        @property
        def default_verify(self):
            return self.get_element(*self._default_verify_edit_field_locator)

        def edit_management_system(self, management_system):
            for key,value in management_system.iteritems():
                # Special cases
                if "host_vnc_port" in key:
                    self.host_default_vnc_port_start.clear()
                    self.host_default_vnc_port_start.send_keys(value[0])
                    self.host_default_vnc_port_end.clear()
                    self.host_default_vnc_port_end.send_keys(value[1])
                elif "server_zone" in key:
                    from selenium.webdriver.support.select import Select
                    if self.server_zone.tag_name == "select":
                        select = Select(self.server_zone)
                        select.select_by_visible_text(value)
                elif "user" in key:
                    # use credentials
                    credentials = self.testsetup.credentials[value]
                    self.default_userid.clear()
                    self.default_userid.send_keys(credentials['username'])
                    self.default_password.clear()
                    self.default_password.send_keys(credentials['password'])
                    self.default_verify.clear()
                    self.default_verify.send_keys(credentials['password'])
                else:
                    # Only try to send keys if there is actually a property
                    if hasattr(self, key):
                        attr = getattr(self, key)
                        attr.clear()
                        attr.send_keys(value)
            return self.click_on_save()

        def click_on_save(self):
            self.get_element(*self._save_button_locator).click()
            self._wait_for_results_refresh()
            return Infrastructure.ManagementSystemsDetail(self.testsetup)

        def click_on_cancel(self):
            self.selenium.find_element(*self._cancel_button_locator).click()
            self._wait_for_results_refresh()
            return Infrastructure.ManagementSystems(self.testsetup)

    class ManagementSystemsDetail(Base):
        _page_title = 'CloudForms Management Engine: Management Systems'
        _management_system_detail_name_locator = (By.XPATH, '//*[@id="accordion"]/div[1]/div[1]/a')
        _management_system_detail_hostname_locator = (By.XPATH, '//*[@id="textual_div"]/dl/dd[1]/div[1]/table/tbody/tr[1]/td[2]')
        _management_system_detail_ip_address_locator = (By.XPATH, '//*[@id="textual_div"]/dl/dd[1]/div[1]/table/tbody/tr[2]/td[2]')
        _management_system_detail_zone_locator = (By.XPATH, '//*[@id="table_div"]/table/tbody/tr[1]/td[2]')
        _management_system_detail_credentials_validity_locator = (By.XPATH, '//*[@id="textual_div"]/dl/dd[1]/div[2]/table/tbody/tr/td[2]')
        _management_system_detail_vnc_port_range_locator = (By.XPATH, '//*[@id="textual_div"]/dl/dd[1]/div[1]/table/tbody/tr[9]/td[2]')

        @property
        def name(self):
            element_text = self.selenium.find_element(*self._management_system_detail_name_locator).text
            return re.search('.*(?=[ ]\(Summary\))', element_text).group(0)

        @property
        def hostname(self):
            return self.selenium.find_element(*self._management_system_detail_hostname_locator).text

        @property
        def zone(self):
            return self.selenium.find_element(*self._management_system_detail_zone_locator).text

        @property
        def credentials_validity(self):
            return self.selenium.find_element(*self._management_system_detail_credentials_validity_locator).text

        @property
        def vnc_port_range(self):
            element_text = self.selenium.find_element(*self._management_system_detail_vnc_port_range_locator).text
            return element_text.split('-')

        
    class PXE(Base):
        _page_title = 'CloudForms Management Engine: PXE'

        _copy_template_locator = (By.CSS_SELECTOR, "tr.tr_btn[title='Copy this Customization Template']")
        _template_name_locator = (By.CSS_SELECTOR, "input#name")
        _image_type_locator = (By.CSS_SELECTOR, "select#img_typ")
        _add_button_locator = (By.CSS_SELECTOR, "div#buttons_on > ul > li > img[title='Add']")
        _refresh_locator = (By.CSS_SELECTOR, "tr.tr_btn[title='Refresh this PXE Server']")
        _pxe_image_names_locator = (By.CSS_SELECTOR, "div#pxe_info_div > fieldset > table[class='style3'] > tbody")

        _add_pxe_locator = (By.CSS_SELECTOR, "tr.tr_btn[title='Add a New PXE Server']")
        #TODO duplicate
        _pxe_name_locator = (By.CSS_SELECTOR, "input#name")
        _pxe_uri_locator = (By.CSS_SELECTOR, "input#uri")
        _pxe_depot_type_locator = (By.CSS_SELECTOR, "select#log_protocol")
        _pxe_access_url_locator = (By.CSS_SELECTOR, "input#access_url")
        _pxe_directory_locator = (By.CSS_SELECTOR, "input#pxe_directory")
        _pxe_windows_images_directory_locator = (By.CSS_SELECTOR, "input#windows_images_directory")
        _pxe_customization_directory_locator = (By.CSS_SELECTOR, "input#customization_directory")
        _pxe_image_menus_filename_locator = (By.CSS_SELECTOR, "input#pxemenu_0")


        @property
        def accordion_region(self):
            from pages.regions.accordion import Accordion
            from pages.regions.treeaccordionitem import TreeAccordionItem
            return Accordion(self.testsetup, TreeAccordionItem)

        @property
        def center_buttons(self):
            from pages.regions.taskbar.center import CenterButtons
            return CenterButtons(self.testsetup)

        #TODO: unused in test
        @property
        def history_buttons(self):
            from pages.regions.taskbar.history import HistoryButtons
            return HistoryButtons(self.testsetup)

        #TODO these clicks can be merged
        def click_on_copy_template(self):
            self.selenium.find_element(*self._copy_template_locator).click()
            self._wait_for_results_refresh()
            return Infrastructure.PXE(self.testsetup)

        #TODO these clicks can be merged
        def click_on_add_pxe_server(self):
            self.selenium.find_element(*self._add_pxe_locator).click()
            self._wait_for_results_refresh()
            return Infrastructure.PXE(self.testsetup)

        #TODO these clicks can be merged
        def click_on_refresh(self):
            self.selenium.find_element(*self._refresh_locator).click()
            return Infrastructure.PXE(self.testsetup)

        def rename_template(self, name):
            template_name = self.selenium.find_element(*self._template_name_locator)
            template_name.clear()
            template_name.send_keys(name)

        def select_image_type(self, image_type):
            self.select_dropdown(image_type, *self._image_type_locator)
            self._wait_for_results_refresh()

        def click_on_add(self):
            self.selenium.find_element(*self._add_button_locator).click()
            self._wait_for_results_refresh()
            return Infrastructure.PXE(self.testsetup)

        def select_depot_type(self, depot_type):
            self.select_dropdown(depot_type, *self._pxe_depot_type_locator)
            self._wait_for_results_refresh()
            return Infrastructure.PXE(self.testsetup)

        def new_pxe_server_fill_data(self, name, uri, access_url, pxe_dir, windows_img_dir, customization_dir, pxe_img_menus_filename):
            #name
            self.selenium.find_element(*self._pxe_name_locator).send_keys(name or "rhel_pxe_server")
            #uri
            self.selenium.find_element(*self._pxe_uri_locator).send_keys(uri or "10.16.120.11/var/www/html/pub/miq/ipxe/")
            #access url
            self.selenium.find_element(*self._pxe_access_url_locator).send_keys(access_url or "http://mgmt1.rhq.lab.eng.bos.redhat.com/ipxe")
            #pxe directory
            self.selenium.find_element(*self._pxe_directory_locator).send_keys(pxe_dir or "pxe")
            #windows images directory
            self.selenium.find_element(*self._pxe_windows_images_directory_locator).send_keys(windows_img_dir or "sources/microsoft")
            #customization directory
            self.selenium.find_element(*self._pxe_customization_directory_locator).send_keys(customization_dir or "customization")
            #pxe image menus filename
            self.selenium.find_element(*self._pxe_image_menus_filename_locator).send_keys(pxe_img_menus_filename or "menu.php")

        def pxe_image_names(self):
            element_text = self.selenium.find_element(*self._pxe_image_names_locator).text
            lines = element_text.split('\n')
            names = []
            for line in lines:
                name, space, test = line.partition(' ')
                names.append(name)
            return names

