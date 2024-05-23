from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import csv

app = FastAPI()

class SearchParams(BaseModel):
    tld: Optional[str] = None
    filetype: Optional[str] = None
    intitle: Optional[str] = None
    inurl: Optional[str] = None
    intext: Optional[str] = None
    meta_keyword: str

def construct_query(tld: Optional[str], filetype: Optional[str], intitle: Optional[str], inurl: Optional[str], intext: Optional[str]) -> str:
    query = ""
    if tld:
        query += f" site:{tld}"
    if filetype:
        query += f" filetype:{filetype}"
    if intitle:
        query += f" intitle:{intitle}"
    if inurl:
        query += f" inurl:{inurl}"
    if intext:
        query += f" intext:{intext}"
    return query

def find_keyword_in_meta(url: str, keyword: str) -> bool:
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

@app.post("/search")
def search_urls(params: SearchParams):
    query = construct_query(params.tld, params.filetype, params.intitle, params.inurl, params.intext)
    meta_keyword = params.meta_keyword
    filtered_urls = []
    for url in search(query, tld="co.in", num=100, stop=100, pause=2):
        print(f"Checking URL: {url}")
        if find_keyword_in_meta(url, meta_keyword):
            filtered_urls.append(url)
    
    with open('filtered_urls.csv', 'w', newline='') as csvfile:
        fieldnames = ['URL']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for url in filtered_urls:
            writer.writerow({'URL': url})
    return {"filtered_urls": filtered_urls}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)