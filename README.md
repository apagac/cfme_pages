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

Prerequisites:

1. Fedora system. Tested on F17 and F18.
2. Cloned repository cfme_pages.
   * Make yourself a new folder, then cd to it
   * git clone https://github.com/RedHatQE/cfme_pages.git
   * Alternatively, you can clone it from your own forked repo.

Setup:

1. Copy template files credentials.yaml, mozwebqa.cfg and pytest.ini from cfme_pages to your newly created directory.
   * cd YourFolder
   * cp cfme_pages/credentials.yaml.template .
   * cp cfme_pages/mozwebqa.cfg.template .
   * cp cfme_pages/pytest.ini.template .
2. Rename all the files.
   * mv credentials.yaml.template credentials.yaml
   * mv mozwebqa.cfg.template mozwebqa.cfg
   * mv pytest.ini.template pytest.ini
3. Edit both files to reflect your environment.
   * In credentials.yaml:
   * username: Your username, used to log in into cfme.
   * password: Your password, used to log in into cfme.
   * In mozwebqa.cfg:
   * baseurl: Url, where to find running version of cfme.
4. Create a virtualenv to run pytest from
   * easy_install virtualenv (yum install python-virtualenv also works for those preferring rpm)
   * virtualenv <name>
   * source <name>/bin/activate 
5. Install all required additional software.
   * List of required items is here: cfme_pages/requirements.txt
   * pip install -Ur cfme_pages/requirements.txt
   * pip install -Ur cfme_tests/requirements.txt (check for error output)
       + you may need to 'yum install libxslt-devel libxml2-devel' before hand 
6. Install chromedriver (or you could just use firefox instead - replace "--driver=chrome" with "--driver=firefox" in pytest.ini).
   * Download latest available for your arch from here: http://code.google.com/p/chromedriver/downloads/list
   * Unzip the file to somewhere on your path (for example to '/usr/bin/chromedriver')
7. Run the tests.
   * PYTHONPATH=cfme_pages/ py.test
8. TIP: to run specific test, add to this command '-k <StringInTestName>'

Reminders:

1. Please, do NOT check files with your edited cretentials into source control.

