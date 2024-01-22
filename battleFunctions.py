import firebase
import consoleFunctions
import random
from colorama import Fore, Style

def selectHeroes():
    def chooseHeroes():
        allHeroes = firebase.getRecords('heroes')
        heroes = []
        heroIDs = []

        for hero in allHeroes:
            heroName = hero.to_dict()['Name']
            heroID = hero.id
            heroes.append(heroName)
            heroIDs.append({'Name':heroName, 'ID':heroID})
    
        print(f"\n{Fore.LIGHTCYAN_EX}Player 1{Style.RESET_ALL} choose a Hero \n")
        selectHeroA = consoleFunctions.selectListValue(heroes)
        print(f"\n{Fore.LIGHTCYAN_EX}{selectHeroA}{Style.RESET_ALL}\n")

        print(f"{Fore.GREEN}Player 2{Style.RESET_ALL} choose a Hero \n")
        selectHeroB = consoleFunctions.selectListValue(heroes)
        print(f"\n{Fore.GREEN}{selectHeroB}{Style.RESET_ALL}\n")

        print(f"{Fore.LIGHTCYAN_EX}{selectHeroA}{Style.RESET_ALL} VS {Fore.GREEN}{selectHeroB}{Style.RESET_ALL}\n")

        for heroID in heroIDs:
            if heroID['Name'] == selectHeroA:
                heroA_id = heroID['ID']
            if heroID['Name'] == selectHeroB:
                heroB_id = heroID['ID']

        heroA = firebase.getRecord('heroes', heroA_id)
        heroB = firebase.getRecord('heroes', heroB_id)

        return(heroA, heroB)
    
    selectedHeros = chooseHeroes()

    heroOptions = ['Start Battle', 'Change Heroes'] 
    heroOption = consoleFunctions.selectListValue(heroOptions) 
    print('')

    while heroOption != 'Start Battle':
        selectedHeros = chooseHeroes()
        heroOption = consoleFunctions.selectListValue(heroOptions) 
        print('')

    heroA = selectedHeros[0]
    heroB = selectedHeros[1]
    return(heroA, heroB)

class Hero:
    def __init__(self, Name, Health, Stamina, Magicka, Healing, HealthRecovery, StaminaRecovery, MagickaRecovery, PhysicalAttack, PhysicalDefence, MagicAttack, MagicDefence, Ultimate):
        self.Name = Name
        self.Health = Health
        self.Stamina = Stamina
        self.Magicka = Magicka
        self.PhysicalAttack = PhysicalAttack
        self.PhysicalDefence = PhysicalDefence
        self.MagicAttack = MagicAttack
        self.MagicDefence = MagicDefence
        self.Healing = Healing
        self.HealthRecovery = HealthRecovery
        self.StaminaRecovery = StaminaRecovery
        self.MagickaRecovery = MagickaRecovery
        self.MaxHealth = Health
        self.MaxStamina = Stamina
        self.MaxMagicka = Magicka
        self.MaxHealing = Healing
        self.Ultimate = Ultimate

    def take_damage(self, damage):
        self.Health = self.Health - damage
        return damage
    
    def use_stamina(self, energyUse):
        self.Stamina = max(0, self.Stamina - energyUse)
        return self.Stamina
    
    def use_magicka(self, energyUse):
        self.Magicka = max(0, self.Magicka - energyUse)
        return self.Magicka
    
    def recover_health(self):
        currentHealth = self.Health
        self.Health = min(self.MaxHealth, self.Health + self.HealthRecovery)
        healthRecovered = self.Health - currentHealth
        return healthRecovered
    
    def recover_stamina(self):
        currentStamina = self.Stamina
        self.Stamina = min(self.MaxStamina, self.Stamina + self.StaminaRecovery)
        staminaRecovered = self.Stamina - currentStamina
        return staminaRecovered
      
    def recover_magicka(self):
        currentMagicka = self.Magicka
        self.Magicka = min(self.MaxMagicka, self.Magicka + self.MagickaRecovery)
        magickaRecovered = self.Magicka - currentMagicka
        return magickaRecovered

