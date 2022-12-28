# from joker_game import Game
# from joker_simulation import Simulation
# import sys
# class Joker():
#     def main():
#         if sys.argv[1] == 'simulation':
#             simulation = Simulation()
#             if int(sys.argv[2]) > 0:
#                 if len(sys.argv) > 3 and sys.argv[3] == 'NOMODEL':
#                     simulation.run(int(sys.argv[2]), False)
#                 else:
#                     simulation.run(int(sys.argv[2]), True)
#             else:
#                 print("An Invald amount of games was entered as the argument for the simulation. 10 game simulations will run.")
#                 if len(sys.argv) > 3 and sys.argv[3] == 'NOMODEL':
#                     simulation.run(10, False)
#                 else:
#                     simulation.run(10, True)
#             simulation.write_to_csv()
#             print("Success! The results of the " + ('10' if int(sys.argv[2]) <= 0 else sys.argv[2]) + " simulations has been recorded in joker_simulations.csv")
#         elif sys.argv[1] == 'game':
#             game = Game()
#             game.run()

# if __name__ == '__main__':
#     Joker.main()
