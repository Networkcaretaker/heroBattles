import click

# Select a value from list by number
def selectListValue(data):
    for i, value in enumerate(data, start=1):
        click.echo(f"{i}. {value}")
    
    selection = click.prompt("Enter the number of your selection", type=int)
    
    if 1 <= selection <= len(data):
            selected_value = data[selection - 1]
    else:
        click.echo("Invalid selection. Please try again.")
        selection = click.prompt("Enter the number of your selection", type=int)

    return(selected_value)