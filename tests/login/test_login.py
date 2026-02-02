import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config.urls import LOGIN_URL, SIGNUP_URL, WELCOME_URL
from playwright.sync_api import expect
import re

# Helper to map element names from the test cases to their CSS selectors from the LOCATORS JSON.
# This ensures that locators specified in the JSON are prioritized.
# If a specific locator is not present in the LOCATORS JSON, Playwright's get_by_ methods are used as a fallback.
# This mapping is static and not loaded at runtime.
LOCATOR_MAP = {
    "snappod_logo_img": "[alt='SnapPod Logo']",
    "welcome_back__h2": "h2:has-text('Welcome Back!')",
    "email___label": "label:has-text('Email *')",
    "password___label": "label:has-text('Password *')",
    "forgot_password_a": "a:has-text('Forgot Password')",
    "login_button": "button:has-text('Login')",
    "or_div": "div:has-text('or')",
    "google_signin_button": "[aria-label='Sign in with Google']", # Mapping for 'Sign in with Google' button
    "don_t_have_an_account__div": "div:has-text('Don\\'t have an account?')",
    "sign_up_here_a": "a:has-text('Sign Up Here')",
    "enter_your_email_address_input": "#login-email",
    "enter_your_password_input": "#login-password",
    "show_password_toggle_span": "[aria-label='Show password']", # Mapping for the show password toggle
    "logging_in_button": "button:has-text('Logging In')" # For checking button state after submission
}

# Explicitly defining locators for clarity and direct usage in tests
EMAIL_INPUT_LOCATOR = LOCATOR_MAP["enter_your_email_address_input"]
PASSWORD_INPUT_LOCATOR = LOCATOR_MAP["enter_your_password_input"]
LOGIN_BUTTON_LOCATOR = LOCATOR_MAP["login_button"]
FORGOT_PASSWORD_LINK_LOCATOR = LOCATOR_MAP["forgot_password_a"]
SIGN_UP_HERE_LINK_LOCATOR = LOCATOR_MAP["sign_up_here_a"]
GOOGLE_SIGN_IN_BUTTON_LOCATOR = LOCATOR_MAP["google_signin_button"]
SHOW_PASSWORD_TOGGLE_LOCATOR = LOCATOR_MAP["show_password_toggle_span"]


def test_login_page_elements_visibility(page):
    """
    TC-LOGIN-001: Verify visibility of all key UI elements on the Login page.
    """
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')

    expect(page.locator(LOCATOR_MAP["snappod_logo_img"])).to_be_visible(timeout=10000)
    expect(page.locator(LOCATOR_MAP["welcome_back__h2"])).to_be_visible(timeout=10000)
    expect(page.locator(LOCATOR_MAP["email___label"])).to_be_visible(timeout=10000)
    expect(page.locator(LOCATOR_MAP["password___label"])).to_be_visible(timeout=10000)
    expect(page.locator(FORGOT_PASSWORD_LINK_LOCATOR)).to_be_visible(timeout=10000)
    expect(page.locator(LOGIN_BUTTON_LOCATOR)).to_be_visible(timeout=10000)
    expect(page.locator(LOCATOR_MAP["or_div"])).to_be_visible(timeout=10000)
    expect(page.locator(GOOGLE_SIGN_IN_BUTTON_LOCATOR)).to_be_visible(timeout=10000)
    expect(page.locator(LOCATOR_MAP["don_t_have_an_account__div"])).to_be_visible(timeout=10000)
    expect(page.locator(SIGN_UP_HERE_LINK_LOCATOR)).to_be_visible(timeout=10000)


def test_successful_login(page):
    """
    TC-LOGIN-002: Verify user can successfully log in with valid credentials.
    Per static site rules: check for submission attempt, not navigation.
    """
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')

    # Using specific input values from the test case
    page.locator(EMAIL_INPUT_LOCATOR).fill("tadikamallasivaparvathi@gmail.com")
    page.locator(PASSWORD_INPUT_LOCATOR).fill("Siva@2001")
    page.locator(LOGIN_BUTTON_LOCATOR).click()

    # For static website, check for button state change (e.g., 'Logging In') as a proxy for submission.
    expect(page.locator(LOCATOR_MAP["logging_in_button"])).to_be_visible(timeout=10000)
    # Per static site rule: "Don't expect URL changes after form submission"
    expect(page).to_have_url(LOGIN_URL)


