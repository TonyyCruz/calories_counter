import pytest
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .author_functional_base import AuthorBaseFunctionalTest


@pytest.mark.functional_test
class AuthorsRegisterFunctionalTest(AuthorBaseFunctionalTest):
    def fill_form_dummy_data(
        self,
        form,
        first_name="Ana",
        last_name="Carolina",
        username="AnaCarolina",
        email="ana@email.com",
        password="Superp@ss01",
        confirm_password="Superp@ss01",
    ):
        form.find_element(By.NAME, "first_name").send_keys(first_name)
        form.find_element(By.NAME, "last_name").send_keys(last_name)
        form.find_element(By.NAME, "username").send_keys(username)
        form.find_element(By.NAME, "email").send_keys(email)
        form.find_element(By.NAME, "password").send_keys(password)
        form.find_element(By.NAME, "confirm_password").send_keys(
            confirm_password
        )

    # >>>>> TESTS <<<<

    def test_empty_first_name_field_error_message(self):
        self.browser.get(self.live_server_url + reverse("authors:register"))
        form = self.get_form(xpath="/html/body/main/div[2]")

        self.fill_form_dummy_data(form=form, first_name=" " * 10)

        first_name_placeholder = self.get_by_placeholder(form, "Ex.: Ana")
        first_name_placeholder.send_keys(Keys.ENTER)

        form = self.get_form(xpath="/html/body/main/div[2]")

        self.assertIn("First name must not be empty", form.text)
        self.assertNotIn("Last name must not be empty", form.text)
        self.assertNotIn("Username must not be empty", form.text)
        self.assertNotIn("Password must not be empty", form.text)
        self.assertNotIn("Confirm password must not be empty", form.text)

    def test_empty_last_name_field_error_message(self):
        self.browser.get(self.live_server_url + reverse("authors:register"))
        form = self.get_form(xpath="/html/body/main/div[2]")

        self.fill_form_dummy_data(form=form, last_name=" " * 10)

        first_name_placeholder = self.get_by_placeholder(form, "Ex.: Carolina")
        first_name_placeholder.send_keys(Keys.ENTER)

        form = self.get_form(xpath="/html/body/main/div[2]")

        self.assertNotIn("First name must not be empty", form.text)
        self.assertIn("Last name must not be empty", form.text)
        self.assertNotIn("Username must not be empty", form.text)
        self.assertNotIn("Password must not be empty", form.text)
        self.assertNotIn("Confirm password must not be empty", form.text)

    def test_empty_username_field_error_message(self):
        self.browser.get(self.live_server_url + reverse("authors:register"))
        form = self.get_form(xpath="/html/body/main/div[2]")

        self.fill_form_dummy_data(form=form, username=" " * 10)

        first_name_placeholder = self.get_by_placeholder(form, "Ex.: @carol")
        first_name_placeholder.send_keys(Keys.ENTER)

        form = self.get_form(xpath="/html/body/main/div[2]")

        self.assertNotIn("First name must not be empty", form.text)
        self.assertNotIn("Last name must not be empty", form.text)
        self.assertIn("Username must not be empty", form.text)
        self.assertNotIn("Password must not be empty", form.text)
        self.assertNotIn("Confirm password must not be empty", form.text)

    def test_empty_password_field_error_message(self):
        self.browser.get(self.live_server_url + reverse("authors:register"))
        form = self.get_form(xpath="/html/body/main/div[2]")

        self.fill_form_dummy_data(form=form, password=" " * 10)

        first_name_placeholder = self.get_by_placeholder(
            form, "[a-z] [A-Z] [0-9] [@*!#$%?]"
        )
        first_name_placeholder.send_keys(Keys.ENTER)

        form = self.get_form(xpath="/html/body/main/div[2]")

        self.assertNotIn("First name must not be empty", form.text)
        self.assertNotIn("Last name must not be empty", form.text)
        self.assertNotIn("Username must not be empty", form.text)
        self.assertIn("Password must not be empty", form.text)
        self.assertNotIn("Confirm password must not be empty", form.text)

    def test_if_it_is_possible_to_create_a_user_with_the_correct_data(self):
        self.browser.get(self.live_server_url + reverse("authors:register"))
        form = self.get_form(xpath="/html/body/main/div[2]")
        self.fill_form_dummy_data(form=form)

        self.get_form(class_name="main-form").submit()

        login_screen = self.browser.find_element(By.TAG_NAME, "body")

        self.assertIn("User created successfully", login_screen.text)
