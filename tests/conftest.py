import sys
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright
import logging
import datetime
import shutil
import time
import threading

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture
def context(browser, request):
    # Extract page type from test file path
    test_file = request.node.fspath.basename
    page_type = test_file.replace("test_", "").replace(".py", "")
    test_name = request.node.name
    
    # Create artifacts directory structure
    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True)
    
    # Organized subdirectories
    videos_dir = artifacts_dir / "videos" / page_type
    traces_dir = artifacts_dir / "traces" / page_type
    videos_dir.mkdir(parents=True, exist_ok=True)
    traces_dir.mkdir(parents=True, exist_ok=True)
    
    # Clean up existing artifacts for this test
    for old_file in videos_dir.glob(f"{test_name}.*"):
        old_file.unlink(missing_ok=True)
    for old_file in traces_dir.glob(f"{test_name}.*"):
        old_file.unlink(missing_ok=True)
    
    context = browser.new_context(record_video_dir=str(videos_dir))
    context.tracing.start(screenshots=True, snapshots=True)
    yield context
    context.tracing.stop(path=str(traces_dir / f"{test_name}.zip"))
    
    # Rename video file to match test name
    try:
        video_files = list(videos_dir.glob("*.webm"))
        if video_files:
            old_video = video_files[0]
            new_video = videos_dir / f"{test_name}.webm"
            old_video.rename(new_video)
    except Exception:
        pass
    
    context.close()

@pytest.fixture
def page(context):
    page = context.new_page()
    yield page
    page.close()

@pytest.fixture
def authenticated_page(context):
    """Login and navigate to welcome page with proper waits"""
    page = context.new_page()
    
    # Navigate to login with timeout
    page.goto("https://dev.vox.snappod.ai/login", timeout=30000)
    page.wait_for_load_state('domcontentloaded', timeout=15000)
    
    # Fill credentials with explicit waits
    email_input = page.locator("#login-email")
    email_input.wait_for(state='visible', timeout=10000)
    email_input.fill("tadikamallasivaparvathi@gmail.com")
    
    password_input = page.locator("#login-password")
    password_input.wait_for(state='visible', timeout=10000)
    password_input.fill("Siva@2001")
    
    # Click login and wait for navigation
    login_button = page.locator("button:has-text('Login')")
    login_button.wait_for(state='visible', timeout=10000)
    login_button.click()
    
    # Wait for login to complete
    page.wait_for_load_state('networkidle', timeout=20000)
    
    # Navigate to welcome page if not already there
    if 'welcome-to-snappod-ai' not in page.url:
        page.goto("https://dev.vox.snappod.ai/welcome-to-snappod-ai", timeout=30000)
        page.wait_for_load_state('domcontentloaded', timeout=15000)
    
    yield page
    page.close()

def extract_simple_error(error_text):
    """Extract simple error reason from complex stack trace"""
    error_str = str(error_text)
    if "element(s) not found" in error_str:
        return "Element not found"
    elif "Target page, context or browser has been closed" in error_str:
        return "Browser closed unexpectedly"
    elif "net::ERR_ABORTED" in error_str:
        return "Navigation failed"
    elif "AssertionError" in error_str:
        return "Assertion failed"
    else:
        return "Test error"

@pytest.fixture(autouse=True)
def log_test_info(request):
    import time
    import threading
    # Extract page type from test file path
    test_file = request.node.fspath.basename
    page_type = test_file.replace("test_", "").replace(".py", "")
    test_name = request.node.name
    
    # Create artifacts directory structure
    artifacts_dir = Path("artifacts")
    log_dir = artifacts_dir / "logs" / page_type
    screenshot_dir = artifacts_dir / "screenshots" / page_type
    log_dir.mkdir(parents=True, exist_ok=True)
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    
    # Clean up existing artifacts for this test
    for old_file in log_dir.glob(f"{test_name}.*"):
        old_file.unlink(missing_ok=True)
    for old_file in screenshot_dir.glob(f"{test_name}.*"):
        old_file.unlink(missing_ok=True)
    
    test_logger = logging.getLogger(test_name)
    test_logger.setLevel(logging.INFO)
    
    # Remove existing handlers
    for handler in test_logger.handlers[:]:
        test_logger.removeHandler(handler)
    
    # Add file handler with clean format
    file_handler = logging.FileHandler(f"artifacts/logs/{page_type}/{test_name}.log", mode='w')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    test_logger.addHandler(file_handler)
    
    test_logger.info(f"Starting test: {test_name}")
    start_time = datetime.datetime.now()
    
    # Schedule screenshot after 5 seconds
    def take_screenshot():
        time.sleep(5)
        try:
            page_fixture = None
            if 'authenticated_page' in request.fixturenames:
                page_fixture = request.getfixturevalue('authenticated_page')
            elif 'page' in request.fixturenames:
                page_fixture = request.getfixturevalue('page')
            
            if page_fixture:
                screenshot_path = f"artifacts/screenshots/{page_type}/{test_name}.png"
                page_fixture.screenshot(path=screenshot_path)
                test_logger.info(f"Screenshot saved: {screenshot_path}")
        except Exception as e:
            test_logger.warning(f"Screenshot failed: {e}")
    
    screenshot_thread = threading.Thread(target=take_screenshot)
    screenshot_thread.daemon = True
    screenshot_thread.start()
    
    yield
    
    end_time = datetime.datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    if hasattr(request.node, 'rep_call'):
        if request.node.rep_call.passed:
            test_logger.info(f"✅ PASSED - {duration:.1f}s")
        elif request.node.rep_call.failed:
            failure_reason = extract_simple_error(request.node.rep_call.longrepr)
            test_logger.error(f"❌ FAILED - {duration:.1f}s - {failure_reason}")
    else:
        test_logger.info(f"COMPLETED - {duration:.1f}s")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)