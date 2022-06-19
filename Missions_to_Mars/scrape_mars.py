from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def scrape_info():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # ***Scrape latest News Headline and Blurb***
    # Visit desired URL
    url = "https://redplanetscience.com/"
    browser.visit(url)

    # Use Beautiful Soup to find the latest headline and blurb
    html = browser.html
    soup = bs(html, 'html.parser')

    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    #print(news_title)
    #print(news_p)

    # Close the browser after scraping
    #browser.quit()

    #----------------------------------------------------------------------
    #----------------------------------------------------------------------
    
    # ***Scrape the latest Mars Image***
    # Visit the desired url
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Use Beautiful Soup to find the latest Mars Image
    html = browser.html
    soup = bs(html, 'html.parser')

    featured_img = soup.find('img', class_="headerimage fade-in")

    # Print out the URL for the image
    featured_img_url = 'https://spaceimages-mars.com/'+ str(featured_img['src'])

    # Close the browser after scraping
    #browser.quit()

    #----------------------------------------------------------------------
    #----------------------------------------------------------------------

    # ***Scrape for tabular data***
    # Read all tabular data from the site using .read_html
    url = 'https://galaxyfacts-mars.com'
    tables = pd.read_html(url)

    # Convert the raw tabular data into Pandas dataframes
    df_mars = tables[0]
    
    # Convert the Pandas df to html code
    html_mars_table = df_mars.to_html()

    #----------------------------------------------------------------------
    #----------------------------------------------------------------------

    # ***Scrape for high res images of Mars***
    # Visit the desired url
    url = 'https://marshemispheres.com/'
    browser.visit(url)


    # Use a loop to click on the 4 links and scrape info from each

    hemisphere_image_urls = []
    hemisphere_images = []

    for page in range(4):
        
        browser.links.find_by_partial_text('Hemisphere')[page].click()
        html = browser.html
        soup = bs(html, 'html.parser')
        
        tag = soup.find('img', class_="wide-image")
        image_url = tag['src']
        image_title = soup.find('h2', class_='title')
        
        dict_entry = {"title: "+str(image_title.text):"img_url (click or copy) : "+"https://marshemispheres.com/"+str(image_url) + " "}
        
        hemisphere_image_urls.append(dict_entry)
        #hemisphere_images.append(tag)
        
        browser.back()

    browser.quit()

    mars_data = {
        "Headline": news_title,
        "Blurb": news_p,
        "Current Mars Image": featured_img_url,
        "Mars Data": html_mars_table,
        "hemisphere_images": hemisphere_image_urls
    }

    return(mars_data)

    
    