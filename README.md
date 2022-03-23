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

NOTE: please see the comment in `app.db.optimal_team.py` because I'm not sure that my algorithm for selecting the best player fits the task

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

## Questions

1. What technology (apart from Python, which is required), DB, and tools did you use and why do you think it’s a good pick? 

Here I use: Fastapi - this is modern fast and lightweight web framework with swagger and requests validation - good choice for a small service. 
As ORM I use SQLAlchemy, since the data is not very big, it's convenient in terms of web development and good in terms of performance to use ORM here. 
As DB I use Postgres, as this is a fast relational db; pandas - it's a standard for data analysis, and it's also fast as 
it's implemented in C. Also I used some other python libraries in requirements, as well as linters from `lint_and_pretty.sh`

2. Let's say we want to add all the players created by users (between 5,000,000 to 20,000,000 new players per month) to the database. We also decide to add real-time updates to the player database. What tech stack will you use? (Language, DB, hosting, etc.) How would you make sure your tool is scalable for higher volumes? 

If we have such a load (approx 120 000 000 rows per year and 7 RPS for inserting), Postgres + some fast python web framework + ORM should work(but optimized raw queries are faster).
We should add indexes by which we filter our data in selects and replicate the db. Also, if, for instance, we execute 
selects only within single user, we could add sharding by username hash, or we could add partitioning by time. 
If we have lots of selects with lots of calculations and joins, we should use raw queries without ORM, and we could also add Redis for caching.
If the load is even greater, you can use any queue for lazy writing to the relational database, or even use kafka.
The tool should be deployed to kubernetes using docker, so we could easily scale db replicas, services, etc.


