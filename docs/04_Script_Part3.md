# Part 3: Zero-Shot Planning (Connecting the Dots)

**Scene 1: The Setup**
*   **Narration:** "So, the model has built a perfect internal understanding of how objects behave. But how does it actually use this abstract imagination to solve a brand-new puzzle on the fly? Let's say we give it a goal—an image of what the solved puzzle looks like. The model maps its current reality to a 'Start' dot, and our goal image to a 'Target' dot, right here in the latent space."

**Scene 2: Imagining Branching Futures (Mở rộng MPC/CEM)**
*   **Narration:** "This is where Model Predictive Control, combined with the Cross-Entropy Method, comes into play. You can simply think of this as the AI *imagining branching futures*. From the starting dot, it simulates thousands of potential action sequences, growing a search tree of possibilities. But it doesn't just guess wildly. It looks at which branches are heading in the right direction, discards the bad ones, and focuses its imagination on the promising paths, growing closer and closer to the goal."

**Scene 3: Picking the Best Path**
*   **Narration:** "As this tree explores the latent landscape, it continuously calculates the mathematical distance between its predicted futures and the goal node. Out of thousands of simulated timelines, it simply highlights and picks the single branch that lands closest to the target. It's planning entirely by visual intuition."

**Scene 4: Zero-Shot & Real World Results (Mở rộng kết quả)**
*   **Narration:** "Finally, it translates that winning abstract path back into physical robot actions. Because the model deeply understands the underlying geometry of the scene, it doesn't need explicit training for every new situation. It can achieve zero-shot behavioral solutions to navigate arbitrarily configured mazes, or perform push manipulation with varied object shapes. The impact of this approach is massive. When tested on challenging, contact-rich tasks, DINO-WM improved upon prior state-of-the-art work by 45% on average."
