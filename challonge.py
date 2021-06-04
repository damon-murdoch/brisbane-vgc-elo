# Application Configuration Variables
import config

# Json Data Read/Write (custom library)
import json_files

# Import Challonge! API Data
import json

# Python elo ladder implementation
import elo

# Python operating system library
import os

# Import requests library
# import request from urllib
from urllib import request

def get_tournament(tourInfo):

  # Dereference the tournament data
  tourInfo = data['tournament']

  # Tournament Id 
  id = tourInfo['id']

  # Tournament name
  name = tourInfo['name']

  # Tournament start date & time
  date = tourInfo['started_at']

  # Tournament game name
  game = tourInfo['game_name']

  # Tournament url key
  url = tourInfo['url']

  # Tournament type / structure
  type = tourInfo['tournament_type']

  # Number of match rounds
  rounds = tourInfo['swiss_rounds']

  return {
    'id': id,
    'name': name,
    'date': date,
    'game': game,
    'url': url,
    'type': type,
    'rounds': rounds
  }

def get_player(playerInfo):

  # Dereference the participant object
  player = playerInfo['participant']

  # Player Id Object 
  id = player['id']

  # Player Tournament Id 
  tid = player['tournament_id']

  # Placeholder name variable
  name = ""

  # Dereference the player's name, some fields may be blank
  # so keep moving down the line where previous is unavailable

  # 'name' > 'username' > 'display_name' > 'challonge_username'

  if 'name' in player and player['name'] != "":
    name = player["name"]

  elif 'username' in player and player['username'] != "": 
    name = player["username"]

  elif 'display_name' in player and player['display_name'] != "":
    name = player["display_name"]

  elif 'challonge_username' in player and player['challonge_username'] != "":
    name = player["challonge_username"]

  # Add a new player to the players list
  return {
    'id': id,
    'tid': tid,
    'name': name
  }

def get_match(matchInfo):

  # Dereference the match object
  match = matchInfo['match']

  # Match Id
  id = match['id']

  # Tournament Id       
  tid = match['tournament_id']

  # Winner Id
  wid = match['winner_id']

  # Loser Id 
  lid = match['loser_id']

  # Round (For ordering)
  round = match['round']

  # Score
  score = match['scores_csv']

  # Add the new round to the list
  return {
    'id': id,
    'tid': tid,
    'wid': wid,
    'lid': lid,
    'round': round,
    'score': score
  }

# Runs if this script is executed
if __name__ == '__main__':

  try:

    target = input('Enter the Challonge Tournament Url Key (e.g. yj78qn73): ')

    # If no target is provided
    if not target:

      # Use the default test target
      target = "yj78qn73"

    # Generate the challonge API request string
    requeststr = "https://api.challonge.com/v1/tournaments/" + target + \
      ".json?include_matches=1&include_participants=1&api_key=" + config.CHALLONGE_API_KEY 

    # Make a request to the server using the provided string
    content = request.urlopen(requeststr)

    # Retrieve the json data from the request
    data = json.load(content)

    # Lookup table based on id 
    # so players with the same 
    # name are identified 
    players = {}

    # Lookup table based on id to 
    # ensure that matches are 
    # ordered properly
    matches = {}

    # Dereference the tournament data
    tourInfo = data['tournament']

    # Create a tournament object with the properties of the tournament
    tournament = get_tournament(tourInfo)
    
    # Create a hashtable containing only the tournament, to be
    # merged with the existing tournament json file
    tournaments = {tournament['id']: tournament}

    # Iterate over the players in the participants list
    for playerInfo in tourInfo['participants']:

      # Create a player object using the player info
      player = get_player(playerInfo)

      # Add the player to the players table
      players[player['id']] = player

    # Iterate over all of the matches in the matches list
    for matchInfo in tourInfo['matches']:
      
      # Create a match object using the match info
      match = get_match(matchInfo)

      # Add the match to the matches table
      matches[match['id']] = match

    # Folder path of the current file
    scriptPath = os.path.dirname(__file__)

    # Data directory
    dataPath = os.path.join(scriptPath,"data")

    # Tournament json file
    toursPath = os.path.join(dataPath, "tournaments.json")

    # Merge the tournament json file with the new metadata
    handle_json.merge_json(tournaments, toursPath)

    # Matches json file
    matchesPath = os.path.join(dataPath, "matches.json")

    # Merge the matches json file with the new metadata
    handle_json.merge_json(matches, matchesPath)

    # Players json file
    playersPath = os.path.join(dataPath, "players.json")

    # Merge the players json file with the new metadata
    handle_json.merge_json(players, playersPath)

  except Exception as e:

    print("Error: ",e)