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

def save_to_csv(data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['URL'])
        urls = set(data)
        for url in urls:
            writer.writerow([url])

def main():
    domain_extension = input("Enter the domain extension (e.g., .com, .net): ")
    file_type = input("Enter the file type (e.g., php): ")
    intitle = input("Enter the intitle keyword (leave blank if not needed): ")
    inurl = input("Enter the inurl keyword (leave blank if not needed): ")
    intext = input("Enter the intext keyword (leave blank if not needed): ")
    num_results = int(input("Enter the number of search results you want to fetch: "))

    query = f'site:*{domain_extension} filetype:{file_type}'

    if intitle:
        query += f' intitle:{intitle}'
    if inurl:
        query += f' inurl:{inurl}'
    if intext:
        query += f' intext:{intext}'

    search_results = search_google(query, num_results=num_results)

    # output_file = f"URLs_{domain_extension}_filetype_{file_type}.csv"
    output_file = f"URLsByOperators.csv"
    save_to_csv(search_results, output_file)
    print(f"CSV file '{output_file}' created successfully.")

if __name__ == "__main__":
    main()