import streamlit as st
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import csv
import io

def construct_query(tld, filetype, intitle, inurl, intext):
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

st.title("Google Scraper & Adsense Approval Finder")

tld = st.text_input("Enter TLD (e.g., .com, .pk, .ca):").strip()
filetype = st.text_input("Enter file type (e.g., php, asp):").strip()
intitle = st.text_input("Enter intitle keyword:").strip()
inurl = st.text_input("Enter inurl keyword:").strip()
intext = st.text_input("Enter intext keyword:").strip()
meta_keyword = st.text_input("Enter keyword to search in HTML:").strip()

if st.button("Search"):
    query = construct_query(tld, filetype, intitle, inurl, intext)
    
    filtered_urls = []
    for url in search(query, tld="co.in", num=100, stop=100, pause=2):
        st.write(f"Checking URL: {url}")
        if find_keyword_in_meta(url, meta_keyword):
            filtered_urls.append(url)

    if filtered_urls:
        st.write("Filtered URLs:")
        for url in filtered_urls:
            st.write(url)
        
        csv_buffer = io.StringIO()
        writer = csv.DictWriter(csv_buffer, fieldnames=['URL'])
        writer.writeheader()
        for url in filtered_urls:
            writer.writerow({'URL': url})

        csv_data = csv_buffer.getvalue()
        st.download_button(
            label="Download CSV File",
            data=csv_data,
            file_name='filtered_urls.csv',
            mime='text/csv'
        )
    else:
        st.write("No URLs found with the given criteria.")
