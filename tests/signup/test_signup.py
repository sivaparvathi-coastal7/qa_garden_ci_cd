import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import re
from config.urls import LOGIN_URL, SIGNUP_URL, WELCOME_URL
from playwright.sync_api import expect

# Extracted CSS selectors from the provided LOCATORS JSON
# This map directly uses the `css_selector` values from the JSON where applicable.
# For input fields where `LOCATORS JSON` only provides a label but the test case uses a placeholder,
# a CSS selector based on `input[placeholder='...']` is constructed. This is a pragmatic
# approach to ensure executability, as the strict `css_selector` for these inputs was not provided in the JSON.
LOCATOR_CSS_MAP = {
    # Visibility and general elements (from LOCATORS JSON)
    "logo_img": "[alt='Logo']",
    "start_creating__h1": "h1:has-text('Start creating!')",
    "already_have_an_account__p": "p:has-text('Already have an account?')",
    "sign_in_here_a": "a:has-text('Sign In Here')",
    "sign_up_with_google_button": "[aria-label='Sign up with Google']",
    "sign_up_with_facebook_button": "[aria-label='Sign up with Facebook']",
    "first_name___label": "label:has-text('First Name *')",
    "last_name___label": "label:has-text('Last Name *')",
    "phone_number_label": "label:has-text('Phone Number')",
    "email___label": "label:has-text('Email *')",
    "password___label": "label:has-text('Password *')",
    "re_enter_password___label": "label:has-text('Re-Enter Password *')",
    "sign_up_button": "button:has-text('Sign Up')",
    
    # Input fields with explicit placeholder CSS selectors in LOCATORS JSON
    "enter_your_first_name_input": "[placeholder='Enter your first name']",
    "1__702__123_4567_input": "[placeholder='1 (702) 123-4567']",

    # Placeholder-based inputs that are not explicitly found as `input[placeholder='...']`
    # in the provided LOCATORS JSON, so we generate them based on the placeholder text
    "lastNameInput_placeholder": "input[placeholder='Enter your last name']",
    "emailInput_placeholder": "input[placeholder='Enter your Email Address']",
    "passwordInput_placeholder": "input[placeholder='Enter password']",
    "reEnterPasswordInput_placeholder": "input[placeholder='Re-Enter your Password']",
}

# Helper to resolve Playwright's getBy... locators from test case JSON to our CSS_LOCATOR_MAP
def resolve_test_case_locator(locator_string):
    if "getByAltText('Logo')" == locator_string:
        return LOCATOR_CSS_MAP["logo_img"]
    elif "getByRole('heading', { name: 'Start creating!' })" == locator_string:
        return LOCATOR_CSS_MAP["start_creating__h1"]
    elif "getByText('Already have an account?')" == locator_string:
        return LOCATOR_CSS_MAP["already_have_an_account__p"]
    elif "getByRole('link', { name: 'Sign In Here' })" == locator_string:
        return LOCATOR_CSS_MAP["sign_in_here_a"]
    elif "getByRole('button', { name: 'Sign up with Google' })" == locator_string:
        return LOCATOR_CSS_MAP["sign_up_with_google_button"]
    elif "getByRole('button', { name: 'Sign up with Facebook' })" == locator_string:
        return LOCATOR_CSS_MAP["sign_up_with_facebook_button"]
    elif "getByLabelText('First Name *')" == locator_string:
        return LOCATOR_CSS_MAP["first_name___label"]
    elif "getByLabelText('Last Name *')" == locator_string:
        return LOCATOR_CSS_MAP["last_name___label"]
    elif "getByLabelText('Phone Number')" == locator_string:
        return LOCATOR_CSS_MAP["phone_number_label"]
    elif "getByLabelText('Email *')" == locator_string:
        return LOCATOR_CSS_MAP["email___label"]
    elif "getByLabelText('Password *')" == locator_string:
        return LOCATOR_CSS_MAP["password___label"]
    elif "getByLabelText('Re-Enter Password *')" == locator_string:
        return LOCATOR_CSS_MAP["re_enter_password___label"]
    elif "getByRole('button', { name: 'Sign Up' })" == locator_string:
        return LOCATOR_CSS_MAP["sign_up_button"]
    elif "getByPlaceholderText('Enter your first name')" == locator_string:
        return LOCATOR_CSS_MAP["enter_your_first_name_input"]
    elif "getByPlaceholderText('Enter your last name')" == locator_string:
        return LOCATOR_CSS_MAP["lastNameInput_placeholder"]
    elif "getByPlaceholderText('1 (702) 123-4567')" == locator_string:
        return LOCATOR_CSS_MAP["1__702__123_4567_input"]
    elif "getByPlaceholderText('Enter your Email Address')" == locator_string:
        return LOCATOR_CSS_MAP["emailInput_placeholder"]
    elif "getByPlaceholderText('Enter password')" == locator_string:
        return LOCATOR_CSS_MAP["passwordInput_placeholder"]
    elif "getByPlaceholderText('Re-Enter your Password')" == locator_string:
        return LOCATOR_CSS_MAP["reEnterPasswordInput_placeholder"]
    # For dynamic messages or generic text, we might use page.get_by_text directly in the test function
    # if it's not a static UI element expected in LOCATOR_CSS_MAP.
    # The current test cases mostly use `page.getByText` for expected error messages directly.
    else:
        # If this point is reached, it means a locator string from the test case inputs
        # was not mapped to a CSS selector as per the rules/pragmatic decisions.
        # This will be treated as an unresolvable locator for `page.locator()`.
        # However, for `page.getByText` and `page.waitForURL`, the string is used directly.
        return None # Indicate it's not a `page.locator()` compatible string from map


