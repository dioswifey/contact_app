#!/usr/bin/env python3
"""
Capture Contact App features with Selenium and add descriptions with Pillow
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image, ImageDraw, ImageFont
import time
import os

# Configuration
APP_URL = "http://127.0.0.1:8000/"
USERNAME = "testuser123"
PASSWORD = "testpass123"
DESKTOP_PATH = r"C:\Users\mega\Desktop"

# Screenshots config: (filename, description)
SCREENSHOTS = [
    ("aaa.png", "Login Page - Beautiful pink retro pixel-art design"),
    ("bbb.png", "Dashboard - Contact management interface"),
    ("ccc.png", "Add Contact Form - Name, Phone, Address inputs"),
    ("ddd.png", "Contact List - View all contacts with edit/delete"),
    ("eee.png", "Category Management - Manage contact categories"),
    ("fff.png", "Search & Filter - Find contacts by name"),
]

def add_description_to_image(image_path, description):
    """Add description text to the bottom of an image using Pillow"""
    try:
        img = Image.open(image_path)
        width, height = img.size

        # Create new image with extra space at bottom for text
        description_height = 50
        new_height = height + description_height
        new_img = Image.new('RGB', (width, new_height), color='white')

        # Paste original image
        new_img.paste(img, (0, 0))

        # Add text
        draw = ImageDraw.Draw(new_img)

        # Try to use a nice font, fall back to default if not available
        try:
            font = ImageFont.truetype("arial.ttf", 14)
        except:
            font = ImageFont.load_default()

        # Add description text
        text_x = 10
        text_y = height + 10
        draw.text((text_x, text_y), description, fill='black', font=font)

        # Save modified image
        new_img.save(image_path, 'PNG')
        print(f"✓ Added description to {image_path}")
    except Exception as e:
        print(f"✗ Error adding description to {image_path}: {e}")

def capture_features():
    """Main function to capture all features"""

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Uncomment for headless mode
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1280,720")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        print(f"Opening app at {APP_URL}...")
        driver.get(APP_URL)
        time.sleep(2)

        # Screenshot 1: Login page (initial load)
        print("Capturing aaa.png - Login page...")
        driver.save_screenshot(os.path.join(DESKTOP_PATH, "aaa.png"))
        add_description_to_image(os.path.join(DESKTOP_PATH, "aaa.png"), SCREENSHOTS[0][1])
        time.sleep(1)

        # Check if already logged in or need to login
        try:
            # Try to find and fill login form
            username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"], input[name="username"]')))
            print("Found login form, logging in...")
            username_input.send_keys(USERNAME)

            password_input = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
            password_input.send_keys(PASSWORD)

            # Find and click login button
            try:
                login_button = driver.find_element(By.XPATH, '//button[contains(text(), "Login")] | //button[contains(text(), "Sign In")] | //button[contains(text(), "log in")]')
                login_button.click()
            except:
                # Try pressing Enter
                password_input.submit()

            time.sleep(3)  # Wait for login to complete
        except Exception as e:
            print(f"Login attempt: {e}")
            time.sleep(2)

        # Screenshot 2: Dashboard after login
        print("Capturing bbb.png - Dashboard...")
        driver.save_screenshot(os.path.join(DESKTOP_PATH, "bbb.png"))
        add_description_to_image(os.path.join(DESKTOP_PATH, "bbb.png"), SCREENSHOTS[1][1])
        time.sleep(1)

        # Screenshot 3: Add contact form
        print("Capturing ccc.png - Add Contact Form...")
        try:
            # Look for add contact button
            add_contact_btns = driver.find_elements(By.XPATH, '//button[contains(text(), "Add")] | //button[contains(text(), "New")] | //a[contains(text(), "Add")]')
            if add_contact_btns:
                add_contact_btns[0].click()
                time.sleep(2)
        except Exception as e:
            print(f"Could not find add contact button: {e}")

        driver.save_screenshot(os.path.join(DESKTOP_PATH, "ccc.png"))
        add_description_to_image(os.path.join(DESKTOP_PATH, "ccc.png"), SCREENSHOTS[2][1])
        time.sleep(1)

        # Try to fill in a test contact
        try:
            name_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[name="name"], input[placeholder*="name"], input[placeholder*="Name"]')
            if name_inputs:
                name_inputs[0].send_keys("Test Contact")

                phone_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[name="phone"], input[placeholder*="phone"]')
                if phone_inputs:
                    phone_inputs[0].send_keys("555-1234")

                address_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[name="address"], input[placeholder*="address"]')
                if address_inputs:
                    address_inputs[0].send_keys("123 Main St")
        except Exception as e:
            print(f"Could not fill form: {e}")

        # Screenshot 4: Contact list
        print("Capturing ddd.png - Contact List...")
        try:
            # Try to close form/go back to list
            close_btns = driver.find_elements(By.XPATH, '//button[contains(text(), "Cancel")] | //a[contains(text(), "Back")]')
            if close_btns:
                close_btns[0].click()
                time.sleep(2)
        except Exception as e:
            print(f"Could not close form: {e}")

        driver.save_screenshot(os.path.join(DESKTOP_PATH, "ddd.png"))
        add_description_to_image(os.path.join(DESKTOP_PATH, "ddd.png"), SCREENSHOTS[3][1])
        time.sleep(1)

        # Screenshot 5: Category management
        print("Capturing eee.png - Category Management...")
        try:
            # Look for categories link/button
            categories_btns = driver.find_elements(By.XPATH, '//a[contains(text(), "Categor")] | //button[contains(text(), "Categor")] | //a[contains(@href, "categor")]')
            if categories_btns:
                categories_btns[0].click()
                time.sleep(2)
        except Exception as e:
            print(f"Could not navigate to categories: {e}")

        driver.save_screenshot(os.path.join(DESKTOP_PATH, "eee.png"))
        add_description_to_image(os.path.join(DESKTOP_PATH, "eee.png"), SCREENSHOTS[4][1])
        time.sleep(1)

        # Screenshot 6: Search and filter
        print("Capturing fff.png - Search & Filter...")
        try:
            # Go back to contacts list if needed
            contacts_btns = driver.find_elements(By.XPATH, '//a[contains(text(), "Contact")] | //button[contains(text(), "Contact")] | //a[contains(@href, "contact")]')
            if contacts_btns:
                contacts_btns[0].click()
                time.sleep(2)
        except Exception as e:
            print(f"Could not navigate back to contacts: {e}")

        # Look for search box
        try:
            search_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="search"], input[placeholder*="search"], input[placeholder*="Search"]')
            if search_inputs:
                search_inputs[0].send_keys("test")
                time.sleep(1)
        except Exception as e:
            print(f"Could not interact with search: {e}")

        driver.save_screenshot(os.path.join(DESKTOP_PATH, "fff.png"))
        add_description_to_image(os.path.join(DESKTOP_PATH, "fff.png"), SCREENSHOTS[5][1])

        print("\n✓ All screenshots captured and saved to:", DESKTOP_PATH)
        for filename, _ in SCREENSHOTS:
            full_path = os.path.join(DESKTOP_PATH, filename)
            if os.path.exists(full_path):
                print(f"  ✓ {filename}")

    finally:
        driver.quit()

if __name__ == "__main__":
    capture_features()
