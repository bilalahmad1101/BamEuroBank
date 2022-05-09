from selenium.webdriver.common.keys import Keys
import unittest
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


class selenium_test(unittest.TestCase): 

    def test_login_with_valid_creds(self):
        chrome_options = Options()
        chrome_options.add_argument("start-maximized")
        #chrome_options.add_experimental_option("detach", True)
        driver = Chrome("driver/chromedriver",chrome_options=chrome_options)
        driver.get("http://localhost:5000")
        username_field = driver.find_element_by_id('login_username')
        password_field = driver.find_element_by_id('login_password')
        valid_username = "test_user01"
        valid_password = "cake123"
        username_field.send_keys(valid_username)
        password_field.send_keys(valid_password)
        password_field.send_keys(Keys.ENTER)
        driver.implicitly_wait(10)
        expected_url = "http://localhost:5000/account?username=" + valid_username
        self.assertEquals(expected_url, driver.current_url)


    ##only use this test with a non existing user - have not implemented delete user 
    def test_sign_up_new_user(self):
        chrome_options = Options()
        chrome_options.add_argument("start-maximized")
        #chrome_options.add_experimental_option("detach", True)
        driver = Chrome("driver/chromedriver",chrome_options=chrome_options)
        driver.get("http://localhost:5000/sign-up")
        username_field = driver.find_element_by_name('sign_up_username')
        password_field = driver.find_element_by_name('sign_up_password')
        confirm_password_field = driver.find_element_by_name('sign_up_confirm_password')
        username = "" #Use a different user name here
        password = "cake123"
        username_field.send_keys(username)
        password_field.send_keys(password)
        confirm_password_field.send_keys(password)
        password_field.send_keys(Keys.ENTER)
        driver.implicitly_wait(10)
        expected_url = "http://localhost:5000/"
        self.assertEquals(expected_url, driver.current_url)
    
    def test_validate_correct_balance_is_shown(self):
        chrome_options = Options()
        chrome_options.add_argument("start-maximized")
        #chrome_options.add_experimental_option("detach", True)
        driver = Chrome("driver/chromedriver",chrome_options=chrome_options)
        driver.get("http://localhost:5000")
        username_field = driver.find_element_by_id('login_username')
        password_field = driver.find_element_by_id('login_password')
        valid_username = "test_user01"
        valid_password = "cake123"
        username_field.send_keys(valid_username)
        password_field.send_keys(valid_password)
        password_field.send_keys(Keys.ENTER)
        driver.implicitly_wait(10)
        expected_value ="100"
        balance_display = driver.find_element_by_id('balance-p').text
        self.assertEqual(expected_value, balance_display[9:len(balance_display)])
    
    def test_validate_transactions_are_shown(self):
        chrome_options = Options()
        chrome_options.add_argument("start-maximized")
        #chrome_options.add_experimental_option("detach", True)
        driver = Chrome("driver/chromedriver",chrome_options=chrome_options)
        driver.get("http://localhost:5000")
        username_field = driver.find_element_by_id('login_username')
        password_field = driver.find_element_by_id('login_password')
        valid_username = "test_user03"
        valid_password = "cake123"
        username_field.send_keys(valid_username)
        password_field.send_keys(valid_password)
        password_field.send_keys(Keys.ENTER)
        driver.implicitly_wait(10)
        expected_value = 3
        rows = driver.find_elements_by_xpath("//table/tbody/tr")
        self.assertEqual(expected_value, len(rows))

    def test_validate_transfer_made_successfully(self):
        chrome_options = Options()
        chrome_options.add_argument("start-maximized")
        #chrome_options.add_experimental_option("detach", True)
        driver = Chrome("driver/chromedriver",chrome_options=chrome_options)
        driver.get("http://localhost:5000")
        username_field = driver.find_element_by_id('login_username')
        password_field = driver.find_element_by_id('login_password')
        valid_username = "test_user01"
        valid_password = "cake123"
        username_field.send_keys(valid_username)
        password_field.send_keys(valid_password)
        password_field.send_keys(Keys.ENTER)
        driver.implicitly_wait(10)
        recipient_field = driver.find_element_by_name('send_to_text')
        amount_field = driver.find_element_by_name('amount_text')
        send_to_username ="test_user04"
        amount_to_send = "20"
        recipient_field.send_keys(send_to_username)
        amount_field.send_keys(amount_to_send)
        amount_field.send_keys(Keys.ENTER)
        balance_display = driver.find_element_by_id('balance-p').text
        expected_value = "80"
        self.assertEqual(expected_value, balance_display[9:len(balance_display)])
        #resetting bamberuo transfer
        driver.get("http://localhost:5000")
        username_field = driver.find_element_by_id('login_username')
        password_field = driver.find_element_by_id('login_password')
        valid_username = "test_user04"
        valid_password = "cake123"
        username_field.send_keys(valid_username)
        password_field.send_keys(valid_password)
        password_field.send_keys(Keys.ENTER)
        driver.implicitly_wait(10)
        recipient_field = driver.find_element_by_name('send_to_text')
        amount_field = driver.find_element_by_name('amount_text')
        send_to_username ="test_user01"
        amount_to_send = "20"
        recipient_field.send_keys(send_to_username)
        amount_field.send_keys(amount_to_send)
        amount_field.send_keys(Keys.ENTER)
