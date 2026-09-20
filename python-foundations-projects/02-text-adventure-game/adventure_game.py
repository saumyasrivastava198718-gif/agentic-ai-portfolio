# ============================================
# PROJECT 2: TEXT-BASED ADVENTURE GAME
# ============================================


def show_status(player):
    print("\n-----------------------------")
    print(f"Location: {player['location']}")
    print(f"Health: {player['health']}")
    print(f"Inventory: {player['inventory']}")
    print("-----------------------------")


def laboratory(player):

    print("\nYou are inside an abandoned AI laboratory.")
    print("You see a CONTROL ROOM and a DARK CORRIDOR.")

    choice = input(
        "Where do you want to go? "
        "(control room/corridor): "
    ).lower()

    if choice == "control room":
        player["location"] = "Control Room"

    elif choice == "corridor":
        player["location"] = "Dark Corridor"

    else:
        print("Invalid choice.")


def control_room(player):

    print("\nYou enter the control room.")
    print("A silver key is lying beside an old computer.")

    if "silver key" not in player["inventory"]:

        choice = input(
            "Do you want to take the key? (yes/no): "
        ).lower()

        if choice == "yes":
            player["inventory"].append("silver key")
            print("You collected the silver key!")

    else:
        print("You already collected the key.")

    player["location"] = "Laboratory"


def dark_corridor(player):

    print("\nYou enter a dark corridor.")
    print("A security robot suddenly appears!")

    choice = input(
        "Do you want to RUN or FIGHT? "
    ).lower()

    if choice == "fight":

        print("The robot attacks you!")

        player["health"] -= 20

        print("You escape after the fight.")

    elif choice == "run":

        print("You run away safely.")

    else:

        print("You hesitate and the robot attacks!")

        player["health"] -= 10

    player["location"] = "Exit Door"


def exit_door(player):

    print("\nYou reach a locked exit door.")

    if "silver key" in player["inventory"]:

        print("You use the silver key.")
        print("The door opens!")
        print("\n🎉 YOU ESCAPED THE AI LAB! 🎉")

        return True

    else:

        print("The door is locked.")
        print("You need to find a key.")

        player["location"] = "Laboratory"

        return False


def main():

    player = {
        "location": "Laboratory",
        "health": 100,
        "inventory": []
    }

    print("==============================")
    print("   ESCAPE THE AI LAB")
    print("==============================")

    print(
        "\nYou wake up inside an abandoned "
        "AI research laboratory."
    )

    game_over = False

    while not game_over:

        show_status(player)

        if player["health"] <= 0:
            print("\nYou have lost all your health.")
            print("GAME OVER!")
            break

        if player["location"] == "Laboratory":
            laboratory(player)

        elif player["location"] == "Control Room":
            control_room(player)

        elif player["location"] == "Dark Corridor":
            dark_corridor(player)

        elif player["location"] == "Exit Door":
            game_over = exit_door(player)


if __name__ == "__main__":
    main()