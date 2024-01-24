import utilities.consoleFunctions as consoleFunctions
import functions.battleFunctions as battleFunctions
import functions.heroFunctions as heroFunctions
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
        print(f'\n{Fore.YELLOW}View Heroes{Style.RESET_ALL}\n')

    if selectFunction == 'Create Hero':
        heroFunctions.createNewHeroesFromInput()

    if selectFunction == 'Player Info':
        print(f'\n{Fore.YELLOW}Player Info{Style.RESET_ALL}\n')

    if selectFunction == 'Exit Game':
        print(f'\n{Fore.YELLOW}Exit Game{Style.RESET_ALL}\n')


