import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk, font
import pyautogui
import time
import threading
import math
import random

class UI:
    """Modern UI styling configuration"""
    
    # Color scheme - Dark theme with accent colors
    BACKGROUND = "#1e1e1e"
    SURFACE = "#2d2d2d" 
    SURFACE_VARIANT = "#404040"
    PRIMARY = "#007acc"
    PRIMARY_VARIANT = "#005a9e"
    ACCENT = "#00d4aa"
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#b3b3b3"
    TEXT_TERTIARY = "#808080"
    SUCCESS = "#4caf50"
    WARNING = "#ff9800"
    ERROR = "#f44336"
    BORDER = "#555555"
    
    # Typography - Modern sans-serif fonts (0xProto priority)
    FONT_FAMILY = "0xProto Nerd Font"
    FONT_FAMILY_ALT = [
        "0xProto",
        "0xProtoNerdFont", 
        "0xProto Nerd Font Regular",
        "0xProto Regular",
        "Segoe UI",
        "Calibri", 
        "Trebuchet MS", 
        "Verdana", 
        "Arial", 
        "Helvetica"
    ]
    
    # Sizes and spacing
    CORNER_RADIUS = 8
    PADDING_SMALL = 8
    PADDING_MEDIUM = 16
    PADDING_LARGE = 24
    
    @classmethod
    def get_font(cls, size=11, weight="normal"):
        """Get a modern font with fallback options"""
        import tkinter.font as tkFont
        
        # Ensure weight is valid
        font_weight = "bold" if weight == "bold" else "normal"
        
        # Get available system fonts
        try:
            available_fonts = list(tkFont.families())
        except:
            available_fonts = []
        
        # Try fonts in order of preference
        preferred_fonts = [
            "0xProto Nerd Font",
            "0xProto", 
            "0xProtoNerdFont",
            cls.FONT_FAMILY
        ] + cls.FONT_FAMILY_ALT
        # Filter for any Proto fonts available
        proto_fonts = [f for f in available_fonts if "0x" in f or "Proto" in f.lower()]
        if proto_fonts:
            print(f"Found Proto fonts: {proto_fonts[:3]}")
        
        for font_name in preferred_fonts:
            if font_name in available_fonts:
                try:
                    print(f"Using font: {font_name}")
                    return tkFont.Font(family=font_name, size=size, weight=font_weight)
                except Exception as e:
                    print(f"Font {font_name} failed: {e}")
                    continue
        
        # Ultimate fallback
        print("Using fallback font: Arial")
        return tkFont.Font(family="Arial", size=size, weight=font_weight)


class ModernFrame(tk.Frame):
    """Custom frame with modern styling"""
    
    def __init__(self, parent, **kwargs):
        # Extract custom options
        bg_color = kwargs.pop('bg_color', UI.SURFACE)
        corner_radius = kwargs.pop('corner_radius', UI.CORNER_RADIUS)
        
        super().__init__(parent, bg=bg_color, **kwargs)
        self.corner_radius = corner_radius
        
        # Add hover effects
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
    def _on_enter(self, event=None):
        """Subtle hover effect"""
        pass
        
    def _on_leave(self, event=None):
        """Reset hover effect"""
        pass


class Button(tk.Button):
    """Custom button with modern styling and hover effects"""
    
    def __init__(self, parent, **kwargs):
        # Extract custom styling
        button_type = kwargs.pop('button_type', 'primary')
        
        if button_type == 'primary':
            bg = UI.PRIMARY
            fg = UI.TEXT_PRIMARY
            active_bg = UI.PRIMARY_VARIANT
        elif button_type == 'accent':
            bg = UI.ACCENT
            fg = UI.BACKGROUND
            active_bg = "#00b894"
        else:  # secondary
            bg = UI.SURFACE_VARIANT
            fg = UI.TEXT_PRIMARY
            active_bg = UI.BORDER
        
        super().__init__(
            parent,
            bg=bg,
            fg=fg,
            activebackground=active_bg,
            activeforeground=fg,
            bd=0,
            relief='flat',
            cursor='hand2',
            font=UI.get_font(10, 'bold'),
            **kwargs
        )
        
        # Store colors for hover effects
        self.default_bg = bg
        self.hover_bg = active_bg
        
        # Bind hover events
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
    def _on_enter(self, event=None):
        """Hover effect"""
        self.config(bg=self.hover_bg)
        
    def _on_leave(self, event=None):
        """Remove hover effect"""
        self.config(bg=self.default_bg)


