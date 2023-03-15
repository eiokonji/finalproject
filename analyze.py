import constants as c
import matplotlib.pyplot as plt

# data
bigList = []
for seed in range(10):
    with open(f'BestFitness500_10_{seed+1}.txt', 'r') as file:
        data = []
        for line in file:
            row = [float(x) for x in line.split()]
            maxFit = max(row)
            data.append(maxFit)
        # with open(f'BestFitness500_10_{seed+1}.txt', 'w') as fp:
        #     for item in data:
        #         fp.write(f"{str(item)}\n")
                
        bigList.append(data)
  
# plotting
line1, = plt.plot(bigList[0], label = 'Seed 1')
line2, = plt.plot(bigList[1], label = 'Seed 2')
line3, = plt.plot(bigList[2], label = 'Seed 3')
line4, = plt.plot(bigList[3], label = 'Seed 4')
line5, = plt.plot(bigList[4], label = 'Seed 5')
line6, = plt.plot(bigList[5], label = 'Seed 6')
line7, = plt.plot(bigList[6], label = 'Seed 7')
line8, = plt.plot(bigList[7], label = 'Seed 8')
line9, = plt.plot(bigList[8], label = 'Seed 9')
line10, = plt.plot(bigList[9], label = 'Seed 10')
leg = plt.legend(loc='lower right')


plt.xlabel('Number of Generations')
plt.ylabel('Best Fitness')
plt.title('Evolution over 500 generations')
ax = plt.gca()

# plt.show()
plt.savefig(f"Evolution_{c.numberOfGenerations}_{c.populationSize}_{c.numOfRuns}.png")

