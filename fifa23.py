import json
import pandas as pd

# Load JSON data
data = json.loads(json_data)

# Extract the relevant fields and create a DataFrame
players = []
for doc in data['docs']:
    player = {
        "playerId": doc["primaryKey"],
        "name": doc["playerjerseyname"],
        "overall_rating": doc["overall_rating"],
        "def": doc["def"],
        "phy": doc["phy"],
        "pac": doc["pac"],
        "dri": doc["dri"],
        "pas": doc["pas"],
        "sho": doc["sho"]
    }
    players.append(player)

# Create a DataFrame
df = pd.DataFrame(players)

# Save the DataFrame to a CSV file
df.to_csv('players_fifa23.csv', index=False)
