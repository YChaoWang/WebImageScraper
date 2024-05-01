import os
import io
from PIL import Image
import urllib.request

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


# Function to resize images
def resize_images(image_urls, target_size):
    resized_images = []
    for i, url in enumerate(image_urls):
        try:
            print(f"Downloading image {i + 1}/{len(image_urls)}...")
            filename, _ = urllib.request.urlretrieve(str(image_urls[i]))
            image = Image.open(filename)

            # Convert to RGB mode if not already in RGB mode or grayscale
            if image.mode == "RGBA" or image.mode == "P":
                image = image.convert("RGB")

            resized_image = image.resize(target_size, Image.LANCZOS)
            resized_images.append(resized_image)
        except Exception as e:
            print(f"Failed to resize image {i + 1}: {e}")
    return resized_images


# Function to download images
def download_images(resized_images, folderPath):
    print("Downloading images...")
    start_time = time.time()
    for i, image in enumerate(resized_images):
        try:
            image.save(os.path.join(folderPath, f"tattoo_{i}.jpg"))
            print(f"Downloaded image {i + 1}/{len(resized_images)}")
        except Exception as e:
            print(f"Failed to download image {i}: {e}")
    end_time = time.time()
    download_time = end_time - start_time
    return download_time


# Main function
def main(num_images_to_scrape):
    # Path to chromedriver and options
    driver_path = (
        "/Users/wangyichao/webscraping/undetectedwebscraper/webdriver/chromedriver"
    )
    options = webdriver.ChromeOptions()
    options.add_argument(
        "--user-data-dir=/Users/wangyichao/Library/Applications Support/Google/Chrome/Default"
    )
    driver = uc.Chrome(options=options)
    driver.minimize_window()

    # URL to scrape
    url = "https://www.google.com/search?sca_esv=556fd070db8e09d3&sca_upv=1&sxsrf=ACQVn08OlWev9pr7WiALdw6vKOD85jQQug:1714307599624&q=tattoos&uds=AMwkrPt4t1EVCCdSUNw8MsX-M3cq5GApVN97bUhpp3qilQiAP9M4yO22OXvJZfnx8Tdmy9Su27qoo1_WCFEudKR48REEuEJI7hah7bwLoM8jEUEu1xrVGj8t9LMevdyz_XRjjjuM0BNIJdVq1qXJtzU3XjReJIFO3tzSfvt_Z2AdrEcr19B-KngneGSjEyDvwrs_cX2wRhzjDS9GPh03Ejsayq8hgz7AEJ4jhEr2zOXlr23RE1KsLGA&udm=2&prmd=isvmnbtz&sa=X&ved=2ahUKEwisnYu89eSFAxUsc_UHHbqhBZoQtKgLegQIDhAB&biw=1510&bih=857&dpr=2"  # 要爬取的google搜尋圖片網址
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait for images to load
    time.sleep(2.5)

    # Find image elements
    image_results = driver.find_elements(
        By.XPATH,
        "//img[contains(@class, 'YQ4gaf') and not(contains(@class, 'zr758c'))]",  # 自行更動 過濾掉小圖片 像是類似圖片等等
    )
    image_urls = []
    for img in image_results:
        image_urls.append(img.get_attribute("src"))

    # Specify folder path to save images
    folderPath = "/Users/wangyichao/webscraping/undetectedwebscraper/images"

    # Create 'images' directory if it doesn't exist
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

    # Resize images
    target_size = (300, 300)  # 設定圖片大小
    start_time = time.time()
    resized_images = resize_images(image_urls[:num_images_to_scrape], target_size)
    end_time = time.time()
    resize_time = end_time - start_time

    # Download images
    download_time = download_images(resized_images, folderPath)

    # Quit driver
    driver.quit()

    # Calculate total time
    total_time = resize_time + download_time

    # Output times
    print(f"Time taken for resizing: {resize_time} seconds")
    print(f"Time taken for downloading: {download_time} seconds")
    print(f"Total time taken: {total_time} seconds")


# Entry point of the script
if __name__ == "__main__":
    num_images_to_scrape = int(input("Enter the number of image URLs to scrape: "))
    main(num_images_to_scrape)
