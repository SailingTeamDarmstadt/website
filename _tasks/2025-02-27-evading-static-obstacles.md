---
title: "Evading Static Obstacles"
date: 2025-02-27
permalink: /2025/02/evading-static-obstacles/
author: "Marcus Kornmann"
image: /assets/2025/02/evading_static_obstacles_2.png
excerpt: "Integrate static obstacles into the route planner so they can be evaded."
---

### **Goal**

Integrate static obstacles into the route planner so they can be evaded.

### **Motivation**

To ensure safe navigation, our autonomous sailboat must be able to avoid known static obstacles such as buoys, docks, underwater hazards, and shorelines while efficiently planning optimal routes.

### **Available Information**

Locations of static obstacles, GPS, Compass, Wind information

### **Requirements**

- Incorporate static obstacle information into the existing route planning algorithm.
- Implement a safety buffer zone around obstacles based on their size and the uncertainty of their position.
- Ensure the system can handle multiple obstacles while still finding efficient paths.
- Prioritize obstacle avoidance while balancing other route optimization factors (wind conditions, energy efficiency, etc.).
- Support both pre-mapped obstacles from charts and newly detected obstacles.

### **Challenges & Considerations**

- *Variable Safety Margins*: Different obstacle types may require different clearance distances based on their nature and the sailing conditions.
- *Computational Efficiency*: Route planning must remain responsive even with numerous obstacles in the vicinity.
- *Integration with Dynamic Obstacle Avoidance*: Later, the system should will be extended to also evade moving obstacles. The implementation should be easily extensible.
- *Uncertainty Handling*: Account for positioning errors in both the sailboat’s location and the mapped obstacles.
- *Path Smoothing*: Generate navigable paths that avoid sharp turns while maintaining safe distances from obstacles.
