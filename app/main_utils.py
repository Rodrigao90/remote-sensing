from donwload_api import *

def welcome_message():
    print('\nWelcome to CARTOGRAFIAS RÁPIDAS!\n')

def task_options():
    task = input('What would you like to do?\n\n' \
            'a. Download products;\n' \
            'b. Preprocess products;\n' \
            'c. Generate DEM;\n' \
            'd. Exit. \n\n' \
            'r: ')
    return task

def to_string(task):
    if isinstance(task, str):
        return task
    else:
        return str(task)

def to_lowercase(task):
    return task.lower()

def check_task_option(task):
    if task == 'a':
        print('\n"Download products" selected! ')
        return 0

    elif task == 'b':
        print('\n"Preprocess products" selected! ')
        return 0

    elif task == 'c':
        print('\n"Generate DEM" selected! ')
        return 0

    elif task == 'd':
        print('\nExiting system...')
        quit()

    else:
        print('\nInvalid option! Try again!')
        return -1
