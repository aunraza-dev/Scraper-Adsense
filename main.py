# import requests
# from bs4 import BeautifulSoup
# import csv

# def find_keyword_in_meta(url, keyword):
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, 'html.parser')
#             meta_tag = soup.find('meta', {'name': 'google-adsense-account'})
#             if meta_tag and keyword.lower() in meta_tag.get('content', '').lower():
#                 return True
#         return False
#     except Exception as e:
#         print(f"Error occurred: {e}")
#         return False

# def main():
#     url = input("Enter the URL of the webpage: ")
#     keyword = "ca-pub"  # Keyword to search for in the meta tag content
#     if find_keyword_in_meta(url, keyword):
#         with open('found_urls.csv', 'a', newline='') as csvfile:
#             csvwriter = csv.writer(csvfile)
#             csvwriter.writerow([url])
#         print(f"Keyword '{keyword}' found in the meta tag of '{url}'. URL added to 'found_urls.csv'")
#     else:
#         print(f"Keyword '{keyword}' not found in the meta tag of '{url}'.")

# if __name__ == "__main__":
#     main()


# import requests
# from bs4 import BeautifulSoup
# import csv

# def find_keyword_in_meta(url, keyword):
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, 'html.parser')
            
#             meta_tag_1 = soup.find('meta', {'name': 'google-adsense-account'})
#             if meta_tag_1 and keyword.lower() in meta_tag_1.get('content', '').lower():
#                 return True

#             meta_tag_2 = soup.find('meta', {'name': 'google-adsense-platform-account'})
#             if meta_tag_2 and keyword.lower() in meta_tag_2.get('content', '').lower():
#                 return True
        
#         return False
#     except Exception as e:
#         print(f"Error occurred: {e}")
#         return False

# def main():
#     url = input("Enter the URL of the webpage: ")
#     keyword = "ca-pub"
#     if find_keyword_in_meta(url, keyword):
#         with open('found_urls.csv', 'a', newline='') as csvfile:
#             csvwriter = csv.writer(csvfile)
#             csvwriter.writerow([url])
#         print(f"Keyword '{keyword}' found in the meta tag of '{url}'. URL added to 'found_urls.csv'")
#     else:
#         print(f"Keyword '{keyword}' not found in the meta tag of '{url}'.")

# if __name__ == "__main__":
#     main()




import requests
from bs4 import BeautifulSoup
import csv

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

def main():
    url = input("Enter the URL of the webpage: ")
    keyword = "adsbygoogle"
    if find_keyword_in_meta(url, keyword):
        with open('found_urls.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([url])
        print(f"Keyword '{keyword}' found in '{url}'. URL added to 'found_urls.csv'")
    else:
        print(f"Keyword '{keyword}' not found in '{url}'.")

if __name__ == "__main__":
    main()