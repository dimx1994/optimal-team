# Optimal Team Builder Web App

### Working with Data 
Export the NBA stats players database: https://www.kaggle.com/drgilermo/nba-players-stats
Store this data in a relational database of your choosing with a suitable schema

Players.csv in a table with the following columns (Player, height, weight, college, born, birth_city, birth_state)

Seasons_Stats.csv in another table with the following columns (Season, Player, name, Position, Age, Games, PTS)

Player_data.csv into yet another table if you are not able to merge it into the Player table

### Build the Web App 
We want to build an Optimal Team Builder Web App: 

You should create a text field in the web app where one can input a specific points sum for a team (e.g: 4000). Once the sum is defined, the tool must show a list of 5 players that constitute the best team one can have for this specific point sum. The best player is defined as the youngest player who has the highest point sum in the least amount of games. (You can also decide to use other attributes in the dataset to define the best player if you wish).

PS: Feel free to use third party libraries to solve this problem

## Solution

**Requirements:**
Application requires docker and docker-compose to be installed and started.

**Installation:**
To start a service run:
```bash
docker-compose up --build
```
To use web interface go to url http://0.0.0.0:5000/

**API:**

You could use api for getting the optimal team:

```bash
 curl "http://0.0.0.0:5000/api/v1/optimal-team?points=4000" 
```
Response:
```json
{
  "points_per_season": 4000,
  "avg_games_in_season": 50,
  "points_per_game": 78.68267864289635,
  "points_per_player": 15.736535728579268,
  "point_guard": {
    "name": "Howard Komives",
    "performance": 15.707692307692307
  },
  "shooting_guard": {
    "name": "Ricky Sobers",
    "performance": 15.731707317073171
  },
  "small_forward": {
    "name": "Wilson Chandler",
    "performance": 15.732394366197184
  },
  "power_forward": {
    "name": "Danny Manning",
    "performance": 15.73076923076923
  },
  "center": {
    "name": "Robert Parish",
    "performance": 15.734177215189874
  }
}
```

Or you could use swagger http://0.0.0.0:5000/docs

TODO: separate env for dev and prod(or use poetry), tests, CI, ...
