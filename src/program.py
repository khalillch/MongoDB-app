from colorama import Fore
import program_surrenders
import program_buyers
import data.mongo_setup as mongo_setup


def main():
    mongo_setup.global_init()

    print_header()

    try:
        while True:
            choice = find_user_intent()
            if choice == 'give':
                program_surrenders.run()
            elif choice == 'take':
                program_buyers.run()
            else:
                print("Not a valid choice !!")
                print("Please choose [t] or [g].")
    except KeyboardInterrupt:
        return


def print_header():

    print(Fore.GREEN + "**************** Khalil's dog shelter   ****************")
    print()
    print(Fore.WHITE + "Welcome to Snake BnB!")
    print("Why are you here?")
    print()


def find_user_intent():
    print("[g] Give a dog to the shelter :(((")
    print("[t] Take a beautiful dog(s) with you :)))")
    print()
    choice = input("g/t ? ")
    if choice == 't':
        return 'take'
    if choice == 'g':
        return 'give'
    return 'not a valid choice'


if __name__ == '__main__':
    main()
