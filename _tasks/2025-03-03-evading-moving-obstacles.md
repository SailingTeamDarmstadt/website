---
title: "Evading Moving Obstacles"
date: 2025-03-03
permalink: /2025/03/evading-moving-obstacles/
author: "Marcus Kornmann"
image: /assets/2025/03/evading_moving_obstacles.jpeg
excerpt: "Extend the route planner to dynamically avoid moving obstacles (other vessels) while maintaining an efficient and safe path to the destination."
---

### **Goal**

Extend the route planner to dynamically avoid moving obstacles (other vessels) while maintaining an efficient and safe path to the destination.

### **Motivation**

Safe autonomous navigation requires not only avoiding static obstacles but also predicting and reacting to the movement of other vessels in compliance with maritime collision regulations (COLREGS). This capability is essential for operating in busy waterways where vessel traffic is common.

### **Available Information**

- Output from boat detection and tracking system (positions, headings, and velocity estimates of nearby vessels)
- Existing static obstacle avoidance system
- GPS, Compass, Wind information
- Maritime collision regulations (COLREGS)
- Own vessel characteristics (turning radius, speed capabilities)

### **Requirements**

- Integrate data from the boat detection and tracking system into the route planner.
- Implement prediction models to forecast the future trajectories of detected vessels.
- Apply appropriate COLREGS rules for different encounter scenarios (head-on, crossing, overtaking).
- Dynamically adjust planned routes in real-time as other vessels‘ movements are updated.
- Maintain appropriate safety distance that scales with relative velocity and vessel size.
- Gracefully handle scenarios with multiple moving obstacles while still evading static obstacles.
- Provide fallback behaviors for emergency collision avoidance when standard planning fails.

### **Challenges & Considerations**

- *Trajectory Prediction*: Accurately forecasting other vessels‘ movements with limited observation time.
- *COLREGS Compliance*: Implementing complex maritime rules that vary by encounter type and vessel classification.
- *Decision Uncertainty*: Handling ambiguous situations where the intentions of other vessels are unclear.
- *Computational Latency*: Ensuring timely reactions when multiple obstacles require simultaneous processing.
- *Graceful Degradation*: Maintaining basic avoidance capabilities even when tracking data is incomplete or uncertain.
- *Risk Assessment*: Quantifying and minimizing collision risk across various possible future scenarios.
- *Integration Complexity*: Merging dynamic obstacle avoidance with existing static obstacle and route optimization systems.

### **Simplifications**

- For predicting other vessels path, in the beginning, assume they will follow their current heading.
- Initially focus on open-water scenarios before handling complex harbor or channel environments.
- Start with basic COLREGS compliance before implementing edge cases and special situations.
- Assume other vessels are also following COLREGS and behaving predictably.
- Begin with constant-velocity prediction models before implementing more complex prediction algorithms.
- For predicting other vessels path, in the beginning, assume they will follow their current heading.
