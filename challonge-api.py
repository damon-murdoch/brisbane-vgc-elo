# Application Configuration Variables
import config

# Import Challonge! API Data
import json

# Python elo ladder implementation
import elo

# Python operating system library
import os

# Import requests library
# import request from urllib
from urllib import request

class Tournament:

  def __init__(self, id, name, date, game, url, type, rounds):

    # Id of the tournament
    # i.e. 4217482
    self.id = id

    # Name of the tournament
    # i.e. "Nino's Magical Pokemon Showdown"
    self.name = name

    # Tournament Start Date
    # i.e. "2018-01-30T12:18:43.667+10:00"
    self.date = date

    # Game of the tournament
    # i.e. "Pokemon Showdown!"
    self.game = game

    # Url of tournament
    # i.e. "yj78qn73"
    self.url = url

    # Type of tournament
    # i.e. "Single Elim"
    self.type = type

    # Rounds of the tournament
    # i.e. 3
    self.rounds = rounds

  def __dict__(self):

    return {
      "id": self.id,
      "name": self.name, 
      "date": self.date, 
      "game": self.game, 
      "url": self.url, 
      "type": self.type,
      "rounds": self.rounds
    }

class Player:

  def __init__(self, id, tid, name):
    
    # Player ID (Tournament specific)
    self.id = id
    
    # Tournament ID (Not sure if I need this)
    self.tid = tid
    
    # Player Name (Tournament Specific)
    # Priority List:
    # 'name' > 'username' > 'display_name' > 'challonge_username'
    self.name = name

  def __dict__(self):

    return {
      "id": self.id,
      "tid": self.tid,
      "name": self.name
    }

class Match:

  def __init__(self, id, tid, wid, lid, round, score):

    # Match Id 
    # i.e. 110242465
    self.id = id

    # Tournament Id 
    # i.e. 4217482
    self.tid = tid

    # Winning player Id
    # i.e. 68069631
    self.wid = wid

    # Losing Player Id
    # i.e. 68063427
    self.lid = lid

    # Match Round 
    # i.e. 1
    self.round = round

    # Match Score
    # i.e. 1-0
    self.score = score

  def __dict__(self):

    return {
      "id": self.id,
      "tid": self.tid,
      "wid": self.wid,
      "lid": self.lid,
      "round": self.round,
      "score": self.score
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
    # Id is used so players with the 
    # same name are identified 
    players = {}

    # Lookup table based on id
    # Contains that player's elo ranking
    ratings = {}

    # List, able to be sorted by round
    # to ensure that matches are ordered
    # properly
    matches = []

    # Dereference the tournament data
    tourinfo = data['tournament']

    # Tournament Id 
    id = tourinfo['id']

    # Tournament name
    name = tourinfo['name']

    # Tournament start date & time
    date = tourinfo['started_at']

    # Tournament game name
    game = tourinfo['game_name']

    # Tournament url key
    url = tourinfo['url']

    # Tournament type / structure
    type = tourinfo['tournament_type']

    # Number of match rounds
    rounds = tourinfo['swiss_rounds']

    tournament = Tournament(id, name, date, game, url, type, rounds)

    # Iterate over the players in the participants list
    for playerinfo in tourinfo['participants']:

      # Dereference the participant object
      player = playerinfo['participant']

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
      players[id] = Player(id, tid, name)

    # Iterate over all of the matches in the matches list
    for matchinfo in tourinfo['matches']:

      # Dereference the match object
      match = matchinfo['match']

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
      matches.append(Match(id, tid, wid, lid, round, score))

    # Get the path of the running script
    dir = os.path.dirname(__file__)

    # Get the path of the data directory
    data_dir = os.path.join(dir, 'data')

    # If the data folder does not exist yet
    if not os.path.exists(data_dir):

      # Create the data folder
      os.mkdir(data_dir)

    # File containing tournament data
    tour_file = os.path.join(data_dir, "tours.json")

    # File containing match data
    match_file = os.path.join(data_dir, "matches.json")
    
    # File containing player data
    player_file = os.path.join(data_dir, "players.csv")

    # Open with all privileges, even if file doesn't exist
    with open(tour_file, "w+") as tour_json:

      # Get the text from the file
      content_json = tour_json.read()

      # If the content is not empty
      if content_json:

        # Get the json data from the file
        content_json = json.loads(content_json)

      else: # No content available

        # Create empty list
        content_json = [json.dumps(tournament.toObject())]

      print(content_json)

    # Open with all privileges, even if file doesn't exist
    with open(match_file, "w+") as match_json:

      # Get the text from the file
      content_json = match_json.read()

      # If the content is not empty
      if content_json:

        # Get the json data from the file
        content_json = json.loads(content_json)

      else: # No content available

        # Create empty list
        # content_json = [json.dumps(tournament.toObject())]
        

      print(content_json)

    # Open with all privileges, even if file doesn't exist
    with open(player_file, "w+") as player_json:

      # Get the json data from the file
      # player_data = json.loads(player_json.read())
      pass

  except Exception as e:

    print("Error: ",e)