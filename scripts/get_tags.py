# /// script
# dependencies = [
#    "requests",
# ]
# ///

import csv
from datetime import datetime
import time
import requests

base_url = 'https://danbooru.donmai.us/tags.json?limit=1000&search[hide_empty]=yes&search[is_deprecated]=no&search[order]=count'

csv_filename = 'tags.csv'

now = datetime.now()
dynamic_header = f'HNoise7676-{now.day}-{now.month}-{now.year}'
headers = {'User-Agent': 'MyTagDownloader/1.0 (Language=Python/requests)'}

with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Dynamic date placed in top header row only
    writer.writerow(['name', 'post_count', dynamic_header])

    for page in range(1, 1001):
        url = f'{base_url}&page={page}'

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()

            if not data:
                print(f'No more data found at page {page}. Stopping.', flush=True)
                break

            stop_script = False
            for item in data:
                if item['post_count'] < 10:
                    stop_script = True
                    break

                # Third column left empty for data rows
                writer.writerow([item['name'], item['post_count'], ''])

            if stop_script:
                print(
                    f'Reached tags with less than 10 posts on page {page}. Stopping.',
                    flush=True,
                )
                break

            file.flush()
        else:
            print(
                f'Failed to fetch data for page {page}. HTTP Status Code:'
                f' {response.status_code}',
                flush=True,
            )
            break

        print(f'Page {page} processed.', flush=True)
        time.sleep(1)

    manual_tags = [['succubus', 319007, ''], ['incubus', 1682026, '']]

    print('Appending manual tags...', flush=True)
    for manual_item in manual_tags:
        writer.writerow(manual_item)

print(f'Data has been written to {csv_filename}', flush=True)