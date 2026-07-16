#!/usr/bin/env python3
"""
Improved Contact App Feature Test - Screenshot Capture
Properly handles login, signup, and all features
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os
import sys
from pathlib import Path

# Configuration
APP_URL = "http://127.0.0.1:8000/"
DESKTOP_PATH = Path.home() / "Desktop"
TEST_USERNAME = f"testuser_{int(time.time())}"
TEST_PASSWORD = "Test@12345"

TESTS = ["testA", "testB", "testC", "testD", "testE", "testF", "testG", "testH", "testI"]
TEST_DESCRIPTIONS = [
    "1. Login Page - Initial load",
    "2. Sign Up Form - New user registration",
    "3. Dashboard - After login",
    "4. Add Contact Form - Create new contact",
    "5. Contact List - View all contacts",
    "6. Category Management - Category organization",
    "7. Search & Filter - Search functionality",
    "8. Edit Contact - Modify contact info",
    "9. Logout - Return to login"
]

def wait_for_element(driver, by, value, timeout=10):
    """Wait for element to be visible"""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )
    except:
        return None

def capture_screenshot(driver, filename, description):
    """Capture and save screenshot"""
    try:
        filepath = DESKTOP_PATH / f"{filename}.png"
        driver.save_screenshot(str(filepath))
        if filepath.exists():
            size = filepath.stat().st_size
            print(f"[OK] {filename}.png ({size:,} bytes) - {description}")
            return True
    except Exception as e:
        print(f"[ERROR] {filename}.png - {str(e)}")
    return False

def test_contact_app():
    """Main test function"""

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1280, 800)

    try:
        print("="*70)
        print("Contact App Feature Test v2 - Full Workflow")
        print("="*70)
        print(f"App URL: {APP_URL}")
        print(f"Test Username: {TEST_USERNAME}")
        print(f"Screenshot Location: {DESKTOP_PATH}")
        print("="*70 + "\n")

        # ============================================
        # Load app
        # ============================================
        print("[SETUP] Loading app...")
        driver.get(APP_URL)
        time.sleep(3)

        # ============================================
        # Test A: Login Page
        # ============================================
        print("\n[1/9] Test A - Login Page")
        capture_screenshot(driver, TESTS[0], TEST_DESCRIPTIONS[0])
        time.sleep(1)

        # ============================================
        # Test B: Sign Up
        # ============================================
        print("\n[2/9] Test B - Sign Up Form")

        # Fill login form
        username_field = wait_for_element(driver, By.NAME, "username", 10)
        if username_field:
            username_field.send_keys(TEST_USERNAME)

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(TEST_PASSWORD)

        time.sleep(1)

        # Click signup button
        signup_btn = driver.find_element(By.ID, "signup-btn")
        signup_btn.click()
        time.sleep(2)

        capture_screenshot(driver, TESTS[1], TEST_DESCRIPTIONS[1])
        time.sleep(1)

        # ============================================
        # Now login with the newly created user
        # ============================================
        print("\n[LOGIN] Logging in with new account...")

        # Fill login form again
        username_field = driver.find_element(By.NAME, "username")
        username_field.clear()
        username_field.send_keys(TEST_USERNAME)

        password_field = driver.find_element(By.NAME, "password")
        password_field.clear()
        password_field.send_keys(TEST_PASSWORD)

        time.sleep(1)

        # Click login button (which is submit on the form)
        login_btn = driver.find_element(By.ID, "login-btn")
        login_btn.click()

        # Wait for dashboard to appear
        print("  Waiting for dashboard to load...")
        time.sleep(4)

        # ============================================
        # Test C: Dashboard / Manage Section
        # ============================================
        print("\n[3/9] Test C - Dashboard")

        # Check if logged in by looking for manage-section
        try:
            manage_section = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.ID, "manage-section"))
            )
            print("  Dashboard loaded successfully")
        except:
            print("  WARNING: Dashboard may not have loaded properly")

        time.sleep(1)
        capture_screenshot(driver, TESTS[2], TEST_DESCRIPTIONS[2])
        time.sleep(1)

        # ============================================
        # Test D: Add Contact Form
        # ============================================
        print("\n[4/9] Test D - Add Contact Form")

        # Fill contact form
        name_input = wait_for_element(driver, By.CSS_SELECTOR, "input[name='name']")
        if name_input:
            name_input.send_keys("John")

        phone_input = driver.find_element(By.CSS_SELECTOR, "input[name='phone']")
        phone_input.send_keys("01012345678")

        addr_input = driver.find_element(By.CSS_SELECTOR, "input[name='addr']")
        addr_input.send_keys("Seoul")

        time.sleep(1)
        capture_screenshot(driver, TESTS[3], TEST_DESCRIPTIONS[3])

        # Submit contact form
        try:
            submit_btn = driver.find_element(By.ID, "contact-submit-btn")
            submit_btn.click()
            print("  Contact added")
            time.sleep(2)
        except:
            print("  Could not submit contact form")

        # ============================================
        # Test E: Contact List
        # ============================================
        print("\n[5/9] Test E - Contact List")
        time.sleep(1)
        capture_screenshot(driver, TESTS[4], TEST_DESCRIPTIONS[4])
        time.sleep(1)

        # ============================================
        # Test F: Category Management
        # ============================================
        print("\n[6/9] Test F - Category Management")

        # Look for category form or panel
        category_form = driver.find_elements(By.ID, "category-form")
        if category_form:
            # Try to add a category
            cat_input = driver.find_elements(By.CSS_SELECTOR, "input[name='name']")
            if len(cat_input) > 1:  # Second input is usually category name
                try:
                    cat_input[1].send_keys("Friends")
                    cat_submit = driver.find_elements(By.TAG_NAME, "button")
                    for btn in cat_submit:
                        if "Add" in btn.text or "Submit" in btn.text:
                            btn.click()
                            break
                    time.sleep(1)
                except:
                    pass

        capture_screenshot(driver, TESTS[5], TEST_DESCRIPTIONS[5])
        time.sleep(1)

        # ============================================
        # Test G: Search & Filter
        # ============================================
        print("\n[7/9] Test G - Search & Filter")

        search_input = driver.find_elements(By.CSS_SELECTOR, "input[type='search']")
        if search_input:
            search_input[0].send_keys("John")
            time.sleep(1)

        capture_screenshot(driver, TESTS[6], TEST_DESCRIPTIONS[6])
        time.sleep(1)

        # ============================================
        # Test H: Edit Contact
        # ============================================
        print("\n[8/9] Test H - Edit Contact")

        # Look for edit buttons
        edit_buttons = driver.find_elements(By.CSS_SELECTOR, "button[data-action='edit']")
        if not edit_buttons:
            # Try alternative selectors
            all_buttons = driver.find_elements(By.TAG_NAME, "button")
            edit_buttons = [btn for btn in all_buttons if "Edit" in btn.text or "edit" in btn.text]

        if edit_buttons:
            edit_buttons[0].click()
            time.sleep(2)

        capture_screenshot(driver, TESTS[7], TEST_DESCRIPTIONS[7])
        time.sleep(1)

        # ============================================
        # Test I: Logout
        # ============================================
        print("\n[9/9] Test I - Logout")

        logout_btn = driver.find_element(By.ID, "logout-btn")
        logout_btn.click()
        time.sleep(2)

        capture_screenshot(driver, TESTS[8], TEST_DESCRIPTIONS[8])

        # ============================================
        # Summary
        # ============================================
        print("\n" + "="*70)
        print("TEST COMPLETE!")
        print("="*70)

        for test_name, description in zip(TESTS, TEST_DESCRIPTIONS):
            filepath = DESKTOP_PATH / f"{test_name}.png"
            if filepath.exists():
                size = filepath.stat().st_size
                print(f"[OK] {test_name}.png ({size:,} bytes)")

        print("="*70 + "\n")
        return True

    except Exception as e:
        print(f"\n[FATAL ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        capture_screenshot(driver, "error", "Error screenshot")
        return False
    finally:
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    success = test_contact_app()
    sys.exit(0 if success else 1)
