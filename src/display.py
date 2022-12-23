class Display(object):
    def cards(cards):
        values = {
            4: lambda: "6",
            5: lambda: "7",
            6: lambda: "8",
            7: lambda: "9",
            8: lambda: "10",
            9: lambda: "J",
            10: lambda: "Q",
            11: lambda: "K",
            12: lambda: "A",
            13: lambda: "✦",
        }
        suits = {
            0: lambda : "♦",
            1: lambda : "♣",
            2: lambda : "♥",
            3: lambda : "♠",
        }

        if len(cards) == 1:
            c0 = cards[0]
            print()
            print("\t ________________      ________________      ________________      ________________ ")
            print("\t|                |    |                |    |                |    |                |")
            if values[c0.value]() == '10': 
                print("\t|  {}            |    |                |    |                |    |                |".format(values[c0.value]()))
            else:
                print("\t|  {}             |    |                |    |                |    |                |".format(values[c0.value]()))
            print("\t|                |    |      * *       |    |      * *       |    |      * *       |")
            print("\t|                |    |    *     *     |    |    *     *     |    |    *     *     |")
            print("\t|                |    |   *       *    |    |   *       *    |    |   *       *    |")
            print("\t|                |    |   *       *    |    |   *       *    |    |   *       *    |")
            print("\t|       {}        |    |          *     |    |          *     |    |          *     |".format("✦" if c0.value == 13 else suits[c0.suit]()))
            print("\t|                |    |         *      |    |         *      |    |         *      |")
            print("\t|                |    |        *       |    |        *       |    |        *       |")
            print("\t|                |    |                |    |                |    |                |")
            print("\t|                |    |                |    |                |    |                |")
            if values[c0.value]() == '10': 
                print("\t|            {}  |    |        *       |    |        *       |    |        *       |".format(values[c0.value]()))
            else:
                print("\t|            {}   |    |        *       |    |        *       |    |        *       |".format(values[c0.value]())) 
            print("\t|________________|    |________________|    |________________|    |________________|")
            print()

        elif len(cards) == 2:
            c0, c1 = cards[0], cards[1]
            print()
            print("\t ________________      ________________      ________________      ________________ ")
            print("\t|                |    |                |    |                |    |                |")
            if values[c0.value]() == '10' and values[c1.value]() == '10':
                print("\t|  {}            |    |  {}            |    |                |    |                |".format(values[c0.value](),values[c1.value]()))
            elif values[c0.value]() == '10': 
                print("\t|  {}            |    |  {}             |    |                |    |                |".format(values[c0.value](),values[c1.value]())) 
            elif values[c1.value]() == '10':
                print("\t|  {}             |    |  {}            |    |                |    |                |".format(values[c0.value](),values[c1.value]()))
            else:
                print("\t|  {}             |    |  {}             |    |                |    |                |".format(values[c0.value](),values[c1.value]()))
            print("\t|                |    |                |    |      * *       |    |      * *       |")
            print("\t|                |    |                |    |    *     *     |    |    *     *     |")
            print("\t|                |    |                |    |   *       *    |    |   *       *    |")
            print("\t|                |    |                |    |   *       *    |    |   *       *    |")
            print("\t|       {}        |    |       {}        |    |          *     |    |          *     |".format("✦" if c0.value == 13 else suits[c0.suit](), "✦" if c1.value == 13 else suits[c1.suit]()))
            print("\t|                |    |                |    |         *      |    |         *      |")
            print("\t|                |    |                |    |        *       |    |        *       |")
            print("\t|                |    |                |    |                |    |                |")
            print("\t|                |    |                |    |                |    |                |")
            if values[c0.value]() == '10' and values[c1.value]() == '10':
                print("\t|            {}  |    |            {}  |    |        *       |    |        *       |".format(values[c0.value](),values[c1.value]()))
            elif values[c0.value]() == '10': 
                print("\t|            {}  |    |            {}   |    |        *       |    |        *       |".format(values[c0.value](),values[c1.value]()))
            elif values[c1.value]() == '10':
                print("\t|            {}   |    |            {}  |    |        *       |    |        *       |".format(values[c0.value](),values[c1.value]()))
            else:
                print("\t|            {}   |    |            {}   |    |        *       |    |        *       |".format(values[c0.value](),values[c1.value]())) 
            print("\t|________________|    |________________|    |________________|    |________________|")
            print()
        elif len(cards) == 3:
            c0, c1, c2 = cards[0], cards[1], cards[2]
            print()
            print("\t ________________      ________________      ________________      ________________ ")
            print("\t|                |    |                |    |                |    |                |")
            # special case if all 3 are 10s
            if values[c0.value]() == '10' and values[c1.value]() == '10' and values[c2.value]() == '10':
                print("\t|  {}            |    |  {}            |    |  {}            |    |                |".format(values[c0.value](),values[c1.value](), values[c2.value]()))
            elif values[c0.value]() == '10' and values[c2.value]() == '10':
                print("\t|  {}            |    |  {}             |    |  {}            |    |                |".format(values[c0.value](),values[c1.value](), values[c2.value]()))
            elif values[c1.value]() == '10' and values[c2.value]() == '10':
                print("\t|  {}             |    |  {}            |    |  {}            |    |                |".format(values[c0.value](),values[c1.value](), values[c2.value]()))
            elif values[c0.value]() == '10' and values[c1.value]() == '10':
                print("\t|  {}            |    |  {}            |    |  {}             |   |                |".format(values[c0.value](),values[c1.value](), values[c2.value]()))
            elif values[c0.value]() == '10': 
                print("\t|  {}            |    |  {}             |    |  {}             |    |                |".format(values[c0.value](),values[c1.value](), values[c2.value]())) 
            elif values[c1.value]() == '10':
                print("\t|  {}             |    |  {}            |    |  {}             |    |                |".format(values[c0.value](),values[c1.value](), values[c2.value]()))
            elif values[c2.value]() == '10':
                print("\t|  {}             |    |  {}             |    |  {}            |    |                |".format(values[c0.value](),values[c1.value](), values[c2.value]()))
            else:
                print("\t|  {}             |    |  {}             |    |  {}             |    |                |".format(values[c0.value](),values[c1.value](), values[c2.value]())) 
            print("\t|                |    |                |    |                |    |      * *       |")
            print("\t|                |    |                |    |                |    |    *     *     |")
            print("\t|                |    |                |    |                |    |   *       *    |")
            print("\t|                |    |                |    |                |    |   *       *    |")
            print("\t|       {}        |    |       {}        |    |       {}        |    |          *     |".format("✦" if c0.value == 13 else suits[c0.suit](), "✦" if c1.value == 13 else suits[c1.suit](), "✦" if c2.value == 13 else suits[c2.suit]() ))
            print("\t|                |    |                |    |                |    |         *      |")
            print("\t|                |    |                |    |                |    |        *       |")
            print("\t|                |    |                |    |                |    |                |")
            print("\t|                |    |                |    |                |    |                |")
            
            if values[c0.value]() == '10' and values[c1.value]() == '10' and values[c2.value]() == '10':
                print("\t|            {}  |    |            {}  |    |            {}  |    |        *       |".format(values[c0.value](),values[c1.value](), values[c2.value]()))
            elif values[c0.value]() == '10' and values[c2.value]() == '10':
                print("\t|            {}  |   |            {}   |    |            {}  |    |        *       |".format(values[c0.value](),values[c1.value](), values[c2.value]()))
            elif values[c1.value]() == '10' and values[c2.value]() == '10':
                print("\t|            {}   |    |            {}  |    |            {}  |    |        *       |".format(values[c0.value](),values[c1.value](), values[c2.value]()))
            elif values[c0.value]() == '10' and values[c1.value]() == '10':
                print("\t|            {}  |    |            {}  |    |            {}   |    |        *       |".format(values[c0.value](),values[c1.value](), values[c2.value]()))
            elif values[c0.value]() == '10': 
                print("\t|            {}  |    |            {}   |    |            {}   |    |        *       |".format(values[c0.value](),values[c1.value](), values[c2.value]()))
            elif values[c1.value]() == '10':
                print("\t|            {}   |    |            {}  |    |            {}   |    |        *       |".format(values[c0.value](),values[c1.value](), values[c2.value]()))
            elif values[c2.value]() == '10':
                print("\t|            {}   |    |            {}   |    |            {}  |    |        *       |".format(values[c0.value](),values[c1.value](), values[c2.value]()))
            else:
                print("\t|            {}   |    |            {}   |    |            {}   |    |        *       |".format(values[c0.value](),values[c1.value](), values[c2.value]())) 
            
            print("\t|________________|    |________________|    |________________|    |________________|")
            print()
        elif len(cards) == 4:
            c0, c1, c2, c3 = cards[0], cards[1], cards[2], cards[3]
            print()
            print("\t ________________      ________________      ________________      ________________ ")
            print("\t|                |    |                |    |                |    |                |")
            # special case if all 3 are 10s
            if values[c0.value]() == '10' and values[c1.value]() == '10' and values[c2.value]() == '10':
                top_num = ("\t|  {}            |    |  {}            |    |  {}            |".format(values[c0.value](),values[c1.value](), values[c2.value]()))
            elif values[c0.value]() == '10' and values[c2.value]() == '10':
                top_num = ("\t|  {}            |    |  {}             |    |  {}            |".format(values[c0.value](),values[c1.value](), values[c2.value]()))
            elif values[c1.value]() == '10' and values[c2.value]() == '10':
                top_num = ("\t|  {}             |    |  {}            |    |  {}            |".format(values[c0.value](),values[c1.value](), values[c2.value]()))
            elif values[c0.value]() == '10' and values[c1.value]() == '10':
                top_num = ("\t|  {}            |    |  {}            |    |  {}             |".format(values[c0.value](),values[c1.value](), values[c2.value]()))
            elif values[c0.value]() == '10': 
                top_num = ("\t|  {}            |    |  {}             |    |  {}             |".format(values[c0.value](),values[c1.value](), values[c2.value]())) 
            elif values[c1.value]() == '10':
                top_num = ("\t|  {}             |    |  {}            |    |  {}             |".format(values[c0.value](),values[c1.value](), values[c2.value]()))
            elif values[c2.value]() == '10':
                top_num = ("\t|  {}             |    |  {}             |    |  {}            |".format(values[c0.value](),values[c1.value](), values[c2.value]()))
            else:
                top_num = ("\t|  {}             |    |  {}             |    |  {}             |".format(values[c0.value](),values[c1.value](), values[c2.value]())) 
            if values[c3.value]() == '10':
                top_num += Display.get_top_of_10()
            else:
                top_num += "    |  {}             |".format(values[c3.value]())

            print(top_num)
            print("\t|                |    |                |    |                |    |                |")
            print("\t|                |    |                |    |                |    |                |")
            print("\t|                |    |                |    |                |    |                |")
            print("\t|                |    |                |    |                |    |                |")
            print("\t|       {}        |    |       {}        |    |       {}        |    |       {}        |".format("✦" if c0.value == 13 else suits[c0.suit](), "✦" if c1.value == 13 else suits[c1.suit](), "✦" if c2.value == 13 else suits[c2.suit]() , "✦" if c3.value == 13 else suits[c3.suit]() ))
            print("\t|                |    |                |    |                |    |                |")
            print("\t|                |    |                |    |                |    |                |")
            print("\t|                |    |                |    |                |    |                |")
            print("\t|                |    |                |    |                |    |                |")
            
            if values[c0.value]() == '10' and values[c1.value]() == '10' and values[c2.value]() == '10':
                bottom_num = ("\t|            {}  |    |            {}  |    |            {}  |".format(values[c0.value](),values[c1.value](), values[c2.value]()))
            elif values[c0.value]() == '10' and values[c2.value]() == '10':
                bottom_num = ("\t|            {}  |    |            {}   |    |            {}  |".format(values[c0.value](),values[c1.value](), values[c2.value]()))
            elif values[c1.value]() == '10' and values[c2.value]() == '10':
                bottom_num = ("\t|            {}   |    |            {}  |    |            {}  |".format(values[c0.value](),values[c1.value](), values[c2.value]()))
            elif values[c0.value]() == '10' and values[c1.value]() == '10':
                bottom_num = ("\t|            {}  |    |            {}  |    |            {}   |".format(values[c0.value](),values[c1.value](), values[c2.value]()))
            elif values[c0.value]() == '10': 
                bottom_num = ("\t|            {}  |    |            {}   |    |            {}   |".format(values[c0.value](),values[c1.value](), values[c2.value]()))
            elif values[c1.value]() == '10':
                bottom_num = ("\t|            {}   |    |            {}  |    |            {}   |".format(values[c0.value](),values[c1.value](), values[c2.value]()))
            elif values[c2.value]() == '10':
                bottom_num = ("\t|            {}   |    |            {}   |    |            {}  |".format(values[c0.value](),values[c1.value](), values[c2.value]()))
            else:
                bottom_num = ("\t|            {}   |    |            {}   |    |            {}   |".format(values[c0.value](),values[c1.value](), values[c2.value]())) 
            
            if values[c3.value]() == '10':
                bottom_num += Display.get_bottom_of_10()
            else:
                bottom_num += "    |             {}  |".format(values[c3.value]())

            print(bottom_num)
            print("\t|________________|    |________________|    |________________|    |________________|")
            print()


    def get_top_of_10():
        return "    |  10            |"
        
    def get_bottom_of_10():
        return "    |            10  |"

    def wild(suit):
        suits = {
            0: lambda : "♦",
            1: lambda : "♣",
            2: lambda : "♥",
            3: lambda : "♠",
        }
        print("\nWildsuit: ", suits[suit]() if suit < 4 else "✖")

    def cards_in_hand(cards):
        print("Currently, you have the following cards in hand: \n", cards)
    
    def playable(cards):
        print("These are the cards that you can play: \n", cards)
    
    def ask_card_choice(amount):
        print("Which card would you like to choose? (1 - " + str(amount) + ")")
        valid = False 
        while not valid:
            choice = int(input())
            if choice > 0 and choice <= amount:
                valid = True
            else:
                print("Please enter a valid value: ")
        return choice - 1
    
    def scores(game):
        for user in game.users:
            if user.id == 0:
                print("Your Score is " + str(user.score))
            else:
                print("USER " +  str(user.id) + "'s Score is " + str(user.score))
    
    def ask_call(dealt):
        print("Based on your cards, how much do you call: " + "(0 - " + str(dealt) + ")")
        valid = False 
        while not valid:
            choice = int(input())
            if choice >= 0 and choice <= dealt:
                valid = True
            else:
                print("Please enter a valid value: ")
        return choice

    def winner_of_hand(game, player):
        if player == 0:
            print("You have won this hand. You have taken a total of " + str(game.users[player].taken) + " cards.")
        else:
            print("Player " + str(player) + " has won this hand. They have taken a total of " + str(game.users[player].taken) + " cards.")