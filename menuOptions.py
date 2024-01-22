import consoleFunctions
import battleFunctions
import heroFunctions
from colorama import Fore, Style

def Main_Menu():
    mainMenu = [
        'Start Battle',
        'View Heroes',
        'Create Hero',
        'Player Info',
        'Exit Game'
    ]

    print(f"\n{Fore.YELLOW}WELCOME TO HERO BATTLES{Style.RESET_ALL}\n")
    selectFunction = consoleFunctions.selectListValue(mainMenu)

    if selectFunction == 'Start Battle':
        battleFunctions.startBattle()

    if selectFunction == 'View Heroes':
        print('View Heroes')

    if selectFunction == 'Create Hero':
        heroFunctions.createNewHeroesFromInput()

    if selectFunction == 'Player Info':
        print('Player Info')

    if selectFunction == 'Exit Game':
        print('Exit Game')