def battle_round(hero1, hero2):

    Hero_1_NAME = f"{Fore.LIGHTCYAN_EX}{hero1.Name}{Style.RESET_ALL}"
    Hero_2_NAME = f"{Fore.GREEN}{hero2.Name}{Style.RESET_ALL}"
    Hero_1_HEALTH = f"{Fore.YELLOW}{hero1.Health}{Style.RESET_ALL}"
    Hero_2_HEALTH = f"{Fore.YELLOW}{hero2.Health}{Style.RESET_ALL}"
    Hero_1_PATTACK = f"{Fore.LIGHTCYAN_EX}{hero1.PhysicalAttack}{Style.RESET_ALL}"
    Hero_2_PATTACK = f"{Fore.GREEN}{hero2.PhysicalAttack}{Style.RESET_ALL}"
    Hero_1_PDEFENCE = f"{Fore.LIGHTCYAN_EX}{hero1.PhysicalDefence}{Style.RESET_ALL}"
    Hero_2_PDEFENCE = f"{Fore.GREEN}{hero2.PhysicalDefence}{Style.RESET_ALL}"
    Hero_1_MATTACK = f"{Fore.LIGHTCYAN_EX}{hero1.MagicAttack}{Style.RESET_ALL}"
    Hero_2_MATTACK = f"{Fore.GREEN}{hero2.MagicAttack}{Style.RESET_ALL}"
    Hero_1_MDEFENCE = f"{Fore.LIGHTCYAN_EX}{hero1.MagicDefence}{Style.RESET_ALL}"
    Hero_2_MDEFENCE = f"{Fore.GREEN}{hero2.MagicDefence}{Style.RESET_ALL}"
    Hero_1_STAMINA = f"{Fore.YELLOW}{hero1.Stamina}{Style.RESET_ALL}"
    Hero_1_MAGICKA = f"{Fore.YELLOW}{hero1.Magicka}{Style.RESET_ALL}"
    Hero_2_STAMINA = f"{Fore.YELLOW}{hero2.Stamina}{Style.RESET_ALL}"
    Hero_2_MAGICKA = f"{Fore.YELLOW}{hero2.Magicka}{Style.RESET_ALL}"
    Hero_1_STAMINA_RECOVERY = f"{Fore.YELLOW}{hero1.StaminaRecovery}{Style.RESET_ALL}"
    Hero_1_MAGICKA_RECOVERY = f"{Fore.YELLOW}{hero1.MagickaRecovery}{Style.RESET_ALL}"
    Hero_2_STAMINA_RECOVERY = f"{Fore.YELLOW}{hero2.StaminaRecovery}{Style.RESET_ALL}"
    Hero_2_MAGICKA_RECOVERY = f"{Fore.YELLOW}{hero2.MagickaRecovery}{Style.RESET_ALL}"

    battleOptions = ['Physical Attack', 'Magic Attack', 'Heal', 'Recover Stamina', 'Recover Magicka']
    healingOptions = ['Heal Self', 'Heal Hero', 'Heal All']
    attackOptions = ['Basic', 'Powerful', 'Ultimate']

    # battleModifier chance | 0.7 = 5% | 0.8 = 10% | 0.9 = 15% | 1.0 = 40% | 1.1 = 15% | 1.2 = 10% | 1.3 = 5%
    battleModifier = [0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4]
    battleMOD = random.choices(battleModifier, weight=(3, 6, 11, 58, 11, 7, 3, 1), k=8)

    # Hero 1 attacks Hero 2
    print(f"{Fore.LIGHTCYAN_EX}-- PLAYER 1 --------------------------------------------------{Style.RESET_ALL}\n")
    print(f"{Hero_1_NAME}'s  Health: {Fore.YELLOW}{hero1.Health}{Style.RESET_ALL}{Fore.LIGHTBLACK_EX}/{hero1.MaxHealth}{Style.RESET_ALL}  Stamina: {Fore.YELLOW}{hero1.Stamina}{Style.RESET_ALL}{Fore.LIGHTBLACK_EX}/{hero1.MaxStamina}{Style.RESET_ALL}  Magicka: {Fore.YELLOW}{hero1.Magicka}{Style.RESET_ALL}{Fore.LIGHTBLACK_EX}/{hero1.MaxMagicka}{Style.RESET_ALL}")
    print(f"{Hero_1_NAME}'s  Healing: {Fore.YELLOW}{hero1.Healing}{Style.RESET_ALL}{Fore.LIGHTBLACK_EX}/{hero1.MaxHealing}{Style.RESET_ALL}  Physical Attack: {Fore.RED}{hero1.PhysicalAttack}{Style.RESET_ALL}  Magic Attack: {Fore.MAGENTA}{hero1.MagicAttack}{Style.RESET_ALL}") 
    print(f"{Hero_1_NAME}'s  Ultimate Power: {Fore.YELLOW}{hero1.Ultimate}{Fore.LIGHTBLACK_EX}/100{Style.RESET_ALL}\n")
    print(f"{Fore.LIGHTCYAN_EX}--------------------------------------------------------------{Style.RESET_ALL}\n")
    print(f"{Hero_1_NAME}, what do you want to do?\n")
    battleOption = consoleFunctions.selectListValue(battleOptions)
    print('')

    if battleOption == 'Physical Attack':
        if hero1.Stamina >= 10:
            print(f"What {battleOption} should {Hero_1_NAME} use?\n")
            attackOption = consoleFunctions.selectListValue(attackOptions)
            
            if attackOption == 'Powerful':
                if hero1.Stamina >= 20:
                    Hero_1_PATTACK = int((hero1.PhysicalAttack * 1.5) * battleMOD)
                    damage_to_hero2 = max(0, Hero_1_PATTACK - hero2.PhysicalDefence)
                    damage_taken = hero2.take_damage(damage_to_hero2)
                    Damage = f"{Fore.RED}{damage_taken}{Style.RESET_ALL}"
                    energyUse = 20
                    hero1.use_stamina(energyUse)
                    hero1.Ultimate = min(100, hero1.Ultimate + 15)
                else:
                    print(f"{Hero_1_NAME} does not have enough stamina to use {Fore.RED}{battleOption} {attackOption}{Style.RESET_ALL}\n")
                    attackOption = 'Basic'

            if attackOption == 'Ultimate':
                if hero1.Stamina >= 10:
                    if hero1.Ultimate >= 50:
                        Hero_1_PATTACK = int((hero1.PhysicalAttack * 3) * battleMOD)
                        damage_to_hero2 = max(0, Hero_1_PATTACK - hero2.PhysicalDefence)
                        damage_taken = hero2.take_damage(damage_to_hero2)
                        Damage = f"{Fore.RED}{damage_taken}{Style.RESET_ALL}"
                        energyUse = 10
                        hero1.Ultimate = hero1.Ultimate - 50
                        hero1.use_stamina(energyUse)
                        Hero_1_PATTACK = hero1.PhysicalAttack * 3
                    else:
                        print(f"{Hero_1_NAME} does not have enough Ultimate Power to use {Fore.RED}{battleOption} {attackOption}{Style.RESET_ALL}\n")
                        attackOption = 'Basic'
                else:
                    print(f"{Hero_1_NAME} does not have enough stamina to use {Fore.RED}{battleOption} {attackOption}{Style.RESET_ALL}\n")
                    attackOption = 'Basic'

            if attackOption == 'Basic':
                Hero_1_PATTACK = int(hero1.PhysicalAttack * battleMOD)
                damage_to_hero2 = max(0, Hero_1_PATTACK - hero2.PhysicalDefence)
                damage_taken = hero2.take_damage(damage_to_hero2)
                Damage = f"{Fore.RED}{damage_taken}{Style.RESET_ALL}"
                energyUse = 10
                hero1.use_stamina(energyUse)
                hero1.Ultimate = min(100, hero1.Ultimate + 10)  

            print(f"\n{Fore.RED}--------------------------- ATTACK ---------------------------{Style.RESET_ALL}")
            print(f"\n{Hero_1_NAME} uses {Fore.YELLOW}{energyUse}{Style.RESET_ALL} stamina with a {Fore.RED}{attackOption} {battleOption}{Style.RESET_ALL}.")
            print(f"{Hero_1_NAME} attacks {Hero_2_NAME} with {Fore.LIGHTCYAN_EX}{Hero_1_PATTACK}{Style.RESET_ALL} power.")
            print(f"{Hero_2_NAME} defends the attack with {Hero_2_PDEFENCE} power")
            print(f"{Hero_1_NAME} deals {Damage} damage.\n")
            print(f"{Fore.RED}--------------------------------------------------------------{Style.RESET_ALL}\n")
        else:
            print(f"\n{Fore.YELLOW}-------------------------- RECOVERY --------------------------{Style.RESET_ALL}")
            print(f"\n{Hero_1_NAME} does not have enough stamina to attack. Remaining Stamina: {Hero_1_STAMINA}")
            recover_stamina = hero1.recover_stamina()
            print(f"{Hero_1_NAME} recovers {Fore.YELLOW}{recover_stamina}{Style.RESET_ALL} stamina.\n")
            print(f"{Fore.YELLOW}--------------------------------------------------------------{Style.RESET_ALL}\n")

    if battleOption == 'Magic Attack':
        if hero1.Magicka >= 10:
            print(f"What {battleOption} should {Hero_1_NAME} use?\n")
            attackOption = consoleFunctions.selectListValue(attackOptions)

            if attackOption == 'Powerful':
                if hero1.Magicka >= 20:
                    Hero_1_MATTACK = int((hero1.MagicAttack * 1.5) * battleMOD)
                    damage_to_hero2 = max(0, Hero_1_MATTACK - hero2.MagicDefence)
                    damage_taken = hero2.take_damage(damage_to_hero2)
                    Damage = f"{Fore.MAGENTA}{damage_taken}{Style.RESET_ALL}"
                    energyUse = 20
                    hero1.use_magicka(energyUse)
                    hero1.Ultimate = min(100, hero1.Ultimate + 15)
                    Hero_1_MATTACK = hero1.MagicAttack * 1.5
                else:
                    print(f"{Hero_1_NAME} does not have enough magicka to use {Fore.MAGENTA}{battleOption} {attackOption}{Style.RESET_ALL}\n")
                    attackOption = 'Basic'

            if attackOption == 'Ultimate':
                if hero1.Magicka >= 10:
                    if hero1.Ultimate >= 50:
                        Hero_1_MATTACK = int((hero1.MagicAttack * 3) * battleMOD)
                        damage_to_hero2 = max(0, Hero_1_MATTACK - hero2.MagicDefence)
                        damage_taken = hero2.take_damage(damage_to_hero2)
                        Damage = f"{Fore.MAGENTA}{damage_taken}{Style.RESET_ALL}"
                        energyUse = 10
                        hero1.Ultimate = hero1.Ultimate - 50
                        hero1.use_magicka(energyUse)
                        Hero_1_MATTACK = hero1.MagicAttack * 3
                    else:
                        print(f"{Hero_1_NAME} does not have enough Ultimate Power to use {Fore.MAGENTA}{battleOption} {attackOption}{Style.RESET_ALL}\n")
                        attackOption = 'Basic'
                else:
                    print(f"{Hero_1_NAME} does not have enough magicka to use {Fore.MAGENTA}{battleOption} {attackOption}{Style.RESET_ALL}\n")
                    attackOption = 'Basic'
                
            if attackOption == 'Basic':
                Hero_1_MATTACK = int(hero1.MagicAttack * battleMOD)
                damage_to_hero2 = max(0, Hero_1_MATTACK - hero2.MagicDefence)
                damage_taken = hero2.take_damage(damage_to_hero2)
                Damage = f"{Fore.MAGENTA}{damage_taken}{Style.RESET_ALL}"
                energyUse = 10
                hero1.use_magicka(energyUse)
                hero1.Ultimate = min(100, hero1.Ultimate + 10)
            
            print(f"\n{Fore.MAGENTA}--------------------------- ATTACK ---------------------------{Style.RESET_ALL}")
            print(f"\n{Hero_1_NAME} uses {Fore.YELLOW}{energyUse}{Style.RESET_ALL} magicka with a {Fore.MAGENTA}{attackOption} {battleOption}{Style.RESET_ALL}.")
            print(f"{Hero_1_NAME} attacks {Hero_2_NAME} with {Fore.LIGHTCYAN_EX}{Hero_1_MATTACK}{Style.RESET_ALL} power.")
            print(f"{Hero_2_NAME} defends the attack with {Hero_2_MDEFENCE}")
            print(f"{Hero_1_NAME} deals {Damage} damage.\n")
            print(f"{Fore.MAGENTA}--------------------------------------------------------------{Style.RESET_ALL}\n")
        else:
            print(f"\n{Fore.YELLOW}-------------------------- RECOVERY --------------------------{Style.RESET_ALL}")
            print(f"\n{Hero_1_NAME} does not have enough magicka to attack. Remaining Magicka: {Hero_1_MAGICKA}")
            recover_magicka = hero1.recover_magicka()
            print(f"{Hero_1_NAME} recovers {Fore.YELLOW}{recover_magicka}{Style.RESET_ALL} magicka.\n")
            print(f"{Fore.YELLOW}--------------------------------------------------------------{Style.RESET_ALL}\n")

    if battleOption == 'Recover Stamina':
        if hero1.Stamina < hero1.MaxStamina:
            recover_stamina = hero1.recover_stamina()
            print(f"\n{Fore.YELLOW}-------------------------- RECOVERY --------------------------{Style.RESET_ALL}")
            print(f"\n{Hero_1_NAME} recovers {Fore.YELLOW}{recover_stamina}{Style.RESET_ALL} Stamina.\n")
            print(f"{Fore.YELLOW}--------------------------------------------------------------{Style.RESET_ALL}\n")
        else:
            print(f"{Hero_1_NAME}'s stamina is already full.\n")
            print(f"{Hero_1_NAME} misses a turn.\n")
    
    if battleOption == 'Recover Magicka':
        if hero1.Magicka < hero1.MaxMagicka:
            recover_magicka = hero1.recover_magicka()
            print(f"\n{Fore.YELLOW}-------------------------- RECOVERY --------------------------{Style.RESET_ALL}")
            print(f"\n{Hero_1_NAME} recovers {Fore.YELLOW}{recover_magicka}{Style.RESET_ALL} Magicka.\n")
            print(f"{Fore.YELLOW}--------------------------------------------------------------{Style.RESET_ALL}\n")
        else:
            print(f"{Hero_1_NAME}'s magicka is already full.\n")
            print(f"{Hero_1_NAME} misses a turn.\n")

    if battleOption == 'Heal':
        if hero1.Healing > 1:
            if hero1.Health < hero1.MaxHealth:
                recover_health = hero1.recover_health()
                hero1.Healing = max(0, hero1.Healing - 2)
                print(f"\n{Fore.YELLOW}---------------------------- HEAL ----------------------------{Style.RESET_ALL}")
                print(f"\n{Hero_1_NAME} recovers {Fore.YELLOW}{recover_health}{Style.RESET_ALL} Health.\n")
                print(f"{Fore.YELLOW}--------------------------------------------------------------{Style.RESET_ALL}\n")
            else:
                print(f"{Hero_1_NAME}'s health is already full.\n")
                print(f"{Hero_1_NAME} misses a turn.\n")
        else:
            print(f"{Hero_1_NAME} does not have enough healing left.\n")
            print(f"{Hero_1_NAME} misses a turn.\n")

    # Check if Hero 2 is defeated
    if hero2.Health <= 0:
        print(f"\n{Fore.LIGHTYELLOW_EX}---------------------------- GAME OVER ------------------------{Style.RESET_ALL}\n")
        print(f"{Hero_2_NAME} has been defeated!")
        print(f"{Hero_1_NAME} wins.\n")
        print(f"{Fore.LIGHTYELLOW_EX}---------------------------------------------------------------{Style.RESET_ALL}\n")
        return
        
    # Hero 2 attacks Hero 1
    print(f"{Fore.GREEN}-- PLAYER 2 --------------------------------------------------{Style.RESET_ALL}\n")
    print(f"{Hero_2_NAME}'s  Health: {Fore.YELLOW}{hero2.Health}{Style.RESET_ALL}{Fore.LIGHTBLACK_EX}/{hero2.MaxHealth}{Style.RESET_ALL}  Stamina: {Fore.YELLOW}{hero2.Stamina}{Style.RESET_ALL}{Fore.LIGHTBLACK_EX}/{hero2.MaxStamina}{Style.RESET_ALL}  Magicka: {Fore.YELLOW}{hero2.Magicka}{Style.RESET_ALL}{Fore.LIGHTBLACK_EX}/{hero2.MaxMagicka}{Style.RESET_ALL}")
    print(f"{Hero_2_NAME}'s  Healing: {Fore.YELLOW}{hero2.Healing}{Style.RESET_ALL}{Fore.LIGHTBLACK_EX}/{hero2.MaxHealing}{Style.RESET_ALL}  Physical Attack: {Fore.RED}{hero2.PhysicalAttack}{Style.RESET_ALL}  Magic Attack: {Fore.MAGENTA}{hero2.MagicAttack}{Style.RESET_ALL}") 
    print(f"{Hero_2_NAME}'s  Ultimate Power: {Fore.YELLOW}{hero2.Ultimate}{Fore.LIGHTBLACK_EX}/100{Style.RESET_ALL}\n")
    print(f"{Fore.GREEN}--------------------------------------------------------------{Style.RESET_ALL}\n")
    print(f"{Hero_2_NAME}, what do you want to do?\n")
    battleOption = consoleFunctions.selectListValue(battleOptions)
    print('')

    if battleOption == 'Physical Attack':
        if hero2.Stamina >= 10:
            print(f"What {battleOption} should {Hero_2_NAME} use?\n")
            attackOption = consoleFunctions.selectListValue(attackOptions)

            if attackOption == 'Powerful':
                if hero2.Stamina >= 20:
                    Hero_2_PATTACK = int((hero2.PhysicalAttack * 1.5) * battleMOD)
                    damage_to_hero1 = max(0, Hero_2_PATTACK - hero1.PhysicalDefence)
                    damage_taken = hero1.take_damage(damage_to_hero1)
                    Damage = f"{Fore.RED}{damage_taken}{Style.RESET_ALL}"
                    energyUse = 20
                    hero2.use_stamina(energyUse)
                    hero2.Ultimate = min(100, hero2.Ultimate + 15)
                    Hero_2_PATTACK = hero2.PhysicalAttack * 1.5
                else:
                    print(f"{Hero_2_NAME} does not have enough stamina to use {Fore.RED}{battleOption} {attackOption}{Style.RESET_ALL}\n")
                    attackOption = 'Basic'
            
            if attackOption == 'Ultimate':
                if hero2.Stamina >= 10:
                    if hero2.Ultimate >= 50:
                        Hero_2_PATTACK = int((hero2.PhysicalAttack * 3) * battleMOD)
                        damage_to_hero1 = max(0, Hero_2_PATTACK - hero1.PhysicalDefence)
                        damage_taken = hero1.take_damage(damage_to_hero1)
                        Damage = f"{Fore.RED}{damage_taken}{Style.RESET_ALL}"
                        energyUse = 10
                        hero2.Ultimate = hero2.Ultimate - 50
                        hero2.use_stamina(energyUse)
                        Hero_2_PATTACK = hero2.PhysicalAttack * 3
                    else:
                        print(f"{Hero_2_NAME} does not have enough Ultimate Power to use {Fore.RED}{battleOption} {attackOption}{Style.RESET_ALL}\n")
                        attackOption = 'Basic'
                else:
                    print(f"{Hero_2_NAME} does not have enough stamina to use {Fore.RED}{battleOption} {attackOption}{Style.RESET_ALL}\n")
                    attackOption = 'Basic'

            if attackOption == 'Basic':
                Hero_2_PATTACK = int(hero2.PhysicalAttack * battleMOD)
                damage_to_hero1 = max(0, Hero_2_PATTACK - hero1.PhysicalDefence)
                damage_taken = hero1.take_damage(damage_to_hero1)
                Damage = f"{Fore.RED}{damage_taken}{Style.RESET_ALL}"
                energyUse = 10
                hero2.use_stamina(energyUse)
                hero2.Ultimate = min(100, hero2.Ultimate + 10)

            print(f"\n{Fore.RED}--------------------------- ATTACK ---------------------------{Style.RESET_ALL}")
            print(f"\n{Hero_2_NAME} uses {Fore.YELLOW}{energyUse}{Style.RESET_ALL} stamina with a {Fore.RED}{attackOption} {battleOption}{Style.RESET_ALL}.")
            print(f"{Hero_2_NAME} attacks {Hero_1_NAME} with {Fore.GREEN}{Hero_2_PATTACK}{Style.RESET_ALL} power.")
            print(f"{Hero_1_NAME} defends the attack with {Hero_1_PDEFENCE} power")
            print(f"{Hero_2_NAME} deals {Damage} damage.\n")
            print(f"{Fore.RED}--------------------------------------------------------------{Style.RESET_ALL}\n")
        else:
            print(f"\n{Fore.YELLOW}-------------------------- RECOVERY --------------------------{Style.RESET_ALL}")
            print(f"\n{Hero_2_NAME} does not have enough stamina to attack. Remaining Stamina: {Hero_2_STAMINA}\n")
            recover_stamina = hero2.recover_stamina()
            print(f"{Hero_2_NAME} recovers {Fore.YELLOW}{recover_stamina}{Style.RESET_ALL} stamina.\n")
            print(f"{Fore.YELLOW}--------------------------------------------------------------{Style.RESET_ALL}\n")

    if battleOption == 'Magic Attack':
        if hero2.Magicka >= 10:
            print(f"What {battleOption} should {Hero_2_NAME} use?\n")
            attackOption = consoleFunctions.selectListValue(attackOptions)

            if attackOption == 'Powerful':
                if hero2.Magicka >= 20:
                    Hero_2_MATTACK = int((hero2.MagicAttack * 1.5) * battleMOD)
                    damage_to_hero1 = max(0, Hero_2_MATTACK - hero1.MagicDefence)
                    damage_taken = hero1.take_damage(damage_to_hero1)
                    Damage = f"{Fore.MAGENTA}{damage_taken}{Style.RESET_ALL}"
                    energyUse = 20
                    hero2.use_magicka(energyUse)
                    hero2.Ultimate = min(100, hero2.Ultimate + 15)
                    Hero_2_MATTACK = hero2.MagicAttack * 1.5
                else:
                    print(f"{Hero_2_NAME} does not have enough magica to use {Fore.MAGENTA}{battleOption} {attackOption}{Style.RESET_ALL}\n")
                    attackOption = 'Basic'

            if attackOption == 'Ultimate':
                if hero2.Magicka >= 10:
                    if hero2.Ultimate >= 50:
                        Hero_2_MATTACK = int((hero2.MagicAttack * 3) * battleMOD)
                        damage_to_hero1 = max(0, Hero_2_MATTACK - hero1.MagicDefence)
                        damage_taken = hero1.take_damage(damage_to_hero1)
                        Damage = f"{Fore.MAGENTA}{damage_taken}{Style.RESET_ALL}"
                        energyUse = 10
                        hero2.Ultimate = hero2.Ultimate - 50
                        hero2.use_magicka(energyUse)
                        Hero_2_MATTACK = hero2.MagicAttack * 3
                    else:
                        print(f"{Hero_2_NAME} does not have enough Ultimate Power to use {Fore.MAGENTA}{battleOption} {attackOption}{Style.RESET_ALL}\n")
                        attackOption = 'Basic'
                else:
                    print(f"{Hero_2_NAME} does not have enough magicka to use {Fore.MAGENTA}{battleOption} {attackOption}{Style.RESET_ALL}\n")
                    attackOption = 'Basic'
            
            if attackOption == 'Basic':
                Hero_2_MATTACK = int(hero2.MagicAttack * battleMOD)
                damage_to_hero1 = max(0, Hero_2_MATTACK - hero1.MagicDefence)
                damage_taken = hero1.take_damage(damage_to_hero1)
                Damage = f"{Fore.MAGENTA}{damage_taken}{Style.RESET_ALL}"
                energyUse = 10
                hero2.use_magicka(energyUse)
                hero2.Ultimate = min(100, hero2.Ultimate + 10)
        
            print(f"\n{Fore.MAGENTA}--------------------------- ATTACK ---------------------------{Style.RESET_ALL}")
            print(f"\n{Hero_2_NAME} uses {Fore.YELLOW}{energyUse}{Style.RESET_ALL} magicka with a {Fore.MAGENTA}{attackOption} {battleOption}{Style.RESET_ALL}.")
            print(f"{Hero_2_NAME} attacks {Hero_1_NAME} with {Fore.GREEN}{Hero_2_MATTACK}{Style.RESET_ALL} power.")
            print(f"{Hero_1_NAME} defends the attack with {Hero_1_MDEFENCE}")
            print(f"{Hero_2_NAME} deals {Damage} damage.\n")
            print(f"{Fore.MAGENTA}--------------------------------------------------------------{Style.RESET_ALL}\n")
        else:
            print(f"\n{Fore.YELLOW}-------------------------- RECOVERY --------------------------{Style.RESET_ALL}")
            print(f"\n{Hero_2_NAME} does not have enough magicka to attack. Remaining Magicka: {Hero_2_MAGICKA}\n")
            recover_magicka = hero2.recover_magicka()
            print(f"{Hero_2_NAME} recovers {Fore.YELLOW}{recover_magicka}{Style.RESET_ALL} magicka.\n")
            print(f"{Fore.YELLOW}--------------------------------------------------------------{Style.RESET_ALL}\n")

    if battleOption == 'Recover Stamina':
        if hero2.Stamina < hero2.MaxStamina:
            recover_stamina = hero2.recover_stamina()
            print(f"\n{Fore.YELLOW}-------------------------- RECOVERY --------------------------{Style.RESET_ALL}")
            print(f"\n{Hero_2_NAME} recovers {Fore.YELLOW}{recover_stamina}{Style.RESET_ALL} Stamina.\n")
            print(f"{Fore.YELLOW}--------------------------------------------------------------{Style.RESET_ALL}\n")
        else:
            print(f"{Hero_2_NAME}'s stamina is already full.\n")
            print(f"{Hero_2_NAME} misses a turn.\n")

    if battleOption == 'Recover Magicka':
        if hero2.Magicka < hero2.MaxMagicka:
            recover_magicka = hero2.recover_magicka()
            print(f"\n{Fore.YELLOW}-------------------------- RECOVERY --------------------------{Style.RESET_ALL}")
            print(f"\n{Hero_2_NAME} recovers {Fore.YELLOW}{recover_magicka}{Style.RESET_ALL} Magicka.\n")
            print(f"{Fore.YELLOW}--------------------------------------------------------------{Style.RESET_ALL}\n")
        else:
            print(f"{Hero_2_NAME}'s magicka is already full.\n")
            print(f"{Hero_2_NAME} misses a turn.\n")

    if battleOption == 'Heal':
        if hero2.Healing > 1:
            if hero2.Health < hero2.MaxHealth:
                recover_health = hero2.recover_health()
                hero2.Healing = max(0, hero2.Healing - 2)
                print(f"\n{Fore.YELLOW}---------------------------- HEAL ----------------------------{Style.RESET_ALL}")
                print(f"\n{Hero_2_NAME} recovers {Fore.YELLOW}{recover_health}{Style.RESET_ALL} Health.\n")
                print(f"{Fore.YELLOW}--------------------------------------------------------------{Style.RESET_ALL}\n")
            else:
                print(f"{Hero_2_NAME}'s health is already full.\n")
                print(f"{Hero_2_NAME} misses a turn.\n")
        else:
            print(f"{Hero_2_NAME} does not have enough healing left.\n")
            print(f"{Hero_2_NAME} misses a turn.\n")

    # Check if Hero 1 is defeated
    if hero1.Health <= 0:
        print(f"\n{Fore.LIGHTYELLOW_EX}---------------------------- GAME OVER ------------------------{Style.RESET_ALL}\n")
        print(f"{Hero_1_NAME} has been defeated!")
        print(f"{Hero_2_NAME} wins.\n")
        print(f"{Fore.LIGHTYELLOW_EX}---------------------------------------------------------------{Style.RESET_ALL}\n")
        return

