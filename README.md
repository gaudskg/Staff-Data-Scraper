# Staff Data Scraper
A Python script to scrape staff data from a school district's website.

## Overview
Staff Data Scraper is a web scraper implemented in Python, using the requests, lxml, time, random, and pandas libraries. The primary objective of this scraper is to extract staff information from a school district's staff directory webpage. The scraper is designed to handle paginated content and supports multiple schools or departments by managing a list of base URLs.

## StaffScraper Class
The StaffScraper class is the main component of the program, which takes a base URL as input during initialization. The class provides several methods to handle various tasks:

### get_html_dom(self, url)
Fetches the HTML content of a given URL and returns the parsed DOM using lxml. It retries the request up to a specified number of times if the status code is not 200.

### extract_pagination_urls(self, url)
Extracts pagination URLs from the given URL, calculates the total number of pages, and returns a list of URLs for all pages.

### get_staff_info(self, url)
Extracts staff information from the given URL by querying the DOM for relevant staff data. It extracts information such as school name, address, state, zip code, first name, last name, staff title, phone, and email.

### scrape_staff_data(self, urls)
Scrapes staff data from a list of URLs. It iterates through each URL, extracts pagination URLs, and extracts staff information from each page. The extracted staff data is then combined into a single pandas DataFrame and saved as a CSV file.


## Getting Started

To get started with the Staff Data Scraper, follow these steps:

1. **Clone the Repository**: Clone the repository to your local machine using the following command and navigate to direcotory:
     ```
     git clone https://github.com/gaudskg/Staff-Data-Scraper
     cd Staff-Data-Scraper
     ```
2. **Install Dependencies**: Navigate to the cloned directory and install the required dependencies using pip and the provided `requirements.txt` file:
    ```
    pip install -r requirements.txt
    ```

4. **Set Up the Script**: Open the `scraper.py` file and modify the `base_url` variable to the URL of the school's staff directory that you want to scrape.

5. **Run the Script**: Execute the script by running the following command:
  ```
  python staff_scraper.py
  or
  python3 staff_scraper.py
  ```

6. **Check Output**: Once the script completes execution, check the generated `staff_directory.csv` file in the same directory for the scraped staff data.

## Usage
You can customize the script further to scrape staff data from multiple schools or departments by modifying the `base_url` variable and providing a list of URLs in the `url_list`.
