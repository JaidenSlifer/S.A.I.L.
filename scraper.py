from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

class ArticleScraper:
  
  def __init__(self, ticker, driver, base_url):
    self.ticker = ticker
    self.base_url = base_url
    self.driver = None

  # initializes chrome webdriver instance
  def initializeScraper(self):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

  # uses ticker instance variable and returns a list of article titles
  def getArticleTitles(self):
    target_url = self.base_url.fomat(self.ticker) #assuming base_url to be formatted with the ticker
    self.driver.get(target_url)

    title_elements = self.driver.find_elements(By.CSS_SELECTOR, 'tr.cursor-pointer.has-label a.tab-link-news')

    article_titles = [element.text for element in title_elements]
    return article_titles
    
  # uses ticker instance variable and return a list of article links
  def getArticleLinks(self):
    # https://finviz.com/quote.ashx?t=TICKER&p=d
    target_url = self.base_url.format(self.ticker)  # Assuming base_url to be formatted with the ticker
    self.driver.get(target_url)

    link_elements = self.driver.find_elements(By.CSS_SELECTOR, 'tr.cursor-pointer.has-label a.tab-link-news')
        
    article_links = [element.get_attribute('href') for element in link_elements]
    return article_links

  # scrapes the article at the given link and returns the text
  def scrapeArticle(self, articleLink):
    self.driver.get(articleLink)
        
    time.sleep(2)  #time for dynamic content to load
    
    #using beautifulsoup to parse the page
    soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        
    #combining all <p> blocks
    paragraphs = soup.find_all('p')
    article_text = ' '.join([p.text for p in paragraphs])

    return article_text
  
  # destroys webdriver instance
  def closeScraper(self):
    if self.driver is not None:
      self.driver.quit()

