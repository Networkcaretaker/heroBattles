import click
from colorama import Fore, Style

# Select a value from list by number
def selectListValue(data):
    for i, value in enumerate(data, start=1):
        click.echo(f"{i}. {value}")
    
    print("")
    selection = click.prompt(f"{Fore.LIGHTCYAN_EX}Enter the number of your selection{Style.RESET_ALL}", type=int)

    x = 'false'

    while x == 'false':
    
        if 1 <= selection <= len(data):
            x = 'true'
            selected_value = data[selection - 1]
        else:
            click.echo(f"\n{Fore.RED}Invalid selection. Please try again.{Style.RESET_ALL}\n")
            for i, value in enumerate(data, start=1):
                click.echo(f"{i}. {value}")
        
            print("")
            selection = click.prompt(f"{Fore.LIGHTCYAN_EX}Enter the number of your selection{Style.RESET_ALL}", type=int)

    return(selected_value)