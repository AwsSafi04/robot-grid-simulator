#!/usr/bin/env python3
"""
Flask Web App - Connects Python Robot Simulator to HTML Interface
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json

# Import your existing RobotSimulator class
from robot_simulator import RobotSimulator

app = Flask(__name__)
CORS(app)  # Enable CORS for web requests

# Global robot instance
robot = RobotSimulator()

@app.route('/')
def index():
    """Serve the main HTML interface"""
    return render_template('index.html')

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current robot status"""
    return jsonify({
        'success': True,
        'data': {
            'x': robot.x,
            'y': robot.y,
            'facing': robot.facing.name,
            'battery': robot.battery_level if robot.enable_battery else 100,
            'moveCount': len(robot.move_history) - 1,
            'obstacles': robot.obstacles,
            'gridSize': robot.grid_size
        }
    })

@app.route('/api/command', methods=['POST'])
def execute_command():
    """Execute a robot command"""
     # Move global declaration to the top!
    
    try:
        global robot 
        data = request.get_json()
        command = data.get('command', '').lower()
        
        print(f"Executing command: {command}")  # Debug log
        
        if command == 'forward':
            result = robot.forward()
        elif command == 'backward':
            result = robot.backward()
        elif command == 'left':
            result = robot.left()
        elif command == 'right':
            result = robot.right()
        elif command == 'recharge':
            result = robot.recharge()
        elif command == 'reset':
            # Reset robot to initial state
            robot = RobotSimulator()
            result = "Robot reset to initial position"
        else:
            return jsonify({
                'success': False,
                'message': f'Unknown command: {command}'
            })
        
        print(f"Result: {result}")  # Debug log
        
        # Return result with current status
        return jsonify({
            'success': True,
            'message': result,
            'data': {
                'x': robot.x,
                'y': robot.y,
                'facing': robot.facing.name,
                'battery': robot.battery_level if robot.enable_battery else 100,
                'moveCount': len(robot.move_history) - 1,
                'obstacles': robot.obstacles
            }
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug log
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/api/diagonal', methods=['POST'])
def execute_diagonal():
    """Execute diagonal movement"""
    try:
        data = request.get_json()
        direction = data.get('direction', '').lower()
        
        print(f"Executing diagonal: {direction}")  # Debug log
        
        result = robot.diagonal_move(direction)
        
        print(f"Result: {result}")  # Debug log
        
        return jsonify({
            'success': True,
            'message': result,
            'data': {
                'x': robot.x,
                'y': robot.y,
                'facing': robot.facing.name,
                'battery': robot.battery_level if robot.enable_battery else 100,
                'moveCount': len(robot.move_history) - 1,
                'obstacles': robot.obstacles
            }
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug log
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/api/turn', methods=['POST'])
def turn_to_direction():
    """Turn robot to specific direction"""
    try:
        data = request.get_json()
        direction = data.get('direction', '').upper()
        
        print(f"Turning to: {direction}")  # Debug log
        
        # Map direction names to Direction enum values
        from robot_simulator import Direction
        direction_map = {
            'NORTH': Direction.NORTH,
            'EAST': Direction.EAST,
            'SOUTH': Direction.SOUTH,
            'WEST': Direction.WEST
        }
        
        if direction not in direction_map:
            return jsonify({
                'success': False,
                'message': f'Invalid direction: {direction}'
            })
        
        target_direction = direction_map[direction]
        
        # Turn until facing the right direction
        turns = 0
        while robot.facing != target_direction and turns < 4:
            robot.right()
            turns += 1
        
        result = f"Turned to face {direction}"
        print(f"Result: {result}")  # Debug log
        
        return jsonify({
            'success': True,
            'message': result,
            'data': {
                'x': robot.x,
                'y': robot.y,
                'facing': robot.facing.name,
                'battery': robot.battery_level if robot.enable_battery else 100,
                'moveCount': len(robot.move_history) - 1,
                'obstacles': robot.obstacles
            }
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug log
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/api/obstacles', methods=['POST'])
def modify_obstacles():
    """Add or remove obstacles"""
    try:
        data = request.get_json()
        action = data.get('action', '').lower()
        
        print(f"Obstacle action: {action}")  # Debug log
        
        if action == 'clear':
            robot.obstacles = []
            message = 'All obstacles cleared'
        elif action == 'reset':
            robot.obstacles = [(2, 2), (3, 4), (1, 3)]
            message = 'Obstacles reset to default'
        elif action == 'toggle':
            x = data.get('x')
            y = data.get('y')
            
            if x is None or y is None:
                return jsonify({'success': False, 'message': 'Missing x or y coordinate'})
            
            # Don't allow obstacle on robot position
            if x == robot.x and y == robot.y:
                return jsonify({'success': False, 'message': 'Cannot place obstacle on robot position'})
            
            # Check if obstacle exists
            obstacle_pos = (x, y)
            if obstacle_pos in robot.obstacles:
                robot.obstacles.remove(obstacle_pos)
                message = f'Removed obstacle at ({x}, {y})'
            else:
                robot.obstacles.append(obstacle_pos)
                message = f'Added obstacle at ({x}, {y})'
        else:
            return jsonify({'success': False, 'message': 'Invalid action'})
        
        print(f"Result: {message}")  # Debug log
        
        return jsonify({
            'success': True,
            'message': message,
            'data': {
                'obstacles': robot.obstacles
            }
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug log
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/api/report', methods=['GET'])
def get_report():
    """Generate detailed robot report"""
    try:
        print("Generating report...")  # Debug log
        
        report = robot.report()
        
        return jsonify({
            'success': True,
            'message': report
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug log
        return jsonify({
            'success': False,
            'message': f'Error generating report: {str(e)}'
        })

if __name__ == '__main__':
    print("Starting Robot Simulator Web Server...")
    print("Open your browser to: http://localhost:5000")
    print("Watch this console for robot command logs!")
    print("=" * 50)

    app.run(debug=True, host='0.0.0.0', port=5000)
