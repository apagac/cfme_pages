from pages.base import Base
from pages.regions.checkboxtree import CheckboxTree
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from pages.regions.taggable import Taggable

class AccessControl(Base):
    _page_title = 'CloudForms Management Engine: Configuration'
    _roles_button = (By.CSS_SELECTOR, "div[title='View Roles']")
    _groups_button = (By.CSS_SELECTOR, "div[title='View Groups']")
    _users_button = (By.CSS_SELECTOR, "div[title='View Users']")

    # ROLES
    def click_on_roles(self):
        self.selenium.find_element(*self._roles_button).click()
        self._wait_for_results_refresh()
        return AccessControl.Roles(self.testsetup)

    class Roles(Base):
        _page_title = 'CloudForms Management Engine: Configuration'
        _add_role_button = (By.CSS_SELECTOR, "a[title='Add a new Role']")

        def click_on_add_new(self):
            self.selenium.find_element(*self._add_role_button).click()
            self._wait_for_results_refresh()
            return AccessControl.NewRole(self.testsetup)

        def click_on_role(self, role_name):
            selector = "td[title='%s']" % role_name
            self.selenium.find_element_by_css_selector(selector).click()
            self._wait_for_results_refresh()
            return AccessControl.ShowRole(self.testsetup)

    class NewRole(Base):
        _submit_role_button = (By.CSS_SELECTOR, "img[title='Add this Role']")
        _name_field = (By.CSS_SELECTOR, "input[name='name']")
        _access_restriction_field = (By.CSS_SELECTOR, "select[name='vm_restriction']")
        _product_features_tree = (By.CSS_SELECTOR, "#features_treebox")

        @property
        def product_features(self):
            return CheckboxTree(self.testsetup, self.selenium.find_element(*self._product_features_tree))

        def fill_name(self, name):
            field = self.selenium.find_element(*self._name_field)
            field.clear()
            return field.send_keys(name)

        def save(self):
            # when editing an existing role, wait until "save" button shows up
            # after ajax validation
            self._wait_for_visible_element(*self._submit_role_button)
            self.selenium.find_element(*self._submit_role_button).click()
            self._wait_for_results_refresh()
            return AccessControl.ShowRole(self.testsetup)

        def select_access_restriction(self, value):
            Select(self.selenium.find_element(*self._access_restriction_field)).select_by_value(value)

    class EditRole(NewRole):
        _name_field = (By.CSS_SELECTOR, "input[name='name']")
        _submit_role_button = (By.CSS_SELECTOR, "img[title='Save Changes']")

        def fill_name(self, name):
            field = self.selenium.find_element(*self._name_field)
            field.clear()
            field.send_keys(name)

    class ShowRole(Base):
        _edit_role_button = (By.CSS_SELECTOR, "a[title='Edit this Role']")
        _delete_role_button = (By.CSS_SELECTOR, "a[title='Delete this Role']")
        _copy_role_button = (By.CSS_SELECTOR, "a[title='Copy this Role to a new Role']")
        _role_name_label = (By.CSS_SELECTOR, ".style1 tr:nth-child(1) td:nth-child(2)")

        def click_on_edit(self):
            self.selenium.find_element(*self._edit_role_button).click()
            self._wait_for_results_refresh()
            return AccessControl.EditRole(self.testsetup)

        def click_on_delete(self):
            self.selenium.find_element(*self._delete_role_button).click()
            self.handle_popup()
            self._wait_for_results_refresh()
            return AccessControl.Roles(self.testsetup)
        
        def click_on_copy(self):
            self.selenium.find_element(*self._copy_role_button).click()
            self._wait_for_results_refresh()
            return AccessControl.NewRole(self.testsetup)

        @property
        def role_name(self):
            return self.selenium.find_element(*self._role_name_label).text.strip()

    # GROUPS
    def click_on_groups(self):
        self.selenium.find_element(*self._groups_button).click()
        self._wait_for_results_refresh()
        return AccessControl.Groups(self.testsetup)

    class Groups(Base):
        _page_title = 'CloudForms Management Engine: Configuration'
        _add_group_button = (By.CSS_SELECTOR, "a[title='Add a new Group']")

        def click_on_add_new(self):
            self.selenium.find_element(*self._add_group_button).click()
            self._wait_for_results_refresh()
            return AccessControl.NewGroup(self.testsetup)

        def click_on_group(self, group_name):
            selector = "td[title='%s']" % group_name
            self.selenium.find_element_by_css_selector(selector).click()
            self._wait_for_results_refresh()
            return AccessControl.ShowGroup(self.testsetup)

    class NewGroup(Base):
        _submit_group_button = (By.CSS_SELECTOR, "img[title='Add this Group']")
        _group_description_field = (By.ID, "description")
        _role_selector= (By.ID, "group_role")
        _company_tags_tree = (By.CSS_SELECTOR, "#myco_treebox")
        _hosts_clusters_tree = (By.CSS_SELECTOR, "#hac_treebox")
        _vms_templates_tree = (By.CSS_SELECTOR, "#vat_treebox")

        @property
        def company_tags(self):
            return CheckboxTree(self.testsetup, self.selenium.find_element(*self._company_tags_tree))

        @property
        def hosts_clusters(self):
            return CheckboxTree(self.testsetup, self.selenium.find_element(*self._hosts_clusters_tree))

        @property
        def vms_templates(self):
            return CheckboxTree(self.testsetup, self.selenium.find_element(*self._vms_templates_tree))

        def fill_info(self, description, role):
            self.selenium.find_element(*self._group_description_field).send_keys(description)
            return self.select_dropdown(role, *self._role_selector)

        def save(self):
            # when editing an existing group, wait until "save" button shows up
            # after ajax validation
            self._wait_for_visible_element(*self._submit_group_button)
            self.selenium.find_element(*self._submit_group_button).click()
            self._wait_for_results_refresh()
            return AccessControl.ShowGroup(self.testsetup)

    class EditGroup(NewGroup):
        _group_description_field = (By.ID, "description")
        _role_selector= (By.ID, "group_role")
        _submit_group_button = (By.CSS_SELECTOR, "img[title='Save Changes']")

        def fill_info(self, description, role):
            field = self.selenium.find_element(*self._group_description_field)
            field.clear()
            field.send_keys(description)
            return self.select_dropdown(role, *self._role_selector)

    class ShowGroup(Base):
        _edit_group_button = (By.CSS_SELECTOR, "a[title='Edit this Group']")
        _delete_group_button = (By.CSS_SELECTOR, "a[title='Delete this Group']")
        _group_name_label = (By.CSS_SELECTOR, ".style1 tr:nth-child(1) td:nth-child(2)")
        _edit_tags_button = (By.CSS_SELECTOR, "li#tag > a")

        def click_on_edit(self):
            self.selenium.find_element(*self._edit_group_button).click()
            self._wait_for_results_refresh()
            return AccessControl.EditGroup(self.testsetup)

        def click_on_delete(self):
            self.selenium.find_element(*self._delete_group_button).click()
            self.handle_popup()
            self._wait_for_results_refresh()
            return AccessControl.Groups(self.testsetup)
        
        def click_on_edit_tags(self):
            self.selenium.find_element(*self._edit_tags_button).click()
            self._wait_for_results_refresh
            return AccessControl.TagGroup(self.testsetup)

        @property
        def group_name(self):
            return self.selenium.find_element(*self._group_name_label).text.strip()

    class TagGroup(ShowGroup, Taggable):
        def save(self):
            return self.save_tag_edits

        def cancel(self):
            return self.cancel_tag_edits

        def reset(self):
            return self.reset_tag_edits

    # USERS
    def click_on_users(self):
        self.selenium.find_element(*self._users_button).click()
        self._wait_for_results_refresh()
        return AccessControl.Users(self.testsetup)

    class Users(Base):
        _page_title = 'CloudForms Management Engine: Configuration'
        _add_user_button = (By.CSS_SELECTOR, "a[title='Add a new User']")

        def click_on_add_new(self):
            self.selenium.find_element(*self._add_user_button).click()
            self._wait_for_results_refresh()
            return AccessControl.NewEditUser(self.testsetup)

        def click_on_user(self, user_name):
            selector = "td[title='%s']" % user_name
            self.selenium.find_element_by_css_selector(selector).click()
            self._wait_for_results_refresh()
            return AccessControl.ShowUser(self.testsetup)

    class NewEditUser(Base):
        _submit_user_button = (By.CSS_SELECTOR, "img[title='Add this User']")
        _save_user_button = (By.CSS_SELECTOR, "img[title='Save Changes']")
        _user_name_field = (By.ID, "name")
        _user_id_field= (By.ID, "userid")
        _user_password_field = (By.ID, "password")
        _user_confirm_password_field = (By.ID, "password2")
        _user_email_field = (By.ID, "email")
        _user_group_selector = (By.ID, "chosen_group")

        def fill_info(self, name, userid, pswd, pswd2, email, group):
            if(name):
                field = self.selenium.find_element(*self._user_name_field)
                field.clear()
                field.send_keys(name)
            if(userid):
                field = self.selenium.find_element(*self._user_id_field)
                field.clear()
                field.send_keys(userid)
            if(pswd):
                field = self.selenium.find_element(*self._user_password_field)
                field.clear()
                field.send_keys(pswd)
            if(pswd2):
                field = self.selenium.find_element(*self._user_confirm_password_field)
                field.clear()
                field.send_keys(pswd2)
            if(email):
                field = self.selenium.find_element(*self._user_email_field)
                field.clear()
                field.send_keys(email)
            if(group):
                self.select_dropdown(group, *self._user_group_selector)

        def click_on_add(self):
            # when editing an existing group, wait until "save" button shows up
            # after ajax validation
            self._wait_for_visible_element(*self._submit_user_button)
            self.selenium.find_element(*self._submit_user_button).click()
            self._wait_for_results_refresh()
            return AccessControl.ShowUser(self.testsetup)
        
        def click_on_save(self):
            self._wait_for_visible_element(*self._save_user_button)
            self.selenium.find_element(*self._save_user_button).click()
            self._wait_for_results_refresh()
            return AccessControl.ShowUser(self.testsetup)

    class ShowUser(Base):
        _edit_user_button = (By.CSS_SELECTOR, "a[title='Edit this User']")
        _delete_user_button = (By.CSS_SELECTOR, "a[title='Delete this User']")
        _copy_user_button = (By.CSS_SELECTOR, "a[title='Copy this User to a new User']")
        _edit_user_tags_button = (By.CSS_SELECTOR, "a[title='Edit My Company Tags for this User']")
        _user_name_label = (By.CSS_SELECTOR, ".style1 tr:nth-child(1) td:nth-child(2)")

        def click_on_edit(self):
            self.selenium.find_element(*self._edit_user_button).click()
            self._wait_for_results_refresh()
            return AccessControl.NewEditUser(self.testsetup)

        def click_on_delete(self):
            self.selenium.find_element(*self._delete_user_button).click()
            self.handle_popup()
            self._wait_for_results_refresh()
            return AccessControl.Users(self.testsetup)
        
        def click_on_copy(self):
            self.selenium.find_element(*self._copy_user_button).click()
            self._wait_for_results_refresh()
            return AccessControl.NewEditUser(self.testsetup)

        def click_on_edit_tags(self):
            self.selenium.find_element(*self._edit_user_tags_button).click()
            self._wait_for_results_refresh
            return AccessControl.TagUser(self.testsetup)

        @property
        def user_name(self):
            return self.selenium.find_element(*self._user_name_label).text.strip()

    class TagUser(ShowUser, Taggable):
        def save(self):
            return self.save_tag_edits

        def cancel(self):
            return self.cancel_tag_edits

        def reset(self):
            return self.reset_tag_edits
 
