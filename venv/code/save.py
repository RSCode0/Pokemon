import json

class Save:
  def __init__(self):
    pass
  
  @staticmethod
  def load_inventory(player_inventory):
    with open("venv/code/json/save.json", "r+", encoding="utf-8") as file:
      data_save = json.load(file)
      
      inventory = data_save["inventory"]
      
      for item in player_inventory:
        player_inventory[item] = inventory[item]
  
  @staticmethod
  def save_inventory(player_inventory):
    with open("venv/code/json/save.json", "r+", encoding="utf-8") as file:
      data_save = json.load(file)
    
    for item in player_inventory:
      data_save["inventory"][item] = player_inventory[item]
    
    with open("venv/code/json/save.json", "w", encoding="utf-8") as file:  
      json.dump(data_save, file, indent=4)
      