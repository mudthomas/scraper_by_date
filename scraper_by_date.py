import requests
import time


sleep_success = 0  # Seconds to sleep after successful request.
sleep_fail = 0  # Seconds to sleep after failed request.
sleep_429 = 30  # Seconds to sleep after http response "Too Many Requests".

def get_filename(year, month, day, prepend, trim):
    if prepend:
        if month < 10:
            month = f"0{month}"
        if day < 10:
            day = f"0{day}"
    if trim:
        year = f"year"[2:]
    return f"FILENAME{year}-{month}-{day}.pdf"

def get_url(filename, year, month, day, prepend, trim):
    if prepend:
        if month < 10:
            month = f"0{month}"
        if day < 10:
            day = f"0{day}"
    if trim:
        year = f"year"[2:]
    return f"http://WEBSITE.WEB/{year}-{month}-{day}/{filename}"

def scrape(start_year, end_year, verbose=False):
    for year in range(start_year, end_year+1):
        for month in range(1, 13):
            for day in range(1, 32):
                filename = get_filename(year, month, day, prepend=True, trim=False)
                url = get_url(filename, year, month, day, prepend=True, trim=False)
                myfile = requests.get(url)
                if verbose:
                    print(f"{year}-{month}-{day}: {myfile.status_code}")
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
    start_year = 2015
    end_year = 2023
    scrape(start_year, end_year, True)