def test_SignUpPageElementsVisibility(page):
    """
    TC-SIGNUP-001: Verify visibility of all key UI elements on the Sign Up page
    """
    inputs = {
        "url": "https://dev.vox.snappod.ai/signup"
    }
    page.goto(SIGNUP_URL, timeout=60000)
    page.wait_for_load_state('networkidle')

    expect(page.locator(resolve_test_case_locator("getByAltText('Logo')"))).to_be_visible(timeout=10000)
    expect(page.locator(resolve_test_case_locator("getByRole('heading', { name: 'Start creating!' })"))).to_be_visible(timeout=10000)
    expect(page.locator(resolve_test_case_locator("getByText('Already have an account?')"))).to_be_visible(timeout=10000)
    expect(page.locator(resolve_test_case_locator("getByRole('link', { name: 'Sign In Here' })"))).to_be_visible(timeout=10000)
    expect(page.locator(resolve_test_case_locator("getByRole('button', { name: 'Sign up with Google' })"))).to_be_visible(timeout=10000)
    expect(page.locator(resolve_test_case_locator("getByRole('button', { name: 'Sign up with Facebook' })"))).to_be_visible(timeout=10000)
    expect(page.locator(resolve_test_case_locator("getByLabelText('First Name *')"))).to_be_visible(timeout=10000)
    expect(page.locator(resolve_test_case_locator("getByLabelText('Last Name *')"))).to_be_visible(timeout=10000)
    expect(page.locator(resolve_test_case_locator("getByLabelText('Phone Number')"))).to_be_visible(timeout=10000)
    expect(page.locator(resolve_test_case_locator("getByLabelText('Email *')"))).to_be_visible(timeout=10000)
    expect(page.locator(resolve_test_case_locator("getByLabelText('Password *')"))).to_be_visible(timeout=10000)
    expect(page.locator(resolve_test_case_locator("getByLabelText('Re-Enter Password *')"))).to_be_visible(timeout=10000)
    expect(page.locator(resolve_test_case_locator("getByRole('button', { name: 'Sign Up' })"))).to_be_visible(timeout=10000)


