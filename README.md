# Final Project
**Name**: Ebubechukwu Okonji

**Option and Grading**: Engineering Option, 44 points

**Expectations**: An executable, concisely documented, neatly illustrated, and well polished extension of previous projects, showing evolved locomotion. 

### Video Submissions
#### 10 Second Summary
![](https://github.com/eiokonji/finalproject/blob/main/readme_imgs/teaser-giffy.gif)

If that seems interesting, here's a [2 Minute Summary Video](https://youtu.be/u4eifnvBlWk)

## Introduction
This project tried to generate 3D creatures that filled 3D space which were evolved to walk in the negative x-direction (or into the screen) - see the image below for a visual representation of the project's coordinate system. Each creature was randomly generated and mutated, and evolved using an adapted tournament style evolution method. The creature is color-coded: "green" links are innervated (they behave like sensors) while "blue" links are not innervated (they lack sensors).

## Building the Creature
There are two aspects to consider: the genotype and the phenotype. The code describing the body/brain geenration is in the ```solution.py``` file.

### Genotype
This refers loosely to the creature's DNA. It describes the logic behind the creature's structure. Inspired by Karl Sims' representation of his creatures, I used a similar diagram to show the creatures genotype (see the left of the diagram below). The root link, which is a cube (or cuboid) will generate a new "link" on any of its faces in the positive direction (i.e., the positive-x, -y, -z directions in the image below). These links will then recursively call other links to be generated in one of these positive directions. The blue arrow which loops back into the link represents this recursive call. You have to set a recursive limit in the code after which no more links will be generated.

<img src="https://github.com/eiokonji/finalproject/blob/main/readme_imgs/finalimg1.png" width=100% height=100%>

### Phenotype
This refers to the physical representation of the creature. It includes how the different links which make up the creature's body are connected to each other. In creating each creature's phenotype, the major constraint observed was that body segments could not be generated on top of each other. To prevent this, the position and size of each segment was stored in a global list upon creation. This data was then used to generate the body of the creature. Additionally, you can see some examples of different morphologies that were generated from the phenotype. 

### Neural Mapping
All joints are linked to all sensors in the creature regardless of their proximity to the sensor. There are no multi-layered neural networks here - it is a direct mapping without any hidden neurons. Although different joints can move in the x-z, y-z and x-y planes, it generally moves in the positive x-direction (into the screen). I've included some examples of how movement in each of these planes can be seen. However, visualizing this behavior may be difficult and I encourage you to watch the attached video for more clarification.

![How are the links and sensors connected?](https://github.com/eiokonji/finalproject/blob/main/readme_imgs/finalimg2.png)
<img src="https://github.com/eiokonji/finalproject/blob/main/readme_imgs/finalimg4.png" width=25% height=25%>

## Evolving the Creature
As mentioned earlier, this creature was evolved with an adapted tournament style evolutionary strategy. Here are the steps involved:
1. Each parent in the population gives birth to a child. The population has now doubled in size.
2. All members of the population will battle each other and the fitter half of the population will dominate the tournament.
3. These members will then become the parents of the next generation and this process will repeat consistently until all the generations have been lived through.

**Note:** If you are curious about the code behind this evolutionary strategy, please look into the ```parallelHillClimber.py``` file and kindly ignore the misnomer. 

#### Sample Size
   - **Population size**: 10
   - **Number of Generations**: 500
   - **Number of Runs**: 10

This yielded a 50,000 sims being generated. It took approximately 40 minutes for the non-erroring runs. Some of these runs proved to not evolve towards their objective. It took a very long time to get all these sims.

## Mutating the Creature
There were multiple ways of mutating the creature; we could: 
   - mutate its body by adjusting the dimensions of different body segments or removing (see C in image below) /adding body segments (see Din image below)
   - mutate its brain by changing the weights of the motor-sensor synaptic connections 
   - mutate the type of link that each body segment was initially assigned (going from a motor to sensor neuron and vice versa) (see B in image below). 
Some of these options can be seen below:
<img src="https://github.com/eiokonji/finalproject/blob/main/readme_imgs/finalimg5.png">

## Conclusion

My results are summarized in the plot below:

<img src="https://github.com/eiokonji/finalproject/blob/main/readme_imgs/Evolution_500_10_10.png">

We see that:
...



## Replicating the Simulations
1. Clone the repository.
2. Navigate to your source folder.

#### Viewing the Unevolved and Evolved Creatures
3. Navigate to the ```constants.py``` file and modify the **populationSize** and **numberOfGenerations** variables as needed
   - I would recommend not making these values too large as it will take a while to run
4. Run ```python3 search.py {seed}``` in your terminal.
   - ```{seed}```: seed, can be any positive, non-zero value
5. The unevolved creature should pop up first. After a while, you will be prompted in the terminal to press the "Enter" key - this aloows you see the evolved creature.

#### Generating the Plot
6. Run the ```analyze.py``` file 
   - Click your IDE's ```Run``` icon or run ```python3 analyze.py``` in your terminal

## Resources
- [Ludobots MOOC](https://www.reddit.com/r/ludobots/wiki/finalproject/)
- [Video Showing Evolution](...)
- [Pyrosim (forked)](https://github.com/jbongard/pyrosim)
- [Prof. Kriegman's "Artificial Life" Seminar at Northwestern University (links to course syllabus)](https://docs.google.com/document/d/1jURIbvpQ0imcaMk-AHUmj_szZNtsA4lZAlcqXa6usXs/edit) 
- [Karl Sims work](https://www.karlsims.com/evolved-virtual-creatures.html)

 
