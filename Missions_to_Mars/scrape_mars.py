from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

#Setup splinter
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

#Create a dictionary to store all results 
def scrape():
    browser = init_browser()
    # news_title, news_p = scrape_1(browser)
    # news_title, news_p = mars_news(browser)

    data = {
        'p_data':scrape_1(browser),
        'f_image': scrape_2(browser),
        'table_data': scrape_3(browser),
        'hemispheres': scrape_4(browser)
    }
    browser.quit()
    return data

# Get most recent Mars story
def scrape_1(browser):
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    #Collect the latest news title and paragraph test from Nasa's website
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    element = soup.select_one('div.list_text')
    news_title = element.find('div', class_='content_title').get_text()
    # news_title = title_pod.get_text()
    news_p = element.find('div', class_='article_teaser_body').get_text()
    return {
        'title':news_title,
        'paragraph': news_p
    }
    

#Get the featured Mars image
def scrape_2(browser):
    url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"
    browser.visit(url+'index.html')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Find and click on the Full Image button
    full_image = browser.find_by_css("button.btn.btn-outline-light")
    full_image.click()
    relative_url = soup.select('a', class_='showing fancybox-thumbs')[2].get('href')
    final_url = url + relative_url
    return final_url

#Get the Mars facts table
def scrape_3(browser):
    url = "https://space-facts.com/mars/"
    browser.visit(url)
    mars_facts=pd.read_html(browser.html)[0]
    mars_facts = mars_facts.rename(columns={0:'Description', 1:'Data'})
    mars_table = mars_facts.to_html(index=False)
    return mars_table

#Get the Mars Hemispheres
def scrape_4(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='item')
    results = []
    for item in items:
        title = item.find('h3').text
        relative = item.find('a').get('href')
        img_url = f"https://astrogeology.usgs.gov{relative}"
        browser.visit(img_url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_url = soup.find('div', class_='downloads').find('a').get('href')
        results.append({
            'title':title,
            'image_url':img_url
        })
    return results

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape())