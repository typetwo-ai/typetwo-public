import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import io
import img2pdf
import os

# Set up Chrome options
options = Options()
# options.add_argument("--headless")  # Headless mode makes this more efficient
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-extensions")

# Create driver
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=options
)


def capture_webpage_as_pdf(driver, output_pdf_path="webpage.pdf"):
    try:
        # driver.execute_script(f'window.scrollTo(0, 10);')
        time.sleep(3)

        # Get page dimensions
        total_width = driver.execute_script("return document.body.scrollWidth")
        total_height = driver.execute_script("return document.body.scrollHeight")

        # Set window size to the content dimensions
        driver.set_window_size(total_width, total_height)
        time.sleep(1)  # Brief pause to let the browser adjust

        # Take full screenshot
        screenshot = driver.get_screenshot_as_png()

        # Convert to image
        img = Image.open(io.BytesIO(screenshot))

        # Save temporary image
        temp_image_path = "temp_screenshot.png"
        img.save(temp_image_path)

        # Convert to PDF
        with open(output_pdf_path, "wb") as f:
            f.write(img2pdf.convert(temp_image_path))

        # Clean up
        # os.remove(temp_image_path)

        print(f"PDF saved to {output_pdf_path}")
        return output_pdf_path

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        return None

    finally:
        driver.quit()

# def capture_webpage_as_pdf(driver, url, output_pdf_path="webpage.pdf"):
#     try:
#         # Navigate to the URL
#         driver.get(url)
#         time.sleep(2)  # Allow page to fully load
#
#         # Get page dimensions
#         page_width = driver.execute_script('return document.documentElement.scrollWidth')
#         page_height = driver.execute_script('return document.documentElement.scrollHeight')
#
#         # Set window size to match page width
#         driver.set_window_size(page_width, 1080)
#         time.sleep(0.5)
#
#         # Create a new image with the full page dimensions
#         stitched_image = Image.new('RGB', (page_width, page_height))
#
#         viewport_height = driver.execute_script('return window.innerHeight')
#         vertical_offset = 0
#
#         for offset in range(0, page_height + viewport_height - 1, viewport_height):
#             driver.execute_script(f'window.scrollTo(0, {vertical_offset});')
#             time.sleep(0.5)
#
#             screenshot = driver.get_screenshot_as_png()
#             img = Image.open(io.BytesIO(screenshot))
#
#             remaining_height = min(viewport_height, page_height - vertical_offset)
#
#             img = img.crop((0, viewport_height - remaining_height, page_width, viewport_height))
#
#             stitched_image.paste(img, (0, vertical_offset))
#             print(f"Captured section at offset {vertical_offset}/{page_height}")
#
#             vertical_offset += viewport_height - 100
#
#         # Save the stitched image as temporary file
#         temp_image_path = "temp_screenshot.png"
#         stitched_image.save(temp_image_path)
#
#         # Convert the image to PDF
#         with open(output_pdf_path, "wb") as f:
#             f.write(img2pdf.convert(temp_image_path))
#
#         # Clean up the temporary file
#         if os.path.exists(temp_image_path):
#             os.remove(temp_image_path)
#
#         print(f"PDF saved to {output_pdf_path}")
#         return output_pdf_path
#
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         import traceback
#         traceback.print_exc()
#         return None
#
#     finally:
#         # Ensure driver is closed properly
#         driver.quit()


# Example usage
url = "https://cbkone.com/"
output_path = "website_screenshot.pdf"
driver.get(url)
capture_webpage_as_pdf(driver, output_path)