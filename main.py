from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
import uvicorn
import subprocess
import json
import os
from pathlib import Path
from typing import Dict, List, Optional
import logging
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="QA Garden UI/UX Test Automation API",
    description="API for managing Playwright test automation, test generation, and artifact management",
    version="1.0.0"
)

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent
TESTS_DIR = PROJECT_ROOT / "tests"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
SCREENSHOTS_DIR = ARTIFACTS_DIR / "screenshots"
VIDEOS_DIR = ARTIFACTS_DIR / "videos"
TEST_LOGS_DIR = ARTIFACTS_DIR / "logs"
TRACES_DIR = ARTIFACTS_DIR / "traces"
TESTCASES_DIR = PROJECT_ROOT / "testcases"
CONFIG_DIR = PROJECT_ROOT / "config"

# Create directories
ARTIFACTS_DIR.mkdir(exist_ok=True)
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
TEST_LOGS_DIR.mkdir(parents=True, exist_ok=True)
TRACES_DIR.mkdir(parents=True, exist_ok=True)
TESTCASES_DIR.mkdir(exist_ok=True)
CONFIG_DIR.mkdir(exist_ok=True)

# External API configuration
EXTERNAL_API_BASE_URL = os.getenv("EXTERNAL_API_BASE_URL")

# Mount static files
app.mount("/screenshots", StaticFiles(directory=str(SCREENSHOTS_DIR)), name="screenshots")
app.mount("/videos", StaticFiles(directory=str(VIDEOS_DIR)), name="videos")
app.mount("/logs", StaticFiles(directory=str(TEST_LOGS_DIR)), name="logs")

@app.get("/")
async def root():
    return {
        "message": "QA Garden UI/UX Test Automation API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "test_execution": "/tests/run/{page_type}",
            "test_generation": "/generate/tests",
            "artifacts": "/artifacts/{page_type}",
            "test_cases": "/testcases/{page_type}",
            "test_results": "/results/{page_type}",
            "locators": "/config/locators/{page_type}"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "project_root": str(PROJECT_ROOT)
    }

