# Robot Grid Simulator
A comprehensive Python-based robot simulation system with both command-line and web interfaces. This project serves as a foundational exercise for AI and ROS2 integration training, featuring advanced robot control logic, path planning, and modern web interface design.

## Project Purpose

This simulator provides hands-on experience in several core areas of robotics and software development:

- **Robot Control Systems:** Implementing movement logic, pathfinding, and basic navigation strategies.
- **Object-Oriented Programming:** Applying clean Python architecture and design principles.
- **Web Development:** Integrating a Flask backend with an interactive HTML/JavaScript frontend.
- **Full-Stack Integration:** Connecting Python logic with a responsive web-based interface.
- **ROS2 Preparation:** Introducing foundational concepts used in modern Robot Operating Systems (ROS2).

##  Quick Start

###  Prerequisites

Make sure you have the following installed on your system:

- **Python 3.7+**
- **Git**
- **Web browser** (for viewing the web interface)
- **(Optional)**: `Flask` and `Flask-CORS`  
  *Only required if you're running the web version*

To install Flask and Flask-CORS:

```bash
pip install flask flask-cors

```
## Setup
1)Clone the repository
```bash
git clone https://github.com/AwsSafi04/robot-grid-simulator.git
cd robot-grid-simulator

```
2)Set up virtual environment
```bash
# Windows
python -m venv robot_env
robot_env\Scripts\activate

# macOS/Linux
python3 -m venv robot_env
source robot_env/bin/activate

```
3)Install dependencies
```bash
pip install -r requirements.txt

```
## Running the Simulator
- **Command-Line Version**
  ```bash
  python robot_simulator.py
- **Web Version**
  ```bash
  python app.py

  ```
  Open http://localhost:5000 in your browser.
  Use buttons or keyboard to control the robot.


## File Structure
```bash
robot-grid-simulator/
├── robot_simulator.py      # Core logic
├── app.py                  # Flask backend
├── requirements.txt        # Dependencies
└── templates/
    └── index.html          # Web UI

  