def startBattle():
    heroesData = selectHeroes()
    heroes = []

    for hero in heroesData:
        heroData = hero.to_dict()
        Ultimate = 0
        hero = Hero(heroData['Name'], heroData['SecondaryStats']['Health'], heroData['SecondaryStats']['Stamina'], heroData['SecondaryStats']['Magicka'], heroData['BattleStats']['Healing'], heroData['SecondaryStats']['HealthRecovery'], heroData['SecondaryStats']['StaminaRecovery'], heroData['SecondaryStats']['MagickaRecovery'], heroData['BattleStats']['PhysicalAttack'], heroData['BattleStats']['PhysicalDefence'], heroData['BattleStats']['MagicAttack'], heroData['BattleStats']['MagicDefence'], Ultimate)
        heroes.append(hero)

    hero1 = heroes[0]
    hero2 = heroes[1]

    print(f"\nBattle begins between {Fore.LIGHTCYAN_EX}{hero1.Name}{Style.RESET_ALL} and {Fore.GREEN}{hero2.Name}{Style.RESET_ALL}! \n")

    round = 0
    while hero1.Health > 0 and hero2.Health > 0:    
        round = round + 1
        if round > 20:
            print(f"\n{Fore.LIGHTYELLOW_EX}---------------------------- GAME OVER ------------------------{Style.RESET_ALL}\n")
            print(f'{Fore.YELLOW}Battle Over: Time is up!{Style.RESET_ALL}')
            print(f'{hero2.Name} wins\n')
            print(f"{Fore.LIGHTYELLOW_EX}---------------------------------------------------------------{Style.RESET_ALL}\n")
            return
        else:
            print(f"{Fore.YELLOW}-- ROUND {round}{Style.RESET_ALL}\n")
            battle_round(hero1, hero2)