import requests
from lxml import etree
import time
import random
import pandas as pd

class StaffScraper:
    def __init__(self, base_url):
        """
        Initialize the StaffScraper class with the base URL for the school's staff directory.
        """
        self.base_url = base_url
        self.max_retries = 5

    def get_html_dom(self, url):
        """
        Fetches a page using requests and lxml, retries up to 'max_retries' times if the status code is not 200,
        and returns the DOM.
        """
        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    dom = etree.HTML(response.content)
                    print(f"{url} fetched successfully....!")
                    return dom
                else:
                    print(f"Received status code {response.status_code} for URL: {url}. Retrying...")
            except Exception as e:
                print(f"Error occurred while fetching URL: {url}. Error: {e}")
                delay = random.uniform(1, 5)
                print(f"Retrying in {delay:.2f} seconds...")
                time.sleep(delay)
        return None

    def extract_pagination_urls(self, url):
        """
        Extract pagination URLs from the given URL.
        """
        pagination_urls = []
        try:
            dom = self.get_html_dom(url)
            if dom is not None:
                page_node = dom.xpath("//li[contains(@class,'item last')]//a/@href")[0]
                total_pages = int(page_node.split('&page=')[-1]) if (page_node and '&page=' in page_node) else None
                if total_pages is not None:
                    for page_num in range(0, total_pages + 1):
                        pagination_urls.append(f"{url}?s=&page={page_num}")
                else:
                    pagination_urls.append(url)
            else:
                raise Exception(f"Failed to fetch page: {url}")
        except Exception as e:
            print(f"An error occurred while fetching pagination URL: {url}. Error: {e}")
        return pagination_urls

    def get_staff_info(self, url):
        """
        Extract staff information from the given URL.
        """
        staff_data = []
        dom = self.get_html_dom(url)
        if dom is not None:
            staff_nodes = dom.xpath("//div[contains(@class,'node staff teaser')]")
            for staff in staff_nodes:
                try:
                    title_node = dom.xpath('//title')
                    title = title_node[0].text.split("|")[-1].strip() if title_node and title_node[0].text else None
                    address_node = dom.xpath("//p[contains(@class,'address')]")
                    address_node = dom.xpath("//a[contains(@class,'address-direction')]/@href")[0]
                    address = address_node.strip().split("daddr=")[-1].replace("++", ", ").replace("+"," ") if address_node else None 
                    state_zip = address.split()[-2:] if address else None
                    state = state_zip[0]
                    zip_code = state_zip[1]
                    first_name, last_name = staff.xpath(".//h2[@class='title']/text()")[0].split(", ")
                    staff_title = staff.xpath(".//div[@class='field job-title']/text()")[0].strip()
                    phone = staff.xpath(".//div[@class='field phone']//a/text()")[0]
                    email = staff.xpath(".//div[@class='field email']//a/text()")[0]
                    staff_data.append({
                        'School Name': title,
                        'Address': address,
                        'State': state,
                        'Zip': zip_code,
                        'First Name': first_name,
                        'Last Name': last_name,
                        'Staff Title': staff_title,
                        'Phone': phone,
                        'Email': email
                    })
                    print({
                        'School Name': title,
                        'Address': address,
                        'State': state,
                        'Zip': zip_code,
                        'First Name': first_name,
                        'Last Name': last_name,
                        'Staff Title': staff_title,
                        'Phone': phone,
                        'Email': email
                    })
                except Exception as e:
                    print("Error:", e)
                    staff_data.append({'School Name': None, 'Address': None, 'State': None, 'Zip': None,'First Name': None, 'Last Name': None, 'Staff Title': None, 'Phone': None, 'Email': None})
        return staff_data

    def scrape_staff_data(self, urls):
        """
        Scrape staff data from the given list of URLs.
        """
        staff_dataframes = []
        for url in urls:
            print(f"Scraping {url}")
            pagination_urls = self.extract_pagination_urls(url)
            for pagination_url in pagination_urls:
                staff_data = self.get_staff_info(pagination_url)
                staff_df = pd.DataFrame(staff_data)
                staff_dataframes.append(staff_df)
        master_df = pd.concat(staff_dataframes)
        master_df = master_df.dropna()
#         print(master_df)
        master_df.to_csv("staff_directory.csv", index=False)

if __name__ == "__main__":
    base_url = "https://isd110.org/our-schools/laketown-elementary/staff-directory"
    # Instead of one base url you can pass multiple school urls in the url_list
    url_list = [base_url]
    scraper = StaffScraper(base_url)
    scraper.scrape_staff_data(url_list)
