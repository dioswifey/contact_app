#!/usr/bin/env python3
"""
Proper login test - ensures manage-section is actually visible before capturing
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

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options)
driver.set_window_size(1280, 800)

try:
    print("Loading app...")
    driver.get(APP_URL)
    time.sleep(3)

    # Step 1: Check login page
    print("\n[Step 1] Login page screenshot...")
    driver.save_screenshot(str(DESKTOP_PATH / "testA.png"))
    print(f"  Saved: testA.png")

    # Step 2: Signup
    print("\n[Step 2] Signing up...")
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    username_field.send_keys(TEST_USERNAME)

    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(TEST_PASSWORD)

    signup_btn = driver.find_element(By.ID, "signup-btn")
    signup_btn.click()
    time.sleep(2)

    driver.save_screenshot(str(DESKTOP_PATH / "testB.png"))
    print(f"  Saved: testB.png")

    # Step 3: Login
    print("\n[Step 3] Logging in...")
    username_field = driver.find_element(By.NAME, "username")
    username_field.clear()
    username_field.send_keys(TEST_USERNAME)

    password_field = driver.find_element(By.NAME, "password")
    password_field.clear()
    password_field.send_keys(TEST_PASSWORD)

    login_btn = driver.find_element(By.ID, "login-btn")
    login_btn.click()

    # Wait for manage-section to be visible
    print("  Waiting for manage-section to be visible...")
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "manage-section"))
        )
        print("  manage-section is visible!")
    except:
        print("  WARNING: manage-section not visible within 10 seconds")

    time.sleep(3)

    # Step 4: Capture dashboard
    print("\n[Step 4] Dashboard screenshot...")
    driver.save_screenshot(str(DESKTOP_PATH / "testC.png"))
    print(f"  Saved: testC.png (MAIN CONTACT MANAGEMENT PAGE)")

    # Step 5: Check page state
    print("\n[Step 5] Checking page state...")
    auth_modal = driver.find_element(By.ID, "auth-modal")
    manage_section = driver.find_element(By.ID, "manage-section")

    auth_modal_hidden = "auth-modal--hidden" in auth_modal.get_attribute("class")
    manage_visible = manage_section.is_displayed()

    print(f"  auth-modal hidden: {auth_modal_hidden}")
    print(f"  manage-section visible: {manage_visible}")

    # Check for contact form
    contact_form = driver.find_element(By.ID, "contact-form")
    print(f"  contact-form exists: {contact_form is not None}")

    # Get page title
    page_title = driver.title
    print(f"  Page title: {page_title}")

    # Get topbar auth state
    topbar = driver.find_element(By.CSS_SELECTOR, ".topbar")
    topbar_auth = topbar.get_attribute("data-auth")
    print(f"  topbar data-auth: {topbar_auth}")

    print("\n[SUCCESS] Login test complete!")

finally:
    driver.quit()
    print("Browser closed.")