def test_SuccessfulSignUp(page):
    """
    TC-SIGNUP-002: Verify user can successfully sign up with valid required data
    """
    inputs = {
        "url": "https://dev.vox.snappod.ai/signup",
        "firstName": "John",
        "lastName": "Doe",
        "phoneNumber": "1234567890",
        "email": "sivaparvathiCS4-G3@coastalseven.com",
        "password": "Coastal@123",
        "firstNameInputLocator": "getByPlaceholderText('Enter your first name')",
        "lastNameInputLocator": "getByPlaceholderText('Enter your last name')",
        "phoneNumberInputLocator": "getByPlaceholderText('1 (702) 123-4567')",
        "emailInputLocator": "getByPlaceholderText('Enter your Email Address')",
        "passwordInputLocator": "getByPlaceholderText('Enter password')",
        "reEnterPasswordInputLocator": "getByPlaceholderText('Re-Enter your Password')",
        "signUpButtonLocator": "getByRole('button', { name: 'Sign Up' })"
    }
    page.goto(SIGNUP_URL, timeout=60000)
    page.wait_for_load_state('networkidle')

    page.locator(resolve_test_case_locator(inputs["firstNameInputLocator"])).fill(inputs["firstName"])
    page.locator(resolve_test_case_locator(inputs["lastNameInputLocator"])).fill(inputs["lastName"])
    page.locator(resolve_test_case_locator(inputs["phoneNumberInputLocator"])).fill(inputs["phoneNumber"])
    page.locator(resolve_test_case_locator(inputs["emailInputLocator"])).fill(inputs["email"])
    page.locator(resolve_test_case_locator(inputs["passwordInputLocator"])).fill(inputs["password"])
    page.locator(resolve_test_case_locator(inputs["reEnterPasswordInputLocator"])).fill(inputs["password"])
    page.locator(resolve_test_case_locator(inputs["signUpButtonLocator"])).click()

    # Note: As per "STATIC WEBSITE HANDLING", actual navigation might not occur.
    # However, following the test case's explicit expectation here.
    expect(page).to_have_url(re.compile(r".*/dashboard/"))


def test_SignUpMissingFirstName(page):
    """
    TC-SIGNUP-003: Verify sign up fails when 'First Name' field is empty
    """
    inputs = {
        "url": "https://dev.vox.snappod.ai/signup",
        "firstName": "",
        "lastName": "Doe",
        "email": "test@example.com",
        "password": "SecurePassword123!",
        "firstNameInputLocator": "getByPlaceholderText('Enter your first name')",
        "lastNameInputLocator": "getByPlaceholderText('Enter your last name')",
        "emailInputLocator": "getByPlaceholderText('Enter your Email Address')",
        "passwordInputLocator": "getByPlaceholderText('Enter password')",
        "reEnterPasswordInputLocator": "getByPlaceholderText('Re-Enter your Password')",
        "signUpButtonLocator": "getByRole('button', { name: 'Sign Up' })"
    }
    page.goto(SIGNUP_URL, timeout=60000)
    page.wait_for_load_state('networkidle')

    page.locator(resolve_test_case_locator(inputs["firstNameInputLocator"])).fill(inputs["firstName"])
    page.locator(resolve_test_case_locator(inputs["lastNameInputLocator"])).fill(inputs["lastName"])
    page.locator(resolve_test_case_locator(inputs["emailInputLocator"])).fill(inputs["email"])
    page.locator(resolve_test_case_locator(inputs["passwordInputLocator"])).fill(inputs["password"])
    page.locator(resolve_test_case_locator(inputs["reEnterPasswordInputLocator"])).fill(inputs["password"])
    page.locator(resolve_test_case_locator(inputs["signUpButtonLocator"])).click()

    expect(page.locator(resolve_test_case_locator(inputs["firstNameInputLocator"]))).to_have_js_property('validationMessage', 'Please fill out this field.')


