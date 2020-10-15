import requests
import json
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from io import BytesIO

def _extract_image(url):
    options = Options();
    options.add_argument("--headless")
    browser = webdriver.Chrome(executable_path="./chromedriver", options=options)
    browser.get(url);
    source_data = browser.page_source
    bs_data = bs(source_data, 'html.parser')
    firstAlbumPhoto = bs_data.find(class_="fbStarGrid fbStarGridAppendedTo")
    hrefClass= firstAlbumPhoto.find(class_="uiMediaThumb _6i9 uiMediaThumbMedium")
    thumbnail = "https://www.facebook.com" + hrefClass.get('href')
    browser.get(thumbnail)
    thumbnailSource = browser.page_source
    bs_Thumbnail = bs( thumbnailSource, 'html.parser')
    thumbnailWrapper = bs_Thumbnail.find(class_="_5pcr userContentWrapper")
    thumbnailHtml = thumbnailWrapper.find(class_="scaledImageFitWidth img")
    thumbnailImgLink = thumbnailHtml.get('src')
    browser.close()
    return thumbnailImgLink

def _extract_post_text(item):
    actualPosts = item.find_all(attrs={"data-testid": "post_message"})
    text = ""
    if actualPosts:
        for posts in actualPosts:
            paragraphs = posts.find_all('p')
            text = ""
            for index in range(0, len(paragraphs)):
                text += paragraphs[index].text
    return text

def main():
    url= [ 'https://www.facebook.com/media/set/?vanity=4ourbar&set=a.174652255905890', "https://www.facebook.com/media/set/?vanity=bonitassofia&set=a.110038697428897", "https://www.facebook.com/media/set/?vanity=food.oxo&set=a.586182594774776", "https://www.facebook.com/foodmoodbg"]
    link = _extract_image(url[0])
    response = requests.get(link)
    image = Image.open( BytesIO(response.content) )
    image.show()

if __name__ == "__main__":
    main()
