import requests
from bs4 import BeautifulSoup
from googlesearch import search
import csv

def search_google(query, num_results=100):
    results = []
    count = 0
    for result in search(query, num=num_results, stop=num_results):
        results.append(result)
        count += 1
        if count >= num_results:
            break
    return results

def save_to_csv(data, domain_extension, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Domain'])
        domains = set()
        for result in data:
            domain = result.split('/')[2]
            if domain.endswith(domain_extension):
                url = f"https://{domain}"
                domains.add(url)
        for url in domains:
            writer.writerow([url])

def main():
    domain_extension = input("Enter the domain extension (e.g., .com, .net): ")
    num_results = int(input("Enter the number of search results you want to fetch: "))

    query = f'site:*{domain_extension}'
    search_results = search_google(query, num_results=num_results)

    output_file = f"Domains_{domain_extension}.csv"
    save_to_csv(search_results, domain_extension, output_file)
    print(f"CSV file '{output_file}' created successfully.")

if __name__ == "__main__":
    main()