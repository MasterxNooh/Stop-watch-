import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QFrame)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont

class EnhancedStopwatch(QWidget):
    """A modern, easy-to-understand stopwatch application"""
    
    def __init__(self):
        super().__init__()
        
        # Time tracking variables
        self.total_milliseconds = 0  # Total elapsed time in milliseconds
        self.is_running = False      # Is the stopwatch currently running?
        
        # Create the timer (will tick every 10ms when active)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)  # Connect timer to update function
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface"""
        self.setWindowTitle("Enhanced Stopwatch")
        self.setFixedSize(400, 250)
        self.setStyleSheet("background-color: #2b2b2b;")  # Dark theme
        
        # Main layout (vertical)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create the time display with explicit font
        self.time_display = QLabel()
        self.time_display.setText("00:00:00.00")  # Set text explicitly
        self.time_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Set font using QFont (more reliable than CSS)
        display_font = QFont("Arial", 24)  # Use Arial which is always available
        display_font.setBold(True)
        self.time_display.setFont(display_font)
        
        # Style the display
        self.time_display.setStyleSheet("""
            QLabel {
                background-color: #1a1a1a;
                color: #00ff88;
                border: 3px solid #00ff88;
                border-radius: 15px;
                padding: 20px;
                min-height: 60px;
            }
        """)
        
        # Create buttons frame
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setSpacing(15)
        
        # Create buttons with simpler text
        self.start_button = self.create_button("START", "#4CAF50", self.start_stop)
        self.reset_button = self.create_button("RESET", "#f44336", self.reset)
        self.lap_button = self.create_button("LAP", "#2196F3", self.record_lap)
        
        # Add buttons to layout
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.lap_button)
        
        # Create lap times display
        self.lap_display = QLabel("Lap Times Will Appear Here")
        self.lap_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lap_display.setStyleSheet("""
            QLabel {
                background-color: #1a1a1a;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 10px;
                padding: 10px;
                font-size: 12px;
                min-height: 40px;
            }
        """)
        
        # Add everything to main layout
        main_layout.addWidget(self.time_display)
        main_layout.addWidget(button_frame)
        main_layout.addWidget(self.lap_display)
        
        self.setLayout(main_layout)
        
        # Force update display to make sure it shows correctly
        self.update_display_text()
        
    def create_button(self, text, color, function):
        """Helper function to create styled buttons"""
        button = QPushButton(text)
        button.clicked.connect(function)
        
        # Set button font
        button_font = QFont("Arial", 12)
        button_font.setBold(True)
        button.setFont(button_font)
        
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                min-width: 100px;
                min-height: 40px;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(color, 0.8)};
            }}
        """)
        return button
    
    def darken_color(self, color, factor=0.9):
        """Helper function to darken colors for hover effects"""
        if color == "#4CAF50":
            return "#45a049" if factor == 0.9 else "#3d8b40"
        elif color == "#f44336":
            return "#da190b" if factor == 0.9 else "#c41e3a"
        elif color == "#2196F3":
            return "#1976D2" if factor == 0.9 else "#1565C0"
        return color
    
    def start_stop(self):
        """Start or stop the stopwatch"""
        if self.is_running:
            # Stop the stopwatch
            self.timer.stop()
            self.is_running = False
            self.start_button.setText("START")
        else:
            # Start the stopwatch
            self.timer.start(10)  # Update every 10 milliseconds
            self.is_running = True
            self.start_button.setText("STOP")
    
    def reset(self):
        """Reset the stopwatch to zero"""
        self.timer.stop()
        self.is_running = False
        self.total_milliseconds = 0
        self.start_button.setText("START")
        self.update_display_text()
        self.lap_display.setText("Lap Times Will Appear Here")
    
    def record_lap(self):
        """Record a lap time"""
        if self.total_milliseconds > 0:
            current_time = self.format_time(self.total_milliseconds)
            current_text = self.lap_display.text()
            
            if current_text == "Lap Times Will Appear Here":
                self.lap_display.setText(f"Lap 1: {current_time}")
            else:
                # Count existing laps and add new one
                lap_count = current_text.count("Lap") + 1
                new_text = f"{current_text} | Lap {lap_count}: {current_time}"
                self.lap_display.setText(new_text)
    
    def update_time(self):
        """Update the time (called every 10ms when running)"""
        self.total_milliseconds += 10
        self.update_display_text()
    
    def format_time(self, milliseconds):
        """Convert milliseconds to HH:MM:SS.CC format"""
        # Calculate time components
        hours = milliseconds // (1000 * 60 * 60)
        minutes = (milliseconds // (1000 * 60)) % 60
        seconds = (milliseconds // 1000) % 60
        centiseconds = (milliseconds // 10) % 100
        
        # Use string formatting to ensure proper display
        time_str = "{:02d}:{:02d}:{:02d}.{:02d}".format(hours, minutes, seconds, centiseconds)
        return time_str
    
    def update_display_text(self):
        """Update the time display with current time"""
        time_text = self.format_time(self.total_milliseconds)
        self.time_display.setText(time_text)
        print(f"Display updated to: {time_text}")  # Debug print

def main():
    """Main function to run the application"""
    app = QApplication(sys.argv)
    
    stopwatch = EnhancedStopwatch()
    stopwatch.show()
    
    # Debug: Print what's actually being displayed
    print(f"Initial display text: '{stopwatch.time_display.text()}'")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()