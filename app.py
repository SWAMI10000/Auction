from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed to use sessions

# Read CSV file and convert it to a DataFrame
players_df = pd.read_csv('players.csv')
players = players_df.to_dict('records')

# Initialize session variables
@app.before_request
def initialize():
    if 'player_index' not in session:
        session['player_index'] = 0
    if 'players_shown' not in session:
        session['players_shown'] = []
    if 'team_summary' not in session:
        session['team_summary'] = {}
    if 'teams' not in session:
        session['teams'] = []

# Helper function to get the next player
def get_next_player():
    available_players = [p for p in players if p['Id'] not in session['players_shown']]
    if available_players:
        player = random.choice(available_players)
        session['players_shown'].append(player['Id'])
        session['player_index'] += 1

        # Calculate base price based on rating
        rating = player['Rating']
        if rating >= 90:
            base_price = 8
        elif rating >= 88:
            base_price = 6
        elif rating >= 85:
            base_price = 4
        elif rating >= 83:
            base_price = 2
        else:
            base_price = 1
        player['BasePrice'] = base_price

        return player
    else:
        return None

@app.route('/')
def index():
    position_counts = players_df['Position'].value_counts().to_dict()
    return render_template('index.html', total_players=len(players), position_counts=position_counts)

@app.route('/setup_teams', methods=['GET', 'POST'])
def setup_teams():
    if request.method == 'POST':
        team_names = request.form.getlist('team_names')
        session['teams'] = team_names
        session['team_summary'] = {team: {'players': 0, 'total_spent': 0, 'player_details': []} for team in team_names}
        return redirect(url_for('start_auction'))
    return render_template('setup_teams.html')

@app.route('/start_auction')
def start_auction():
    player = get_next_player()
    teams = session.get('teams', [])
    team_summary = session.get('team_summary')
    return render_template('auction.html', player=player, teams=teams, total_players=len(players), team_summary=team_summary, players_left=len(players) - len(session['players_shown']))

@app.route('/player_sold', methods=['POST'])
def player_sold():
    player_id = int(request.form['player_id'])
    price = float(request.form['price'])
    team = request.form['team']
    
    # Update team summary
    team_summary = session.get('team_summary')
    player_details = next(player for player in players if player['Id'] == player_id)
    player_details['Price'] = price
    team_summary[team]['players'] += 1
    team_summary[team]['total_spent'] += price
    team_summary[team]['player_details'].append(player_details)
    session['team_summary'] = team_summary
    
    player = get_next_player()
    if player:
        return render_template('auction.html', player=player, teams=list(team_summary.keys()), total_players=len(players), team_summary=team_summary, players_left=len(players) - len(session['players_shown']))
    else:
        return "All players have been auctioned!"

@app.route('/player_unsold')
def player_unsold():
    player = get_next_player()
    team_summary = session.get('team_summary')
    if player:
        return render_template('auction.html', player=player, teams=session['teams'], total_players=len(players), team_summary=team_summary, players_left=len(players) - len(session['players_shown']))
    else:
        return "All players have been auctioned!"

@app.route('/team_summary')
def team_summary():
    team_summary = session.get('team_summary')
    return render_template('team_summary.html', team_summary=team_summary)

@app.route('/restart')
def restart():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
