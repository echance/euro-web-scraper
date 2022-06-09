from selenium import webdriver
from selenium.webdriver.common.by import By
from pymongo import MongoClient

mongoClient = MongoClient(port=27017)
db = mongoClient.eurodb

driver = webdriver.Chrome("F:\\chromedriver_win32\\chromedriver.exe")
driver.get("https://eurovision.tv/event/turin-2022/participants")

links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/participant/']")

participant_links = []
full_participant_data = []

for link in links:
    print(link.get_attribute("href"))
    participant_links.append(link.get_attribute("href"))

for link in participant_links:
    driver.get(link)
    country = driver.find_element(By.CSS_SELECTOR, "a[href*='/country']")
    youtube = driver.find_element(By.CSS_SELECTOR, "a[href*='/watch']")
    youtube_link = youtube.get_attribute("href") if (youtube is None) else None
    song = driver.find_element(By.XPATH, "//dd[contains(@class, 'text-sm')]/div/div[1]")
    artist = driver.find_element(By.XPATH, "//h1[contains(@class, 'font-bold')]")
    lyrics = driver.find_element(By.CSS_SELECTOR, "div.whitespace-pre-line")
    participant_json = {
        "country": country.text,
        "artist": artist.text,
        "song": song.text,
        "youtube": youtube_link,
        "lyrics": lyrics.text
    }
    full_participant_data.append(participant_json)
db.participant.drop()
db['participant']
db.participant.insert_many(full_participant_data)