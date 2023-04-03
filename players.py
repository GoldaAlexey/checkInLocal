import db
from typing import Dict, List, NamedTuple

class Player :
    def __init__(self, first_name, username, account_id):
        self.account_id = account_id
        self.first_name = first_name
        if username == None:
            self.username = first_name
        else:
            self.username = username
        self.social_credits = 100
    account_id : int
    first_name : str
    username : str
    social_credits : int

def get_list_of_players() -> List[Player]:
        """Возвращает справочник зарегистрированных пользователей из БД"""
        players = db.fetchall(
            "players", "first_name username account_id  social_credits".split()
        )
        return players

def get_player_sc_by_account_id(account_id : int) -> int:
        """Возвращает справочник зарегистрированных пользователей из БД"""
        players = db.fetchall(
            "players", "first_name account_id social_credits".split()
        )
        for player in players:
             if player['account_id'] == account_id:
                  return player['social_credits']
        return None

def check_user_id(id : int) -> bool:
      players = get_list_of_players()
      for player in players:
          print(player)
      for player in players:
        if player['account_id'] == id :
            return True
      return False

def add_user(player : Player) -> bool:
    if(check_user_id(player.account_id) == False):
        db.insert("players", {
            "first_name": player.first_name,
            "username": player.username,
            "account_id" : player.account_id,
            "social_credits" : player.social_credits
        })
        return True
    return False