def test_invalid_credentials_login(page):
    """
    TC-LOGIN-003: Verify login fails with invalid credentials and shows error.
    """
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')

    # Using specific input values from the test case
    page.locator(EMAIL_INPUT_LOCATOR).fill("invaliduser@example.com")
    page.locator(PASSWORD_INPUT_LOCATOR).fill("WrongPassword123")
    page.locator(LOGIN_BUTTON_LOCATOR).click()

    # Using page.get_by_text for dynamic error message as no specific CSS selector is provided for it in LOCATORS JSON
    expect(page.get_by_text("Email does not exists,Please sign up first")).to_be_visible(timeout=10000)
    expect(page).to_have_url(LOGIN_URL)


def test_empty_email_login(page):
    """
    TC-LOGIN-004: Verify login fails when email field is empty.
    """
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')

    # Using specific input values from the test case
    page.locator(EMAIL_INPUT_LOCATOR).fill("")
    page.locator(PASSWORD_INPUT_LOCATOR).fill("AnyPassword123")
    page.locator(LOGIN_BUTTON_LOCATOR).click()

    # Using to_have_js_property for browser-level validation message
    expect(page.locator(EMAIL_INPUT_LOCATOR)).to_have_js_property('validationMessage', 'Please fill out this field.')
    expect(page).to_have_url(LOGIN_URL)


def test_empty_password_login(page):
    """
    TC-LOGIN-005: Verify login fails when password field is empty.
    """
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')

    # Using specific input values from the test case
    page.locator(EMAIL_INPUT_LOCATOR).fill("test@example.com")
    page.locator(PASSWORD_INPUT_LOCATOR).fill("")
    page.locator(LOGIN_BUTTON_LOCATOR).click()

    # Using to_have_js_property for browser-level validation message
    expect(page.locator(PASSWORD_INPUT_LOCATOR)).to_have_js_property('validationMessage', 'Please fill out this field.')
    expect(page).to_have_url(LOGIN_URL)


def test_invalid_email_format_login(page):
    """
    TC-LOGIN-006: Verify login fails with invalid email format.
    """
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')

    # Using specific input values from the test case
    page.locator(EMAIL_INPUT_LOCATOR).fill("invalid-email")
    page.locator(PASSWORD_INPUT_LOCATOR).fill("ValidPassword123")
    page.locator(LOGIN_BUTTON_LOCATOR).click()

    # Using to_have_js_property with regex for browser-level validation message
    expect(page.locator(EMAIL_INPUT_LOCATOR)).to_have_js_property('validationMessage', re.compile(r'@'))
    expect(page).to_have_url(LOGIN_URL)


def test_show_password_toggle(page):
    """
    TC-LOGIN-007: Verify 'Show password' toggle changes password input type.
    """
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')

    # Using specific input values from the test case
    page.locator(PASSWORD_INPUT_LOCATOR).fill("TestPassword123")
    expect(page.locator(PASSWORD_INPUT_LOCATOR)).to_have_attribute('type', 'password')

    page.locator(SHOW_PASSWORD_TOGGLE_LOCATOR).click()
    expect(page.locator(PASSWORD_INPUT_LOCATOR)).to_have_attribute('type', 'text')

    page.locator(SHOW_PASSWORD_TOGGLE_LOCATOR).click()
    expect(page.locator(PASSWORD_INPUT_LOCATOR)).to_have_attribute('type', 'password')


def test_navigate_to_sign_up_page(page):
    """
    TC-LOGIN-008: Verify 'Sign Up Here' link navigates to the Sign Up page.
    """
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')

    page.locator(SIGN_UP_HERE_LINK_LOCATOR).click()
    # Using SIGNUP_URL from config.urls
    expect(page).to_have_url(SIGNUP_URL)


def test_forgot_password_link_opens_modal(page):
    """
    TC-LOGIN-009: Verify 'Forgot Password' link opens the password reset modal.
    """
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')

    page.locator(FORGOT_PASSWORD_LINK_LOCATOR).click()

    # 'Reset Password' heading is not in LOCATORS JSON, using page.get_by_role as fallback
    expect(page.get_by_role("heading", name="Reset Password")).to_be_visible(timeout=10000)


def test_sign_in_with_google_button(page):
    """
    TC-LOGIN-010: Verify 'Sign in with Google' button initiates Google authentication flow.
    """
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')

    page.locator(GOOGLE_SIGN_IN_BUTTON_LOCATOR).click()

    # Using re.compile for Python regex pattern matching for URL
    expect(page).to_have_url(re.compile(r"accounts\.google\.com"), timeout=30000)


