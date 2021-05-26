import inquirer
from inquirer.themes import GreenPassion
from colorama import Fore, Back, Style


# Choose one
def define_list(name, message, options):
    questions = [
    inquirer.List(name,
                    message=message,
                    choices=options
                    ),
    ]
    answers = inquirer.prompt(questions, theme=GreenPassion())
    response = answers[name]
    return response


# Choose many
def define_checkbox(name, message, options):
    questions = [
    inquirer.Checkbox(name,
                    message=message,
                    choices=options
                    ),
    ]
    answers = inquirer.prompt(questions, theme=GreenPassion())
    response = answers[name]
    return response
