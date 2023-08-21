import requests
from bs4 import BeautifulSoup

# URL of the main page with a list of article links
main_url = "https://elpais.com/america/"

# Send a GET request to the main URL
response = requests.get(main_url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find all the article links on the page
article_links = soup.find_all("a", class_="docs-creator")
labels = [i.get_text() for i in article_links]

# Loop through the article links and access and print the content of each article
for link in article_links:
    article_url = link["href"]  # Extract the "href" attribute to get the article URL

    # Send a GET request to the article URL
    article_response = requests.get(article_url)

    # Parse the article HTML content using BeautifulSoup
    article_soup = BeautifulSoup(article_response.content, "html.parser")

    # Find and extract the article title and content based on the HTML structure
    title = article_soup.find("h1").text.strip()
    content = article_soup.find("div", class_="article-body").text.strip()

    # Print the article title and content
    print("Title:", title)
    print("Content:", content)
    print("\n---\n")  # Separator between articles


print(labels)
