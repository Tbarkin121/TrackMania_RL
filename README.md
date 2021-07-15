Working on creating an environment to run RL algorithms in trackmania.

Step 1) locating the memory addresses of interesting features to be used. These are things like car state, game state, ect... Using Cheat Engine to probe the memory and determine static addresses has been working well so far

Step 2) Access the state in python with MemoryReadWrite. This is working well so far

Step 3) Send commands back to the game from python. This is the next thing to focus on. 

Step 4) Launching trackmania sessions and keeping track of the PID. The goal would be able to run several instances of the environment in parellel. It looks very doable as long as we can keep track of where our .exe is. 

Step 5) Formalizing the code into a 'gym' structure. This is going to need a bit of work since we will need to navigate menues to make things work... Not quite sure how to tackle this yet. 

