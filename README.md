# euro-web-scraper
Quick and dirty scrapers to acquire data from eurovision.tv. Solely for data collection to update MongoDB database.
Generated data can be seen in participant-data.json, participant-scores.json, and participant-data-updated-scores.json

# Scripts
euroscraper-2022.py was the first iteration, which scraped data for Eurovision 2022 participants
euroscraper-participant-data.py scrapes all data from historic events
euroscraper-get-scores.py scrapes scoreboard pages for each year and outputs scores by year and country
euroscraper-update-scores.py updates generated participant-data.json with participant-scores.json matching each country to scores