def proper_capitalization():
    options = {"rock": "Rock", "paper": "Paper", "scissors": "Scissors"}

    selection = input("Choose: rock, paper, or scissors?").lower()

    if selection in options:
        return options[selection]
    else:
        print("Not a valid choice!")
        return "Error"