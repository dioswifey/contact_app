#!/usr/bin/env python3
"""
Create PDF with screenshots and descriptions
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os

PROJECT_DIR = Path("C:\\big21\\vibe-coding\\project\\contact_app")
SCREENSHOTS = [
    ("testA_login_page.png", "1. Login Page", "Initial login/signup screen with username and password fields. Users can either log in or create a new account from here."),
    ("testB_dashboard.png", "2. Contact Management Dashboard", "Main dashboard showing Add Contact form (left), Contact List (bottom), and Manage Categories panel (right). All features accessible from here."),
    ("testC_add_contact.png", "3. Add Contact Form (Filled)", "Contact form with fields for Name, Phone Number, Address, and Category dropdown. Shows form ready to submit."),
    ("testD_contact_list.png", "4. Contact List View", "Displays all saved contacts with their information. Each contact can be edited or deleted with unique ID for precision."),
    ("testE_search.png", "5. Search & Filter Contacts", "Search functionality allowing users to find contacts by name. Shows search results dynamically."),
    ("testF_categories.png", "6. Manage Categories", "Category management panel showing existing categories (가족, 친구, 기타) with Edit/Delete buttons. Can add new categories."),
    ("testG_edit_dialog.png", "7. Edit Category", "Dialog for editing category name. Users can modify existing category information."),
    ("testH_delete.png", "8. Delete Category", "Delete confirmation for removing categories. Shows current state before deletion action."),
    ("testI_logout.png", "9. Logout & Return to Login", "User successfully logged out and returned to login page. Session ended securely."),
]

def create_pdf_with_descriptions():
    """Create PDF with screenshots and descriptions"""

    print("Creating PDF with descriptions...")

    images = []

    for i, (filename, title, description) in enumerate(SCREENSHOTS, 1):
        filepath = PROJECT_DIR / filename
        if not filepath.exists():
            print(f"  WARNING: {filename} not found, skipping...")
            continue

        try:
            # Open screenshot
            img = Image.open(filepath)
            width, height = img.size

            # Create new image with space for text
            text_height = 120
            new_height = height + text_height
            new_img = Image.new('RGB', (width, new_height), color=(255, 255, 255))

            # Paste original screenshot
            new_img.paste(img, (0, 0))

            # Add text
            draw = ImageDraw.Draw(new_img)

            # Try to load font, fallback to default
            try:
                title_font = ImageFont.truetype("arial.ttf", 16)
                desc_font = ImageFont.truetype("arial.ttf", 12)
            except:
                try:
                    title_font = ImageFont.truetype("Arial.ttf", 16)
                    desc_font = ImageFont.truetype("Arial.ttf", 12)
                except:
                    title_font = ImageFont.load_default()
                    desc_font = ImageFont.load_default()

            # Draw title
            title_color = (0, 0, 0)
            desc_color = (80, 80, 80)

            draw.text((15, height + 10), title, fill=title_color, font=title_font)
            draw.text((15, height + 35), description, fill=desc_color, font=desc_font)

            # Convert to RGB for PDF
            if new_img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', new_img.size, (255, 255, 255))
                background.paste(new_img, mask=new_img.split()[-1] if new_img.mode == 'RGBA' else None)
                new_img = background

            images.append(new_img)
            print(f"  [OK] {filename} - {title}")

        except Exception as e:
            print(f"  [ERROR] {filename}: {str(e)}")

    if not images:
        print("\n[ERROR] No images to create PDF")
        return False

    try:
        # Create PDF
        pdf_path = Path.home() / "Desktop" / "Contact_App_Test_Report.pdf"
        images[0].save(
            pdf_path,
            save_all=True,
            append_images=images[1:],
            duration=200,
            loop=0
        )

        size = pdf_path.stat().st_size
        print(f"\n[SUCCESS] PDF created!")
        print(f"  File: {pdf_path.name}")
        print(f"  Size: {size:,} bytes")
        print(f"  Pages: {len(images)}")
        print(f"  Location: {Path.home() / 'Desktop'}")
        return True

    except Exception as e:
        print(f"\n[ERROR] Failed to create PDF: {str(e)}")
        return False

if __name__ == "__main__":
    success = create_pdf_with_descriptions()
    exit(0 if success else 1)
