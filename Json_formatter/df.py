import json
import pandas as pd

# Load the JSON data
with open('players.json', 'r') as file:
    data = json.load(file)

# Extract the relevant information and convert to a DataFrame
players = []
for item in data['items']:
    player = {
        'Id': item['id'],
        'Position': item['position']['label'],
        'ShieldUrl': item['shieldUrl'],
        'Rating':item['overallRating']
    }
    players.append(player)

df = pd.DataFrame(players)

df.to_csv('players.csv', index=False)
df.head()
