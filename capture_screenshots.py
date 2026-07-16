#!/usr/bin/env python3
"""
Capture Contact App features with Playwright and add descriptions with Pillow
"""

from playwright.sync_api import sync_playwright
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

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 1280, "height": 720})

        try:
            print(f"Opening app at {APP_URL}...")
            page.goto(APP_URL, wait_until="load")
            time.sleep(2)

            # Screenshot 1: Login page (initial load)
            print("Capturing aaa.png - Login page...")
            page.screenshot(path=os.path.join(DESKTOP_PATH, "aaa.png"))
            add_description_to_image(os.path.join(DESKTOP_PATH, "aaa.png"), SCREENSHOTS[0][1])
            time.sleep(1)

            # Check if already logged in or need to login
            # Try to find login form
            try:
                username_input = page.locator('input[name="username"], input[type="text"][placeholder*="user"], input[id*="username"]')
                if username_input.is_visible(timeout=2000):
                    print("Found login form, logging in...")
                    username_input.fill(USERNAME)

                    password_input = page.locator('input[type="password"]')
                    password_input.fill(PASSWORD)

                    # Find and click login button
                    login_button = page.locator('button:has-text("Login"), button:has-text("Sign In"), button:has-text("log in")')
                    if login_button.is_visible(timeout=1000):
                        login_button.click()
                    else:
                        # Try alternative - press Enter
                        password_input.press("Enter")

                    time.sleep(3)  # Wait for login to complete
                else:
                    # Try signup
                    print("Login form not visible, looking for signup...")
                    signup_button = page.locator('button:has-text("Sign Up"), button:has-text("Register"), a:has-text("Sign Up")')
                    if signup_button.is_visible(timeout=1000):
                        signup_button.click()
                        time.sleep(2)

                        # Fill signup form
                        username_input = page.locator('input[name="username"], input[type="text"][placeholder*="user"]')
                        username_input.fill(USERNAME)

                        password_input = page.locator('input[type="password"]')
                        password_input.fill(PASSWORD)

                        signup_submit = page.locator('button:has-text("Sign Up"), button:has-text("Register")')
                        signup_submit.click()
                        time.sleep(3)
            except Exception as e:
                print(f"Login/signup attempt: {e}")
                time.sleep(2)

            # Screenshot 2: Dashboard after login
            print("Capturing bbb.png - Dashboard...")
            page.screenshot(path=os.path.join(DESKTOP_PATH, "bbb.png"))
            add_description_to_image(os.path.join(DESKTOP_PATH, "bbb.png"), SCREENSHOTS[1][1])
            time.sleep(1)

            # Screenshot 3: Add contact form
            print("Capturing ccc.png - Add Contact Form...")
            try:
                # Look for add contact button
                add_contact_btn = page.locator('button:has-text("Add Contact"), button:has-text("New Contact"), a:has-text("Add"), button[id*="add"]')
                if add_contact_btn.is_visible(timeout=2000):
                    add_contact_btn.first.click()
                    time.sleep(2)
            except:
                print("Could not find add contact button")

            page.screenshot(path=os.path.join(DESKTOP_PATH, "ccc.png"))
            add_description_to_image(os.path.join(DESKTOP_PATH, "ccc.png"), SCREENSHOTS[2][1])
            time.sleep(1)

            # Try to fill in a test contact
            try:
                name_input = page.locator('input[name="name"], input[placeholder*="name"], input[placeholder*="Name"]')
                if name_input.is_visible(timeout=1000):
                    name_input.fill("Test Contact")

                    phone_input = page.locator('input[name="phone"], input[placeholder*="phone"], input[placeholder*="Phone"]')
                    if phone_input.is_visible(timeout=500):
                        phone_input.fill("555-1234")

                    address_input = page.locator('input[name="address"], input[placeholder*="address"], input[placeholder*="Address"]')
                    if address_input.is_visible(timeout=500):
                        address_input.fill("123 Main St")
            except:
                pass

            # Screenshot 4: Contact list
            print("Capturing ddd.png - Contact List...")
            try:
                # Try to close form/go back to list
                close_btn = page.locator('button:has-text("Cancel"), a:has-text("Back")')
                if close_btn.is_visible(timeout=1000):
                    close_btn.first.click()
                    time.sleep(2)
            except:
                pass

            page.screenshot(path=os.path.join(DESKTOP_PATH, "ddd.png"))
            add_description_to_image(os.path.join(DESKTOP_PATH, "ddd.png"), SCREENSHOTS[3][1])
            time.sleep(1)

            # Screenshot 5: Category management
            print("Capturing eee.png - Category Management...")
            try:
                # Look for categories link/button
                categories_btn = page.locator('a:has-text("Categories"), button:has-text("Categories"), a[href*="categor"]')
                if categories_btn.is_visible(timeout=2000):
                    categories_btn.first.click()
                    time.sleep(2)
                else:
                    # Try to find it in menu
                    menu_links = page.locator('nav a, .nav a, .menu a')
                    for i in range(menu_links.count()):
                        link = menu_links.nth(i)
                        if "categor" in link.text_content().lower():
                            link.click()
                            time.sleep(2)
                            break
            except Exception as e:
                print(f"Could not navigate to categories: {e}")

            page.screenshot(path=os.path.join(DESKTOP_PATH, "eee.png"))
            add_description_to_image(os.path.join(DESKTOP_PATH, "eee.png"), SCREENSHOTS[4][1])
            time.sleep(1)

            # Screenshot 6: Search and filter
            print("Capturing fff.png - Search & Filter...")
            try:
                # Go back to contacts list if needed
                contacts_btn = page.locator('a:has-text("Contacts"), button:has-text("Contacts"), a[href*="contact"]')
                if contacts_btn.is_visible(timeout=1000):
                    contacts_btn.first.click()
                    time.sleep(2)
            except:
                pass

            # Look for search box
            try:
                search_input = page.locator('input[type="search"], input[placeholder*="search"], input[placeholder*="Search"]')
                if search_input.is_visible(timeout=1000):
                    search_input.fill("test")
                    time.sleep(1)
            except:
                pass

            page.screenshot(path=os.path.join(DESKTOP_PATH, "fff.png"))
            add_description_to_image(os.path.join(DESKTOP_PATH, "fff.png"), SCREENSHOTS[5][1])

            print("\n✓ All screenshots captured and saved to:", DESKTOP_PATH)
            for filename, _ in SCREENSHOTS:
                full_path = os.path.join(DESKTOP_PATH, filename)
                if os.path.exists(full_path):
                    print(f"  ✓ {filename}")

        finally:
            browser.close()

if __name__ == "__main__":
    capture_features()
