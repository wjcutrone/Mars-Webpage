# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def mars_news(browser):
    # Scrape Mars News
    # Visit the mars nasa news site
    url = "https://redplanetscience.com/"
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("div.list_text", wait_time=1)
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, "html.parser")
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("div.list_text")
        # Use the parent element to find the first ‘a’ tag and save it as ‘news_title’
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return news_title, news_p

mars_news("https://redplanetscience.com/")






