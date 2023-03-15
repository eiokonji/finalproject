from simulation import SIMULATION
import sys

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]

sim = SIMULATION(directOrGUI, solutionID)
sim.Run()
sim.Get_Fitness(solutionID)