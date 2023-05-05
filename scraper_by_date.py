import requests
import time

start_year = 1979
end_year = 2023
sleep_time = 5

def get_filename(year, month, day, prepend, trim):
    if prepend:
        if month<10:
            month = f"0{month}"
        if day<10:
            day = f"0{day}"
    if trim:
        year = f"year"[2:]
    return f"FILENAME{year}-{month}-{day}.pdf"

def get_url(filename, year, month, day, prepend, trim):
    if prepend:
        if month<10:
            month = f"0{month}"
        if day<10:
            day = f"0{day}"
    if trim:
        year = f"year"[2:]
    return f"http://WEBSITE.WEB/{year}-{month}-{day}/{filename}"

bad_request = 0
good_request = 0
year = start_year
while year <= end_year:
    for month in range(1,13):
        for day in range(1, 32):
            filename = get_filename(year, month, day, prepend=True, trim=False)
            url = get_url(filename, year, month, day, prepend=True, trim=False)
            myfile = requests.get(url)
            if myfile.status_code != 404:
                save_file = open(f'scraped_files/{filename}', 'wb').write(myfile.content)
                good_request += 1
                time.sleep(sleep_time)
            else:
                bad_request += 1
    year += 1

print("Done")
print(f"Good requests\t: {good_request}")
print(f"Bad requests\t: {bad_request}")
