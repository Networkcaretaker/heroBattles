import csv
import random

class Hero:
    def __init__(self, name, health, attack, defense):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense

    def take_damage(self, damage):
        # damage_taken = max(0, damage - self.defense)
        damage_taken = damage
        self.health = self.health - damage
        return damage

def load_heroes_from_csv(file_path):
    heroes = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            hero = Hero(row['heroName'], int(row['heroHealth']), int(row['heroAttack']), int(row['heroDefence']))
            heroes.append(hero)
    return heroes

def battle_round(hero1, hero2):
    # Hero 1 attacks Hero 2
    damage_to_hero2 = max(0, hero1.attack - hero2.defense)
    damage_taken = hero2.take_damage(damage_to_hero2)
    print(f"{hero1.name} attacks {hero2.name} and deals {damage_to_hero2} damage. {hero2.name}'s health: {hero2.health}")

    # Check if Hero 2 is defeated
    if hero2.health <= 0:
        print(f"{hero2.name} has been defeated!")
        return

    # Hero 2 attacks Hero 1
    damage_to_hero1 = max(0, hero2.attack - hero1.defense)
    damage_taken = hero1.take_damage(damage_to_hero1)
    print(f"{hero2.name} counterattacks {hero1.name} and deals {damage_to_hero1} damage. {hero1.name}'s health: {hero1.health}")

    # Check if Hero 1 is defeated
    if hero1.health <= 0:
        print(f"{hero1.name} has been defeated!")

def main():
    heroes = load_heroes_from_csv('heroes.csv')

    if len(heroes) != 2:
        print("Error: Please provide exactly two heroes for the battle.")
        return

    hero1, hero2 = heroes[0], heroes[1]

    print(f"Battle begins between {hero1.name} and {hero2.name}!")

    while hero1.health > 0 and hero2.health > 0:
        battle_round(hero1, hero2)

    print("Battle ends.")

if __name__ == "__main__":
    main()











    # Get Data from Database
docs = hero_database.stream()

for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")



# Example Data
heroID = 'BddZ36TyBnpO88E4hekU'
heroData = {
    'heroName': "Jimmy",
    'heroLevel': 1,
    'heroHealth': 1200,
    'heroAttack': 200,
    'heroDefence': 60
    }
dataset = 'heroes_collection'

# Test Functions
# test = getRecord(dataset, heroID)
# print(f"{test.id} => {test.to_dict()}")

tests = getRecords(dataset)
for test in tests:
   print(f"{test.id} => {test.to_dict()}")
  
# addRecord(dataset, heroData)

# updateRecord(dataset, heroID, heroData)