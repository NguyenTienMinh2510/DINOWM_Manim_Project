# Kế Hoạch Triển Khai Video DINO-WM (Phong cách 3Blue1Brown)

---

## Part 1: The Problem with "Imagining" Pixels (Phụ trách: Minh)

**The Goal:** 
Hook the viewer by explaining what a "World Model" is and why predicting the future pixel-by-pixel is a computational nightmare.

**The Narrative:** 
Humans don't plan their day by imagining every photon of light that will hit their eyes; we think in abstract concepts (e.g., "door", "handle", "open"). Yet, traditional AI world models try to predict the exact pixels of the next video frame to figure out what happens when an action is taken. This requires massive compute and gets distracted by irrelevant details (like shadows or background textures).

**The Visuals (3B1B Style):**
* Start with a simple grid of pixels representing a robot's camera view.
* Show an action (e.g., an arrow representing "move forward").
* Animate the screen splitting into millions of little pixel equations, showing the network struggling to predict the exact RGB values of a complex, noisy background.
* Fade the chaotic pixels into a clean, geometric abstraction (dots representing "concepts" or "objects") to hint at the solution.

**Your To-Do List for Part 1:**
- [ ] Write the script focusing on the analogy between human abstract planning and robot pixel-planning.
- [ ] Animate a basic 2D robot environment (e.g., moving a block).
- [ ] Create a visual representation of "pixel space" (a dense, chaotic 3D matrix) vs. "latent space" (a clean, sparse geometric vector space).

---

## Part 2: The DINO-WM Solution (Seeing in Latent Space) (Phụ trách: Long)

**The Goal:** 
Explain the core innovation of the paper: using DINOv2's pre-trained visual features to bypass the pixel problem entirely.

**The Narrative:** 
Enter DINO-WM. Instead of making the AI learn what the world looks like from scratch, we borrow a "brain" that already understands images (DINOv2). DINOv2 breaks an image down into "patches" and converts them into rich embeddings (lists of numbers that capture meaning, like "this is a corner" or "this is an apple"). DINO-WM simply learns the rules of physics inside this embedding space. When the robot takes an action, the Vision Transformer (ViT) predicts how these abstract numbers change, without ever decoding them back into an image.

**The Visuals (3B1B Style):**
* Show an image being sliced into a grid of patches.
* Animate each patch transforming into a glowing vector (a column of numbers).
* Show a timeline: `State(t) + Action → State(t+1)`. But instead of images on the timeline, use glowing vector clusters.
* Show a "decoder" crossed out with a red X—emphasizing that we never go back to pixels, saving massive compute.

**Your To-Do List for Part 2:**
- [ ] Write the script explaining DINOv2's spatial patch features in simple terms (think of them as "concept blocks").
- [ ] Animate the transformation of an image into patch embeddings (matrices/vectors).
- [ ] Animate the autoregressive Vision Transformer (ViT) predicting the next set of vectors in a sequence.

---

## Part 3: Zero-Shot Planning (Connecting the Dots) (Phụ trách: Cường)

**The Goal:** 
Bring it all together to show how this abstract imagination allows the AI to solve brand-new tasks on the fly.

**The Narrative:** 
Because the model now perfectly understands how objects behave in this abstract space, we can give it a goal (an image of the solved puzzle). The model converts the goal into a target vector. Then, using Model Predictive Control (MPC) and the Cross-Entropy Method (CEM), it simulates thousands of possible action sequences in its "imagination." It simply picks the path that gets its predicted vectors closest to the target vector. Because it understands the underlying geometry of the scene, it can solve new mazes or manipulate new objects it wasn't explicitly trained on (Zero-Shot).

**The Visuals (3B1B Style):**
* Place a "Start" vector dot and a "Goal" vector dot in a dark, empty 3D coordinate space.
* Animate a tree of branching paths growing from the Start dot (representing simulated actions).
* Highlight the branch that lands closest to the Goal dot.
* Translate that winning path back into physical robot actions on a real-world task.

**Your To-Do List for Part 3:**
- [ ] Write the script explaining MPC/CEM as simply "imagining branching futures and picking the best one."
- [ ] Animate a search tree exploring a latent space landscape, calculating the distance to a goal node.
- [ ] Summarize the paper's results (e.g., 45% improvement on contact-rich tasks) using clean, minimalist bar charts.

> **Pro-Tip for the 3B1B Vibe (Dành cho cả team):** If you are using Python, look into the **Manim** (Mathematical Animation Engine) library, which was built by Grant Sanderson (the creator of 3Blue1Brown) specifically to generate these exact types of glowing, math-focused animations!