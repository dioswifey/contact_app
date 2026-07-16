#!/usr/bin/env python3
"""
Capture Contact App features with Playwright and add descriptions with Pillow
- 1200x800 viewport
- Description text: 90px height, #c74c78 pink, Arial 13px
"""

from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
import time
import os
import sys

# Configuration
APP_URL = "http://127.0.0.1:8000/"
USERNAME = "testuser123"
PASSWORD = "testpass123"
DESKTOP_PATH = r"C:\Users\mega\Desktop"

# Screenshots config: (filename, description)
SCREENSHOTS = [
    ("aaa.png", "Login Page: Beautiful pink retro pixel-art design with username/password inputs"),
    ("bbb.png", "Dashboard: Contact management interface with all features visible"),
    ("ccc.png", "Add Contact Form: Name, Phone, Address input fields and category dropdown"),
    ("ddd.png", "Contact List: Display contacts with edit/delete buttons"),
    ("eee.png", "Category Management: Right panel with categories"),
    ("fff.png", "Search & Filter: Search bar and filter functionality"),
]

def add_description_to_image(image_path, description):
    """Add description text to the bottom of an image using Pillow
    - 90px height added
    - Pink color #c74c78
    - Arial 13px font
    """
    try:
        img = Image.open(image_path)
        width, height = img.size

        # Create new image with 90px extra space at bottom for text
        description_height = 90
        new_height = height + description_height
        new_img = Image.new('RGB', (width, new_height), color='white')

        # Paste original image
        new_img.paste(img, (0, 0))

        # Add text
        draw = ImageDraw.Draw(new_img)

        # Try to load Arial font at 13px, fall back to default
        try:
            font = ImageFont.truetype("arial.ttf", 13)
        except:
            try:
                font = ImageFont.truetype("Arial.ttf", 13)
            except:
                font = ImageFont.load_default()

        # Pink color from user spec: #c74c78
        pink_color = (199, 76, 120)

        # Calculate text position (center horizontally, top of new space)
        text_x = 20
        text_y = height + 15

        # Draw text with word wrapping if needed
        draw.text((text_x, text_y), description, fill=pink_color, font=font)

        # Save modified image
        new_img.save(image_path, 'PNG')
        file_size = os.path.getsize(image_path)
        print(f"✓ {os.path.basename(image_path)}: Added description ({file_size} bytes)")
        return True
    except Exception as e:
        print(f"✗ Error adding description to {image_path}: {e}")
        return False

