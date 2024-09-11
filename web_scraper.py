import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from fpdf import FPDF
import os

def get_raw_data(website_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    page = requests.get(website_url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find_all('a', href=True)
    data = []
    for link in links:
        data.append([link['href'], link.text])
    return data

def get_product_data(website_url, product_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    page = requests.get(website_url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    product_data = []
    for item in soup.find_all('div', {'class': 'product'}):
        if product_name.lower() in item.text.lower():
            product_data.append([item.find('h2', {'class': 'product-title'}).text, item.find('p', {'class': 'product-price'}).text])
    return product_data

def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Link", "Text"])  # header row
        for row in data:
            writer.writerow(row)

def save_to_pdf(data, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Product Data", ln=True, align='C')
    pdf.ln(10)
    for row in data:
        pdf.cell(200, 10, txt=row[0], ln=True, align='L')
        pdf.cell(200, 10, txt=row[1], ln=True, align='L')
    pdf.output(filename)

def main():
    print("Web Scraper")
    print("-----------")
    print("1. Get raw data of a website")
    print("2. Get data of a specific product from a website")
    choice = input("Enter your choice (1/2): ")
    
    if choice == '1':
        website_url = input("Enter the website URL: ")
        data = get_raw_data(website_url)
        print("Data extracted successfully!")
        filename = f"raw_data_{os.urandom(4).hex()}.csv"
        save_to_csv(data, filename)
        print(f"Data saved to {filename}")
        filename = f"raw_data_{os.urandom(4).hex()}.pdf"
        save_to_pdf(data, filename)
        print(f"Data saved to {filename}")
    
    elif choice == '2':
        website_url = input("Enter the website URL: ")
        product_name = input("Enter the product name: ")
        data = get_product_data(website_url, product_name)
        print("Data extracted successfully!")
        filename = f"{product_name}_{os.urandom(4).hex()}.csv"
        save_to_csv(data, filename)
        print(f"Data saved to {filename}")
        filename = f"{product_name}_{os.urandom(4).hex()}.pdf"
        save_to_pdf(data, filename)
        print(f"Data saved to {filename}")

if __name__ == "__main__":
    main()