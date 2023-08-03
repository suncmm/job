import requests
from bs4 import BeautifulSoup

url = "https://www.liepin.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
print(soup)

# Code to scrape job information from the website goes here

# Example code to print the scraped information
for job in job_list:
    print(job.title)
    print(job.company)
    print(job.location)
    print(job.salary)
    print(job.description)
    print()

