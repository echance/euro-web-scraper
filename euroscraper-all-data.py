from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json


options = Options()
options.headless = True
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://eurovision.tv/events")

# Get all links to Eurovision events from every year on events page
all_events = driver.find_elements(By.CSS_SELECTOR, "a[href*='/event/']")
filtered_events = []

# Filter invalid event links and remove duplicates
for event in all_events:
    url_string = event.get_attribute("href")
    if (url_string not in filtered_events and url_string[-4:].isnumeric()):
        filtered_events.append(f"Added {url_string} to filtered_events")
        

participant_links = []
full_participant_data = []
event_index_map = {}

# Make index map for dictionary list
def get_dictionary_index(list, key, value):
    for index, dictionary in enumerate(list):
        if dictionary[key] == value:
            return index
    return None

# Get participant links from each year and push link/year object to array. Calling build_participant_data in nested loops caused issues.
def get_participants(event):
    # Get year from end of each event url
    year = event[-4:]
    # Each year will be a key to hold participant data object
    full_participant_data.append({
        'year': year,
        'participants': []
    })
    event_index_map[year] = len(full_participant_data) - 1
    # Go to participants page for year (ex: event = https://eurovision.tv/event/copenhagen-1964)
    driver.get(event+"/participants")
    # Get individual participant links
    participant_links_by_year = driver.find_elements(By.CSS_SELECTOR, "a[href*='/participant/']")
    # Loop through selected year's participants and build data
    for link in participant_links_by_year:
        current_participant_link = link.get_attribute("href")
        if ("withdrew-from-the-competition-but-still-voted" not in current_participant_link):
            participant_links.append({"link": current_participant_link, "year": year})
            

for event in filtered_events:
    get_participants(event)

# Build data using each participant link
def build_participant_data(current_participant_link, year):
    print('Getting data for: ' + current_participant_link + ' for year: ' + year)
    driver.get(current_participant_link)
    country = driver.find_element(By.CSS_SELECTOR, "a[href*='/country']")
    youtube = ''
    try: 
        youtube = driver.find_element(By.CSS_SELECTOR, "a[href*='/watch']").get_attribute("href")
    except:
        print('No youtube found for ' + current_participant_link)
    song = driver.find_element(By.XPATH, "//dd[contains(@class, 'text-sm')]/div/div[1]")
    artist = driver.find_element(By.XPATH, "//h1[contains(@class, 'font-bold')]")
    lyrics = ''
    try:
        lyrics = driver.find_element(By.CSS_SELECTOR, "div.whitespace-pre-line").text
    except:
        print('No lyrics found')
    
    participant_json = {
        "country": country.text,
        "artist": artist.text,
        "song": song.text,
        "youtube": youtube,
        "lyrics": lyrics,
        "final_score": ''
    }
    full_participant_data[event_index_map[year]]['participants'].append(participant_json)

# Loop through all participant links
for current_link in participant_links:

    build_participant_data(current_link['link'], current_link['year'])

# Write data to json file
with open('participant-data.json', 'w', encoding='utf8') as fp:
    json.dump(full_participant_data, fp)

driver.close()
