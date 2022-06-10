import json

participant_data_file = open('./generated/participant-data.json')
participant_scores_file = open('./generated/participant-scores.json')

participant_data = json.load(participant_data_file)
print(type(participant_data))
participant_scores = json.load(participant_scores_file)

for data in participant_data:
    print(data)
    year = data["year"]
    print(f"Year: {year}")
    scores = participant_scores[year]
    for participant in data["participants"]:
        country = participant["country"]
        if country in scores:
            participant["final_score"] = scores[country]
        else:
            participant["final_score"] = 0

# Write data to json file
with open('./generated/participant-data-updated-scores.json', 'w', encoding='utf8') as fp:
    json.dump(participant_data, fp)