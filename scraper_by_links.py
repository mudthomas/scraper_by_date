from bs4 import BeautifulSoup, SoupStrainer
import requests
import time

sleep_success = 0  # Seconds to sleep after successful request.
sleep_fail = 0  # Seconds to sleep after failed request.
sleep_429 = 30  # Seconds to sleep after http response "Too Many Requests".

def scraper(url, filetypes):
    page = requests.get(url)
    data = page.text
    soup = BeautifulSoup(data)
    for link in soup.find_all('a'):
        print(link.get('href'))
        filetype = f"{link.get('href')}"[-3:].lower()  # Assumes filetype is length is 3
        if filetype in filetypes:
            myfile = requests.get(link.get('href').replace("%20", " "))  # Fixes space characters in links
            filename = link.get('href').split("/")[-1].replace("%20", " ")  # Fixes space characters in files
            if myfile.status_code < 400:
                save_file = open(f'scraped_files/{filename}', 'wb').write(myfile.content)
                time.sleep(sleep_success)
            elif myfile.status_code == 429:
                day -= 1
                print(f"Got a 429 response for {filename}.")
                print(f"Sleeping for {sleep_429} seconds.")
                time.sleep(sleep_429)
            else:
                time.sleep(sleep_fail)

if __name__ == "__main__":
    urls = ["http://www.DOMAIN.WEB/WEBSITE1.html",
            "http://www.DOMAIN.WEB/WEBSITE2.html"]  # Websites to scrape
    filetypes = ["pdf"]  # Filenames to scrape
    for i in range(len(filetypes)):
        filetypes[i] = filetypes[i].lower()  # This makes sure filetypes are lower case
    for url in urls:
        scraper(url, filetypes)  # Calls the scraper
