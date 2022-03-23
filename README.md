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
 curl "http://0.0.0.0:5000/api/v1/optimal-team?points=100" 
```
Response:
```json
{"players":[{"name":"George McLeod","points":12},{"name":"Jack McMahon","points":507},{"name":"Monk Meineke","points":725},{"name":"Stan Miasek","points":512},{"name":"Stan Miasek","points":283}]}
```

Or you could use swagger http://0.0.0.0:5000/docs

TODO: separate env for dev and prod(or use poetry), tests, CI, ...