def test_forgot_password_modal_elements_visibility(page):
    """
    TC-FORGOTPASS-001: Verify visibility of all key UI elements in the Forgot Password modal.
    Note: Locators for modal elements are not provided in LOCATORS JSON,
    hence using Playwright's get_by_ methods as fallback.
    """
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')

    page.locator(FORGOT_PASSWORD_LINK_LOCATOR).click()

    # Fallback to get_by_ methods for modal elements not in LOCATORS JSON
    reset_password_heading = page.get_by_role("heading", name="Reset Password")
    close_button = page.get_by_label("Close") # Assuming a common 'Close' label for modal close button
    instruction_text = page.get_by_text("Enter your email address to receive a password reset link.") # Inferring text
    email_address_label = page.get_by_text("Email Address")
    email_input_modal = page.get_by_placeholder("Enter your email address") # Assuming placeholder for the email input
    send_reset_code_button = page.get_by_role("button", name="Send Reset Code")

    expect(close_button).to_be_visible(timeout=10000)
    expect(reset_password_heading).to_be_visible(timeout=10000)
    expect(instruction_text).to_be_visible(timeout=10000)
    expect(email_address_label).to_be_visible(timeout=10000)
    expect(email_input_modal).to_be_visible(timeout=10000)
    expect(send_reset_code_button).to_be_visible(timeout=10000)


def test_close_forgot_password_modal(page):
    """
    TC-FORGOTPASS-002: Verify 'Close' button closes the Forgot Password modal.
    """
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')

    page.locator(FORGOT_PASSWORD_LINK_LOCATOR).click()

    reset_password_heading = page.get_by_role("heading", name="Reset Password")
    close_button = page.get_by_label("Close")

    expect(reset_password_heading).to_be_visible(timeout=10000)
    close_button.click()
    expect(reset_password_heading).not_to_be_visible(timeout=10000)


def test_send_reset_code_valid_email(page):
    """
    TC-FORGOTPASS-003: Verify sending reset code with a valid email address.
    Per static site rules, check for success message/modal closing, not actual email sending.
    """
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')

    page.locator(FORGOT_PASSWORD_LINK_LOCATOR).click()

    email_input_modal = page.get_by_placeholder("Enter your email address")
    send_reset_code_button = page.get_by_role("button", name="Send Reset Code")
    reset_password_heading = page.get_by_role("heading", name="Reset Password")

    # Using specific input values from the test case
    email_input_modal.fill("tadikamallasivaparvathi@gmail.com")
    send_reset_code_button.click()

    # Verifying success message and modal closing as per test case
    expect(page.get_by_text("Password reset email sent. Please check your inbox.")).to_be_visible(timeout=10000)
    expect(reset_password_heading).not_to_be_visible(timeout=10000)


def test_send_reset_code_invalid_email_format(page):
    """
    TC-FORGOTPASS-004: Verify error message for invalid email format when sending reset code.
    """
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')

    page.locator(FORGOT_PASSWORD_LINK_LOCATOR).click()

    email_input_modal = page.get_by_placeholder("Enter your email address")
    send_reset_code_button = page.get_by_role("button", name="Send Reset Code")
    reset_password_heading = page.get_by_role("heading", name="Reset Password")

    # Using specific input values from the test case
    email_input_modal.fill("bad-email")
    send_reset_code_button.click()

    # Using to_have_js_property with regex for browser-level validation message
    expect(email_input_modal).to_have_js_property('validationMessage', re.compile(r'@'))
    expect(reset_password_heading).to_be_visible(timeout=10000)


def test_send_reset_code_empty_email(page):
    """
    TC-FORGOTPASS-005: Verify error message for empty email when sending reset code.
    """
    page.goto(LOGIN_URL, timeout=60000)
    page.wait_for_load_state('networkidle')

    page.locator(FORGOT_PASSWORD_LINK_LOCATOR).click()

    email_input_modal = page.get_by_placeholder("Enter your email address")
    send_reset_code_button = page.get_by_role("button", name="Send Reset Code")
    reset_password_heading = page.get_by_role("heading", name="Reset Password")

    # Using specific input values from the test case
    email_input_modal.fill("")
    send_reset_code_button.click()

    # Using to_have_js_property for browser-level validation message
    expect(email_input_modal).to_have_js_property('validationMessage', "Please fill out this field.")
    expect(reset_password_heading).to_be_visible(timeout=10000)