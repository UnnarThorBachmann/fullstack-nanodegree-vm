#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        conn = psycopg2.connect("dbname=tournament")
        curr = conn.cursor()
        return conn, curr
    except:
        print("Error connecting to the tournament database.")
    


def deleteMatches():
    """Remove all the match records from the database."""
    conn,curr = connect()
    curr.execute("DELETE FROM match;")
    conn.commit() 
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn,curr = connect()
    curr.execute("DELETE FROM player;")
    conn.commit() 
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn,curr = connect()
    curr.execute("SELECT count(player.id) FROM player;")
    row = curr.fetchone()
    conn.commit() 
    conn.close()
    if row:
       return int(row[0])
    else:
        return 0

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn,curr = connect()
    curr.execute("INSERT INTO player (name) values(%s);",(name,))
    conn.commit() 
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn,curr = connect()
    curr.execute("""
          SELECT nr_matches_view.ids, nr_matches_view.names, nr_matches_view.matches, nr_wins_view.wins
          FROM (nr_matches_view join nr_wins_view on nr_wins_view.ids = nr_matches_view.ids)
          ORDER BY nr_wins_view.wins DESC;
    """)
    rows = curr.fetchall()
    return [(row[0],row[1],row[3],row[2]) for row in rows]

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn,curr = connect()

    curr.execute("INSERT INTO match(id_winner,id_loser) values(%s,%s);",(str(winner),str(loser)))
    conn.commit() 
    conn.close()
 
def opponents_so_far(curr,player_id):
    """ Helper functions for swissPairings.
        Returns a set of players player_id has already played.

    Returns: A set of string id's (id1, id2, ..., idn)
    where id1, id2, ... , idn are the ids of the players
    curr has already played with.
    """
    curr.execute("SELECT * from match where id_winner=%s or id_loser =%s;" % (player_id,player_id))
    rows = curr.fetchall()
    ex_opponents = []
    for ex_opponent in rows:
        if int(player_id) == ex_opponent[1]:
           ex_opponents.append(ex_opponent[2])
        else: 
           ex_opponents.append(ex_opponent[1])
    return set(ex_opponents)

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    This is not particularly fast algorithm since I have fetch the ex_opponents set
    from the database to draw players together. In my opinion a O(nm) algorithm were
    n is the number of players and m is the number of matches. Could of course been
    made faster by storing the matches but then I wanted to use the database.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn,curr = connect()

    curr.execute("SELECT * from nr_wins_view")
    rows = curr.fetchall()
    
    players = []
    players_names = {}
    is_matched = {}
    pairings = []
    # Sorting players in descending order of wins.
    for row in rows:    
        player_id = str(row[0])
        players_names[player_id] = str(row[1])
        is_matched[player_id] = False
        players.append(player_id)

    # A player is matched with the player below him on the list
    # who has not already been matched and is not an ex-opponent.
    for i in range(len(players)):
        # If matched go to the next one.
        if is_matched[players[i]]:
           continue
        else:
            ex_opponents_set = opponents_so_far(curr,players[i])
            # Find the next opponent which is not already matched and
            # not an ex opponent.
            for j in range(i+1,len(players)):
                if (not is_matched[players[j]]) and  (not int(players[j]) in ex_opponents_set):
                   pairings.append((int(players[i]), players_names[players[i]],int(players[j]), players_names[players[j]]))
                   is_matched[players[i]] = True
                   is_matched[players[j]] = True
                   break
                else:
                    pass
    conn.close()

    return pairings
