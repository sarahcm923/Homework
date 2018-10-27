# Dependencies
from bs4 import BeautifulSoup as BS
import requests
import pymongo

def scrape():
    # ### NASA MARS
        # NASA link: https://mars.nasa.gov/news/
    mars_news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    mars_news_response = requests.get(mars_news_url)
    mars_news_soup = BS(mars_news_response.text, 'lxml')

    # Retrieve the parent divs for all articles
    results = mars_news_soup.find('div', class_='slide')
    print(results)

    # Loop through results to retrieve article title, header, and timestamp of article
    mars_news_title = results.find('div', class_='content_title').text
    mars_news_p = results.find('div', class_='rollover_description_inner').text
    
    # ### JPL Mars Images
    from splinter import Browser
    # https://splinter.readthedocs.io/en/latest/drivers/chrome.html
    #get_ipython().system('which chromedriver')
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # JPL link: https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)

    html = browser.html
    jpl_soup = BS(html, 'html.parser')

    # Retrieve the parent divs for all articles
    results = jpl_soup.find('footer')

    # Loop through results to retrieve article title, header, and timestamp of article
    a = results.find('a')
    featured_image_url = results.a['data-fancybox-href']
    feature_url = ('https://www.jpl.nasa.gov' + featured_image_url)

    # ### Mars Weather
    # Twitter URL: https://twitter.com/marswxreport?lang=en
    twt_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twt_url)

    html = browser.html
    twt_soup = BS(html, 'html.parser')

    # Retrieve the parent divs for all articles
    twt_result = twt_soup.find('div', class_='js-tweet-text-container')
    mars_weather = twt_result.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    # ### Mars Facts
    # Facts URL: http://space-facts.com/mars/
    fact_url = 'http://space-facts.com/mars/'
    browser.visit(fact_url)

    html = browser.html
    fact_soup = BS(html, 'html.parser')

    import pandas as pd
    table = fact_soup.find('table', attrs={'class':'tablepress tablepress-id-mars'})
    table_rows = table.find_all('tr')
    row_list = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        row_list.append(row)

    fact_df = pd.DataFrame(row_list, columns=["Type", "Stat"])
    fact_html = fact_df.to_html()


    # ### Mars Hemisphere
    # USGS site: https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
    pic_1_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(pic_1_url)

    html = browser.html
    pic_1_soup = BS(html, 'html.parser')

    # Retrieve the parent divs for all articles
    pic_1 = pic_1_soup.find('div', class_='downloads')
    a = pic_1.find('a')
    img1_url = pic_1.a['href']

    title_1= pic_1_soup.find('h2', class_="title").text

    hemisphere_image_urls = [{"title":title_1, "img_url":img1_url}]

    pic_2_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(pic_2_url)

    html = browser.html
    pic_2_soup = BS(html, 'html.parser')

    # Retrieve the parent divs for all articles
    pic_2 = pic_2_soup.find('div', class_='downloads')
    a = pic_2.find('a')
    img2_url = pic_2.a['href']

    title_2= pic_2_soup.find('h2', class_="title").text

    hemisphere_image_urls.append({"title":title_2, "img_url":img2_url})

    pic_3_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(pic_3_url)

    html = browser.html
    pic_3_soup = BS(html, 'html.parser')

    # Retrieve the parent divs for all articles
    pic_3 = pic_3_soup.find('div', class_='downloads')
    a = pic_3.find('a')
    img3_url = pic_3.a['href']

    title_3= pic_3_soup.find('h2', class_="title").text

    hemisphere_image_urls.append({"title":title_3, "img_url":img3_url})

    pic_4_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(pic_4_url)

    html = browser.html
    pic_4_soup = BS(html, 'html.parser')

    # Retrieve the parent divs for all articles
    pic_4 = pic_4_soup.find('div', class_='downloads')
    a = pic_4.find('a')
    img4_url = pic_4.a['href']

    title_4= pic_4_soup.find('h2', class_="title").text

    hemisphere_image_urls.append({"title":title_4, "img_url":img4_url})

    scrape_dict = {"mars_news_title": mars_news_title,
                    "mars_news_p" : mars_news_p,
                    "feature_url" : feature_url,
                    "mars_weather" : mars_weather,
                    "fact_html" : fact_html,
                    "hemisphere_image_urls" : hemisphere_image_urls}

    return scrape_dict