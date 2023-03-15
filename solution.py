import numpy as np
import os
import pyrosim.pyrosim as pyrosim
import random
import time
import constants as c


class SOLUTION:
	def __init__(self, nextAvailableID):
		self.myID = nextAvailableID
		self.maxLinks = random.randint(4, 7)
		# sensor, neurons, motors
		self.sensors = []
		self.motors = []
		self.currNeuron = 0
		self.numMotorNeurons = 0
		self.numSensorNeurons = 0
		# making links
		self.linksList = []
		self.linksSizeList = []
		self.linksPositionsList = []
		self.materials = []
		self.colors = []
		self.size = []
		# init some other vars
		self.mat = ""
		self.col = ""
		self.linkposn = []
		# making joints
		self.joints = []
		self.jointPositions = []
		self.jointAxes = []
		# init some other vars
		self.jointposn = []
		self.Initialize_Body_Info()
		self.weights = np.random.rand(self.numSensorNeuron, self.numMotorNeuron) * 2 - 1

	# -------------------------------------------------------- #
    #              create body + brain + sim
    # -------------------------------------------------------- #
	def Start_Simulation(self, directOrGUI):
		if self.myID == 0:
			self.Create_World()
		self.Create_Body()
		self.Create_Brain()
		# suppress errors
		os.system(f"start /B python simulate.py {directOrGUI} {self.myID} >nul 2>&1")

	def Wait_For_Simulation_To_End(self):
		# check simulation is finished and fitness file ready to be read OTHERWISE sleep search.py
		# DONT CHANGE THE TIME SLEEP PERIOD
		file = f"fitness{self.myID}.txt"
		while not os.path.exists(file):
			time.sleep(1/100)

		# read in the fitness value
		while True:
			try:
				f = open(file, "r")
				break
			except:
				pass
		readFile = f.read()
		self.fitness = float(readFile.strip('\n'))
		f.close()
		os.system(f"del {file}")     
        
	def Create_World(self):
		# pretty straightforward
		pyrosim.Start_SDF("world.sdf")
		pyrosim.End()

	def Create_Body(self):
		# again, pretty straightforward
		pyrosim.Start_URDF(f"body{self.myID}.urdf")
		self.Body_Data_To_Body()
		pyrosim.End()

	def Initialize_Body_Info(self):
		for link in range(self.maxLinks+1):
			# self.color <- get link color  || self.size <- get link size
			self.Get_Link_Color_Material()
			self.Get_Link_Size()

			# case 1: it's the first link -- absolute referencing
			if link == 0:
				self.axis ="x"

				# links: store name, position, material, color, size
				self.linksList.append(f"Link{str(link)}")
				self.linksPositionsList.append([0, 0, 1])
				self.materials.append(self.mat)
				self.colors.append(self.col)
				self.linksSizeList.append(self.size)

				# joints: store name, axis, position
				self.jointAxes.append(self.Get_Joint_Axis())
				self.joints.append(f"Link{str(link)}_Link{str(link+1)}")
				self.jointPositions.append([self.size[0]/2, 0, 1])

			# case 2: it's the last link -- no joints needed
			elif link == self.maxLinks:
				self.Get_Link_Position()

				# links: store name, position, material, color, size
				self.linksList.append(f"Link{str(link)}")
				self.linksPositionsList.append(self.linkposn)
				self.materials.append(self.mat)
				self.colors.append(self.col)
				self.linksSizeList.append(self.size)

			# case 3: it's a middle link
			else:
				self.Get_Link_Position()

				# links: store name, position, material, color, size
				self.linksList.append(f"Link{link}")
				self.linksPositionsList.append(self.linkposn)
				self.materials.append(self.mat)
				self.colors.append(self.col)
				self.linksSizeList.append(self.size)

				# joints: store name, axis, position
				self.jointAxes.append(self.Get_Joint_Axis())
				self.joints.append(f"Link{link}_Link{link+1}")
				self.Get_Joint_Position(link)
				self.jointPositions.append(self.jointposn)

		self.numSensorNeuron = self.materials.count("Green")
		self.numMotorNeuron = len(self.joints)

	def Body_Data_To_Body(self):
		# use the generated info aboutlinks and joints to render them in pyrosim
		for link in range(len(self.linksList)):
			# make a link
			pyrosim.Send_Cube(name=self.linksList[link], 
								pos=self.linksPositionsList[link], 
								size=self.linksSizeList[link],
								materialName=self.materials[link],
								colorRgba=self.colors[link])
			# add sensor links to self.sensors
			if self.materials[link] == "Green": 
				self.sensors.append(self.linksList[link])

		for joint in range(len(self.joints)):
			# make a joint
			pyrosim.Send_Joint(name=self.joints[joint],
								parent=self.linksList[joint], 
								child=self.linksList[joint+1], 
								type="revolute",
								position=self.jointPositions[joint], 
								jointAxis=self.jointAxes[joint])
			# add all joints to self.motors
			self.motors.append(self.joints[joint])

	def Create_Brain(self):
		# sensors, neurons, synapses
		pyrosim.Start_NeuralNetwork(f"brain{str(self.myID)}.nndf")

		for s in range(len(self.sensors)):
			pyrosim.Send_Sensor_Neuron(name=self.currNeuron, linkName=self.sensors[s])
			self.currNeuron +=1

		for m in range(len(self.motors)):
			pyrosim.Send_Motor_Neuron(name=self.currNeuron, jointName=self.motors[m])
			self.currNeuron +=1

		for s in range(self.numSensorNeuron):
			for m in range(self.numMotorNeuron):
				pyrosim.Send_Synapse(sourceNeuronName=s, targetNeuronName=m+self.numSensorNeuron, weight=self.weights[s][m])
		pyrosim.End()

		self.currNeuron = 0
		self.sensors.clear()
		self.motors.clear()

	def Set_ID(self, nextAvailableID):
		self.myID = nextAvailableID
	# -------------------------------------------------------- #
	#                            mutation
	# -------------------------------------------------------- #
	def Mutate(self):
		if len(self.linksList) - 2 > 1:
			self.linksInd = random.randint(1, len(self.linksList)-2)
		else:
			self.linksInd = 1

		probMutate = random.random()
		if probMutate < 1/3:
			self.Mutate_Sensors()
			self.Mutate_Body()
			self.Mutate_Neurons()
		elif probMutate < 2/3:
			self.Mutate_Body()
			self.Mutate_Neurons()
		else:
			self.Mutate_Body()

	def Mutate_Sensors(self):
		# Switch sensors
		if self.materials[self.linksInd] == "Green":
			self.materials[self.linksInd] = "Blue"
			self.colors[self.linksInd] = "0 0 1.0 1.0"
		else:
			self.materials[self.linksInd] = "Green"
			self.colors[self.linksInd] = "0 1.0 0 1.0"

	def Mutate_Body(self):
		# Mutate random body size
		if random.random() < 0.5:
			self.Get_Link_Size()
			self.linksSizeList[self.linksInd] = self.size
			self.Mutate_Position()

		# Add a link at the end or del a link at the end
		if random.random() < 0.5:
			if random.random() > 0.8:
				self.Add_New_Link()
			else:
				# remove last link
				# list of all relevant lists, remove last one
				self.everything = [self.linksList,
									self.linksSizeList,
									self.linksPositionsList,
									self.materials,
									self.colors,
									self.joints,
									self.jointPositions,
									self.jointAxes]
				for list in self.everything:
					list.pop()

	def Mutate_Neurons(self):
		# Mutate synapses: remake s
		self.numSensorNeuron = self.materials.count("Green")
		self.numMotorNeuron = len(self.joints)
		self.weights = np.random.rand(self.numSensorNeuron, self.numMotorNeuron) * 2 - 1

	def Mutate_Position(self):
		# mutate the joints' positions
		if self.jointPositions[self.linksInd][0] != 0:
			self.jointPositions[self.linksInd][0] = self.size[0]/2

		if self.jointPositions[self.linksInd][1] != 0:
			self.jointPositions[self.linksInd][1] = self.size[1]/2

		if self.jointPositions[self.linksInd][2] != 0:
			self.jointPositions[self.linksInd][2] = self.size[2]/2

		# mutate the links' position
		if self.linksPositionsList[self.linksInd][0] != 0:
			self.linksPositionsList[self.linksInd][0] = self.size[0]/2

		if self.linksPositionsList[self.linksInd][1] != 0:
			self.linksPositionsList[self.linksInd][1] = self.size[1]/2

		if self.linksPositionsList[self.linksInd][2] != 0:
			self.linksPositionsList[self.linksInd][2] = self.size[2]/2

	# ------------------------------------------------------- # 
    #                         helpers
    # ------------------------------------------------------- # 
	def Get_Link_Color_Material(self):
		if random.random() >= 0.5:
			self.mat = "Green"
			self.col = "0 1.0 0 1.0"
		else:
			self.mat = "Blue"
			self.col = "0 0 1.0 1.0"

	def Get_Link_Size(self):
		x = random.uniform(0.2, 0.6)
		y = random.uniform(0.3, 0.6)
		z = random.uniform(0.1, 0.6)
		self.size = [x, y, z]

	def Get_Joint_Position(self, link):
		# general purpose
		options = {
			"a" : random.choice([[0, self.linksSizeList[link][1] / 2, self.linksSizeList[link][2] / 2],
								[self.linksSizeList[link][0] / 2, self.linksSizeList[link][1] / 2, 0]]),

			"b" : random.choice([[self.linksSizeList[link][0] / 2, self.linksSizeList[link][1] / 2, 0],
								[self.linksSizeList[link][0] / 2, 0, self.linksSizeList[link][2] / 2]]),

			"c" : random.choice([[self.linksSizeList[link][0]/2, 0, self.linksSizeList[link][2]/2],
								[0, self.linksSizeList[link][1]/2, self.linksSizeList[link][2]/2]])
		}

		if self.linksPositionsList[link][1] != 0:
			self.jointposn = options["a"]
			if self.jointposn[1] != 0:
				self.axis = "x"
			else:
				self.axis = "z"

		elif self.linksPositionsList[link][0] != 0:
			self.jointposn = options["b"]
			if self.jointposn[1] != 0:
				self.axis = "y"
			else:
				self.axis = "z"

		else:
			self.jointposn = options["c"]
			if self.jointposn[1] != 0:
				self.axis = "x"
			else:
				self.axis = "y"

	def Get_Link_Position(self):
		if self.axis == "x":
			self.linkposn = [self.size[0]/2, 0, 0]
		elif self.axis == "y":
			self.linkposn = [0, self.size[1]/2, 0]
		else:
			self.linkposn = [0, 0, self.size[2]/2]

	def Get_Joint_Axis(self):
		probAxis = random.random()
		if probAxis < 0.3:
			return "1 0 0"
		elif probAxis < 0.6:
			return "0 1 0"
		else:
			return "0 0 1"

	def Add_New_Link(self):
		# basically repeat Initialize_Body_Info but one link
		self.Get_Link_Color_Material()
		self.Get_Link_Size()
		nextID = len(self.linksList)

		# links: store name, position, material, color, size
		self.Get_Link_Position()
		self.linksList.append(f"Link{str(nextID)}")
		self.linksPositionsList.append(self.linkposn)
		self.materials.append(self.mat)
		self.colors.append(self.col)
		self.linksSizeList.append(self.size)

		# joints: store name, axis, position
		self.jointAxes.append(self.Get_Joint_Axis())
		self.joints.append(f"Link{str(nextID-1)}_Link{str(nextID)}")
		self.Get_Joint_Position(nextID-2)
		self.jointPositions.append(self.jointposn)

		
