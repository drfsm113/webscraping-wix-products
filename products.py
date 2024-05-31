import time
import json
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

# Function to scroll to the bottom of the page
def scroll_to_bottom(driver):
    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait for a short interval to let content load
    time.sleep(2)

# Dictionary containing URLs and their corresponding categories
urls = {
    "https://www.preciousthingsdecor.com/fiber-sculptures-and-murals": "fiber_sculptures_and_murals",
    "https://www.preciousthingsdecor.com/god-idols-1": "god_idols",
    "https://www.preciousthingsdecor.com/tanjore-paintings-1": "tanjore_paintings",
    "https://www.preciousthingsdecor.com/brass": "brass",
    "https://www.preciousthingsdecor.com/painted-wall-plates": "painted_wall_plates",
    "https://www.preciousthingsdecor.com/cheriyal-masks-and-sculptures": "cheriyal_masks_and_sculptures"
}

# Dictionary to store product data and count category-wise
category_data = {}

# Set to store unique product URLs
unique_urls = set()

# Setting up Chrome WebDriver using ChromeDriverManager
options = Options()
options.add_argument('--headless')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Iterate over each URL
for url, category in urls.items():
    # Create a list to store product data for this category
    products_data = []
    
    # Loop through pages
    page_num = 1
    while True:
        page_url = f"{url}?page={page_num}"
        # print(f"Scraping page {page_num} of category {category}")
        driver.get(page_url)
        # Wait for a short interval to let content load
        time.sleep(2)

        # Scroll down to load more content until no more products are loaded
        prev_height = 0
        while True:
            # Scroll to the bottom of the page
            scroll_to_bottom(driver)
            # Calculate new scroll height and compare with the previous scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == prev_height:
                break  # No new content loaded, exit loop
            prev_height = new_height

        # Parse the HTML content after all products are loaded
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all product list items
        products = soup.find_all('li', {'data-hook': 'product-list-grid-item'})

        # Iterate through each product and extract the details
        for product in products:
            # Extract the product detail page URL
            detail_link_tag = product.find('a', {'data-hook': 'product-item-container'})
            product_detail_url = detail_link_tag['href'] if detail_link_tag else 'N/A'
            print(f"Product detail URL: {product_detail_url}")
            
            # Check if this product URL has already been processed
            if product_detail_url in unique_urls:
                print("Skipping duplicate product URL")
                continue  # Skip if already processed
            
            # Add the product URL to the set of unique URLs
            unique_urls.add(product_detail_url)

            # Extract the product name
            name_tag = product.find('h3', {'data-hook': 'product-item-name'})
            product_name = name_tag.text.strip() if name_tag else 'N/A'
            # print(f"Product name: {product_name}")

            # Extract the product price
            price_tag = product.find('span', {'data-hook': 'product-item-price-to-pay'})
            product_price = price_tag.text.strip() if price_tag else 'N/A'
            # print(f"Product price: {product_price}")

            # Extract the product image URL
            img_tag = product.find('img')
            product_image_url = img_tag['src'] if img_tag else 'N/A'
            # print(f"Product image URL: {product_image_url}")

            # Add the product data to the list
            products_data.append({
                "name": product_name,
                "price": product_price,
                "image_url": product_image_url,
                "detail_url": product_detail_url
            })

        # Check for the next page link
        next_page_link = soup.find('link', {'rel': 'next'})
        if next_page_link:
            page_num += 1  # Move to the next page
        else:
            break  # No more pages left, exit loop

    # Add the product data for this category to the dictionary
    category_data[category] = {
        "count": len(products_data),
        "products": products_data
    }

# Close the WebDriver
driver.quit()

# Print category-wise product counts and data
print("Category-wise product counts and data:")
for category, data in category_data.items():
    print(f"{category}: {data['count']} products")
    print("Product data:")
    for product in data['products']:
        print(product)
        print()
    print()

# Save all the data to a JSON file
with open('category_data.json', 'w') as json_file:
    json.dump(category_data, json_file, indent=4)

print("Data saved to category_data.json successfully.")