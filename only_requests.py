# Script where only the requests for the descriptions are made (in case that
# there have been undesired errors in the request of descriptions). It is just
# a copy of the end of the booking_scraping.py script

import time
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

###############################################################################

# PARAMETERS THAT CAN BE MODIFIED

# Folder path for URL data (which we will use to access the complete descriptions)
url_data_path = "files/accommodation_urls"
# Folder path for saving description data
description_data_path = "files/accommodation_descriptions/"

# Modify the header for requests
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

###############################################################################

# After exiting the loop where we extract all of the general accommodation data,
# we can make requests to extract the descriptions of each accommodation that has
# been found

# Step 1: import all URL .csv into dataframes in a loop
dataframes = []
# os.listdir(folder_path) lists all files in the specified folder
for file in os.listdir(url_data_path):
    if file.endswith(".csv"):
        file_path = os.path.join(url_data_path, file)
        df_url = pd.read_csv(file_path)
        dataframes.append(df_url)

# Step 2: concatenate all dataframes along the rows (indexes, axis = 0)
df_url_combined = pd.concat(dataframes, axis=0, ignore_index=True)

# Step 3: keep only unique values among a subset of columns (so that the extraction
# of descriptions is more efficient)
df_url_unique = df_url_combined.drop_duplicates(subset=['hotel_name']).reset_index(drop = True)
print(f'Reading the descriptions for {len(df_url_unique)} accommodations.')

# Initialize variable to measure time
start_time = time.time()

# Step 4: extract the accommodation descriptions using requests and BeautifulSoup
## Create a copy of the URL unique data frame where we will store the descriptions
description_df = df_url_unique.copy()
## Create a column with empty strings where we will store the descriptions
description_df['description'] = ""
## Iterate through all rows: len(description_df)
for i in range(len(description_df)):
    try:
        # Fetch the HTML content
        response = requests.get(description_df['url'][i], headers=headers)
        response.raise_for_status()  # Raise an error for failed requests
        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        # We locate and save the description of the accommodation
        description_tag = soup.find('p', class_='a53cbfa6de b3efd73f69', attrs={'data-testid': 'property-description'})
        # Check if description exists, and if so update the dataframe. 
        # NOTE (ChatGPT): Performance: .at is faster for scalar operations (like 
        # setting a single cell value) compared to .loc.
        if description_tag:
            description_df.at[i, 'description'] = description_tag.get_text(strip = True)
        else:  # If description tag does not exist
            description_df.at[i, 'description'] = "Description not found"
    except Exception as e:
        # Log the error and continue
        description_df.at[i, 'description'] = f"Error: {str(e)}"
    
    # Save the dataframe every 100 rows
    if (i + 1) % 100 == 0 or i == len(description_df) - 1:  # Save on every 100 rows or at the last row
        name_description_data = os.path.join(description_data_path, f'descriptions_{i + 1}.csv')
        description_df.to_csv(name_description_data, index=False)
        print(f"Progress saved at row {i + 1} in file: {name_description_data}")

        # Calculate time remaining
        elapsed_time = time.time() - start_time
        elapsed_minutes = elapsed_time / 60  # Convert elapsed time to minutes
        rows_processed = i + 1
        avg_time_per_row = elapsed_time / rows_processed
        remaining_rows = len(description_df) - rows_processed
        estimated_time_remaining = avg_time_per_row * remaining_rows
        # Convert estimated time remaining to hours, minutes, and seconds
        hours, rem = divmod(estimated_time_remaining, 3600)
        minutes, seconds = divmod(rem, 60)
        print(f"Time elapsed: {elapsed_minutes:.2f} minutes | Estimated time remaining: {int(hours)}h {int(minutes)}m {int(seconds)}s")