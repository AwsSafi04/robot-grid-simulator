#!/usr/bin/env python3
"""
Robot Grid Simulator - AI & ROS2 Integration Training
A 5x5 grid robot simulator with basic movement and optional enhancements.
"""

import sys
from enum import Enum
from typing import Tuple, List, Optional


class Direction(Enum):
    """Enumeration for robot facing directions."""
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class RobotSimulator:
    """
    A robot simulator that operates on a 5x5 grid.
    
    The robot can move forward, turn left/right, and report its status.
    Optional features include battery simulation, obstacles, and diagonal movement.
    """
    
    def __init__(self, grid_size: int = 5, enable_battery: bool = True, enable_obstacles: bool = True):
        """
        Initialize the robot simulator.
        
        Args:
            grid_size: Size of the square grid (default 5x5)
            enable_battery: Enable battery level simulation
            enable_obstacles: Enable obstacle placement
        """
        self.grid_size = grid_size
        self.x = 0  # Starting X position
        self.y = 0  # Starting Y position
        self.facing = Direction.NORTH  # Starting direction
        
        # Optional features
        self.enable_battery = enable_battery
        self.battery_level = 100 if enable_battery else None
        self.battery_drain_per_move = 5
        
        # Obstacles (optional enhancement)
        self.enable_obstacles = enable_obstacles
        self.obstacles: List[Tuple[int, int]] = []
        if enable_obstacles:
            # Add some default obstacles
            self.obstacles = [(2, 2), (3, 4), (1, 3)]
        
        # Movement history for tracking
        self.move_history: List[Tuple[int, int, Direction]] = []
        self._record_position()
        
    def _record_position(self):
        """Record current position and direction in history."""
        self.move_history.append((self.x, self.y, self.facing))
    
    def _is_valid_position(self, x: int, y: int) -> bool:
        """
        Check if a position is valid (within grid and not an obstacle).
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            bool: True if position is valid
        """
        # Check grid boundaries
        if not (0 <= x < self.grid_size and 0 <= y < self.grid_size):
            return False
        
        # Check obstacles
        if self.enable_obstacles and (x, y) in self.obstacles:
            return False
        
        return True
    
    def _get_next_position(self, reverse: bool = False) -> Tuple[int, int]:
        """
        Get the next position based on current facing direction.
        
        Args:
            reverse: If True, get position behind the robot
            
        Returns:
            Tuple[int, int]: Next (x, y) position
        """
        multiplier = -1 if reverse else 1
        
        if self.facing == Direction.NORTH:
            return (self.x, self.y + (1 * multiplier))
        elif self.facing == Direction.EAST:
            return (self.x + (1 * multiplier), self.y)
        elif self.facing == Direction.SOUTH:
            return (self.x, self.y - (1 * multiplier))
        elif self.facing == Direction.WEST:
            return (self.x - (1 * multiplier), self.y)
    
    def _check_battery(self) -> bool:
        """
        Check if robot has enough battery for a move.
        
        Returns:
            bool: True if battery is sufficient or disabled
        """
        if not self.enable_battery:
            return True
        return self.battery_level >= self.battery_drain_per_move
    
    def _consume_battery(self):
        """Consume battery for a move."""
        if self.enable_battery:
            self.battery_level = max(0, self.battery_level - self.battery_drain_per_move)
    
    def forward(self) -> str:
        """
        Move the robot forward one step in the current facing direction.
        
        Returns:
            str: Status message about the move
        """
        try:
            # Check battery
            if not self._check_battery():
                return "ERROR: Insufficient battery to move"
            
            # Calculate next position
            next_x, next_y = self._get_next_position()
            
            # Validate position
            if not self._is_valid_position(next_x, next_y):
                if (next_x, next_y) in self.obstacles:
                    return f"ERROR: Cannot move to ({next_x}, {next_y}) - obstacle present"
                else:
                    return f"ERROR: Cannot move to ({next_x}, {next_y}) - outside grid boundaries"
            
            # Execute move
            self.x, self.y = next_x, next_y
            self._consume_battery()
            self._record_position()
            
            return f"Moved forward to ({self.x}, {self.y})"
            
        except Exception as e:
            return f"ERROR: Unexpected error during forward movement: {str(e)}"
    
    def backward(self) -> str:
        """
        Move the robot backward one step (opposite to current facing direction).
        
        Returns:
            str: Status message about the move
        """
        try:
            # Check battery
            if not self._check_battery():
                return "ERROR: Insufficient battery to move"
            
            # Calculate backward position (reverse=True)
            next_x, next_y = self._get_next_position(reverse=True)
            
            # Validate position
            if not self._is_valid_position(next_x, next_y):
                if (next_x, next_y) in self.obstacles:
                    return f"ERROR: Cannot move backward to ({next_x}, {next_y}) - obstacle present"
                else:
                    return f"ERROR: Cannot move backward to ({next_x}, {next_y}) - outside grid boundaries"
            
            # Execute move
            self.x, self.y = next_x, next_y
            self._consume_battery()
            self._record_position()
            
            return f"Moved backward to ({self.x}, {self.y})"
            
        except Exception as e:
            return f"ERROR: Unexpected error during backward movement: {str(e)}"
    
    def left(self) -> str:
        """
        Turn the robot left (counter-clockwise).
        
        Returns:
            str: Status message about the turn
        """
        try:
            self.facing = Direction((self.facing.value - 1) % 4)
            return f"Turned left, now facing {self.facing.name}"
        except Exception as e:
            return f"ERROR: Unexpected error during left turn: {str(e)}"
    
    def right(self) -> str:
        """
        Turn the robot right (clockwise).
        
        Returns:
            str: Status message about the turn
        """
        try:
            self.facing = Direction((self.facing.value + 1) % 4)
            return f"Turned right, now facing {self.facing.name}"
        except Exception as e:
            return f"ERROR: Unexpected error during right turn: {str(e)}"
    
    def report(self) -> str:
        """
        Generate a status report of the robot's current state.
        
        Returns:
            str: Detailed status report
        """
        try:
            report_lines = [
                f"Robot Status Report:",
                f"Position: ({self.x}, {self.y})",
                f"Facing: {self.facing.name}",
                f"Grid Size: {self.grid_size}x{self.grid_size}"
            ]
            
            if self.enable_battery:
                battery_status = "CRITICAL" if self.battery_level <= 20 else "OK"
                report_lines.append(f"Battery: {self.battery_level}% ({battery_status})")
            
            if self.enable_obstacles:
                report_lines.append(f"Obstacles at: {self.obstacles}")
            
            report_lines.append(f"Total moves: {len(self.move_history) - 1}")
            
            return "\n".join(report_lines)
            
        except Exception as e:
            return f"ERROR: Could not generate report: {str(e)}"
    
    def diagonal_move(self, direction: str) -> str:
        """
        Optional enhancement: Move diagonally.
        
        Args:
            direction: 'ne', 'se', 'sw', 'nw' for northeast, southeast, southwest, northwest
            
        Returns:
            str: Status message about the move
        """
        try:
            if not self._check_battery():
                return "ERROR: Insufficient battery to move"
            
            direction_map = {
                'ne': (1, 1),   # northeast
                'se': (1, -1),  # southeast
                'sw': (-1, -1), # southwest
                'nw': (-1, 1)   # northwest
            }
            
            if direction.lower() not in direction_map:
                return "ERROR: Invalid diagonal direction. Use: ne, se, sw, nw"
            
            dx, dy = direction_map[direction.lower()]
            next_x, next_y = self.x + dx, self.y + dy
            
            if not self._is_valid_position(next_x, next_y):
                return f"ERROR: Cannot move diagonally to ({next_x}, {next_y})"
            
            self.x, self.y = next_x, next_y
            self._consume_battery()
            self._record_position()
            
            return f"Moved diagonally {direction.upper()} to ({self.x}, {self.y})"
            
        except Exception as e:
            return f"ERROR: Unexpected error during diagonal movement: {str(e)}"
    
    def display_grid(self) -> str:
        """
        Display the current grid with robot position and obstacles.
        
        Returns:
            str: ASCII representation of the grid
        """
        try:
            print("\n" + "="*25)
            print("   CURRENT GRID STATE")
            print("="*25)
            
            # Display from top to bottom (y decreases)
            for y in range(self.grid_size - 1, -1, -1):
                row = []
                for x in range(self.grid_size):
                    if x == self.x and y == self.y:
                        # Robot position with direction
                        direction_symbols = {
                            Direction.NORTH: '^',
                            Direction.EAST: '>',
                            Direction.SOUTH: 'v',
                            Direction.WEST: '<'
                        }
                        row.append(direction_symbols[self.facing])
                    elif (x, y) in self.obstacles:
                        row.append('X')  # Obstacle
                    else:
                        row.append('.')  # Empty space
                row_str = ' '.join(row)
                print(f"{y} | {row_str}")
            
            # Add x-axis labels
            print('  +' + '-' * (self.grid_size * 2))
            x_labels = '  | ' + ' '.join(str(i) for i in range(self.grid_size))
            print(x_labels)
            print()
            print("Legend: ^ > v < = Robot facing direction")
            print("        X = Obstacle, . = Empty space")
            print("="*25)
            
        except Exception as e:
            print(f"ERROR: Could not display grid: {str(e)}")
    
    def recharge(self) -> str:
        """
        Optional enhancement: Recharge the robot's battery.
        
        Returns:
            str: Status message about recharging
        """
        if not self.enable_battery:
            return "Battery system is disabled"
        
        self.battery_level = 100
        return "Battery recharged to 100%"
    
    def execute_command(self, command: str) -> str:
        """
        Execute a command string and display grid for movement commands.
        
        Args:
            command: Command to execute
            
        Returns:
            str: Result of command execution
        """
        command = command.strip().lower()
        
        try:
            result = ""
            show_grid = False  # Flag to determine if we should show grid
            
            if command == 'forward' or command == 'f':
                result = self.forward()
                show_grid = True
            elif command == 'backward' or command == 'back' or command == 'b':
                result = self.backward()
                show_grid = True
            elif command == 'left' or command == 'l':
                result = self.left()
                show_grid = True
            elif command == 'right' or command == 'r':
                result = self.right()
                show_grid = True
            elif command == 'report':
                result = self.report()
            elif command == 'recharge':
                result = self.recharge()
            elif command.startswith('diagonal '):
                direction = command.split()[1]
                result = self.diagonal_move(direction)
                show_grid = True
            elif command == 'grid':
                self.display_grid()
                result = "Grid displayed above"
            elif command == 'help':
                result = self.get_help()
            else:
                result = f"ERROR: Unknown command '{command}'. Type 'help' for available commands."
            
            # Show grid after movement commands
            if show_grid:
                self.display_grid()
                
            return result
                
        except Exception as e:
            return f"ERROR: Failed to execute command '{command}': {str(e)}"
    
    def get_help(self) -> str:
        """
        Return help text with available commands.
        
        Returns:
            str: Help text
        """
        help_text = [
            "Available Commands:",
            "  forward (f)     - Move forward one step",
            "  backward (b)    - Move backward one step", 
            "  left (l)        - Turn left",
            "  right (r)       - Turn right", 
            "  report          - Show robot status",
            "  grid            - Display current grid",
            "  diagonal <dir>  - Move diagonally (ne/se/sw/nw)",
            "  recharge        - Recharge battery to 100%",
            "  help            - Show this help",
            "  quit            - Exit simulator"
        ]
        return '\n'.join(help_text)


def main():
    """Main function to run the robot simulator interactively."""
    print("Robot Grid Simulator - AI & ROS2 Integration Training")
    print("=" * 50)
    
    # Initialize robot with optional features
    robot = RobotSimulator(grid_size=5, enable_battery=True, enable_obstacles=True)
    
    print("Robot initialized at (0, 0) facing NORTH")
    print("Type 'help' for available commands, 'quit' to exit")
    
    # Show initial grid state
    robot.display_grid()
    
    while True:
        try:
            command = input("Enter command: ").strip()
            
            if command.lower() == 'quit':
                print("Shutting down robot simulator...")
                break
            
            if not command:
                continue
                
            result = robot.execute_command(command)
            print(result)
            print()  # Empty line for readability
            
        except KeyboardInterrupt:
            print("\n\nShutting down robot simulator...")
            break
        except Exception as e:
            print(f"ERROR: Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()