@app.get("/testcases/{page_type}")
async def get_testcases(page_type: str):
    """Get test cases from external API and save locally"""
    valid_pages = ["login", "signup", "welcome"]
    if page_type not in valid_pages:
        raise HTTPException(status_code=400, detail=f"Invalid page type. Must be one of: {valid_pages}")
    
    try:
        # Try to fetch from external API first
        if EXTERNAL_API_BASE_URL:
            external_url = f"{EXTERNAL_API_BASE_URL}/testcases/{page_type}"
            
            response = requests.get(external_url, timeout=10)
            if response.status_code == 200:
                test_cases = response.json()
                
                # Save to local file as backup
                local_file = TESTCASES_DIR / f"{page_type}_testcases.json"
                with open(local_file, 'w', encoding='utf-8') as f:
                    json.dump(test_cases, f, indent=2)
                
                return test_cases
        
        # Fallback to local file
        local_file = TESTCASES_DIR / f"{page_type}_testcases.json"
        if local_file.exists():
            with open(local_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        raise HTTPException(status_code=404, detail=f"Test cases not found for {page_type}")
        
    except requests.exceptions.RequestException as e:
        # Fallback to local file on API error
        local_file = TESTCASES_DIR / f"{page_type}_testcases.json"
        if local_file.exists():
            with open(local_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        raise HTTPException(status_code=500, detail=f"Failed to fetch test cases: {str(e)}")

@app.get("/config/locators/{page_type}")
async def get_locators(page_type: str):
    """Get locators from external API and save as Python file"""
    valid_pages = ["login", "signup", "welcome"]
    if page_type not in valid_pages:
        raise HTTPException(status_code=400, detail=f"Invalid page type. Must be one of: {valid_pages}")
    
    try:
        # Try to fetch from external API first
        if EXTERNAL_API_BASE_URL:
            external_url = f"{EXTERNAL_API_BASE_URL}/config/locators/{page_type}"
            
            response = requests.get(external_url, timeout=10)
            if response.status_code == 200:
                locators_data = response.json()
                
                # Save to local Python file
                local_file = CONFIG_DIR / f"{page_type}_locators.py"
                with open(local_file, 'w', encoding='utf-8') as f:
                    f.write(f"# {page_type.title()} Page Locators\n")
                    f.write(f"{page_type.upper()}_LOCATORS = {json.dumps(locators_data, indent=4)}\n")
                
                return locators_data
        
        # Fallback to local file
        local_file = CONFIG_DIR / f"{page_type}_locators.py"
        if local_file.exists():
            with open(local_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract locators from Python file
                import ast
                tree = ast.parse(content)
                for node in tree.body:
                    if isinstance(node, ast.Assign):
                        return ast.literal_eval(node.value)
        
        raise HTTPException(status_code=404, detail=f"Locators not found for {page_type}")
        
    except requests.exceptions.RequestException as e:
        # Fallback to local file on API error
        local_file = CONFIG_DIR / f"{page_type}_locators.py"
        if local_file.exists():
            with open(local_file, 'r', encoding='utf-8') as f:
                content = f.read()
                import ast
                tree = ast.parse(content)
                for node in tree.body:
                    if isinstance(node, ast.Assign):
                        return ast.literal_eval(node.value)
        raise HTTPException(status_code=500, detail=f"Failed to fetch locators: {str(e)}")

@app.post("/tests/run/{page_type}")
async def run_tests(page_type: str, background_tasks: BackgroundTasks):
    """Run Playwright tests for specific page type"""
    valid_pages = ["login", "signup", "welcome"]
    if page_type not in valid_pages:
        raise HTTPException(status_code=400, detail=f"Invalid page type. Must be one of: {valid_pages}")
    
    test_path = TESTS_DIR / page_type / f"test_{page_type}.py"
    if not test_path.exists():
        raise HTTPException(status_code=404, detail=f"Test file not found: {test_path}")
    
    try:
        cmd = ["python", "-m", "pytest", str(test_path), "-v", "--tb=short"]
        result = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=300)
        
        return {
            "status": "completed",
            "page_type": page_type,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "artifacts_available": f"/artifacts/{page_type}"
        }
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "message": "Test execution timed out after 5 minutes"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test execution failed: {str(e)}")

@app.post("/generate/tests")
async def generate_tests():
    """Generate test files using the LLM-based test generation script"""
    try:
        cmd = ["python", "generate_script.py"]
        result = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=120)
        
        return {
            "status": "completed",
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "message": "Test generation completed"
        }
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "message": "Test generation timed out after 2 minutes"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test generation failed: {str(e)}")

@app.get("/artifacts/{page_type}")
async def get_artifacts(page_type: str):
    """Get available artifacts for a page type"""
    valid_pages = ["login", "signup", "welcome"]
    if page_type not in valid_pages:
        raise HTTPException(status_code=400, detail=f"Invalid page type. Must be one of: {valid_pages}")
    
    artifacts = {
        "page_type": page_type,
        "screenshots": [],
        "videos": [],
        "logs": []
    }
    
    # Get screenshots
    screenshots_path = SCREENSHOTS_DIR / page_type
    if screenshots_path.exists():
        artifacts["screenshots"] = [f.name for f in screenshots_path.glob("*.png")]
    
    # Get videos
    videos_path = VIDEOS_DIR / page_type
    if videos_path.exists():
        artifacts["videos"] = [f.name for f in videos_path.glob("*.webm")]
    
    # Get logs
    logs_path = TEST_LOGS_DIR / page_type
    if logs_path.exists():
        artifacts["logs"] = [f.name for f in logs_path.glob("*.log")]
    
    return artifacts

if __name__ == "__main__":
    uvicorn.run(app, host="192.168.1.40", port=8002)