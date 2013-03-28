cfme_pages
==============

CloudForms Management Engine Page Objects library

Background
--------------

The testing framework being used is py.test.  
http://pytest.org/latest

We are also using a plugin from the mozwebqa people to integrate py.test with Selenium.  
https://github.com/davehunt/pytest-mozwebqa

Style guide  
https://wiki.mozilla.org/QA/Execution/Web_Testing/Docs/Automation/StyleGuide

Contributing
--------------

Submit a pull request from a fork to contribute.

As for design... If its a component that can be shared between different pages (trees, accordions, etc.), then it should be turned into a region. This is a standalone bit of code that models just a small portion of a page. From there, these regions can be composited into a page object. The page objects themselves should expose properties that represent items on the page, and also any "services" that the page has. So, rather than write a test with 'Fill in username, fill in password, click submit', you would create a 'login' method on the page that takes the username and password as an argument. This will shield the tests from changing implementation of that login method. If you want pass something different, create a new method, like 'login_with_enter_key', so as to allow other variations of the service.

If an action results in a new page, and there is only one outcome, the action should return the page that results.

Generally, the api for the page will result from the tests. If there is a specific test that you are working on, it is recommended that you write the test first, thinking about how to keep the test from breaking should something in the UI change. The style guide above has lots of great examples and guidance.

Adding a new page
---------------

When adding a new page, there are a couple of places that need to be updated. One, the header_menu.py will need to have a couple of entries added. The click() method on the HeaderMenu class will need to be adjusted, as well as the click() method on HeaderMenuItem. The page class itself will need a submenus property added to it, so as to facilitate which submenus are available from that top-level tab. Each of the tabs will have a page object, and sub-menus should have an inner class under that. There are already examples in the source tree. Ask if you have a question. :)


