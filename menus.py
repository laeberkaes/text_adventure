# def title_screen_selections():
#     option = input("> ")
#     if option.lower() == ("play"):
#         game.setup_game()
#     elif option.lower() == ("help"):
#         help_menu()
#     elif option.lower() == ("quit"):
#         sys.exit()
#
#     while option.lower() not in ["play","help","quit"]:
#         print("Invalid command. Type 'play', 'help', 'quit'")
#         title_screen_selections()

def title_screen():
    print("#"*(4+len("Welcome to the Text RPG")))
    print("# Welcome to the Text RPG #")
    print("#"*(4+len("Welcome to the Text RPG")))
    print("# " + (" "*int((len("Welcome to the Text RPG")-6)/2)) + "-play-" + (" "*int((len("Welcome to the Text RPG")-6)/2)) + " #")
    print("# " + (" "*int((len("Welcome to the Text RPG")-6)/2)) + "-help-" + (" "*int((len("Welcome to the Text RPG")-6)/2)) + " #")
    print("# " + (" "*int((len("Welcome to the Text RPG")-6)/2)) + "-quit-" + (" "*int((len("Welcome to the Text RPG")-6)/2)) + " #")
    print("#"*(4+len("Welcome to the Text RPG"))+"\n")
    title_screen_selections()

def help_menu():
    print("#"*27)
    print("# Welcome to the Text RPG #")
    print("#"*27)
    print(" -- Use up, down, left, right to move")
    print(" -- Type your commands to do them")
    print(" -- Good luck and have fun!")
    title_screen()
    title_screen_selections()
