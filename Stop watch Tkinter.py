import tkinter as tk
from tkinter import ttk
import time

class EnhancedStopwatch:
    """A modern, easy-to-understand stopwatch application using Tkinter"""
    
    def __init__(self):
        # Create main window
        self.root = tk.Tk()
        self.root.title("Enhanced Stopwatch")
        self.root.geometry("450x300")
        self.root.resizable(False, False)
        self.root.configure(bg='#2b2b2b')
        
        # Time tracking variables
        self.total_milliseconds = 0  # Total elapsed time in milliseconds
        self.is_running = False      # Is the stopwatch currently running?
        self.start_time = 0         # When did we last start?
        
        # For updating the display
        self.update_job = None      # Store the scheduled update job
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface"""
        # Configure style for modern look
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2b2b2b', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Time display
        self.time_display = tk.Label(
            main_frame,
            text="00:00:00.00",
            font=('Courier New', 32, 'bold'),
            fg='#00ff88',
            bg='#1a1a1a',
            relief='solid',
            bd=3,
            padx=20,
            pady=20
        )
        self.time_display.pack(pady=(0, 20))
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg='#2b2b2b')
        button_frame.pack(pady=(0, 20))
        
        # Create buttons
        self.start_button = self.create_button(
            button_frame, "▶ START", '#4CAF50', self.start_stop, 0
        )
        
        self.reset_button = self.create_button(
            button_frame, "↻ RESET", '#f44336', self.reset, 1
        )
        
        self.lap_button = self.create_button(
            button_frame, "⏱ LAP", '#2196F3', self.record_lap, 2
        )
        
        # Lap times display
        lap_frame = tk.Frame(main_frame, bg='#1a1a1a', relief='solid', bd=1)
        lap_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 0))
        
        # Lap times label
        lap_title = tk.Label(
            lap_frame,
            text="LAP TIMES",
            font=('Arial', 10, 'bold'),
            fg='#ffffff',
            bg='#1a1a1a'
        )
        lap_title.pack(pady=(5, 0))
        
        # Scrollable lap times display
        self.lap_display = tk.Text(
            lap_frame,
            height=4,
            font=('Arial', 10),
            fg='#ffffff',
            bg='#1a1a1a',
            relief='flat',
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        self.lap_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Add initial message
        self.update_lap_display("Ready to start timing...")
        
    def create_button(self, parent, text, color, command, column):
        """Helper function to create styled buttons"""
        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=('Arial', 12, 'bold'),
            fg='white',
            bg=color,
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        button.grid(row=0, column=column, padx=10)
        
        # Add hover effects
        def on_enter(event):
            button.config(bg=self.darken_color(color))
            
        def on_leave(event):
            button.config(bg=color)
            
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        return button
    
    def darken_color(self, color):
        """Helper function to darken colors for hover effects"""
        color_map = {
            '#4CAF50': '#45a049',
            '#f44336': '#da190b',
            '#2196F3': '#1976D2'
        }
        return color_map.get(color, color)
    
    def start_stop(self):
        """Start or stop the stopwatch"""
        if self.is_running:
            # Stop the stopwatch
            self.is_running = False
            
            # Add the elapsed time since last start
            elapsed = int((time.time() - self.start_time) * 1000)
            self.total_milliseconds += elapsed
            
            # Cancel the update job
            if self.update_job:
                self.root.after_cancel(self.update_job)
                
            self.start_button.config(text="▶ START")
            self.update_lap_display("Stopped")
            
        else:
            # Start the stopwatch
            self.is_running = True
            self.start_time = time.time()
            self.start_button.config(text="⏸ STOP")
            self.update_display()  # Start the update loop
            self.update_lap_display("Running...")
    
    def reset(self):
        """Reset the stopwatch to zero"""
        # Stop if running
        if self.is_running:
            self.is_running = False
            if self.update_job:
                self.root.after_cancel(self.update_job)
        
        # Reset everything
        self.total_milliseconds = 0
        self.start_button.config(text="▶ START")
        self.time_display.config(text="00:00:00.00")
        
        # Clear lap times
        self.lap_display.config(state=tk.NORMAL)
        self.lap_display.delete(1.0, tk.END)
        self.lap_display.config(state=tk.DISABLED)
        self.update_lap_display("Ready to start timing...")
    
    def record_lap(self):
        """Record a lap time"""
        if self.total_milliseconds > 0 or self.is_running:
            current_ms = self.get_current_milliseconds()
            current_time = self.format_time(current_ms)
            
            # Get current lap count
            current_text = self.lap_display.get(1.0, tk.END).strip()
            lap_count = current_text.count("Lap ") + 1
            
            lap_text = f"Lap {lap_count}: {current_time}\n"
            
            self.lap_display.config(state=tk.NORMAL)
            if "Ready to start" in current_text or "Running..." in current_text or "Stopped" in current_text:
                self.lap_display.delete(1.0, tk.END)
            self.lap_display.insert(tk.END, lap_text)
            self.lap_display.see(tk.END)  # Scroll to bottom
            self.lap_display.config(state=tk.DISABLED)
    
    def get_current_milliseconds(self):
        """Get the current total milliseconds including running time"""
        current_ms = self.total_milliseconds
        if self.is_running:
            elapsed = int((time.time() - self.start_time) * 1000)
            current_ms += elapsed
        return current_ms
    
    def update_display(self):
        """Update the time display (called repeatedly when running)"""
        if self.is_running:
            current_ms = self.get_current_milliseconds()
            time_string = self.format_time(current_ms)
            self.time_display.config(text=time_string)
            
            # Schedule next update in 10ms
            self.update_job = self.root.after(10, self.update_display)
    
    def format_time(self, milliseconds):
        """Convert milliseconds to HH:MM:SS.CC format"""
        # Calculate time components
        hours = milliseconds // (1000 * 60 * 60)
        minutes = (milliseconds // (1000 * 60)) % 60
        seconds = (milliseconds // 1000) % 60
        centiseconds = (milliseconds // 10) % 100
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{centiseconds:02d}"
    
    def update_lap_display(self, message):
        """Update the lap display with a status message"""
        self.lap_display.config(state=tk.NORMAL)
        self.lap_display.delete(1.0, tk.END)
        self.lap_display.insert(1.0, message)
        self.lap_display.config(state=tk.DISABLED)
    
    def run(self):
        """Start the main event loop"""
        self.root.mainloop()

def main():
    """Main function to run the application"""
    stopwatch = EnhancedStopwatch()
    stopwatch.run()

if __name__ == "__main__":
    main()