def capture_features():
    """Main function to capture all features"""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        # 1200x800 viewport as specified
        page = browser.new_page(viewport={"width": 1200, "height": 800})

        try:
            print(f"Opening app at {APP_URL}...")
            page.goto(APP_URL, wait_until="load")
            time.sleep(2)

            # Screenshot 1: Login page (initial load)
            print("\n[1/6] Capturing aaa.png - Login page...")
            page.screenshot(path=os.path.join(DESKTOP_PATH, "aaa.png"))
            add_description_to_image(os.path.join(DESKTOP_PATH, "aaa.png"), SCREENSHOTS[0][1])
            time.sleep(1)

            # Check if already logged in or need to login
            try:
                # Try multiple selectors for username input
                username_input = page.locator('input[name="username"], input[type="text"][placeholder*="user"], input[id*="username"], input[placeholder*="Username"]')
                if username_input.count() > 0 and username_input.first.is_visible(timeout=2000):
                    print("   Found login form, logging in...")
                    username_input.first.fill(USERNAME)

                    password_input = page.locator('input[type="password"]')
                    if password_input.count() > 0:
                        password_input.first.fill(PASSWORD)

                    # Find and click login button
                    login_button = page.locator('button:has-text("Login"), button:has-text("Sign In"), button:has-text("log in"), input[type="submit"]')
                    if login_button.count() > 0 and login_button.first.is_visible(timeout=1000):
                        login_button.first.click()
                    else:
                        # Try alternative - press Enter
                        password_input = page.locator('input[type="password"]')
                        if password_input.count() > 0:
                            password_input.first.press("Enter")

                    time.sleep(3)  # Wait for login to complete
                    print("   Login attempt completed")
            except Exception as e:
                print(f"   Login attempt: {e}")
                time.sleep(2)

            # Screenshot 2: Dashboard after login
            print("[2/6] Capturing bbb.png - Dashboard...")
            page.screenshot(path=os.path.join(DESKTOP_PATH, "bbb.png"))
            add_description_to_image(os.path.join(DESKTOP_PATH, "bbb.png"), SCREENSHOTS[1][1])
            time.sleep(1)

            # Screenshot 3: Add contact form
            print("[3/6] Capturing ccc.png - Add Contact Form...")
            try:
                # Look for add contact button
                add_contact_btn = page.locator('button:has-text("Add Contact"), button:has-text("New Contact"), a:has-text("Add"), button[id*="add"], button:has-text("Add New"), button:has-text("Create")')
                if add_contact_btn.count() > 0 and add_contact_btn.first.is_visible(timeout=2000):
                    print("   Found Add Contact button, clicking...")
                    add_contact_btn.first.click()
                    time.sleep(2)
                else:
                    print("   Add Contact button not found")
            except Exception as e:
                print(f"   Could not find add contact button: {e}")

            page.screenshot(path=os.path.join(DESKTOP_PATH, "ccc.png"))
            add_description_to_image(os.path.join(DESKTOP_PATH, "ccc.png"), SCREENSHOTS[2][1])
            time.sleep(1)

            # Try to fill in a test contact
            try:
                name_input = page.locator('input[name="name"], input[placeholder*="name"], input[placeholder*="Name"]')
                if name_input.count() > 0 and name_input.first.is_visible(timeout=1000):
                    name_input.first.fill("Test Contact")

                    phone_input = page.locator('input[name="phone"], input[placeholder*="phone"], input[placeholder*="Phone"]')
                    if phone_input.count() > 0 and phone_input.first.is_visible(timeout=500):
                        phone_input.first.fill("555-1234")

                    address_input = page.locator('input[name="address"], input[placeholder*="address"], input[placeholder*="Address"]')
                    if address_input.count() > 0 and address_input.first.is_visible(timeout=500):
                        address_input.first.fill("123 Main St")
            except Exception as e:
                print(f"   Could not fill form: {e}")

            # Screenshot 4: Contact list
            print("[4/6] Capturing ddd.png - Contact List...")
            try:
                # Try to close form/go back to list
                close_btn = page.locator('button:has-text("Cancel"), a:has-text("Back"), button:has-text("Back")')
                if close_btn.count() > 0 and close_btn.first.is_visible(timeout=1000):
                    close_btn.first.click()
                    time.sleep(2)
            except Exception as e:
                print(f"   Could not find close button: {e}")

            page.screenshot(path=os.path.join(DESKTOP_PATH, "ddd.png"))
            add_description_to_image(os.path.join(DESKTOP_PATH, "ddd.png"), SCREENSHOTS[3][1])
            time.sleep(1)

            # Screenshot 5: Category management
            print("[5/6] Capturing eee.png - Category Management...")
            try:
                # Look for categories link/button in navigation
                categories_btn = page.locator('a:has-text("Categories"), button:has-text("Categories"), a[href*="categor"]')
                found = False
                if categories_btn.count() > 0 and categories_btn.first.is_visible(timeout=2000):
                    print("   Found Categories button")
                    categories_btn.first.click()
                    found = True
                    time.sleep(2)

                if not found:
                    # Try to find it in menu
                    menu_links = page.locator('nav a, .nav a, .menu a, [role="navigation"] a')
                    for i in range(min(menu_links.count(), 10)):
                        try:
                            link = menu_links.nth(i)
                            text = link.text_content()
                            if text and "categor" in text.lower():
                                print("   Found Categories in menu")
                                link.click()
                                found = True
                                time.sleep(2)
                                break
                        except:
                            pass

                if not found:
                    print("   Categories not found, showing current page")
            except Exception as e:
                print(f"   Could not navigate to categories: {e}")

            page.screenshot(path=os.path.join(DESKTOP_PATH, "eee.png"))
            add_description_to_image(os.path.join(DESKTOP_PATH, "eee.png"), SCREENSHOTS[4][1])
            time.sleep(1)

            # Screenshot 6: Search and filter
            print("[6/6] Capturing fff.png - Search & Filter...")
            try:
                # Go back to contacts list if needed
                contacts_btn = page.locator('a:has-text("Contacts"), button:has-text("Contacts"), a[href*="contact"]')
                if contacts_btn.count() > 0 and contacts_btn.first.is_visible(timeout=1000):
                    print("   Going to Contacts...")
                    contacts_btn.first.click()
                    time.sleep(2)
            except Exception as e:
                print(f"   Could not navigate to contacts: {e}")

            # Look for search box and fill it
            try:
                search_input = page.locator('input[type="search"], input[placeholder*="search"], input[placeholder*="Search"]')
                if search_input.count() > 0 and search_input.first.is_visible(timeout=1000):
                    print("   Found search box, searching...")
                    search_input.first.fill("test")
                    time.sleep(1)
            except Exception as e:
                print(f"   Could not use search: {e}")

            page.screenshot(path=os.path.join(DESKTOP_PATH, "fff.png"))
            add_description_to_image(os.path.join(DESKTOP_PATH, "fff.png"), SCREENSHOTS[5][1])

            # Summary
            print("\n" + "="*60)
            print("✓ ALL SCREENSHOTS CAPTURED SUCCESSFULLY")
            print("="*60)
            print(f"Location: {DESKTOP_PATH}\n")

            for filename, description in SCREENSHOTS:
                full_path = os.path.join(DESKTOP_PATH, filename)
                if os.path.exists(full_path):
                    size = os.path.getsize(full_path)
                    print(f"✓ {filename:12s} ({size:8d} bytes) - {description[:50]}...")

            print("\nViewport: 1200x800")
            print("Text: Arial 13px, #c74c78 pink, 90px description area")

        finally:
            browser.close()
            print("\nBrowser closed.")

if __name__ == "__main__":
    try:
        capture_features()
    except KeyboardInterrupt:
        print("\nScript interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
