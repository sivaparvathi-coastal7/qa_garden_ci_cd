import sys
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright, expect
import logging
import datetime
import time
import threading
import os
from dotenv import load_dotenv

load_dotenv()
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture
def context(browser):
    context = browser.new_context()
    yield context
    context.close()

@pytest.fixture
def page(context):
    page = context.new_page()
    yield page
    page.close()

@pytest.fixture
def authenticated_page(context):
    page = context.new_page()
    page.goto("https://dev.vox.snappod.ai/login", timeout=60000)
    page.wait_for_load_state("networkidle")

    page.locator("#login-email").fill(os.getenv("VALID_EMAIL", "tadikamallasivaparvathi@gmail.com"))
    page.locator("#login-password").fill(os.getenv("VALID_PASSWORD", "Siva@2001"))
    page.locator("button:has-text('Login')").click()

    page.wait_for_load_state("networkidle")
    yield page
    page.close()