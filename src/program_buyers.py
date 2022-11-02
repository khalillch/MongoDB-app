import datetime
from colorama import Fore
from dateutil import parser

from infrastructure.switchlang import switch
import infrastructure.state as state
import services.data_service as svc


def run():
    print(' ****************** Welcome buyer **************** ')
    print()

    show_commands()

    while True:
        action = get_action()

        with switch(action) as s:
            s.case('c', create_account)
            s.case('a', create_account)
            s.case('l', log_into_account)
            s.case('d', list_dogs)
            s.case('t', take_dog)
            s.case('y', list_cages)
            s.case('r', register_cage)
            """
            s.case('u', update_availability)
            """
            s.case('m', lambda: 'change_mode')
            s.case(['x', 'bye', 'exit', 'exit()'], exit_app)
            s.case('?', show_commands)
            s.case('', lambda: None)
            s.default(unknown_command)

        if action:
            print()

        if s.result == 'change_mode':
            return


def show_commands():
    print('What action would you like to take:')
    print('[C]reate an [a]ccount')
    print('[L]ogin to your account')
    print('View [D]ogs')
    print('[T]ake a dog home with you :))')
    print('[R]egister a cage')
    print('List cages [y]')
    print('[U]pdate cage availability')
    print('[V]iew your bookings')
    print('Change [M]ode (guest or host)')
    print('e[X]it app')
    print('[?] Help (this info)')
    print()


def create_account():
    print(' ****************** REGISTER **************** ')
    name = input("your name:")
    email = input("your email:")
    if svc.find_account_by_email(email):
        error_msg("ERROR: email already used")
        return
    state.active_account = svc.create_account(name, email)
    success_msg(f"Created new account with id {state.active_account.id}.")


def log_into_account():
    print(' ****************** LOGIN **************** ')
    email = input("your email: ")
    account = svc.find_account_by_email(email)
    if not account:
        error_msg("ERROR: There is no such account")
        return
    state.active_account = account
    success_msg('Logged in successfully.')


def list_dogs():
    print(' ****************** List of available dogs **************** ')
    dogs = svc.find_dogs()
    if not dogs:
        error_msg("Sorry there is no dogs available")
        return
    success_msg("Available dogs: ")
    print(dogs)


def take_dog():
    print(" ****************** Take a dog **************** ")
    if not state.active_account:
        error_msg("Please Login")
        return
    account = state.active_account
    name = input("Dog's name : ")
    size = input("Dog's size : ")
    if not svc.find_dog(name, size):
        error_msg("There is no dog with such a description")
        return
    svc.delete_dog(name, size)
    svc.add_dog_to_customer(account.id, name)
    success_msg(f"Congratulations you will take the dog home with you")


def register_cage():
    size = input("give the cage's size : ")
    cage = svc.create_cage(size)
    success_msg(f"Cage with id {cage.id} created successfully !")


def list_cages():
    cages = svc.find_cages()
    if not cages:
        error_msg("ERROR: There is no available cage for now")
        return
    success_msg("The available cages are:")
    print(cages)


def get_action():
    text = '> '
    if state.active_account:
        text = f'{state.active_account.name}> '

    action = input(Fore.YELLOW + text + Fore.WHITE)
    return action.strip().lower()


def exit_app():
    print()
    print('bye')
    raise KeyboardInterrupt()


def unknown_command():
    print("Sorry we didn't understand that command.")


def success_msg(text):
    print(Fore.LIGHTGREEN_EX + text + Fore.WHITE)


def error_msg(text):
    print(Fore.LIGHTRED_EX + text + Fore.WHITE)


"""

def log_into_account():
    print(' ****************** LOGIN **************** ')

    email = input('What is your email? ').strip().lower()
    account = svc.find_account_by_email(email)

    if not account:
        error_msg(f'Could not find account with email {email}.')
        return

    state.active_account = account
    success_msg('Logged in successfully.')


def register_cage():
    print(' ****************** REGISTER CAGE **************** ')

    if not state.active_account:
        error_msg('You must login first to register a cage.')
        return

    meters = input('How many square meters is the cage? ')
    if not meters:
        error_msg('Cancelled')
        return

    meters = float(meters)
    carpeted = input("Is it carpeted [y, n]? ").lower().startswith('y')
    has_toys = input("Have snake toys [y, n]? ").lower().startswith('y')
    allow_dangerous = input("Can you host venomous snakes [y, n]? ").lower().startswith('y')
    name = input("Give your cage a name: ")
    price = float(input("How much are you charging?  "))

    cage = svc.register_cage(
        state.active_account, name,
        allow_dangerous, has_toys, carpeted, meters, price
    )

    state.reload_account()
    success_msg(f'Register new cage with id {cage.id}.')


def list_cages(suppress_header=False):
    if not suppress_header:
        print(' ******************     Your cages     **************** ')

    if not state.active_account:
        error_msg('You must login first to register a cage.')
        return

    cages = svc.find_cages_for_user(state.active_account)
    print(f"You have {len(cages)} cages.")
    for idx, c in enumerate(cages):
        print(f' {idx + 1}. {c.name} is {c.square_meters} meters.')
        for b in c.bookings:
            print('      * Booking: {}, {} days, booked? {}'.format(
                b.check_in_date,
                (b.check_out_date - b.check_in_date).days,
                'YES' if b.booked_date is not None else 'no'
            ))


def update_availability():
    print(' ****************** Add available date **************** ')

    if not state.active_account:
        error_msg("You must log in first to register a cage")
        return

    list_cages(suppress_header=True)

    cage_number = input("Enter cage number: ")
    if not cage_number.strip():
        error_msg('Cancelled')
        print()
        return

    cage_number = int(cage_number)

    cages = svc.find_cages_for_user(state.active_account)
    selected_cage = cages[cage_number - 1]

    success_msg("Selected cage {}".format(selected_cage.name))

    start_date = parser.parse(
        input("Enter available date [yyyy-mm-dd]: ")
    )
    days = int(input("How many days is this block of time? "))

    svc.add_available_date(
        selected_cage,
        start_date,
        days
    )

    success_msg(f'Date added to cage {selected_cage.name}.')


def view_bookings():
    print(' ****************** Your bookings **************** ')

    if not state.active_account:
        error_msg("You must log in first to register a cage")
        return

    cages = svc.find_cages_for_user(state.active_account)

    bookings = [
        (c, b)
        for c in cages
        for b in c.bookings
        if b.booked_date is not None
    ]

    print("You have {} bookings.".format(len(bookings)))
    for c, b in bookings:
        print(' * Cage: {}, booked date: {}, from {} for {} days.'.format(
            c.name,
            datetime.date(b.booked_date.year, b.booked_date.month, b.booked_date.day),
            datetime.date(b.check_in_date.year, b.check_in_date.month, b.check_in_date.day),
            b.duration_in_days
        ))



"""