def test_SignUpMissingLastName(page):
    """
    TC-SIGNUP-004: Verify sign up fails when 'Last Name' field is empty
    """
    inputs = {
        "url": "https://dev.vox.snappod.ai/signup",
        "firstName": "John",
        "lastName": "",
        "email": "test@example.com",
        "password": "SecurePassword123!",
        "firstNameInputLocator": "getByPlaceholderText('Enter your first name')",
        "lastNameInputLocator": "getByPlaceholderText('Enter your last name')",
        "emailInputLocator": "getByPlaceholderText('Enter your Email Address')",
        "passwordInputLocator": "getByPlaceholderText('Enter password')",
        "reEnterPasswordInputLocator": "getByPlaceholderText('Re-Enter your Password')",
        "signUpButtonLocator": "getByRole('button', { name: 'Sign Up' })"
    }
    page.goto(SIGNUP_URL, timeout=60000)
    page.wait_for_load_state('networkidle')

    page.locator(resolve_test_case_locator(inputs["firstNameInputLocator"])).fill(inputs["firstName"])
    page.locator(resolve_test_case_locator(inputs["lastNameInputLocator"])).fill(inputs["lastName"])
    page.locator(resolve_test_case_locator(inputs["emailInputLocator"])).fill(inputs["email"])
    page.locator(resolve_test_case_locator(inputs["passwordInputLocator"])).fill(inputs["password"])
    page.locator(resolve_test_case_locator(inputs["reEnterPasswordInputLocator"])).fill(inputs["password"])
    page.locator(resolve_test_case_locator(inputs["signUpButtonLocator"])).click()

    expect(page.locator(resolve_test_case_locator(inputs["lastNameInputLocator"]))).to_have_js_property('validationMessage', 'Please fill out this field.')


def test_SignUpMissingEmail(page):
    """
    TC-SIGNUP-005: Verify sign up fails when 'Email' field is empty
    """
    inputs = {
        "url": "https://dev.vox.snappod.ai/signup",
        "firstName": "John",
        "lastName": "Doe",
        "email": "",
        "password": "SecurePassword123!",
        "firstNameInputLocator": "getByPlaceholderText('Enter your first name')",
        "lastNameInputLocator": "getByPlaceholderText('Enter your last name')",
        "emailInputLocator": "getByPlaceholderText('Enter your Email Address')",
        "passwordInputLocator": "getByPlaceholderText('Enter password')",
        "reEnterPasswordInputLocator": "getByPlaceholderText('Re-Enter your Password')",
        "signUpButtonLocator": "getByRole('button', { name: 'Sign Up' })"
    }
    page.goto(SIGNUP_URL, timeout=60000)
    page.wait_for_load_state('networkidle')

    page.locator(resolve_test_case_locator(inputs["firstNameInputLocator"])).fill(inputs["firstName"])
    page.locator(resolve_test_case_locator(inputs["lastNameInputLocator"])).fill(inputs["lastName"])
    page.locator(resolve_test_case_locator(inputs["emailInputLocator"])).fill(inputs["email"])
    page.locator(resolve_test_case_locator(inputs["passwordInputLocator"])).fill(inputs["password"])
    page.locator(resolve_test_case_locator(inputs["reEnterPasswordInputLocator"])).fill(inputs["password"])
    page.locator(resolve_test_case_locator(inputs["signUpButtonLocator"])).click()

    expect(page.locator(resolve_test_case_locator(inputs["emailInputLocator"]))).to_have_js_property('validationMessage', 'Please fill out this field.')


def test_SignUpMissingPassword(page):
    """
    TC-SIGNUP-006: Verify sign up fails when 'Password' field is empty
    """
    inputs = {
        "url": "https://dev.vox.snappod.ai/signup",
        "firstName": "John",
        "lastName": "Doe",
        "email": "test@example.com",
        "password": "",
        "reEnterPassword": "SecurePassword123!",
        "firstNameInputLocator": "getByPlaceholderText('Enter your first name')",
        "lastNameInputLocator": "getByPlaceholderText('Enter your last name')",
        "emailInputLocator": "getByPlaceholderText('Enter your Email Address')",
        "passwordInputLocator": "getByPlaceholderText('Enter password')",
        "reEnterPasswordInputLocator": "getByPlaceholderText('Re-Enter your Password')",
        "signUpButtonLocator": "getByRole('button', { name: 'Sign Up' })"
    }
    page.goto(SIGNUP_URL, timeout=60000)
    page.wait_for_load_state('networkidle')

    page.locator(resolve_test_case_locator(inputs["firstNameInputLocator"])).fill(inputs["firstName"])
    page.locator(resolve_test_case_locator(inputs["lastNameInputLocator"])).fill(inputs["lastName"])
    page.locator(resolve_test_case_locator(inputs["emailInputLocator"])).fill(inputs["email"])
    page.locator(resolve_test_case_locator(inputs["passwordInputLocator"])).fill(inputs["password"])
    page.locator(resolve_test_case_locator(inputs["reEnterPasswordInputLocator"])).fill(inputs["reEnterPassword"])
    page.locator(resolve_test_case_locator(inputs["signUpButtonLocator"])).click()

    expect(page.locator(resolve_test_case_locator(inputs["passwordInputLocator"]))).to_have_js_property('validationMessage', 'Please fill out this field.')


