import requests
import csv
import time
from datetime import datetime # Imported datetime to get the current date

base_url = 'https://danbooru.donmai.us/tags.json?limit=1000&search[hide_empty]=yes&search[is_deprecated]=no&search[order]=count&search[post_count]=25..'

csv_filename = 'tags.csv'

# Get the current date and format it as Day-Month-Year (e.g., 10-3-2026)
now = datetime.now()
dynamic_header = f'HNoise7676-{now.day}-{now.month}-{now.year}'

with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Use the dynamic header variable here
    writer.writerow(['name', 'post_count', dynamic_header])

    # Loop through pages 1 to 1000
    for page in range(1, 1001):
        url = f'{base_url}&page={page}'

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            if not data:
                print(f'No more data found at page {page}. Stopping.', flush=True)
                break

            # Process and write the data
            stop_script = False
            for item in data:
                # Double-check post_count and break if it drops below 10
                if item['post_count'] < 10:
                    stop_script = True
                    break
                
                # Write data to the CSV
                writer.writerow([item['name'], item['post_count']])

            if stop_script:
                print(f'Reached tags with less than 10 posts on page {page}. Stopping.', flush=True)
                break

            file.flush()
        else:
            print(f'Failed to fetch data for page {page}. HTTP Status Code: {response.status_code}', flush=True)
            break

        print(f'Page {page} processed.', flush=True)
        # 1-second delay to be polite to the API
        time.sleep(1)

print(f'Data has been written to {csv_filename}', flush=True)
