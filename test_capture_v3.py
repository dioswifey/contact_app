#!/usr/bin/env python3
"""
Contact App Feature Test v3 - Robust version with better error handling
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
from pathlib import Path

APP_URL = "http://127.0.0.1:8000/"
DESKTOP_PATH = Path.home() / "Desktop"
TEST_USERNAME = f"testuser_{int(time.time())}"
TEST_PASSWORD = "Test@12345"

TESTS = ["testA", "testB", "testC", "testD", "testE", "testF", "testG", "testH", "testI"]

def capture_screenshot(driver, filename, description):
    """Capture and save screenshot"""
    try:
        filepath = DESKTOP_PATH / f"{filename}.png"
        driver.save_screenshot(str(filepath))
        if filepath.exists():
            size = filepath.stat().st_size
            print(f"  [OK] {filename}.png ({size:,} bytes)")
            return True
    except Exception as e:
        print(f"  [ERROR] Failed to capture: {str(e)}")
    return False

def safe_input(driver, selector, text, timeout=5):
    """Safely input text into element"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.3)
        # Clear and input
        element.clear()
        element.send_keys(text)
        return True
    except Exception as e:
        print(f"    Could not input to {selector}: {str(e)}")
        return False

def safe_click(driver, selector, timeout=5):
    """Safely click element"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.3)
        element.click()
        return True
    except Exception as e:
        print(f"    Could not click {selector}: {str(e)}")
        return False

def main():
    print("="*70)
    print("Contact App Feature Test v3")
    print("="*70)

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1280, 800)

    try:
        # Load app
        print("\n[SETUP] Loading application...")
        driver.get(APP_URL)
        time.sleep(4)

        # Test A: Login Page
        print("\n[1/9] Capturing Login Page...")
        capture_screenshot(driver, TESTS[0], "Login Page - Initial load")
        time.sleep(1)

        # Sign up
        print("\n[2/9] Creating new account...")
        print("  Filling signup form...")
        safe_input(driver, "input[name='username']", TEST_USERNAME)
        safe_input(driver, "input[name='password']", TEST_PASSWORD)
        time.sleep(1)

        print("  Clicking Sign Up button...")
        safe_click(driver, "#signup-btn")
        time.sleep(2)

        capture_screenshot(driver, TESTS[1], "Sign Up Form - New account created")
        time.sleep(1)

        # Login
        print("\n[LOGIN] Logging in...")
        safe_input(driver, "input[name='username']", TEST_USERNAME)
        safe_input(driver, "input[name='password']", TEST_PASSWORD)
        time.sleep(1)

        print("  Clicking Log In button...")
        safe_click(driver, "#login-btn")
        print("  Waiting for dashboard...")
        time.sleep(5)

        # Test C: Dashboard
        print("\n[3/9] Capturing Dashboard...")
        capture_screenshot(driver, TESTS[2], "Dashboard - After login")
        time.sleep(1)

        # Test D: Add Contact
        print("\n[4/9] Capturing Add Contact Form...")
        safe_input(driver, "input[name='name']", "John")
        safe_input(driver, "input[name='phone']", "01012345678")
        safe_input(driver, "input[name='addr']", "Seoul")
        time.sleep(1)

        capture_screenshot(driver, TESTS[3], "Add Contact Form - Filled form")

        print("  Submitting contact...")
        safe_click(driver, "#contact-submit-btn")
        time.sleep(3)

        # Test E: Contact List
        print("\n[5/9] Capturing Contact List...")
        capture_screenshot(driver, TESTS[4], "Contact List - View contacts")
        time.sleep(1)

        # Test F: Category Management
        print("\n[6/9] Capturing Category Management...")
        # Scroll to category section
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        capture_screenshot(driver, TESTS[5], "Category Management - Categories")
        time.sleep(1)

        # Test G: Search
        print("\n[7/9] Capturing Search & Filter...")
        search_input = driver.find_element(By.CSS_SELECTOR, "input[type='search']")
        search_input.clear()
        search_input.send_keys("John")
        time.sleep(1)
        capture_screenshot(driver, TESTS[6], "Search & Filter - Search results")
        time.sleep(1)

        # Test H: Edit (simulated)
        print("\n[8/9] Capturing Edit Contact...")
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

        # Look for and click first contact's edit button (if available)
        try:
            edit_btns = driver.find_elements(By.CSS_SELECTOR, "button[data-action='edit']")
            if not edit_btns:
                # Try alternative selector
                all_btns = driver.find_elements(By.TAG_NAME, "button")
                edit_btns = [b for b in all_btns if "Edit" in (b.get_attribute("textContent") or "")]

            if edit_btns:
                edit_btns[0].click()
                time.sleep(2)
        except:
            pass

        capture_screenshot(driver, TESTS[7], "Edit Contact - Edit form")
        time.sleep(1)

        # Test I: Logout
        print("\n[9/9] Capturing Logout...")
        try:
            safe_click(driver, "#logout-btn")
            time.sleep(2)
        except:
            print("  Could not click logout")

        capture_screenshot(driver, TESTS[8], "Logout - Back to login")
        time.sleep(1)

        # Summary
        print("\n" + "="*70)
        print("CAPTURE COMPLETE!")
        print("="*70)

        for test_name in TESTS:
            filepath = DESKTOP_PATH / f"{test_name}.png"
            if filepath.exists():
                size = filepath.stat().st_size
                print(f"[OK] {test_name}.png ({size:,} bytes)")

        print("="*70 + "\n")

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    main()