def test_SignUpMissingReEnterPassword(page):
    """
    TC-SIGNUP-007: Verify sign up fails when 'Re-Enter Password' field is empty
    """
    inputs = {
        "url": "https://dev.vox.snappod.ai/signup",
        "firstName": "John",
        "lastName": "Doe",
        "email": "test@example.com",
        "password": "SecurePassword123!",
        "reEnterPassword": "",
        "firstNameInputLocator": "getByPlaceholderText('Enter your first name')",
        "lastNameInputLocator": "getByPlaceholderText('Enter your last name')",
        "emailInputLocator": "getByPlaceholderText('Enter your Email Address')",
        "passwordInputLocator": "getByPlaceholderText('Enter password')",
        "reEnterPasswordInputLocator": "getByPlaceholderText('Re-Enter your Password')",
        "signUpButtonLocator": "getByRole('button', { name: 'Sign Up' })"
    }
    page.goto(SIGNUP_URL, timeout=60000)
    page.wait_for_load_state('networkidle')

    page.locator(resolve_test_case_locator(inputs["firstNameInputLocator"])).fill(inputs["firstName"])
    page.locator(resolve_test_case_locator(inputs["lastNameInputLocator"])).fill(inputs["lastName"])
    page.locator(resolve_test_case_locator(inputs["emailInputLocator"])).fill(inputs["email"])
    page.locator(resolve_test_case_locator(inputs["passwordInputLocator"])).fill(inputs["password"])
    page.locator(resolve_test_case_locator(inputs["reEnterPasswordInputLocator"])).fill(inputs["reEnterPassword"])
    page.locator(resolve_test_case_locator(inputs["signUpButtonLocator"])).click()

    expect(page.locator(resolve_test_case_locator(inputs["reEnterPasswordInputLocator"]))).to_have_js_property('validationMessage', 'Please fill out this field.')


def test_SignUpInvalidEmailFormat(page):
    """
    TC-SIGNUP-008: Verify sign up fails with invalid email format
    """
    inputs = {
        "url": "https://dev.vox.snappod.ai/signup",
        "firstName": "John",
        "lastName": "Doe",
        "email": "invalid-email",
        "password": "SecurePassword123!",
        "firstNameInputLocator": "getByPlaceholderText('Enter your first name')",
        "lastNameInputLocator": "getByPlaceholderText('Enter your last name')",
        "emailInputLocator": "getByPlaceholderText('Enter your Email Address')",
        "passwordInputLocator": "getByPlaceholderText('Enter password')",
        "reEnterPasswordInputLocator": "getByPlaceholderText('Re-Enter your Password')",
        "signUpButtonLocator": "getByRole('button', { name: 'Sign Up' })"
    }
    page.goto(SIGNUP_URL, timeout=60000)
    page.wait_for_load_state('networkidle')

    page.locator(resolve_test_case_locator(inputs["firstNameInputLocator"])).fill(inputs["firstName"])
    page.locator(resolve_test_case_locator(inputs["lastNameInputLocator"])).fill(inputs["lastName"])
    page.locator(resolve_test_case_locator(inputs["emailInputLocator"])).fill(inputs["email"])
    page.locator(resolve_test_case_locator(inputs["passwordInputLocator"])).fill(inputs["password"])
    page.locator(resolve_test_case_locator(inputs["reEnterPasswordInputLocator"])).fill(inputs["password"])
    page.locator(resolve_test_case_locator(inputs["signUpButtonLocator"])).click()

    expect(page.locator(resolve_test_case_locator(inputs["emailInputLocator"]))).to_have_js_property('validationMessage', re.compile(r'@'))


