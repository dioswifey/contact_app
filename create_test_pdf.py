#!/usr/bin/env python3
"""
Create PDF from test screenshots
Combines testA.png through testI.png into a single PDF
"""

from PIL import Image
import os
from pathlib import Path

DESKTOP_PATH = Path.home() / "Desktop"
TESTS = ["testA", "testB", "testC", "testD", "testE", "testF", "testG", "testH", "testI"]
TEST_DESCRIPTIONS = [
    "1. Login Page - Initial load with username/password fields",
    "2. Dashboard - After successful login with contact interface",
    "3. Add Contact Form - Input form for creating new contact",
    "4. Contact List View - Display of all user contacts",
    "5. Category Management - Category organization and management",
    "6. Search & Filter - Contact search and filter functionality",
    "7. Edit Contact - Editing existing contact information",
    "8. Delete Confirmation - Confirmation dialog for contact deletion",
    "9. Logout & Return to Login - After logout back to login page"
]

def create_pdf_from_screenshots():
    """Create a PDF document from all test screenshots"""

    print("="*70)
    print("Creating PDF from test screenshots...")
    print("="*70)

    images = []
    image_paths = []

    # Load all screenshots
    for test_name in TESTS:
        filepath = DESKTOP_PATH / f"{test_name}.png"
        if filepath.exists():
            try:
                img = Image.open(filepath)
                # Convert RGBA to RGB if necessary (for PNG images)
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Create white background
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                images.append(img)
                image_paths.append(filepath)
                print(f"[OK] Loaded {test_name}.png")
            except Exception as e:
                print(f"[ERROR] Failed to load {test_name}.png: {str(e)}")
        else:
            print(f"[SKIP] {test_name}.png not found")

    if not images:
        print("\n[ERROR] No screenshots found!")
        return False

    # Create PDF
    try:
        pdf_path = DESKTOP_PATH / "Contact_App_Test_Report.pdf"
        images[0].save(
            pdf_path,
            save_all=True,
            append_images=images[1:],
            duration=200,
            loop=0
        )

        if pdf_path.exists():
            size = pdf_path.stat().st_size
            print(f"\n[OK] PDF created successfully!")
            print(f"    File: {pdf_path.name}")
            print(f"    Size: {size:,} bytes")
            print(f"    Pages: {len(images)}")
            return True
        else:
            print(f"\n[ERROR] PDF file was not created")
            return False

    except Exception as e:
        print(f"\n[ERROR] Failed to create PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = create_pdf_from_screenshots()

    print("\n" + "="*70)
    if success:
        print("Test Report PDF is ready on your Desktop!")
        print("File: Contact_App_Test_Report.pdf")
    else:
        print("Failed to create PDF")
    print("="*70)
