#!/usr/bin/env python3
"""
Capture Contact App features with Selenium
Saves as testA.png, testB.png, testC.png, etc.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import os
import sys

# Configuration
APP_URL = "http://127.0.0.1:8000/"
USERNAME = "testuser123"
PASSWORD = "testpass123"
DESKTOP_PATH = r"C:\Users\mega\Desktop"

# Test sequence names
TESTS = ["testA", "testB", "testC", "testD", "testE", "testF", "testG", "testH", "testI"]
TEST_DESCRIPTIONS = [
    "1. Login Page - Initial load",
    "2. Dashboard - After login",
    "3. Add Contact Form",
    "4. Contact List View",
    "5. Category Management",
    "6. Search & Filter",
    "7. Edit Contact",
    "8. Delete Confirmation",
    "9. Logout & Return to Login"
]

def capture_screenshot(driver, filename, description):
    """Capture a screenshot and save it"""
    try:
        filepath = os.path.join(DESKTOP_PATH, f"{filename}.png")
        driver.save_screenshot(filepath)

        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"[OK] {filename}.png ({size} bytes) - {description}")
            return True
        else:
            print(f"[FAIL] Could not save {filename}.png")
            return False
    except Exception as e:
        print(f"[ERROR] {filename}.png - {str(e)}")
        return False

def capture_features():
    """Main function to capture all features with Selenium"""

    # Setup Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    try:
        # Launch Chrome
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(1280, 800)

        print("="*70)
        print("Contact App Feature Test - Screenshot Capture")
        print("="*70)
        print(f"Opening app at {APP_URL}...")

        # Navigate to app
        driver.get(APP_URL)
        time.sleep(3)

        # Test A: Login Page
        print("\n[1/9] Test A - Login Page")
        capture_screenshot(driver, TESTS[0], TEST_DESCRIPTIONS[0])
        time.sleep(1)

        # Try to login
        try:
            print("  - Attempting to login...")
            username_field = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.clear()
            username_field.send_keys(USERNAME)

            password_field = driver.find_element(By.NAME, "password")
            password_field.clear()
            password_field.send_keys(PASSWORD)

            # Try to find and click login button
            try:
                login_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Login') or contains(text(), 'Sign In')]")
                login_btn.click()
            except:
                password_field.send_keys(u"")  # Press Enter

            time.sleep(3)
        except Exception as e:
            print(f"  - Login attempt: {str(e)}")

        # Test B: Dashboard after login
        print("\n[2/9] Test B - Dashboard")
        capture_screenshot(driver, TESTS[1], TEST_DESCRIPTIONS[1])
        time.sleep(1)

        # Test C: Add Contact Form
        print("\n[3/9] Test C - Add Contact Form")
        try:
            # Look for add button
            add_btns = driver.find_elements(By.XPATH, "//button[contains(text(), 'Add') or contains(text(), 'New')]")
            if add_btns:
                add_btns[0].click()
                time.sleep(2)
        except:
            pass

        capture_screenshot(driver, TESTS[2], TEST_DESCRIPTIONS[2])
        time.sleep(1)

        # Try to fill form
        try:
            inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input[type='email'], input[type='tel']")
            if len(inputs) > 0:
                inputs[0].send_keys("John Doe")
            if len(inputs) > 1:
                inputs[1].send_keys("john@example.com")
            if len(inputs) > 2:
                inputs[2].send_keys("010-1234-5678")
            time.sleep(1)
        except:
            pass

        # Test D: Contact List
        print("\n[4/9] Test D - Contact List View")
        try:
            # Try to go back to list
            cancel_btns = driver.find_elements(By.XPATH, "//button[contains(text(), 'Cancel') or contains(text(), 'Back')]")
            if cancel_btns:
                cancel_btns[0].click()
                time.sleep(2)
        except:
            pass

        capture_screenshot(driver, TESTS[3], TEST_DESCRIPTIONS[3])
        time.sleep(1)

        # Test E: Category Management
        print("\n[5/9] Test E - Category Management")
        try:
            # Look for categories link
            cat_links = driver.find_elements(By.XPATH, "//a[contains(text(), 'Categor') or contains(text(), 'categor')]")
            if cat_links:
                cat_links[0].click()
                time.sleep(2)
        except:
            pass

        capture_screenshot(driver, TESTS[4], TEST_DESCRIPTIONS[4])
        time.sleep(1)

        # Test F: Search & Filter
        print("\n[6/9] Test F - Search & Filter")
        try:
            # Look for search input
            search_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='search'], input[placeholder*='search' i]")
            if search_inputs:
                search_inputs[0].send_keys("test")
                time.sleep(1)
        except:
            pass

        capture_screenshot(driver, TESTS[5], TEST_DESCRIPTIONS[5])
        time.sleep(1)

        # Test G: Edit Contact
        print("\n[7/9] Test G - Edit Contact")
        try:
            edit_btns = driver.find_elements(By.XPATH, "//button[contains(text(), 'Edit') or contains(text(), 'edit')]")
            if edit_btns:
                edit_btns[0].click()
                time.sleep(2)
        except:
            pass

        capture_screenshot(driver, TESTS[6], TEST_DESCRIPTIONS[6])
        time.sleep(1)

        # Test H: Delete Confirmation
        print("\n[8/9] Test H - Delete Confirmation")
        try:
            delete_btns = driver.find_elements(By.XPATH, "//button[contains(text(), 'Delete') or contains(text(), 'delete')]")
            if delete_btns:
                delete_btns[0].click()
                time.sleep(1)
        except:
            pass

        capture_screenshot(driver, TESTS[7], TEST_DESCRIPTIONS[7])
        time.sleep(1)

        # Test I: Logout
        print("\n[9/9] Test I - Logout & Return to Login")
        try:
            logout_btns = driver.find_elements(By.XPATH, "//button[contains(text(), 'Logout') or contains(text(), 'logout')]")
            if logout_btns:
                logout_btns[0].click()
                time.sleep(2)
        except:
            pass

        capture_screenshot(driver, TESTS[8], TEST_DESCRIPTIONS[8])
        time.sleep(1)

        # Print summary
        print("\n" + "="*70)
        print("Screenshot Capture Complete!")
        print("="*70)
        print(f"Saved to: {DESKTOP_PATH}\n")

        for test_name, description in zip(TESTS, TEST_DESCRIPTIONS):
            filepath = os.path.join(DESKTOP_PATH, f"{test_name}.png")
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                print(f"[OK] {test_name}.png ({size:,} bytes)")

        print("\n" + "="*70)

    except Exception as e:
        print(f"\nFatal error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            driver.quit()
        except:
            pass
        print("\nBrowser closed.")

if __name__ == "__main__":
    try:
        capture_features()
    except KeyboardInterrupt:
        print("\nScript interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nFatal error: {str(e)}")
        sys.exit(1)
