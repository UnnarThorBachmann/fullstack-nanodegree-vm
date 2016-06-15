-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE player(
id serial PRIMARY KEY,
name text
);

CREATE TABLE match(
id serial,
id_winner integer REFERENCES player (id),
id_loser integer REFERENCES player (id)
);

CREATE VIEW nr_matches_view AS
  select player.id as ids, player.name as names, count(match.id_winner) as matches
  from player left join match on (player.id=match.id_winner or player.id=match.id_loser)
  group by player.id order by matches desc;
    
CREATE VIEW nr_wins_view AS
  select player.id as ids, player.name as names, count(match.id_winner) as wins
  from player left join match on (player.id=match.id_winner)
  group by player.id order by wins desc;
