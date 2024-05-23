import requests
from bs4 import BeautifulSoup
from googlesearch import search
import csv
from fastapi import FastAPI, HTTPException, Form, UploadFile, File
from fastapi.responses import FileResponse
import os

app = FastAPI()

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
    file_exists = os.path.isfile(filename)
    
    with open(filename, mode='a' if file_exists else 'w', newline='') as file:
        writer = csv.writer(file)
        
        if not file_exists:
            writer.writerow(['URL'])
        
        existing_urls = set()
        
        if file_exists:
            with open(filename, mode='r') as existing_file:
                reader = csv.reader(existing_file)
                next(reader)  # Skip header
                for row in reader:
                    existing_urls.add(row[0])
        
        new_urls = set(data)
        urls_to_write = new_urls - existing_urls
        
        for url in urls_to_write:
            writer.writerow([url])

def find_keyword_in_meta(url, keyword):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            meta_tag_1 = soup.find('meta', {'name': 'google-adsense-account'})
            if meta_tag_1 and keyword.lower() in meta_tag_1.get('content', '').lower():
                return True

            meta_tag_2 = soup.find('meta', {'name': 'google-adsense-platform-account'})
            if meta_tag_2 and keyword.lower() in meta_tag_2.get('content', '').lower():
                return True

            script_tags = soup.find_all('script')
            for script_tag in script_tags:
                if keyword.lower() in script_tag.get('src', '').lower():
                    return True
                
            ins_tags = soup.find_all('ins')
            for ins_tag in ins_tags:
                if keyword.lower() in ins_tag.get('data-ad-client', '').lower():
                    return True

        return False
    except Exception as e:
        print(f"Error occurred: {e}")
        return False

@app.post("/scrapURLsByOperators/")
async def search_and_create_csv(
    domain_extension: str = Form(...),
    file_type: str = Form(...),
    intitle: str = Form(""),
    inurl: str = Form(""),
    intext: str = Form(""),
    num_results: int = Form(100)
):
    query = f'site:*{domain_extension} filetype:{file_type}'

    if intitle:
        query += f' intitle:{intitle}'
    if inurl:
        query += f' inurl:{inurl}'
    if intext:
        query += f' intext:{intext}'

    try:
        search_results = search_google(query, num_results=num_results)
        output_file = "URLsByOperators.csv"
        save_to_csv(search_results, output_file)

        if not os.path.exists(output_file):
            raise HTTPException(status_code=500, detail="File creation failed.")

        return FileResponse(output_file, media_type='text/csv', filename=output_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/filterOut/")
async def search_keyword_in_meta(file: UploadFile = File(...), keyword: str = "adsbygoogle"):
    try:
        input_file = "URLsByOperators.csv"
        output_file = "found_urls.csv"

        with open(input_file, "wb") as f:
            f.write(file.file.read())

        with open(input_file, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader, None)
            found_urls = []

            for row in csvreader:
                url = row[0]
                if find_keyword_in_meta(url, keyword):
                    found_urls.append(url)

        with open(output_file, 'w', newline='') as outfile:
            csvwriter = csv.writer(outfile)
            csvwriter.writerow(['URL'])
            for url in found_urls:
                csvwriter.writerow([url])

        return FileResponse(output_file, media_type='text/csv', filename=output_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
