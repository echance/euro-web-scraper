from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
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
        filtered_events.append(url_string)
        print(f"Added {url_string} to filtered_events")

scores_by_year = {}
def get_final_score_links(event):
    year = event[-4:]
    scores_by_year[year] = {}
    print(f"Current Year: {year} checking {event}/grand-final")
    headers = {"User-Agent":
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0"}
    response = requests.get(f"{event}/grand-final", headers=headers)
    if response.status_code == 200:
        navigate_to = f"{event}/grand-final"
    else:
        navigate_to = f"{event}/final"
    
    print(f"Navigating to: {navigate_to}")
    driver.get(navigate_to)
    try:
        tbody = driver.find_element(By.TAG_NAME, "tbody")
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            country = row.find_elements(By.TAG_NAME, "td")[1].text
            score = row.find_elements(By.TAG_NAME, "td")[4].text
            try:
                score = int(''.join(filter(str.isdigit, score)))
                scores_by_year[year][country] = score
            except:
                scores_by_year[year][country] = 0
            # print(f"Country: {country} / Score: {score}")
    except Exception as e:
        print(f"Big uh oh found in the year {year}")
        print(e)


for event in filtered_events:
    # if int(event[-4:]) > 2020:
    get_final_score_links(event)

# Write data to json file
with open('./generated/participant-scores.json', 'w', encoding='utf8') as fp:
    json.dump(scores_by_year, fp)

        
driver.close()