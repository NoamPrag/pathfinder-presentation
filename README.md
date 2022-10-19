# Pathfinder Presentation

This presentation explains the algorithm for creating smooth paths and trajectory for FRC swerve robots, used in Orbit 1690's Pathfinder software.
The algorithm was developed in 2021's off-season, specifically optimized for swerve drive.
The original algorithm is written in Go.

## How to present
Just open an http server at the current directory:
```
git clone https://github.com/NoamPrag/pathfinder-presentation
cd pathfinder-presentation
python3 -m http.server
```

## Tools
animations - [manim](https://github.com/3b1b/manim.git)<br/>
presentation - [revealjs](https://revealjs.com/)<br/>
combination of the two - [manim-reveal](https://github.com/RickDW/manim-revealjs)

### How it works
Manim takes the scenes written python code and generates mp4 files containing the animations. What manim-revealjs does is to generate mp4 files but along with a json file containing "stops" for the presentation fragment animations.


## Build
### Requirements
manim and manim-revealjs can be installed with:
`pip install manim manim-revealjs`

### Generate animations
`python3 -m manim render my_slide.py MyScene`<br/>
Where 'my_slide.py' is the file containing the scene to be rendered and 'MyScene' is the name of the scene.