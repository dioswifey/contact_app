"""
Capture Contact App Features with Descriptions
Uses Playwright to screenshot 6 key features and adds descriptions
"""
import time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Installing playwright...")
    import subprocess
    subprocess.run(["pip", "install", "playwright", "pillow", "-q"])
    from playwright.sync_api import sync_playwright

# Desktop path
DESKTOP_PATH = Path.home() / "Desktop"

# Feature descriptions
FEATURES = [
    {
        "name": "aaa",
        "description": "Login Page - Beautiful pink retro pixel-art design with username/password inputs and login/signup buttons",
        "actions": None
    },
    {
        "name": "bbb",
        "description": "Dashboard - After successful login, displays contact management interface with all features",
        "actions": [("fill", "[name=username]", "testuser123"), ("fill", "[name=password]", "testpass123"), ("click", "button:has-text('Log In')")]
    },
    {
        "name": "ccc",
        "description": "Add Contact Form - Input fields for Name, Phone, Address with category dropdown and Add button",
        "actions": [("fill", "[name=username]", "testuser123"), ("fill", "[name=password]", "testpass123"), ("click", "button:has-text('Log In')"), ("wait", 2)]
    },
    {
        "name": "ddd",
        "description": "Contact List - Displays added contacts with edit/delete buttons and search functionality",
        "actions": [("fill", "[name=username]", "testuser123"), ("fill", "[name=password]", "testpass123"), ("click", "button:has-text('Log In')"), ("wait", 2), ("fill", ".cf--name", "John Doe"), ("fill", ".cf--phone", "01012345678"), ("fill", ".cf--addr", "Seoul")]
    },
    {
        "name": "eee",
        "description": "Category Management - Right panel showing categories with edit/delete buttons",
        "actions": [("fill", "[name=username]", "testuser123"), ("fill", "[name=password]", "testpass123"), ("click", "button:has-text('Log In')"), ("wait", 2)]
    },
    {
        "name": "fff",
        "description": "Search and Filter - Search bar to find contacts by name with smart filtering",
        "actions": [("fill", "[name=username]", "testuser123"), ("fill", "[name=password]", "testpass123"), ("click", "button:has-text('Log In')"), ("wait", 2), ("fill", "#search-input", "test")]
    }
]

def add_text_to_image(image_path, description):
    """Add description text to bottom of image"""
    try:
        img = Image.open(image_path)
        width, height = img.size

        # Create new image with extra space for text
        text_height = 90
        new_img = Image.new('RGB', (width, height + text_height), color=(254, 248, 245))
        new_img.paste(img, (0, 0))

        # Add text
        draw = ImageDraw.Draw(new_img)

        # Try to use a nice font
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 13)
            title_font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 14)
        except:
            font = ImageFont.load_default()
            title_font = font

        # Draw description with wrapping
        words = description.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + (" " + word if current_line else word)
            if len(test_line) > 75:
                lines.append(current_line)
                current_line = word
            else:
                current_line = test_line
        if current_line:
            lines.append(current_line)

        # Draw text
        y_offset = height + 12
        for line in lines:
            draw.text((15, y_offset), line, fill=(199, 76, 120), font=font)
            y_offset += 22

        # Save
        new_img.save(image_path)
        print(f"✓ {image_path.name} - {description}")
    except Exception as e:
        print(f"⚠ Could not add text: {e}")

def capture_feature(page, feature, idx):
    """Capture a single feature"""
    try:
        print(f"\n📸 Feature {idx+1}/6: {feature['name'].upper()}")

        # Execute actions if provided
        if feature['actions']:
            for action in feature['actions']:
                if action[0] == "fill":
                    try:
                        page.fill(action[1], action[2])
                    except:
                        pass
                elif action[0] == "click":
                    try:
                        page.click(action[1])
                    except:
                        pass
                elif action[0] == "wait":
                    time.sleep(action[1])

        # Take screenshot
        screenshot_path = DESKTOP_PATH / f"{feature['name']}.png"
        page.screenshot(path=str(screenshot_path), full_page=True)

        # Add description
        add_text_to_image(screenshot_path, feature['description'])
        return True
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def main():
    """Main capture workflow"""
    print("="*70)
    print("🎮 Contact App Feature Capture - 6 Key Flows")
    print("="*70)

    with sync_playwright() as p:
        # Launch browser
        print("\n🚀 Launching browser...")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 1200, "height": 800})

        # Navigate to app
        print("🌐 Navigating to http://127.0.0.1:8000/")
        page.goto("http://127.0.0.1:8000/")
        time.sleep(1)

        # Capture each feature
        success_count = 0
        for idx, feature in enumerate(FEATURES):
            if capture_feature(page, feature, idx):
                success_count += 1
            time.sleep(1)

        # Close browser
        browser.close()

        print("\n" + "="*70)
        print(f"✅ Complete: {success_count}/{len(FEATURES)} features captured")
        print(f"📁 Saved to: {DESKTOP_PATH}")
        print("="*70)

if __name__ == "__main__":
    main()
