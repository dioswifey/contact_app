#!/usr/bin/env python3
"""Quick Playwright capture script"""
import time
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    import subprocess
    subprocess.run(["pip", "install", "-q", "playwright", "pillow"])
    from playwright.sync_api import sync_playwright
    from PIL import Image, ImageDraw, ImageFont

DESKTOP = Path.home() / "Desktop"
FEATURES = [
    ("aaa", "Login Page - Beautiful pink retro pixel-art design with username/password inputs and login/signup buttons"),
    ("bbb", "Dashboard - Contact management interface with all features visible after successful login"),
    ("ccc", "Add Contact Form - Input fields for Name, Phone, Address with category dropdown"),
    ("ddd", "Contact List - View and manage contacts with edit/delete buttons and search"),
    ("eee", "Category Management - Right panel showing categories with edit/delete options"),
    ("fff", "Search & Filter - Search bar and filtering functionality for contacts")
]

def add_description(img_path, desc):
    """Add description to image bottom"""
    try:
        img = Image.open(img_path)
        w, h = img.size
        new_img = Image.new('RGB', (w, h+90), (254, 248, 245))
        new_img.paste(img, (0, 0))
        draw = ImageDraw.Draw(new_img)
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 13)
        except:
            font = ImageFont.load_default()

        words = desc.split()
        lines, line = [], ""
        for w in words:
            test = line + (" " + w if line else w)
            if len(test) > 75:
                lines.append(line)
                line = w
            else:
                line = test
        if line:
            lines.append(line)

        y = h + 10
        for ln in lines:
            draw.text((15, y), ln, fill=(199, 76, 120), font=font)
            y += 22
        new_img.save(img_path)
    except:
        pass

with sync_playwright() as p:
    print("🎮 Capturing Contact App Features...")
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1200, "height": 800})
    page.goto("http://127.0.0.1:8000/")
    time.sleep(1)

    # Capture 1: Login Page
    page.screenshot(path=str(DESKTOP / "aaa.png"), full_page=True)
    add_description(DESKTOP / "aaa.png", FEATURES[0][1])
    print(f"✓ aaa.png - {FEATURES[0][1][:50]}...")

    # Login
    page.fill("[name=username]", "testuser123")
    page.fill("[name=password]", "testpass123")
    page.click("button:has-text('Log In')")
    time.sleep(2)

    # Capture 2: Dashboard
    page.screenshot(path=str(DESKTOP / "bbb.png"), full_page=True)
    add_description(DESKTOP / "bbb.png", FEATURES[1][1])
    print(f"✓ bbb.png - {FEATURES[1][1][:50]}...")

    # Capture 3: Add Contact Form (scroll to top)
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(1)
    page.screenshot(path=str(DESKTOP / "ccc.png"), full_page=True)
    add_description(DESKTOP / "ccc.png", FEATURES[2][1])
    print(f"✓ ccc.png - {FEATURES[2][1][:50]}...")

    # Add a contact
    page.fill(".cf--name", "John Doe")
    page.fill(".cf--phone", "01012345678")
    page.fill(".cf--addr", "Seoul")
    page.click(".btn--submit")
    time.sleep(1)

    # Capture 4: Contact List
    page.screenshot(path=str(DESKTOP / "ddd.png"), full_page=True)
    add_description(DESKTOP / "ddd.png", FEATURES[3][1])
    print(f"✓ ddd.png - {FEATURES[3][1][:50]}...")

    # Capture 5: Categories (scroll to right)
    page.evaluate("document.querySelector('.col-right').scrollIntoView()")
    time.sleep(1)
    page.screenshot(path=str(DESKTOP / "eee.png"), full_page=True)
    add_description(DESKTOP / "eee.png", FEATURES[4][1])
    print(f"✓ eee.png - {FEATURES[4][1][:50]}...")

    # Capture 6: Search
    page.evaluate("window.scrollTo(0, 0)")
    page.fill("#search-input", "John")
    time.sleep(1)
    page.screenshot(path=str(DESKTOP / "fff.png"), full_page=True)
    add_description(DESKTOP / "fff.png", FEATURES[5][1])
    print(f"✓ fff.png - {FEATURES[5][1][:50]}...")

    browser.close()
    print("\n✅ Complete! All 6 features captured to Desktop.")