def test_SignUpMismatchedPasswords(page):
    """
    TC-SIGNUP-009: Verify sign up fails when passwords do not match
    """
    inputs = {
        "url": "https://dev.vox.snappod.ai/signup",
        "firstName": "John",
        "lastName": "Doe",
        "email": "test@example.com",
        "password": "SecurePassword123!",
        "reEnterPassword": "MismatchPassword123",
        "firstNameInputLocator": "getByPlaceholderText('Enter your first name')",
        "lastNameInputLocator": "getByPlaceholderText('Enter your last name')",
        "emailInputLocator": "getByPlaceholderText('Enter your Email Address')",
        "passwordInputLocator": "getByPlaceholderText('Enter password')",
        "reEnterPasswordInputLocator": "getByPlaceholderText('Re-Enter your Password')",
        "signUpButtonLocator": "getByRole('button', { name: 'Sign Up' })",
        "expectedErrorMessage": "Passwords do not match."
    }
    page.goto(SIGNUP_URL, timeout=60000)
    page.wait_for_load_state('networkidle')

    page.locator(resolve_test_case_locator(inputs["firstNameInputLocator"])).fill(inputs["firstName"])
    page.locator(resolve_test_case_locator(inputs["lastNameInputLocator"])).fill(inputs["lastName"])
    page.locator(resolve_test_case_locator(inputs["emailInputLocator"])).fill(inputs["email"])
    page.locator(resolve_test_case_locator(inputs["passwordInputLocator"])).fill(inputs["password"])
    page.locator(resolve_test_case_locator(inputs["reEnterPasswordInputLocator"])).fill(inputs["reEnterPassword"])
    page.locator(resolve_test_case_locator(inputs["signUpButtonLocator"])).click()

    expect(page.get_by_text(inputs["expectedErrorMessage"])).to_be_visible(timeout=10000)


def test_SignUpShortPassword(page):
    """
    TC-SIGNUP-010: Verify sign up fails with a password that is too short
    """
    inputs = {
        "url": "https://dev.vox.snappod.ai/signup",
        "firstName": "John",
        "lastName": "Doe",
        "email": "shortpass@example.com",
        "password": "short",
        "firstNameInputLocator": "getByPlaceholderText('Enter your first name')",
        "lastNameInputLocator": "getByPlaceholderText('Enter your last name')",
        "emailInputLocator": "getByPlaceholderText('Enter your Email Address')",
        "passwordInputLocator": "getByPlaceholderText('Enter password')",
        "reEnterPasswordInputLocator": "getByPlaceholderText('Re-Enter your Password')",
        "signUpButtonLocator": "getByRole('button', { name: 'Sign Up' })",
        "expectedErrorMessage": "Password must be at least 8 characters long."
    }
    page.goto(SIGNUP_URL, timeout=60000)
    page.wait_for_load_state('networkidle')

    page.locator(resolve_test_case_locator(inputs["firstNameInputLocator"])).fill(inputs["firstName"])
    page.locator(resolve_test_case_locator(inputs["lastNameInputLocator"])).fill(inputs["lastName"])
    page.locator(resolve_test_case_locator(inputs["emailInputLocator"])).fill(inputs["email"])
    page.locator(resolve_test_case_locator(inputs["passwordInputLocator"])).fill(inputs["password"])
    page.locator(resolve_test_case_locator(inputs["reEnterPasswordInputLocator"])).fill(inputs["password"])
    page.locator(resolve_test_case_locator(inputs["signUpButtonLocator"])).click()

    expect(page.get_by_text(inputs["expectedErrorMessage"])).to_be_visible(timeout=10000)


