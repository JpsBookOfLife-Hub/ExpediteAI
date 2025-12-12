"""Modal UI overlay for displaying question answers."""
import tkinter as tk
import threading
import ctypes
from ctypes import wintypes
from typing import Optional


class AnswerModal:
    """Minimalistic dark-themed modal for displaying answers."""
    
    def __init__(self):
        self.root: Optional[tk.Tk] = None
        self.thread: Optional[threading.Thread] = None
        self.lock = threading.Lock()
        self._setup_window()
    
    def _setup_window(self):
        """Initialize the modal window with dark theme."""
        # Create tkinter root in a separate thread
        def create_window():
            self.root = tk.Tk()
            self.root.withdraw()  # Hide initially
            
            # Configure window properties
            self.root.overrideredirect(True)  # Remove window decorations
            self.root.attributes("-topmost", True)  # Always on top
            self.root.attributes("-alpha", 0.95)  # Slight transparency
            
            # Initialize click-through support (will be set when showing)
            self._hwnd = None
            self._gwl_exstyle = -20
            self._ws_ex_transparent = 0x20
            
            # Dark theme colors
            bg_color = "#1a1a1a"
            text_color = "#e0e0e0"
            border_color = "#ffffff"  # White border
            
            # Set root background to white for border effect
            self.root.configure(bg=border_color)
            
            # Create border frame (white)
            border_frame = tk.Frame(
                self.root,
                bg=border_color,
                padx=2,  # 2px white border
                pady=2
            )
            border_frame.pack(fill=tk.BOTH, expand=True)
            
            # Create main frame (dark background)
            self.frame = tk.Frame(
                border_frame,
                bg=bg_color,
                padx=20,
                pady=15,
                relief=tk.FLAT
            )
            self.frame.pack(fill=tk.BOTH, expand=True)
            
            # Answer label
            self.answer_label = tk.Label(
                self.frame,
                bg=bg_color,
                fg=text_color,
                font=("Segoe UI", 11),
                justify=tk.LEFT,
                wraplength=400,
                anchor="w"
            )
            self.answer_label.pack(fill=tk.BOTH, expand=True)
            
            # Store colors for later use
            self.bg_color = bg_color
            self.text_color = text_color
            self.warning_color = "#ff9800"  # Orange for warnings
            
            # Start the tkinter mainloop
            self.root.mainloop()
        
        # Start tkinter in a daemon thread
        self.thread = threading.Thread(target=create_window, daemon=True)
        self.thread.start()
        
        # Wait for window to be created
        import time
        max_wait = 2.0
        waited = 0.0
        while not self.root and waited < max_wait:
            time.sleep(0.1)
            waited += 0.1
    
    def _make_click_through(self):
        """Initialize Windows API constants for click-through."""
        if not self.root:
            return
        
        # Windows API constants
        GWL_EXSTYLE = -20
        WS_EX_TRANSPARENT = 0x20
        
        # Get window handle - need to wait for window to be mapped
        self.root.update_idletasks()
        hwnd = self.root.winfo_id()
        
        # Store for later use
        self._hwnd = hwnd
        self._gwl_exstyle = GWL_EXSTYLE
        self._ws_ex_transparent = WS_EX_TRANSPARENT
    
    def _set_click_through(self, enable: bool):
        """Enable or disable click-through for the window."""
        if not hasattr(self, '_hwnd') or not self._hwnd:
            return
        
        try:
            ex_style = ctypes.windll.user32.GetWindowLongPtrW(self._hwnd, self._gwl_exstyle)
            
            if enable:
                # Enable click-through
                ex_style |= self._ws_ex_transparent
            else:
                # Disable click-through
                ex_style &= ~self._ws_ex_transparent
            
            ctypes.windll.user32.SetWindowLongPtrW(self._hwnd, self._gwl_exstyle, ex_style)
        except Exception:
            pass  # Silently fail if API call doesn't work
    
    def show_answer(self, answer_text: str, duration: int = 3, is_warning: bool = False):
        """
        Display the answer in the modal and auto-dismiss after duration.
        
        Args:
            answer_text: The answer text to display
            duration: Number of seconds before auto-dismissing
            is_warning: If True, display with warning styling (orange text)
        """
        if not self.root:
            # Wait a bit more if root isn't ready
            import time
            time.sleep(0.2)
            if not self.root:
                print("Warning: Modal window not ready yet")
                return
        
        # Use after() to schedule on the tkinter thread
        def _show():
            if not self.root:
                return
            
            # Update answer text and styling
            text_color = self.warning_color if is_warning else self.text_color
            self.answer_label.config(text=answer_text, fg=text_color)
            
            # Position window at bottom-left
            self._position_window()
            
            # Show window and bring to front
            self.root.deiconify()
            self.root.lift()  # Bring to front
            self.root.attributes("-topmost", True)  # Ensure stays on top
            self.root.update()
            self.root.update_idletasks()
            
            # Initialize window handle for click-through if not already done
            if not self._hwnd:
                try:
                    self._hwnd = self.root.winfo_id()
                except:
                    pass
            
            # Make window click-through so clicks pass through to windows underneath
            # This allows you to interact with your browser while the modal is visible
            self._set_click_through(True)
            
            # Schedule auto-dismiss
            self.root.after(duration * 1000, self._hide_with_click_through)
        
        # Schedule on tkinter thread
        if self.root:
            self.root.after(0, _show)
    
    def _position_window(self):
        """Position the window at the bottom-left of the screen."""
        if not self.root:
            return
        
        # Calculate window size (includes 4px for border: 2px on each side)
        window_width = 454  # 450 + 4px border
        window_height = 124  # 120 + 4px border
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Position at bottom-left with some padding
        x = 20
        y = screen_height - window_height - 20
        
        # Set geometry
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.update_idletasks()
    
    def hide(self):
        """Hide the modal window."""
        self._hide_with_click_through()
    
    def _hide_with_click_through(self):
        """Hide the modal window and enable click-through."""
        if self.root:
            def _hide():
                if self.root:
                    # Enable click-through when hidden (though it's hidden anyway)
                    self._set_click_through(True)
                    self.root.withdraw()
            self.root.after(0, _hide)
    
    def destroy(self):
        """Destroy the modal window."""
        if self.root:
            def _destroy():
                if self.root:
                    self.root.quit()
                    self.root.destroy()
            self.root.after(0, _destroy)

