# Sw00pGenerator3000 (SG3K)

The Sw00pGenerator3000, or SG3K, is a cutting-edge GPS analysis tool meticulously crafted to empower swoopers at every level of expertise. Whether you're taking your first plunge into the exhilarating world of swooping or you're a seasoned competitor seeking continuous improvement, the SG3K is your key to accelerating your learning curve. With this advanced tool, you can make remarkable progress in refining your performance while minimizing the number of jumps needed.

But wait, what's swooping without FlySight? FlySight is not your ordinary GPS; it's tailor-made for wingsuit pilots and introduces a revolutionary feature. Providing real-time audible indications of glide ratio, horizontal, or vertical speed, FlySight takes your flying experience to new heights. For more detailed information on FlySight, check out this [link](https://github.com/flysight/flysight). Thanks to the flysight we can visualize our swoop and get the following information out of it.

## Requirements

To successfully use the Sw00pGenerator3000, you'll need the following:

- **Make**: A build automation tool to manage the build process.
- **Docker**: A platform for developing, shipping, and running applications in containers.
- **Mapbox token**: An access token for using Mapbox services, required for some of the visualisation features.

## Steps to Get Started 

1. Clone this repository
2. Execute **'make copy'** or **'make c'** to generate an **.env** file
3. Enter your Mapbox token in the **.env** file
4. Run **'make docker-compose-up'** or **'make dc'**
5. Navigate to http://localhost:8888/lab/tree/notebook/sg3k_pro.ipynb and follow the instructions in the notebook

## Flight Analysis Metrics

The Sw00pGenerator3000 provides a comprehensive set of metrics to help you refine your swooping skills. Below are the key performance indicators for your recent flight:

```
exited airplane:      5728.9 ft AGL
toggle search:        828.3 ft AGL, 83.2 m back, -102.2 m offset
initiated turn:       777.9 ft AGL, 81.3 m back, -68.9 m offset
max vertical speed:   185.0 ft AGL, 94.7 m back, -37.3 m offset (95.0 km/u)
started rollout:      151.0 ft AGL, 92.1 m back, -32.8 m offset (91.3 km/u)
finished rollout:     2.2 ft AGL, 0.0 m back, 0.0 m offset
max horizontal speed: 29.9 ft AGL, 49.1 m back, -15.7 m offset (86.5 km/u)

degrees of rotation:      ---- deg (--- -hand)
time to execute turn:     15.4 sec
time during rollout:      4.6 sec
time aloft during swoop:  7.0 sec

entry gate speed:      65.2 km/u
distance to stop:      52.77 m
```

## Visualisations

The Sw00pGenerator3000 provides a range of visualisations to help you gain a deeper understanding of your flight. These visualisations offer a detailed breakdown of your performance, allowing you to identify areas for improvement and refine your skills.

### Overview

This provides a comprehensive overview of the maneuver, displaying elevation, horizontal speed, vertical speed, and the dive angle. Additionally, two vertical lines are incorporated to offer more information regarding the commencement and conclusion of the rollout.

![overview](notebook/img/overview.png)

### Side View Of Flight Path

A profile view of the flight path: This perspective offers a clear observation of the landing's rollout, revealing the steepness and proximity to the gate during the approach. Additionally, it provides insight into the altitude at which the maneuver was initiated.

![sideview](notebook/img/sideview.png)

### Overhead View Of Flight Path

Get a bird's-eye view of your flight trajectory, providing a unique perspective on your performance.

![overhead](notebook/img/overhead.png)

### Map

See your flight trajectory overlaid on satellite imagery, giving you a real-world perspective on your flight.

![map](notebook/img/map.png)

### Horizontal Speed

This plot illustrates your horizontal speed throughout the maneuver, helping you identify areas where you can improve your speed and agility.

![speed](notebook/img/speed.png)