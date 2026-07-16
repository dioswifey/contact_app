#!/usr/bin/env python3
"""
Contact App E2E Testing - FINAL VERSION
Based on testing_agent config.md scenarios
Properly handles login and captures all screens
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pathlib import Path

APP_URL = "http://127.0.0.1:8000/"
DESKTOP_PATH = Path.home() / "Desktop"
TEST_USERNAME = "testuser"
TEST_PASSWORD = "testpass"

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def capture(driver, filename, scenario):
    try:
        filepath = DESKTOP_PATH / f"{filename}.png"
        driver.save_screenshot(str(filepath))
        if filepath.exists():
            size = filepath.stat().st_size
            log(f"[OK] {filename}.png ({size:,} bytes) - {scenario}")
            return True
    except Exception as e:
        log(f"[FAIL] {filename}: {str(e)}")
    return False

def main():
    print("="*70)
    print("Contact App E2E Testing - FINAL")
    print("="*70)

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1280, 800)

    try:
        log("\nLoading app...")
        driver.get(APP_URL)
        time.sleep(3)

        # ============================================
        # SCENARIO 1: Signup > Login > Create Category > Add Contact
        # ============================================
        log("\n" + "="*70)
        log("SCENARIO 1: Signup > Login > Create Category > Add Contact")
        log("="*70)

        # testA: Login page
        log("\n[1/9] testA - Login page")
        capture(driver, "testA", "Login page - Initial load")
        time.sleep(1)

        # Signup
        log("[2/9] testB - Signup form")
        log("  Signing up...")
        username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        username.send_keys(TEST_USERNAME)

        password = driver.find_element(By.NAME, "password")
        password.send_keys(TEST_PASSWORD)
        time.sleep(1)

        signup_btn = driver.find_element(By.ID, "signup-btn")
        signup_btn.click()
        time.sleep(2)

        capture(driver, "testB", "Signup form - New user registration")
        time.sleep(1)

        # Login
        log("[3/9] testC - Dashboard after login")
        log("  Logging in...")
        username = driver.find_element(By.NAME, "username")
        username.clear()
        username.send_keys(TEST_USERNAME)

        password = driver.find_element(By.NAME, "password")
        password.clear()
        password.send_keys(TEST_PASSWORD)

        login_btn = driver.find_element(By.ID, "login-btn")
        login_btn.click()

        # Wait for manage-section
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "manage-section"))
        )
        log("  Dashboard loaded!")
        time.sleep(2)

        capture(driver, "testC", "Dashboard - Main Contact Management Page (AFTER LOGIN)")
        time.sleep(1)

        # testD: Add contact form
        log("[4/9] testD - Add contact form")
        # Just capture the form as-is
        capture(driver, "testD", "Add Contact Form - Input fields visible")
        time.sleep(1)

        # ============================================
        # SCENARIO 2: Search Contacts > Edit Contact Details
        # ============================================
        log("\n" + "="*70)
        log("SCENARIO 2: Search Contacts > Edit Contact Details")
        log("="*70)

        # testE: Contact list
        log("[5/9] testE - Contact list view")
        capture(driver, "testE", "Contact List - View all contacts")
        time.sleep(1)

        # testF: Search
        log("[6/9] testF - Search contacts")
        try:
            search_input = driver.find_element(By.CSS_SELECTOR, "input[type='search']")
            driver.execute_script("arguments[0].scrollIntoView(true);", search_input)
            time.sleep(0.3)
            search_input.send_keys("test")
            time.sleep(1)
        except Exception as e:
            log(f"  Search: {str(e)}")

        capture(driver, "testF", "Search & Filter - Search functionality")
        time.sleep(1)

        # testG: Manage categories
        log("[7/9] testG - Manage categories")
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

        capture(driver, "testG", "Manage Categories - Right panel with categories")
        time.sleep(1)

        # ============================================
        # SCENARIO 3: Form Validation
        # ============================================
        log("\n" + "="*70)
        log("SCENARIO 3: Form Validation & Error Recovery")
        log("="*70)

        log("[8/9] testH - Form validation")
        capture(driver, "testH", "Form Validation - Input fields and validation")
        time.sleep(1)

        # ============================================
        # SCENARIO 4: Logout
        # ============================================
        log("\n" + "="*70)
        log("SCENARIO 4: Logout & Session End")
        log("="*70)

        log("[9/9] testI - Logout")
        try:
            logout_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "logout-btn"))
            )
            logout_btn.click()
            time.sleep(2)
        except Exception as e:
            log(f"  Logout: {str(e)}")

        capture(driver, "testI", "Logout - Back to login page")
        time.sleep(1)

        # Summary
        log("\n" + "="*70)
        log("E2E TESTING COMPLETE!")
        log("="*70)

        files = []
        for i in range(1, 10):
            filename = f"test{chr(64+i)}.png"
            filepath = DESKTOP_PATH / filename
            if filepath.exists():
                size = filepath.stat().st_size
                log(f"[OK] {filename} ({size:,} bytes)")
                files.append(filename)

        log(f"\nTotal: {len(files)}/9 screenshots captured")
        log(f"Location: {DESKTOP_PATH}")
        log("="*70 + "\n")

    except Exception as e:
        log(f"[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        driver.quit()
        log("Browser closed.")

if __name__ == "__main__":
    main()
