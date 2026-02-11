import os
import time
from playwright.sync_api import sync_playwright, TimeoutError

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://inventory.teamrabbil.com/public/UploadPage", wait_until="networkidle")

    for filename in os.listdir("images"):
        file_path = os.path.join("images", filename)

        # Set input type file
        page.set_input_files("input[name='file']", file_path)
        page.wait_for_timeout(500)  # small wait to ensure file is loaded

        page.click("button[type='submit']")

        # Wait for success alert
        try:
            page.wait_for_selector(".alert.alert-success", timeout=5000)
            print(f"{filename} file uploaded")
        except TimeoutError:
            print(f"{filename} upload failed")

        time.sleep(5)

    browser.close()