class SplashScreen:
    """Modern circular splash screen with gradient and slide-up animation"""
    
    def __init__(self, main_callback):
        self.main_callback = main_callback
        self.splash = tk.Toplevel()
        self.gradient_frames = []
        self.animation_frame = 0
        self.setup_splash()
        self.animate_entrance()
        
    def setup_splash(self):
        """Setup simple black square splash screen"""
        # Remove window decorations
        self.splash.overrideredirect(True)
        
        # Set size for square design
        self.size = 300
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        
        # Center on screen
        self.center_x = (screen_width - self.size) // 2
        self.center_y = (screen_height - self.size) // 2
        
        self.splash.geometry(f"{self.size}x{self.size}+{self.center_x}+{self.center_y}")
        
        # Set black background
        self.splash.configure(bg='#000000')
        
        # Make it topmost and transparent initially
        self.splash.attributes('-topmost', True)
        self.splash.attributes('-alpha', 0.0)
        
        # Create content
        self.create_splash_content()
        
    def create_splash_content(self):
        """Create simple splash screen content with logo only"""
        # Create main frame for centering content
        main_frame = tk.Frame(self.splash, bg='#000000')
        main_frame.pack(fill='both', expand=True)
        
        # Center the logo
        logo_frame = tk.Frame(main_frame, bg='#000000')
        logo_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Main logo
        self.logo_label = tk.Label(
            logo_frame,
            text="⌨",
            font=UI.get_font(48),
            bg='#000000',
            fg='#ffffff'
        )
        self.logo_label.pack()
        
        # App name below logo
        self.title_label = tk.Label(
            logo_frame,
            text="Keystroke Replayer",
            font=UI.get_font(16, 'bold'),
            bg='#000000',
            fg='#ffffff'
        )
        self.title_label.pack(pady=(10, 0))

        
    def animate_entrance(self):
        """Simple fade-in animation"""
        def fade_in(alpha=0.0):
            if alpha <= 0.95:
                self.splash.attributes('-alpha', alpha)
                self.splash.after(30, lambda: fade_in(alpha + 0.05))
            else:
                # Set final opacity and hold for 3 seconds
                self.splash.attributes('-alpha', 0.95)
                self.splash.after(3000, self.fade_out)
        
        fade_in()
        
    def fade_out(self):
        """Simple fade out animation"""
        def fade_out_step(alpha=0.95):
            if alpha > 0.0:
                new_alpha = max(0.0, alpha - 0.08)
                self.splash.attributes('-alpha', new_alpha)
                self.splash.after(40, lambda: fade_out_step(new_alpha))
            else:
                self.splash.destroy()
                self.main_callback()
        
        fade_out_step()


