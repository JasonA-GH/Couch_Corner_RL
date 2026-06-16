# Couch_Corner_RL
Trying to find the shape with the highest surface area that can round the corner. By using Reinforcement learning with the surface area being the reward, the AI attempts to make the best moves to keep the most surface area.

If the polygon touches the wall, any vertices that touch the wall will be pushed in, losing surface area.

The AI is currently in an early state (only a few hundred thousand timesteps) so it doesn't do very well
<img width="1280" height="720" alt="AI_1" src="https://github.com/user-attachments/assets/682848ec-0a81-4af8-a58b-6eb54b497af0" />
It actually failed. I set a lower limit on the surface area and it quickly reaches it and the simulation ends.

Here is a human attempt. Not bad but I do believe the agent can do much better with much smoother inputs
<img width="1280" height="720" alt="Human_1_24" src="https://github.com/user-attachments/assets/97120cd1-c07e-4d2e-a29a-e37084a11849" />