def test_SignUpInvalidPhoneNumberFormat(page):
    """
    TC-SIGNUP-011: Verify sign up handles invalid phone number format (if required/validated)
    """
    inputs = {
        "url": "https://dev.vox.snappod.ai/signup",
        "firstName": "John",
        "lastName": "Doe",
        "phoneNumber": "123",
        "email": "phone@example.com",
        "password": "SecurePassword123!",
        "firstNameInputLocator": "getByPlaceholderText('Enter your first name')",
        "lastNameInputLocator": "getByPlaceholderText('Enter your last name')",
        "phoneNumberInputLocator": "getByPlaceholderText('1 (702) 123-4567')",
        "emailInputLocator": "getByPlaceholderText('Enter your Email Address')",
        "passwordInputLocator": "getByPlaceholderText('Enter password')",
        "reEnterPasswordInputLocator": "getByPlaceholderText('Re-Enter your Password')",
        "signUpButtonLocator": "getByRole('button', { name: 'Sign Up' })",
        "expectedErrorMessage": "Please enter a valid phone number."
    }
    page.goto(SIGNUP_URL, timeout=60000)
    page.wait_for_load_state('networkidle')

    page.locator(resolve_test_case_locator(inputs["firstNameInputLocator"])).fill(inputs["firstName"])
    page.locator(resolve_test_case_locator(inputs["lastNameInputLocator"])).fill(inputs["lastName"])
    page.locator(resolve_test_case_locator(inputs["phoneNumberInputLocator"])).fill(inputs["phoneNumber"])
    page.locator(resolve_test_case_locator(inputs["emailInputLocator"])).fill(inputs["email"])
    page.locator(resolve_test_case_locator(inputs["passwordInputLocator"])).fill(inputs["password"])
    page.locator(resolve_test_case_locator(inputs["reEnterPasswordInputLocator"])).fill(inputs["password"])
    page.locator(resolve_test_case_locator(inputs["signUpButtonLocator"])).click()

    expect(page.get_by_text(inputs["expectedErrorMessage"])).to_be_visible(timeout=10000)


def test_NavigateToLoginPageFromSignUp(page):
    """
    TC-SIGNUP-012: Verify 'Sign In Here' link navigates to the Login page
    """
    inputs = {
        "url": "https://dev.vox.snappod.ai/signup",
        "signInLinkLocator": "getByRole('link', { name: 'Sign In Here' })",
        "expectedLoginUrl": "https://dev.vox.snappod.ai/login"
    }
    page.goto(SIGNUP_URL, timeout=60000)
    page.wait_for_load_state('networkidle')

    page.locator(resolve_test_case_locator(inputs["signInLinkLocator"])).click()

    expect(page).to_have_url(inputs["expectedLoginUrl"])


def test_SignUpWithGoogleButton(page):
    """
    TC-SIGNUP-013: Verify 'Sign up with Google' button initiates Google authentication flow
    """
    inputs = {
        "url": "https://dev.vox.snappod.ai/signup",
        "googleSignUpButtonLocator": "getByRole('button', { name: 'Sign up with Google' })"
    }
    page.goto(SIGNUP_URL, timeout=60000)
    page.wait_for_load_state('networkidle')

    page.locator(resolve_test_case_locator(inputs["googleSignUpButtonLocator"])).click()

    expect(page).to_have_url(re.compile(r"accounts\.google\.com"))


def test_SignUpWithFacebookButton(page):
    """
    TC-SIGNUP-014: Verify 'Sign up with Facebook' button initiates Facebook authentication flow
    """
    inputs = {
        "url": "https://dev.vox.snappod.ai/signup",
        "facebookSignUpButtonLocator": "getByRole('button', { name: 'Sign up with Facebook' })"
    }
    page.goto(SIGNUP_URL, timeout=60000)
    page.wait_for_load_state('networkidle')

    page.locator(resolve_test_case_locator(inputs["facebookSignUpButtonLocator"])).click()

    expect(page).to_have_url(re.compile(r"www\.facebook\.com"))