class KeystrokeReplayer:
    def __init__(self, root):
        self.root = root
        self.is_closing = False
        self.is_paused = False
        self.resume_requested = False
        self.current_replay_thread = None
        self.setup_window()
        
        # Configure pyautogui settings
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.01
        
        self.setup_modern_ui()
        self.setup_window_effects()
        self.setup_global_hotkeys()
    def setup_global_hotkeys(self):
        """Setup global hotkeys that work system-wide"""
        try:
            from pynput import keyboard
            
            def on_press(key):
                try:
                    if key == keyboard.Key.f9:
                        self.toggle_pause_resume()
                except AttributeError:
                    pass
            
            # Start global listener in a separate thread
            self.listener = keyboard.Listener(on_press=on_press)
            self.listener.daemon = True
            self.listener.start()
        except ImportError:
            # Fallback to window-focused hotkeys if pynput not available
            self.setup_local_hotkeys()
            
    def setup_local_hotkeys(self):
        """Fallback local hotkeys (only work when window has focus)"""
        self.root.bind('<F9>', self.toggle_pause_resume)
        self.root.focus_set()
        
    def toggle_pause_resume(self, event=None):
        """Toggle pause/resume of the current replay"""
        if self.current_replay_thread and self.current_replay_thread.is_alive():
            if self.is_paused:
                # Resume
                self.is_paused = False
                self.resume_requested = True
                self.update_status("Resumed (F9 to pause)", UI.SUCCESS, "▶")
                self.replay_button.config(text="⏸ Replaying...")
            else:
                # Pause
                self.is_paused = True
                self.update_status("Paused (F9 to resume)", UI.WARNING, "⏸")
                self.replay_button.config(text="⏸ Paused - F9 to Resume")
        
        return 'break'  # Prevent event from bubbling up
        
    def setup_window(self):
        """Configure the main window with modern styling"""
        self.root.title("Keystroke Replayer")
        
        # Set minimum size and make resizable - increased height for new settings
        self.root.minsize(800, 750)  # Increased from 700x600 to accommodate settings
        self.root.geometry("900x800")  # Increased from 800x700
        
        # Modern window styling
        self.root.configure(bg=UI.BACKGROUND)
        
        # Try to remove title bar decorations (Windows)
        try:
            self.root.wm_attributes('-alpha', 0.98)  # Slight transparency
        except:
            pass
            
        # Center window on screen
        self.center_window()
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def setup_window_effects(self):
        """Setup modern window effects"""
        # Fade in effect
        self.root.attributes('-alpha', 0.0)
        self.fade_in()
        
    def fade_in(self):
        """Fade in the main window"""
        def fade_step(alpha=0.0):
            if alpha <= 0.98:
                self.root.attributes('-alpha', alpha)
                self.root.after(30, lambda: fade_step(alpha + 0.05))
        
        fade_step()
        
    def fade_out(self, callback=None):
        """Fade out the window before closing"""
        def fade_step(alpha=0.98):
            if alpha >= 0.0:
                self.root.attributes('-alpha', alpha)
                self.root.after(20, lambda: fade_step(alpha - 0.08))
            else:
                if callback:
                    callback()
                else:
                    self.root.destroy()
        
        fade_step()
        
    def on_closing(self):
        """Handle window closing with fade effect"""
        if not self.is_closing:
            self.is_closing = True
            self.fade_out()
        
    def setup_modern_ui(self):
        """Setup the modern UI with dark theme and contemporary styling"""
        # Create main container with padding
        self.main_container = ModernFrame(
            self.root, 
            bg_color=UI.BACKGROUND,
            relief='flat',
            bd=0
        )
        self.main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Configure grid weights for responsiveness
        self.main_container.columnconfigure(0, weight=1)
        self.main_container.rowconfigure(1, weight=1)  # Text area row (row 1, not 2)
        
        # Header section (row 0)
        self.create_header()
        
        # Text input section (row 1)
        self.create_text_section()
        
        # Settings section (row 2)
        self.create_settings_section()
        
        # Action buttons section (row 3)
        self.create_action_section()
        
        # Status section (row 4)
        self.create_status_section()
        
        # Footer/Instructions (row 5)
        self.create_footer()
    
    def toggle_settings(self):
        """Toggle the visibility of settings panel with smooth animation"""
        # Prevent multiple animations
        if hasattr(self, 'animating') and self.animating:
            return
            
        self.animating = True
        
        if self.settings_collapsed:
            # Expand settings
            self.settings_toggle_btn.configure(text="▼ Replay Settings")
            self.settings_content.pack(fill='x', padx=20, pady=(0, 20))
            self.settings_collapsed = False
            # Small delay for smooth feel
            self.root.after(150, lambda: setattr(self, 'animating', False))
        else:
            # Collapse settings  
            self.settings_toggle_btn.configure(text="▶ Replay Settings")
            # Small delay before hiding for smooth feel
            self.root.after(100, self.complete_collapse)
    
    def complete_collapse(self):
        """Complete the collapse animation"""
        self.settings_content.pack_forget()
        self.settings_collapsed = True
        self.animating = False
        
    def create_header(self):
        """Create modern header with app title and icon"""
        header_frame = ModernFrame(self.main_container, bg_color=UI.BACKGROUND)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.columnconfigure(1, weight=1)
        
        # App icon
        icon_frame = tk.Frame(header_frame, bg=UI.PRIMARY, width=50, height=50)
        icon_frame.grid(row=0, column=0, padx=(0, 15))
        icon_frame.pack_propagate(False)
        
        icon_label = tk.Label(
            icon_frame,
            text="⌨",
            font=UI.get_font(24),
            bg=UI.PRIMARY,
            fg=UI.TEXT_PRIMARY
        )
        icon_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title section
        title_frame = tk.Frame(header_frame, bg=UI.BACKGROUND)
        title_frame.grid(row=0, column=1, sticky="w")
        
        title_label = tk.Label(
            title_frame,
            text="Keystroke Replayer",
            font=UI.get_font(20, 'bold'),
            bg=UI.BACKGROUND,
            fg=UI.TEXT_PRIMARY
        )
        title_label.pack(anchor='w')
        
        subtitle_label = tk.Label(
            title_frame,
            text="Automated text input for restricted applications",
            font=UI.get_font(11),
            bg=UI.BACKGROUND,
            fg=UI.TEXT_SECONDARY
        )
        subtitle_label.pack(anchor='w')
        
    def create_text_section(self):
        """Create the text input area with modern styling"""
        text_frame = ModernFrame(self.main_container, bg_color=UI.BACKGROUND)
        text_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        text_frame.columnconfigure(0, weight=1)
        
        # Section label
        text_label = tk.Label(
            text_frame,
            text="Text to Replay",
            font=UI.get_font(14, 'bold'),
            bg=UI.BACKGROUND,
            fg=UI.TEXT_PRIMARY
        )
        text_label.grid(row=0, column=0, sticky="w", pady=(0, 8))
        
        # Custom text area with modern styling
        text_container = tk.Frame(text_frame, bg=UI.BORDER, relief='flat', bd=2)
        text_container.grid(row=1, column=0, sticky="ew")
        text_container.columnconfigure(0, weight=1)
        
        self.text_area = tk.Text(
            text_container,
            wrap=tk.WORD,
            font=UI.get_font(11),
            bg=UI.SURFACE,
            fg=UI.TEXT_PRIMARY,
            insertbackground=UI.PRIMARY,
            selectbackground=UI.PRIMARY_VARIANT,
            selectforeground=UI.TEXT_PRIMARY,
            relief='flat',
            bd=0,
            height=12
        )
        
        # Custom scrollbar
        scrollbar = tk.Scrollbar(
            text_container,
            orient=tk.VERTICAL,
            command=self.text_area.yview,
            bg=UI.SURFACE_VARIANT,
            troughcolor=UI.SURFACE,
            activebackground=UI.PRIMARY,
            relief='flat',
            bd=0,
            width=12
        )
        
        self.text_area.configure(yscrollcommand=scrollbar.set)
        
        self.text_area.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        scrollbar.grid(row=0, column=1, sticky="ns", pady=8, padx=(0, 8))
        
        text_container.rowconfigure(0, weight=1)
        
    def create_settings_section(self):
        """Create comprehensive settings section with realistic typing options"""
        # Main settings container
        settings_container = ModernFrame(self.main_container, bg_color=UI.SURFACE, relief='flat', bd=0)
        settings_container.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        settings_container.columnconfigure(0, weight=1)
        
        # Add subtle border effect
        border_frame = tk.Frame(settings_container, bg=UI.BORDER, height=1)
        border_frame.pack(fill='x')
        
        # Settings header with toggle button (always visible)
        header_frame = tk.Frame(settings_container, bg=UI.SURFACE)
        header_frame.pack(fill='x', padx=20, pady=15)
        
        # State for collapsible settings
        self.settings_collapsed = False
        self.animating = False  # Prevent multiple animations
        
        # Toggle button
        self.settings_toggle_btn = tk.Button(
            header_frame,
            text="▼ Replay Settings",
            font=UI.get_font(14, 'bold'),
            fg=UI.TEXT_PRIMARY,
            bg=UI.SURFACE,
            activebackground=UI.SURFACE_VARIANT,
            activeforeground=UI.TEXT_PRIMARY,
            relief='flat',
            bd=0,
            cursor='hand2',
            command=self.toggle_settings
        )
        self.settings_toggle_btn.pack(anchor='w')
        
        # Settings content (collapsible frame)
        self.settings_content = tk.Frame(settings_container, bg=UI.SURFACE)
        self.settings_content.pack(fill='x', padx=20, pady=(0, 20))
        
        # Basic settings row
        basic_frame = tk.Frame(self.settings_content, bg=UI.SURFACE)
        basic_frame.pack(fill='x', pady=(0, 15))
        basic_frame.columnconfigure(1, weight=1)
        basic_frame.columnconfigure(3, weight=1)
        
        # Delay setting
        delay_label = tk.Label(
            basic_frame,
            text="Delay (seconds):",
            font=UI.get_font(11),
            bg=UI.SURFACE,
            fg=UI.TEXT_PRIMARY
        )
        delay_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        self.delay_var = tk.StringVar(value="3")
        delay_spinbox = tk.Spinbox(
            basic_frame,
            from_=1, to=10, width=8,
            textvariable=self.delay_var,
            font=UI.get_font(11),
            bg=UI.SURFACE_VARIANT,
            fg=UI.TEXT_PRIMARY,
            buttonbackground=UI.PRIMARY,
            relief='flat',
            bd=1
        )
        delay_spinbox.grid(row=0, column=1, sticky="w", padx=(0, 30))
        
        # Speed setting
        speed_label = tk.Label(
            basic_frame,
            text="Speed (words/min):",
            font=UI.get_font(11),
            bg=UI.SURFACE,
            fg=UI.TEXT_PRIMARY
        )
        speed_label.grid(row=0, column=2, sticky="w", padx=(0, 10))
        
        self.speed_var = tk.StringVar(value="60")  # Default 60 WPM
        speed_spinbox = tk.Spinbox(
            basic_frame,
            from_=10, to=150, width=8,  # 10-150 WPM range
            textvariable=self.speed_var,
            font=UI.get_font(11),
            bg=UI.SURFACE_VARIANT,
            fg=UI.TEXT_PRIMARY,
            buttonbackground=UI.PRIMARY,
            relief='flat',
            bd=1
        )
        speed_spinbox.grid(row=0, column=3, sticky="w")
        
        # Realism section
        realism_frame = tk.LabelFrame(
            self.settings_content,
            text=" Realistic Typing Simulation ",
            font=UI.get_font(12, 'bold'),
            bg=UI.SURFACE,
            fg=UI.TEXT_PRIMARY,
            relief='flat',
            bd=1
        )
        realism_frame.pack(fill='x', pady=(10, 0))
        realism_frame.configure(highlightbackground=UI.BORDER)
        
        # Typo simulation row
        typo_frame = tk.Frame(realism_frame, bg=UI.SURFACE)
        typo_frame.pack(fill='x', padx=15, pady=10)
        typo_frame.columnconfigure(1, weight=1)
        
        # Random backspaces/typos
        self.typos_var = tk.BooleanVar(value=False)
        typos_check = tk.Checkbutton(
            typo_frame,
            text="Random Typos & Corrections",
            variable=self.typos_var,
            font=UI.get_font(11),
            bg=UI.SURFACE,
            fg=UI.TEXT_PRIMARY,
            selectcolor=UI.SURFACE_VARIANT,
            activebackground=UI.SURFACE,
            activeforeground=UI.TEXT_PRIMARY
        )
        typos_check.grid(row=0, column=0, sticky="w", padx=(0, 20))
        
        typo_chance_label = tk.Label(
            typo_frame,
            text="Typo Chance (%):",
            font=UI.get_font(10),
            bg=UI.SURFACE,
            fg=UI.TEXT_SECONDARY
        )
        typo_chance_label.grid(row=0, column=1, sticky="w", padx=(0, 5))
        
        self.typo_chance_var = tk.StringVar(value="5")
        typo_chance_spinbox = tk.Spinbox(
            typo_frame,
            from_=1, to=25, width=5,
            textvariable=self.typo_chance_var,
            font=UI.get_font(10),
            bg=UI.SURFACE_VARIANT,
            fg=UI.TEXT_PRIMARY,
            relief='flat',
            bd=1
        )
        typo_chance_spinbox.grid(row=0, column=2, sticky="w")
        
        # Pauses row
        pause_frame = tk.Frame(realism_frame, bg=UI.SURFACE)
        pause_frame.pack(fill='x', padx=15, pady=(0, 10))
        pause_frame.columnconfigure(1, weight=1)
        
        # Realistic pauses
        self.pauses_var = tk.BooleanVar(value=True)
        pauses_check = tk.Checkbutton(
            pause_frame,
            text="Realistic Pauses",
            variable=self.pauses_var,
            font=UI.get_font(11),
            bg=UI.SURFACE,
            fg=UI.TEXT_PRIMARY,
            selectcolor=UI.SURFACE_VARIANT,
            activebackground=UI.SURFACE,
            activeforeground=UI.TEXT_PRIMARY
        )
        pauses_check.grid(row=0, column=0, sticky="w", padx=(0, 20))
        
        pause_chance_label = tk.Label(
            pause_frame,
            text="Pause Chance (%):",
            font=UI.get_font(10),
            bg=UI.SURFACE,
            fg=UI.TEXT_SECONDARY
        )
        pause_chance_label.grid(row=0, column=1, sticky="w", padx=(0, 5))
        
        self.pause_chance_var = tk.StringVar(value="15")
        pause_chance_spinbox = tk.Spinbox(
            pause_frame,
            from_=5, to=50, width=5,
            textvariable=self.pause_chance_var,
            font=UI.get_font(10),
            bg=UI.SURFACE_VARIANT,
            fg=UI.TEXT_PRIMARY,
            relief='flat',
            bd=1
        )
        pause_chance_spinbox.grid(row=0, column=2, sticky="w", padx=(0, 15))
        
        pause_duration_label = tk.Label(
            pause_frame,
            text="Max Pause (sec):",
            font=UI.get_font(10),
            bg=UI.SURFACE,
            fg=UI.TEXT_SECONDARY
        )
        pause_duration_label.grid(row=0, column=3, sticky="w", padx=(0, 5))
        
        self.pause_duration_var = tk.StringVar(value="2.0")
        pause_duration_spinbox = tk.Spinbox(
            pause_frame,
            from_=0.5, to=5.0, increment=0.1, width=5,
            textvariable=self.pause_duration_var,
            font=UI.get_font(10),
            bg=UI.SURFACE_VARIANT,
            fg=UI.TEXT_PRIMARY,
            relief='flat',
            bd=1
        )
        pause_duration_spinbox.grid(row=0, column=4, sticky="w")
        
        # Speed variation row
        variation_frame = tk.Frame(realism_frame, bg=UI.SURFACE)
        variation_frame.pack(fill='x', padx=15, pady=(0, 10))
        variation_frame.columnconfigure(1, weight=1)
        
        # Speed variation
        self.variation_var = tk.BooleanVar(value=True)
        variation_check = tk.Checkbutton(
            variation_frame,
            text="Speed Variation",
            variable=self.variation_var,
            font=UI.get_font(11),
            bg=UI.SURFACE,
            fg=UI.TEXT_PRIMARY,
            selectcolor=UI.SURFACE_VARIANT,
            activebackground=UI.SURFACE,
            activeforeground=UI.TEXT_PRIMARY
        )
        variation_check.grid(row=0, column=0, sticky="w", padx=(0, 20))
        
        variation_label = tk.Label(
            variation_frame,
            text="Variation (±%):",
            font=UI.get_font(10),
            bg=UI.SURFACE,
            fg=UI.TEXT_SECONDARY
        )
        variation_label.grid(row=0, column=1, sticky="w", padx=(0, 5))
        
        self.variation_amount_var = tk.StringVar(value="30")
        variation_spinbox = tk.Spinbox(
            variation_frame,
            from_=10, to=100, width=5,
            textvariable=self.variation_amount_var,
            font=UI.get_font(10),
            bg=UI.SURFACE_VARIANT,
            fg=UI.TEXT_PRIMARY,
            relief='flat',
            bd=1
        )
        variation_spinbox.grid(row=0, column=2, sticky="w")
        
        # Word rewriting row
        rewrite_frame = tk.Frame(realism_frame, bg=UI.SURFACE)
        rewrite_frame.pack(fill='x', padx=15, pady=(0, 15))
        rewrite_frame.columnconfigure(1, weight=1)
        
        # Word rewriting
        self.rewrite_var = tk.BooleanVar(value=False)
        rewrite_check = tk.Checkbutton(
            rewrite_frame,
            text="Word Rewriting",
            variable=self.rewrite_var,
            font=UI.get_font(11),
            bg=UI.SURFACE,
            fg=UI.TEXT_PRIMARY,
            selectcolor=UI.SURFACE_VARIANT,
            activebackground=UI.SURFACE,
            activeforeground=UI.TEXT_PRIMARY
        )
        rewrite_check.grid(row=0, column=0, sticky="w", padx=(0, 20))
        
        rewrite_chance_label = tk.Label(
            rewrite_frame,
            text="Rewrite Chance (%):",
            font=UI.get_font(10),
            bg=UI.SURFACE,
            fg=UI.TEXT_SECONDARY
        )
        rewrite_chance_label.grid(row=0, column=1, sticky="w", padx=(0, 5))
        
        self.rewrite_chance_var = tk.StringVar(value="8")  # Higher default for more visible rewriting
        rewrite_chance_spinbox = tk.Spinbox(
            rewrite_frame,
            from_=1, to=15, width=5,
            textvariable=self.rewrite_chance_var,
            font=UI.get_font(10),
            bg=UI.SURFACE_VARIANT,
            fg=UI.TEXT_PRIMARY,
            relief='flat',
            bd=1
        )
        rewrite_chance_spinbox.grid(row=0, column=2, sticky="w")
        
    def create_action_section(self):
        """Create modern action buttons"""
        action_frame = ModernFrame(self.main_container, bg_color=UI.BACKGROUND)
        action_frame.grid(row=3, column=0, sticky="ew", pady=(0, 20))
        
        # Center the buttons
        button_container = tk.Frame(action_frame, bg=UI.BACKGROUND)
        button_container.pack(anchor='center')
        
        # Primary action button
        self.replay_button = Button(
            button_container,
            text="▶ Start Replay",
            button_type='primary',
            width=15,
            height=2,
            command=self.start_replay
        )
        self.replay_button.pack(side=tk.LEFT, padx=(0, 15))
        
        # Secondary action button
        clear_button = Button(
            button_container,
            text="🗑 Clear Text",
            button_type='secondary',
            width=15,
            height=2,
            command=self.clear_text
        )
        clear_button.pack(side=tk.LEFT)
        
    def create_status_section(self):
        """Create modern status display"""
        status_frame = ModernFrame(self.main_container, bg_color=UI.BACKGROUND)
        status_frame.grid(row=4, column=0, sticky="ew", pady=(0, 20))
        
        # Status indicator with icon
        self.status_container = tk.Frame(status_frame, bg=UI.BACKGROUND)
        self.status_container.pack(anchor='center')
        
        self.status_icon = tk.Label(
            self.status_container,
            text="●",
            font=UI.get_font(16),
            bg=UI.BACKGROUND,
            fg=UI.SUCCESS
        )
        self.status_icon.pack(side=tk.LEFT, padx=(0, 8))
        
        self.status_label = tk.Label(
            self.status_container,
            text="Ready to replay keystrokes",
            font=UI.get_font(12),
            bg=UI.BACKGROUND,
            fg=UI.TEXT_PRIMARY
        )
        self.status_label.pack(side=tk.LEFT)
        
    def create_footer(self):
        """Create modern footer with instructions"""
        footer_frame = ModernFrame(self.main_container, bg_color=UI.SURFACE_VARIANT)
        footer_frame.grid(row=5, column=0, sticky="ew")
        
        instructions_text = (
            "Guide: Paste text → Configure settings → Start → Switch to target app\n"
            "Safety: Move mouse to top-left to stop • F9 to pause/resume • Enable realism features"
        )
        
        instructions_label = tk.Label(
            footer_frame,
            text=instructions_text,
            font=UI.get_font(10),
            bg=UI.SURFACE_VARIANT,
            fg=UI.TEXT_SECONDARY,
            justify=tk.LEFT,
            wraplength=700
        )
        instructions_label.pack(padx=20, pady=15)
    def clear_text(self):
        """Clear the text area with visual feedback"""
        self.text_area.delete(1.0, tk.END)
        self.update_status("Text cleared", UI.ACCENT, "●")
        
    def update_status(self, message, color=None, icon="●"):
        """Update status with modern styling and icon"""
        if color is None:
            color = UI.TEXT_PRIMARY
            
        self.status_label.config(text=message, fg=color)
        self.status_icon.config(fg=color, text=icon)
        
    def start_replay(self):
        """Start the keystroke replay process with modern UI feedback"""
        text_to_replay = self.text_area.get(1.0, tk.END).strip()
        
        if not text_to_replay:
            messagebox.showwarning("No Text", "Please enter some text to replay!")
            return
            
        try:
            delay = int(self.delay_var.get())
            base_speed = int(self.speed_var.get())
        except ValueError:
            messagebox.showerror("Invalid Settings", "Please enter valid numbers for delay and speed!")
            return
            
        # Get realism settings
        settings = {
            'base_speed': base_speed,
            'use_typos': self.typos_var.get(),
            'typo_chance': int(self.typo_chance_var.get()),
            'use_pauses': self.pauses_var.get(),
            'pause_chance': int(self.pause_chance_var.get()),
            'pause_duration': float(self.pause_duration_var.get()),
            'use_variation': self.variation_var.get(),
            'variation_amount': int(self.variation_amount_var.get()),
            'use_rewrite': self.rewrite_var.get(),
            'rewrite_chance': int(self.rewrite_chance_var.get())
        }
        
        # Reset pause state
        self.is_paused = False
        self.resume_requested = False
        
        # Update UI for replay state
        self.replay_button.config(state='disabled', text="⏸ Replaying... (F9 to pause)")
        
        # Start replay in a separate thread
        self.current_replay_thread = threading.Thread(target=self.replay_keystrokes_realistic, args=(text_to_replay, delay, settings), daemon=True)
        self.current_replay_thread.start()
        
    def replay_keystrokes_realistic(self, text, delay, settings):
        """Replay keystrokes with realistic typing simulation"""
        try:
            # Countdown with modern styling
            for i in range(delay, 0, -1):
                self.update_status(f"Starting replay in {i} seconds...", UI.WARNING, "⏱")
                time.sleep(1)
            
            self.update_status("Replaying keystrokes with realistic simulation...", UI.ERROR, "▶")
            
            # Reset pyautogui pause
            pyautogui.PAUSE = 0.01
            
            # Realistic typing simulation
            self.simulate_realistic_typing(text, settings)
            
            self.update_status("Replay completed successfully!", UI.SUCCESS, "✓")
            
        except pyautogui.FailSafeException:
            self.update_status("Replay stopped by user (failsafe triggered)", UI.ERROR, "⏹")
        except Exception as e:
            self.update_status(f"Error during replay: {str(e)}", UI.ERROR, "⚠")
        finally:
            # Re-enable the replay button with modern styling
            self.root.after(0, lambda: [
                self.replay_button.config(state='normal', text="▶ Start Replay")
            ])
            
    def simulate_realistic_typing(self, text, settings):
        """Simulate realistic human typing with typos, pauses, speed variation, and word rewriting"""
        import random
        
        # Convert WPM to more accurate interval calculation
        wpm = settings['base_speed']
        # Direct calculation: WPM means words per minute, so chars per minute = WPM * average_word_length
        # But let's be more direct: if user wants 100 WPM, they should get fast typing
        # Average typing: 1 word = ~5 chars + 1 space = 6 keystrokes per word
        keystrokes_per_minute = wpm * 6
        keystrokes_per_second = keystrokes_per_minute / 60
        base_interval = 1.0 / keystrokes_per_second if keystrokes_per_second > 0 else 0.01
        
        # Ensure minimum speed for very high WPM
        base_interval = max(0.005, base_interval)  # Never faster than 5ms per keystroke
        
        words = text.split()
        
        for word_index, word in enumerate(words):
            # Check for pause request
            if self.is_paused:
                self.wait_for_resume()
            
            # Add space before word (except first word)
            if word_index > 0:
                # Only add pauses if enabled and at a reasonable frequency
                if settings['use_pauses'] and random.randint(1, 100) <= settings['pause_chance']:
                    pause_duration = random.uniform(0.1, settings['pause_duration'])
                    self.pausable_sleep(pause_duration)
                
                pyautogui.write(' ')
                # Don't apply variable delay to spaces for speed
                time.sleep(base_interval)
            
            # Calculate word-specific speed (longer words typed faster) but less extreme
            word_speed_factor = self.calculate_word_speed_factor(word)
            word_interval = base_interval * word_speed_factor
            
            # Word rewriting (remove excessive debugging)
            if (settings['use_rewrite'] and 
                len(word) > 2 and 
                random.randint(1, 100) <= settings['rewrite_chance']):
                self.rewrite_word(word, word_interval, settings)
            # Should we introduce a typo in this word?
            elif (settings['use_typos'] and 
                  len(word) > 2 and 
                  random.randint(1, 100) <= settings['typo_chance']):
                self.type_word_with_typo(word, word_interval, settings)
            else:
                self.type_word_normally(word, word_interval, settings)
                
    def calculate_word_speed_factor(self, word):
        """Calculate speed factor based on word length - longer words typed faster but less extreme"""
        word_length = len(word)
        if word_length <= 3:
            return 1.1  # Short words typed slightly slower (10% slower)
        elif word_length <= 5:
            return 1.0  # Medium words at base speed
        elif word_length <= 8:
            return 0.9  # Long words typed slightly faster (10% faster)
        else:
            return 0.8  # Very long words typed faster (20% faster)
                
    def wait_for_resume(self):
        """Wait until resume is requested"""
        while self.is_paused and not self.resume_requested:
            time.sleep(0.1)
        self.resume_requested = False
        
    def pausable_sleep(self, duration):
        """Sleep that can be interrupted by pause requests"""
        start_time = time.time()
        while time.time() - start_time < duration:
            if self.is_paused:
                self.wait_for_resume()
                start_time = time.time()  # Reset timer after resume
            time.sleep(0.05)
            
    def rewrite_word(self, word, base_interval, settings):
        """Type a word, then delete it and retype correctly (simulates changing mind)"""
        import random
        
        # Type a slightly wrong version of the word first
        wrong_word = self.create_wrong_word(word)
        
        # Type the wrong word
        for char in wrong_word:
            if self.is_paused:
                self.wait_for_resume()
            pyautogui.write(char)
            self.variable_delay(base_interval, settings)
        
        # Pause to "think" about it (shorter for fast typing)
        think_time = 0.3 if base_interval < 0.02 else random.uniform(0.5, 1.0)
        self.pausable_sleep(think_time)
        
        # Delete the wrong word
        for i in range(len(wrong_word)):
            if self.is_paused:
                self.wait_for_resume()
            # Use faster backspace method
            pyautogui.press('backspace')
            time.sleep(max(0.005, base_interval * 0.3))  # Much faster deletion
        
        # Type the correct word
        for char in word:
            if self.is_paused:
                self.wait_for_resume()
            pyautogui.write(char)
            self.variable_delay(base_interval, settings)
            
    def create_wrong_word(self, correct_word):
        """Create a plausible wrong version of a word"""
        import random
        
        # More obvious wrong variants for better visibility
        wrong_variants = [
            # Missing last letter(s)
            correct_word[:-1] if len(correct_word) > 2 else correct_word + 'x',
            correct_word[:-2] if len(correct_word) > 3 else correct_word[:-1],
            # Wrong common endings
            correct_word[:-3] + 'ing' if len(correct_word) > 4 else correct_word + 'ing',
            correct_word[:-2] + 'ed' if len(correct_word) > 3 else correct_word + 'ed',
            correct_word + 's' if not correct_word.endswith('s') else correct_word[:-1],
            # Doubled letter in middle
            correct_word[:len(correct_word)//2] + correct_word[len(correct_word)//2] + correct_word[len(correct_word)//2:] if len(correct_word) > 3 else correct_word + 'x',
            # Common misspellings
            correct_word.replace('ei', 'ie') if 'ei' in correct_word else correct_word.replace('ie', 'ei'),
            # Random extra letter
            correct_word + random.choice('aeiou'),
            # Wrong first letter
            random.choice('abcdefghijklmnopqrstuvwxyz') + correct_word[1:] if len(correct_word) > 2 else correct_word + 'x'
        ]
        
        # Filter out variants that are the same as original and ensure minimum difference
        valid_variants = [v for v in wrong_variants if v != correct_word and len(v) > 0 and abs(len(v) - len(correct_word)) <= 3]
        
        return random.choice(valid_variants) if valid_variants else correct_word + 'x'
        
    def type_word_with_typo(self, word, base_interval, settings):
        """Type a word with a realistic typo and correction"""
        import random
        import string
        
        # Choose a position for the typo (not first or last character)
        typo_position = random.randint(1, len(word) - 2)
        
        # Type characters up to typo position
        for i in range(typo_position):
            if self.is_paused:
                self.wait_for_resume()
            pyautogui.write(word[i])
            self.variable_delay(base_interval, settings)
        
        # Type a wrong character (adjacent key or random letter)
        wrong_char = self.get_wrong_character(word[typo_position])
        pyautogui.write(wrong_char)
        self.variable_delay(base_interval, settings)
        
        # Type a few more characters before realizing the mistake
        chars_after_typo = min(2, len(word) - typo_position - 1)
        for i in range(chars_after_typo):
            if self.is_paused:
                self.wait_for_resume()
            pyautogui.write(word[typo_position + 1 + i])
            self.variable_delay(base_interval, settings)
        
        # Pause briefly (realization of mistake)
        self.pausable_sleep(random.uniform(0.3, 0.8))
        
        # Backspace to fix the typo
        backspace_count = chars_after_typo + 1
        for _ in range(backspace_count):
            if self.is_paused:
                self.wait_for_resume()
            pyautogui.press('backspace')
            self.variable_delay(base_interval * 0.7, settings)  # Faster backspacing
        
        # Type the correct characters
        for i in range(typo_position, len(word)):
            if self.is_paused:
                self.wait_for_resume()
            pyautogui.write(word[i])
            self.variable_delay(base_interval, settings)
    
    def type_word_normally(self, word, base_interval, settings):
        """Type a word normally with natural speed variation"""
        # For very fast typing (high WPM), type the whole word at once
        if base_interval < 0.01 and not settings['use_variation']:
            pyautogui.write(word)
            time.sleep(base_interval * len(word))
        else:
            # Type character by character with delays
            for char in word:
                if self.is_paused:
                    self.wait_for_resume()
                pyautogui.write(char)
                self.variable_delay(base_interval, settings)
    
    def get_wrong_character(self, correct_char):
        """Get a realistic wrong character (adjacent key or similar)"""
        import random
        
        # Keyboard layout for adjacent key errors
        keyboard_adjacents = {
            'q': 'wa', 'w': 'qeas', 'e': 'wrds', 'r': 'etdf', 't': 'ryfg',
            'y': 'tugh', 'u': 'yihj', 'i': 'uojk', 'o': 'ipkl', 'p': 'ol',
            'a': 'qwsz', 's': 'awedxz', 'd': 'serfcx', 'f': 'drtgvc',
            'g': 'ftyhbv', 'h': 'gyujnb', 'j': 'hiumk', 'k': 'jiolm',
            'l': 'kop', 'z': 'asx', 'x': 'zsdc', 'c': 'xdfv', 'v': 'cfgb',
            'b': 'vghn', 'n': 'bhjm', 'm': 'njk'
        }
        
        correct_lower = correct_char.lower()
        
        if correct_lower in keyboard_adjacents:
            # 70% chance for adjacent key error
            if random.random() < 0.7:
                adjacent_chars = keyboard_adjacents[correct_lower]
                wrong_char = random.choice(adjacent_chars)
            else:
                # 30% chance for random letter
                wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
        else:
            # For non-letters, just pick a random letter
            wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
        
        # Maintain case
        if correct_char.isupper():
            wrong_char = wrong_char.upper()
        
        return wrong_char
    
    def variable_delay(self, base_interval, settings):
        """Apply variable delay based on settings"""
        import random
        
        if settings['use_variation'] and base_interval > 0.01:  # Only vary if not at minimum speed
            variation = settings['variation_amount'] / 100.0
            # Reduce variation impact at high speeds
            if base_interval < 0.02:  # For very fast typing
                variation *= 0.5  # Reduce variation by half
            # Generate variation factor between (1 - variation) and (1 + variation)
            factor = random.uniform(1 - variation, 1 + variation)
            actual_interval = base_interval * factor
        else:
            actual_interval = base_interval
        
        # Ensure minimum delay but allow very fast speeds
        actual_interval = max(0.005, actual_interval)  # 5ms minimum instead of 10ms
        time.sleep(actual_interval)

def main():
    """Main application entry point with splash screen"""
    try:
        # Check if pyautogui is available
        import pyautogui
    except ImportError:
        print("Error: pyautogui is not installed.")
        print("Please install it using: pip install pyautogui")
        return
    
    def launch_main_app():
        """Launch the main application after splash"""
        root = tk.Tk()
        app = KeystrokeReplayer(root)
        
        # Set initial status
        app.update_status("Ready to replay keystrokes", UI.SUCCESS, "●")
        
        root.mainloop()
    
    # Create root for splash
    splash_root = tk.Tk()
    splash_root.withdraw()  # Hide the root window
    
    # Show splash screen
    SplashScreen(launch_main_app)
    
    splash_root.mainloop()

if __name__ == "__main__":
    main()
