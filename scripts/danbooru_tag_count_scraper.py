import requests
import csv
import time

# Base URL without the page parameter
base_url = 'https://danbooru.donmai.us/tags.json?limit=1000&search[hide_empty]=yes&search[is_deprecated]=no&search[order]=count'

# Specify the filename for the CSV
csv_filename = 'tags.csv'

# Open a file to write
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(['name', 'post_count'])

    # Loop through pages 1 to 1000
    for page in range(1, 1001):
        # Update the URL with the current page
        url = f'{base_url}&page={page}'
        
        # Fetch the JSON data
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            
            # Break the loop if the data is empty (no more tags to fetch)
            if not data:
                print(f'No more data found at page {page}. Stopping.', flush=True)
                break
            
            # Write the data
            for item in data:
                writer.writerow([item['name'],item['post_count']])
            
            # Explicitly flush the data to the file
            file.flush()
        else:
            print(f'Failed to fetch data for page {page}. HTTP Status Code: {response.status_code}', flush=True)
            break

        print(f'Page {page} processed.', flush=True)
        # Sleep for 1 second so we don't DDOS Danbooru too much
        time.sleep(1)

print(f'Data has been written to {csv_filename}', flush=True)
