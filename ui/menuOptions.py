import utilities.consoleFunctions as consoleFunctions
import functions.battleFunctions as battleFunctions
import functions.heroFunctions as heroFunctions
import functions.backendFunctions as backendFunctions
from colorama import Fore, Style

def Main_Menu():
    mainMenu = [
        'Start Battle',
        'View Heroes',
        'Create Hero',
        'Player Info',
        'System Options',
        'Exit Game'
    ]
    systemOptions = [
        'Update Race Data',
        'Update Class Data',
        'Update Role Data',
        'Update Hero Data',
        'Go Back'
    ]
    validFileType = [
        'CSV',
        'JSON'
    ]

    print(f"\n{Fore.YELLOW}WELCOME TO HERO BATTLES{Style.RESET_ALL}\n")
    selectFunction = consoleFunctions.selectListValue(mainMenu)

    while selectFunction != '':

        if selectFunction == 'Start Battle':
            battleFunctions.startBattle()
            selectFunction = consoleFunctions.selectListValue(mainMenu)

        if selectFunction == 'View Heroes':
            print(f'\n{Fore.YELLOW}View Heroes{Style.RESET_ALL}\n')
            selectFunction = consoleFunctions.selectListValue(mainMenu)

        if selectFunction == 'Create Hero':
            heroFunctions.createNewHeroesFromInput()
            selectFunction = consoleFunctions.selectListValue(mainMenu)

        if selectFunction == 'Player Info':
            print(f'\n{Fore.YELLOW}Player Info{Style.RESET_ALL}\n')
            selectFunction = consoleFunctions.selectListValue(mainMenu)

        if selectFunction == 'System Options':
            print(f'\n{Fore.YELLOW}System Options{Style.RESET_ALL}\n')
            selectFunction = consoleFunctions.selectListValue(systemOptions)

            if selectFunction == 'Update Race Data':
                print(f'\n{Fore.YELLOW}Update Race Data{Style.RESET_ALL}\n')
                backendFunctions.uploadHeroRaceFromCsvToFirebase()
                selectFunction = consoleFunctions.selectListValue(systemOptions)

            if selectFunction == 'Update Class Data':
                print(f'\n{Fore.YELLOW}Update Class Data{Style.RESET_ALL}\n')
                backendFunctions.uploadHeroClassFromCsvToFirebase()
                selectFunction = consoleFunctions.selectListValue(systemOptions)

            if selectFunction == 'Update Role Data':
                print(f'\n{Fore.YELLOW}Update Role Data{Style.RESET_ALL}\n')
                backendFunctions.uploadHeroRoleFromCsvToFirebase()
                selectFunction = consoleFunctions.selectListValue(systemOptions)

            if selectFunction == 'Update Hero Data':
                print(f'\n{Fore.YELLOW}Update Hero Data{Style.RESET_ALL}\n')
                selectFileType = input("Select File Type (CSV or JSON): ")
                while selectFileType not in validFileType:
                    print(f'{Fore.RED}Error:{Style.RESET_ALL} Select a valid file type.')
                    selectFileType = input("Select File Type (CSV or JSON): ")
                if selectFileType == 'CSV':
                    print(f'{Fore.RED}Warning:{Style.RESET_ALL} This function will overwrite the saved JSON file \n Do you want to continue? (Type NO to cancel)')
                    warningCheck = input("Continue: ")
                    if warningCheck == 'NO':
                        print(f"\{Fore.GREEN}Update Hero Data{Style.RESET_ALL} cancelled\n")
                        selectFunction = consoleFunctions.selectListValue(systemOptions)

                heroFunctions.createNewHeroesFromFile(selectFileType)
                selectFunction = consoleFunctions.selectListValue(systemOptions)

            if selectFunction == 'Go Back':
                print(f'\n{Fore.YELLOW}Main Menu{Style.RESET_ALL}\n')
                selectFunction = consoleFunctions.selectListValue(mainMenu)

        if selectFunction == 'Exit Game':
            print(f'\n{Fore.YELLOW}Exit Game{Style.RESET_ALL}\n')
            exit()




