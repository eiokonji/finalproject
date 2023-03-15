from parallelHillClimber import PARALLEL_HILL_CLIMBER
import constants as c
import random
import sys

random.seed(int(sys.argv[1]))
c.seed = int(sys.argv[1])
print(f"\nSeed: {c.seed}")

phc = PARALLEL_HILL_CLIMBER()
phc.Evolve()
input("View evolved creature! \nPress \"Enter\" key...")
phc.Show_Best()