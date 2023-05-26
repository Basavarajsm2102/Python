import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape product listing page
def scrape_product_listing(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.find_all('div', {'data-component-type': 's-search-result'})

    data = []
    for product in products:
        product_data = {}
        try:
            product_url = 'https://www.amazon.in' + product.find('a', {'class': 'a-link-normal s-no-outline'})['href']
            product_name = product.find('a', {'class': 'a-link-normal s-no-outline'}).text.strip()
            product_price = product.find('span', {'class': 'a-offscreen'}).text.strip()
            product_rating = product.find('span', {'class': 'a-icon-alt'}).text.strip().split()[0]
            product_reviews = product.find('span', {'class': 'a-size-base'}).text.strip()

            product_data['Product URL'] = product_url
            product_data['Product Name'] = product_name
            product_data['Product Price'] = product_price
            product_data['Rating'] = product_rating
            product_data['Number of Reviews'] = product_reviews

            data.append(product_data)
        except:
            continue

    return data

# Function to scrape product details page
def scrape_product_details(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        description = soup.find('div', {'id': 'feature-bullets'}).text.strip()
    except:
        description = ''
    try:
        asin = soup.find('th', string='ASIN').find_next_sibling('td').text.strip()
    except:
        asin = ''
    try:
        product_description = soup.find('div', {'id': 'productDescription'}).text.strip()
    except:
        product_description = ''
    try:
        manufacturer = soup.find('a', {'id': 'bylineInfo'}).text.strip()
    except:
        manufacturer = ''

    product_data = {
        'Description': description,
        'ASIN': asin,
        'Product Description': product_description,
        'Manufacturer': manufacturer
    }

    return product_data

# Main function to scrape data
def scrape_data():
    base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{}'
    num_pages = 20  # Number of pages to scrape
    data = []

    for page in range(1, num_pages + 1):
        url = base_url.format(page)
        product_listings = scrape_product_listing(url)

        for product in product_listings:
            product_url = product['Product URL']
            product_details = scrape_product_details(product_url)
            product.update(product_details)
            data.append(product)

    # Export data to CSV
    keys = data[0].keys()
    csv_filename = 'amazon_products.csv'  # Specify the path for the CSV file

    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    print(f"Data scraped successfully. The CSV file '{csv_filename}' has been created.")

# Scrape data and export to CSV
scrape_data()