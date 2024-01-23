import random

# Battle Modifier
battleModifier = [0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4]
battleMOD = random.choices(battleModifier, weights=(5, 10, 15, 50, 10, 5, 3, 2), k=1)

print(f"battleMod: {battleMOD}")

# Box Modifier
boxModifier = ['gold', 'item', 'gem','hero']
battleMOD = random.choices(boxModifier, weights=(60, 20, 15, 5), k=1)

# Gold Modifier
goldModifier = [50, 100, 250, 1000]
goldMOD = random.choices(goldModifier, weights=(60, 20, 15, 5), k=1)
