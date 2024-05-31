import json

# Read the JSON file
with open('category_data.json', 'r') as json_file:
    category_data = json.load(json_file)

# Iterate over each category
for category, data in category_data.items():
    print(f"Category: {category}")
    print(f"Total products: {data['count']}")
    print("Product details:")
    # Iterate over each product in the category
    for product in data['products']:
        # Extract and print the detail_url
        detail_url = product['detail_url']
        print(f"Detail URL: {detail_url}")
