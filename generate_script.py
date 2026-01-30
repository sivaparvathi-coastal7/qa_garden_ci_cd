import os
import sys
from pathlib import Path
import json
import google.genai as genai


from dotenv import load_dotenv

# =========================
# ENV SETUP
# =========================
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set in environment variables")

client = genai.Client(api_key=API_KEY)
# =========================
# CONFIG
# =========================
MODEL_NAME = "models/gemini-flash-latest"

PROJECT_ROOT = Path(__file__).resolve().parent
PROMPT_FILE = PROJECT_ROOT / "prompt.txt"

CONFIG_DIR = PROJECT_ROOT / "config"
TESTCASES_DIR = PROJECT_ROOT / "testcases"
OUTPUT_TESTS_DIR = PROJECT_ROOT / "tests"

OUTPUT_TESTS_DIR.mkdir(exist_ok=True)

# =========================
# UTILITIES
# =========================
def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""

def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def inject_pythonpath(code: str) -> str:
    injection = (
        "import sys\n"
        "from pathlib import Path\n"
        "ROOT_DIR = Path(__file__).resolve().parent.parent\n"
        "sys.path.insert(0, str(ROOT_DIR))\n\n"
    )
    return injection + code

# =========================
# LLM INTEGRATION
# =========================
def call_llm(prompt: str) -> str:
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    return response.text
def extract_code_only(text: str) -> str:
    if "```python" in text:
        return text.split("```python")[1].split("```")[0].strip()
    if "```" in text:
        return text.split("```")[1].split("```")[0].strip()

    stripped = text.strip()
    if stripped.startswith(("import ", "from ", "def ", "class ")):
        return stripped

    raise RuntimeError("Could not extract Python code from LLM response")
def sanitize_llm_code(code: str) -> str:
    # Fix JS regex → Python string
    code = code.replace(
        "to_have_url(/",
        "to_have_url(\""
    ).replace(
        "/)",
        "\")"
    )

    # Remove JS-only keywords
    code = code.replace("await ", "")
    code = code.replace("async ", "")

    return code

# =========================
# PAGE DISCOVERY
# =========================
def infer_pages():
    pages = []
    for tc_file in TESTCASES_DIR.glob("*_testcases.json"):
        page = tc_file.stem.replace("_testcases", "")
        locator_file = CONFIG_DIR / f"{page}_locators.json"
        if locator_file.exists():
            pages.append(page)
    return pages

# =========================
# GENERATE conftest.py
# =========================
def generate_conftest():
    content = """
import sys
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright, expect
import logging
import datetime
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

    page.locator("#login-email").fill("test@example.com")
    page.locator("#login-password").fill("password")
    page.locator("button:has-text('Login')").click()

    page.wait_for_load_state("networkidle")
    yield page
    page.close()
"""
    write_file(OUTPUT_TESTS_DIR / "conftest.py", content.strip())
    print("conftest.py generated")

# =========================
# GENERATE TESTS PER PAGE
# =========================
def generate_page_tests(page: str, base_prompt: str):
    locator_file = CONFIG_DIR / f"{page}_locators.json"
    testcase_file = TESTCASES_DIR / f"{page}_testcases.json"

    if not locator_file.exists() or not testcase_file.exists():
        print(f"Skipping {page} (missing files)")
        return

    locator_json = locator_file.read_text(encoding="utf-8")
    testcase_json = testcase_file.read_text(encoding="utf-8")

    page_prompt = f"""
{base_prompt}

PAGE: {page}

LOCATORS JSON:
{locator_json}

TEST CASES JSON:
{testcase_json}

Generate a complete pytest Playwright test file.
Output ONLY valid Python code.
"""

    print(f"Generating tests for {page}...")
    raw_output = call_llm(page_prompt)
    test_code = extract_code_only(raw_output)
    test_code = sanitize_llm_code(test_code)
    test_code = inject_pythonpath(test_code)

    test_dir = OUTPUT_TESTS_DIR / page
    out_path = test_dir / f"test_{page}.py"
    write_file(out_path, test_code)

    print(f"Generated {out_path}")

# =========================
# MAIN
# =========================
def main():
    print("Starting LLM-based test generation")

    base_prompt = read_file(PROMPT_FILE)
    if not base_prompt:
        raise RuntimeError("prompt.txt is missing or empty")

    pages = infer_pages()
    if not pages:
        raise RuntimeError("No valid pages detected")

    generate_conftest()

    for page in pages:
        generate_page_tests(page, base_prompt)

    print("Test generation completed successfully")
    generated = list(OUTPUT_TESTS_DIR.rglob("test_*.py"))
    if not generated:
        raise RuntimeError("No tests were generated by LLM")

if __name__ == "__main__":
    main()
