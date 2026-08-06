# main.py
#
# Random Password Generator with Modern Python GUI
# Built using CustomTkinter and beginner-friendly Python concepts.
# No OOP (Classes), advanced concepts, or complex libraries are used.

import random
import string
import customtkinter
from tkinter import messagebox, PhotoImage

# ---------------------------------------------------------
# 1. System configurations
# ---------------------------------------------------------
# Set the dark theme and modern purple/blue color scheme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# ---------------------------------------------------------
# 2. Main Window Setup
# ---------------------------------------------------------
app = customtkinter.CTk()
app.title("🔐 Random Password Generator")
app.geometry("650x520")
app.resizable(False, False)

# Center the window on the screen
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x_coordinate = (screen_width // 2) - (650 // 2)
y_coordinate = (screen_height // 2) - (520 // 2)
app.geometry(f"650x520+{x_coordinate}+{y_coordinate}")

# Load application icon (fails silently if icon not found/supported)
try:
    icon_image = PhotoImage(file="assets/icon.png")
    app.iconphoto(False, icon_image)
except Exception:
    pass

# ---------------------------------------------------------
# 3. Global Variables / Application State
# ---------------------------------------------------------
history_list = []      # Stores the last 5 generated passwords
password_hidden = False # Tracks whether the password is obfuscated with asterisks

# ---------------------------------------------------------
# 4. Helper & Callback Functions
# ---------------------------------------------------------

def generate_password():
    """Generates a random password based on the user's settings."""
    # Read the password length from the entry box
    length_str = length_entry.get().strip()
    
    # Validation 1: Check if the length field is empty
    if not length_str:
        messagebox.showerror("Validation Error", "Password length cannot be empty!")
        return
        
    # Validation 2: Check if the input is a valid positive number
    if not length_str.isdigit():
        messagebox.showerror("Validation Error", "Password length must be a valid positive number!")
        return
        
    # Convert validated string to integer
    length = int(length_str)
    
    # Validation 3: Check if the length is too small
    if length < 4:
        messagebox.showerror("Validation Error", "Password length must be at least 4 characters!")
        return
        
    # Validation 4: Check if the length is too large
    if length > 50:
        messagebox.showerror("Validation Error", "Password length cannot exceed 50 characters!")
        return
        
    # Read checkbox values
    upper = upper_var.get()
    lower = lower_var.get()
    digits = digits_var.get()
    symbols = symbols_var.get()
    
    # Validation 5: Ensure at least one option is selected
    if not (upper or lower or digits or symbols):
        messagebox.showerror("Validation Error", "At least one character option must be selected!")
        return
        
    # Build the pool of characters to select from
    characters = ""
    if upper:
        characters += string.ascii_uppercase
    if lower:
        characters += string.ascii_lowercase
    if digits:
        characters += string.digits
    if symbols:
        characters += string.punctuation
        
    # Generate password using a simple loop
    password = ""
    for i in range(length):
        password += random.choice(characters)
        
    # Display the generated password in the entry widget
    # We must temporarily set it to normal state to modify it, then make it readonly again
    password_entry.configure(state="normal")
    password_entry.delete(0, "end")
    password_entry.insert(0, password)
    password_entry.configure(state="readonly")
    
    # Update the password strength visual bars and text label
    update_strength_indicator(password)
    
    # Reset visibility toggle button if password was hidden
    global password_hidden
    if password_hidden:
        password_entry.configure(show="")
        toggle_visibility_btn.configure(text="👁 Hide")
        password_hidden = False
        
    # Add the newly generated password to history
    add_to_history(password)
    
    # Clear any previous copy messages
    toast_label.configure(text="")


def copy_password():
    """Copies the currently generated password to the clipboard."""
    password = password_entry.get()
    
    # Check if a password exists to copy
    if not password:
        messagebox.showwarning("Copy Warning", "No password generated yet!")
        return
        
    # Clear system clipboard and copy the password
    app.clipboard_clear()
    app.clipboard_append(password)
    
    # Update UI to show feedback
    toast_label.configure(text="✓ Password Copied!", text_color="#22c55e")
    app.after(2000, clear_toast)


def clear_toast():
    """Clears the clipboard feedback message after a delay."""
    try:
        toast_label.configure(text="")
    except Exception:
        pass


def clear_fields():
    """Resets all generator options and inputs to their default states."""
    # Reset length fields to 12
    length_entry.delete(0, "end")
    length_entry.insert(0, "12")
    length_slider.set(12)
    
    # Reset checkboxes to default checked state
    upper_var.set(True)
    lower_var.set(True)
    digits_var.set(True)
    symbols_var.set(True)
    
    # Clear generated password
    password_entry.configure(state="normal")
    password_entry.delete(0, "end")
    password_entry.configure(state="readonly")
    
    # Reset visibility toggle
    password_entry.configure(show="")
    toggle_visibility_btn.configure(text="👁 Hide")
    global password_hidden
    password_hidden = False
    
    # Reset strength indicator colors and text
    strength_label.configure(text="Strength: -", text_color="#9ca3af")
    bar1.configure(fg_color="#2e2e3e")
    bar2.configure(fg_color="#2e2e3e")
    bar3.configure(fg_color="#2e2e3e")
    
    # Clear copying notifications
    toast_label.configure(text="")


def update_strength_indicator(password):
    """Calculates password strength based on length and updates the UI."""
    length = len(password)
    
    # Weak: 4 to 7 characters
    if length < 8:
        strength_label.configure(text="Strength: Weak", text_color="#ef4444")
        bar1.configure(fg_color="#ef4444")
        bar2.configure(fg_color="#2e2e3e")
        bar3.configure(fg_color="#2e2e3e")
        
    # Medium: 8 to 11 characters
    elif length < 12:
        strength_label.configure(text="Strength: Medium", text_color="#f97316")
        bar1.configure(fg_color="#f97316")
        bar2.configure(fg_color="#f97316")
        bar3.configure(fg_color="#2e2e3e")
        
    # Strong: 12+ characters
    else:
        strength_label.configure(text="Strength: Strong", text_color="#22c55e")
        bar1.configure(fg_color="#22c55e")
        bar2.configure(fg_color="#22c55e")
        bar3.configure(fg_color="#22c55e")


def add_to_history(password):
    """Adds a generated password to the history, showing the last 5."""
    global history_list
    # Remove if it already exists to avoid duplicates, moving it to the top
    if password in history_list:
        history_list.remove(password)
        
    # Insert at the beginning of the list
    history_list.insert(0, password)
    
    # Limit list to 5 passwords
    if len(history_list) > 5:
        history_list = history_list[:5]
        
    # Refresh the sidebar UI
    update_history_ui()


def update_history_ui():
    """Destroys old history buttons and re-draws the current history list."""
    # Destroy all current widgets inside the history container
    for widget in history_container.winfo_children():
        widget.destroy()
        
    # If history is empty, show default placeholder text
    if not history_list:
        no_history_label = customtkinter.CTkLabel(
            history_container,
            text="No history yet",
            font=("Inter", 12, "italic"),
            text_color="#6b7280"
        )
        no_history_label.pack(pady=15)
        return
        
    # Generate widgets for each password in the list
    for pwd in history_list:
        # Create a container frame for styling
        row_frame = customtkinter.CTkFrame(history_container, fg_color="transparent")
        row_frame.pack(fill="x", pady=4, padx=5)
        
        # Obfuscate long passwords in sidebar for clean visual look
        display_text = pwd
        if len(display_text) > 18:
            display_text = display_text[:15] + "..."
            
        # Create a button for the password. Clicking copies it.
        pwd_btn = customtkinter.CTkButton(
            row_frame,
            text=display_text,
            font=("Consolas", 12),
            text_color="#a5b4fc",
            fg_color="#1e1e2e",
            hover_color="#312e81",
            anchor="w",
            height=32,
            corner_radius=6,
            command=make_copy_callback(pwd)
        )
        pwd_btn.pack(fill="x", expand=True)


def make_copy_callback(password_to_copy):
    """Creates a callback function for history buttons to prevent variable scoping bugs."""
    def callback():
        app.clipboard_clear()
        app.clipboard_append(password_to_copy)
        toast_label.configure(text="✓ Copied from history!", text_color="#22c55e")
        app.after(2000, clear_toast)
    return callback


def clear_history():
    """Wipes the history list and refreshes the UI."""
    global history_list
    history_list.clear()
    update_history_ui()


def toggle_password_visibility():
    """Toggles showing and hiding the password in the output field."""
    global password_hidden
    if password_hidden:
        password_entry.configure(show="")
        toggle_visibility_btn.configure(text="👁 Hide")
        password_hidden = False
    else:
        password_entry.configure(show="*")
        toggle_visibility_btn.configure(text="👁 Show")
        password_hidden = True


def on_slider_move(value):
    """Updates the length textbox when the slider is moved."""
    length_val = int(value)
    length_entry.delete(0, "end")
    length_entry.insert(0, str(length_val))


def on_entry_change(event):
    """Updates the slider position when a user manually inputs a valid number."""
    val_str = length_entry.get().strip()
    if val_str.isdigit():
        val = int(val_str)
        if 4 <= val <= 50:
            length_slider.set(val)


# ---------------------------------------------------------
# 5. UI Layout & Design (Sidebar and Main Area)
# ---------------------------------------------------------

# Sidebar Frame (History Panel)
sidebar_frame = customtkinter.CTkFrame(app, width=180, corner_radius=0, fg_color="#111118")
sidebar_frame.grid(row=0, column=0, sticky="nsw")
sidebar_frame.grid_propagate(False) # Keep sidebar width locked at 180px

# Main Frame (Generator Controls Panel)
main_frame = customtkinter.CTkFrame(app, corner_radius=0, fg_color="#0f0f12")
main_frame.grid(row=0, column=1, sticky="nsew")

# Configure main window grid grid columns to expand the right panel
app.grid_columnconfigure(0, weight=0)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

# --- Sidebar Widgets ---
sidebar_title = customtkinter.CTkLabel(
    sidebar_frame, 
    text="🔑 Recent", 
    font=("Outfit", 16, "bold"), 
    text_color="#ffffff"
)
sidebar_title.pack(pady=(25, 2), padx=15, anchor="w")

sidebar_subtitle = customtkinter.CTkLabel(
    sidebar_frame, 
    text="Click a password to copy", 
    font=("Inter", 10), 
    text_color="#6b7280"
)
sidebar_subtitle.pack(pady=(0, 20), padx=15, anchor="w")

# Scrollable / dynamic history container
history_container = customtkinter.CTkFrame(sidebar_frame, fg_color="transparent")
history_container.pack(fill="both", expand=True, padx=10) # pack layout inside sidebar
update_history_ui()

# Clear history button at the bottom
clear_history_btn = customtkinter.CTkButton(
    sidebar_frame,
    text="Clear History",
    font=("Inter", 11),
    fg_color="transparent",
    text_color="#f87171",
    hover_color="#2d1515",
    height=25,
    command=clear_history
)
clear_history_btn.pack(side="bottom", pady=20, fill="x", padx=15)


# --- Main Frame Widgets ---
# Application Title & Subheading
title_label = customtkinter.CTkLabel(
    main_frame, 
    text="🔐 Random Password Generator", 
    font=("Outfit", 22, "bold"), 
    text_color="#ffffff"
)
title_label.pack(pady=(20, 2), padx=20)

subtitle_label = customtkinter.CTkLabel(
    main_frame, 
    text="Generate Strong & Secure Passwords", 
    font=("Inter", 12), 
    text_color="#9ca3af"
)
subtitle_label.pack(pady=(0, 10), padx=20)

# Card Frame (Contains length, choices, and strength controls)
card_frame = customtkinter.CTkFrame(
    main_frame, 
    corner_radius=12, 
    fg_color="#181824", 
    border_width=1, 
    border_color="#2d2d44"
)
card_frame.pack(pady=10, padx=25, fill="both", expand=True)

# Grid layout configurations for card controls alignment
card_frame.grid_columnconfigure(0, weight=1)
card_frame.grid_columnconfigure(1, weight=1)

# Row 1: Password Length Headers
length_title_label = customtkinter.CTkLabel(
    card_frame, 
    text="Password Length", 
    font=("Inter", 12, "bold"), 
    text_color="#ffffff"
)
length_title_label.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 5))

# Row 1 Slider + Entry Container
len_control_frame = customtkinter.CTkFrame(card_frame, fg_color="transparent")
len_control_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=15, pady=(0, 10))

length_slider = customtkinter.CTkSlider(
    len_control_frame, 
    from_=4, 
    to=50, 
    number_of_steps=46, 
    command=on_slider_move, 
    progress_color="#6366f1", 
    button_color="#818cf8"
)
length_slider.pack(side="left", fill="x", expand=True, padx=(0, 10))
length_slider.set(12)

length_entry = customtkinter.CTkEntry(
    len_control_frame, 
    width=45, 
    height=28, 
    font=("Consolas", 12, "bold"), 
    justify="center",
    border_color="#2d2d44"
)
length_entry.pack(side="right")
length_entry.insert(0, "12")
length_entry.bind("<KeyRelease>", on_entry_change)

# Row 2: Character Settings Header
options_title_label = customtkinter.CTkLabel(
    card_frame, 
    text="Character Settings", 
    font=("Inter", 12, "bold"), 
    text_color="#ffffff"
)
options_title_label.grid(row=2, column=0, sticky="w", padx=15, pady=(10, 5))

# Row 3 & 4 Checkbox Variables and Elements
upper_var = customtkinter.BooleanVar(value=True)
lower_var = customtkinter.BooleanVar(value=True)
digits_var = customtkinter.BooleanVar(value=True)
symbols_var = customtkinter.BooleanVar(value=True)

cb_upper = customtkinter.CTkCheckBox(
    card_frame, 
    text="Include Uppercase Letters", 
    variable=upper_var, 
    font=("Inter", 11), 
    fg_color="#6366f1", 
    hover_color="#4f46e5"
)
cb_upper.grid(row=3, column=0, sticky="w", padx=20, pady=5)

cb_lower = customtkinter.CTkCheckBox(
    card_frame, 
    text="Include Lowercase Letters", 
    variable=lower_var, 
    font=("Inter", 11), 
    fg_color="#6366f1", 
    hover_color="#4f46e5"
)
cb_lower.grid(row=3, column=1, sticky="w", padx=20, pady=5)

cb_digits = customtkinter.CTkCheckBox(
    card_frame, 
    text="Include Numbers (0-9)", 
    variable=digits_var, 
    font=("Inter", 11), 
    fg_color="#6366f1", 
    hover_color="#4f46e5"
)
cb_digits.grid(row=4, column=0, sticky="w", padx=20, pady=5)

cb_symbols = customtkinter.CTkCheckBox(
    card_frame, 
    text="Include Symbols (!@#$)", 
    variable=symbols_var, 
    font=("Inter", 11), 
    fg_color="#6366f1", 
    hover_color="#4f46e5"
)
cb_symbols.grid(row=4, column=1, sticky="w", padx=20, pady=5)

# Row 5: Password Strength Indicator
strength_frame = customtkinter.CTkFrame(card_frame, fg_color="transparent")
strength_frame.grid(row=5, column=0, columnspan=2, sticky="ew", padx=15, pady=(15, 10))

strength_label = customtkinter.CTkLabel(
    strength_frame, 
    text="Strength: -", 
    font=("Inter", 12, "bold"), 
    text_color="#9ca3af"
)
strength_label.pack(side="left", padx=(5, 15))

# Strength indicator visual blocks
bars_frame = customtkinter.CTkFrame(strength_frame, fg_color="transparent")
bars_frame.pack(side="left")

bar1 = customtkinter.CTkFrame(bars_frame, width=35, height=8, corner_radius=4, fg_color="#2e2e3e")
bar1.pack(side="left", padx=2)
bar2 = customtkinter.CTkFrame(bars_frame, width=35, height=8, corner_radius=4, fg_color="#2e2e3e")
bar2.pack(side="left", padx=2)
bar3 = customtkinter.CTkFrame(bars_frame, width=35, height=8, corner_radius=4, fg_color="#2e2e3e")
bar3.pack(side="left", padx=2)

# Row 6: Password Output Title
output_title_label = customtkinter.CTkLabel(
    card_frame, 
    text="Generated Password Output", 
    font=("Inter", 12, "bold"), 
    text_color="#ffffff"
)
output_title_label.grid(row=6, column=0, sticky="w", padx=15, pady=(10, 2))

# Row 7 Output Display & Show/Hide Button
output_container = customtkinter.CTkFrame(card_frame, fg_color="transparent")
output_container.grid(row=7, column=0, columnspan=2, sticky="ew", padx=15, pady=(0, 15))

password_entry = customtkinter.CTkEntry(
    output_container,
    font=("Consolas", 15, "bold"),
    text_color="#bb9af7",
    fg_color="#111118",
    border_color="#2d2d44",
    height=38,
    state="readonly"
)
password_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

toggle_visibility_btn = customtkinter.CTkButton(
    output_container,
    text="👁 Hide",
    width=75,
    height=38,
    font=("Inter", 11),
    fg_color="#2e2e3e",
    hover_color="#3e3e5e",
    command=toggle_password_visibility
)
toggle_visibility_btn.pack(side="right")


# --- Main Action Buttons ---
actions_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
actions_frame.pack(pady=5, padx=25, fill="x")

generate_btn = customtkinter.CTkButton(
    actions_frame,
    text="⚡ Generate Password",
    font=("Inter", 13, "bold"),
    fg_color="#7c3aed",
    hover_color="#6d28d9",
    height=40,
    command=generate_password
)
generate_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))

copy_btn = customtkinter.CTkButton(
    actions_frame,
    text="📋 Copy",
    font=("Inter", 13, "bold"),
    fg_color="#0284c7",
    hover_color="#0369a1",
    height=40,
    width=100,
    command=copy_password
)
copy_btn.pack(side="left", padx=(0, 10))

clear_btn = customtkinter.CTkButton(
    actions_frame,
    text="🧹 Clear",
    font=("Inter", 13, "bold"),
    fg_color="#374151",
    hover_color="#4b5563",
    height=40,
    width=90,
    command=clear_fields
)
clear_btn.pack(side="right")

# Copy confirmation popup label
toast_label = customtkinter.CTkLabel(
    main_frame, 
    text="", 
    font=("Inter", 11, "bold"), 
    text_color="#22c55e"
)
toast_label.pack(pady=(2, 5))

# Footer containing random security quotes
quote_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
quote_frame.pack(side="bottom", fill="x", pady=(5, 15), padx=20)

quotes = [
    "A secure password is your first line of digital defense.",
    "Passwords are like toothbrushes: choose a good one, don't share it, and change it regularly.",
    "Double your safety with strong passwords and multi-factor authentication.",
    "Complexity beats length, but length and complexity together are unbeatable.",
    "Make your passwords hard to guess but easy for you to remember."
]
random_quote = random.choice(quotes)

quote_label = customtkinter.CTkLabel(
    quote_frame,
    text=f'"{random_quote}"',
    font=("Inter", 10, "italic"),
    text_color="#6b7280",
    wraplength=420,
    justify="center"
)
quote_label.pack()

# Start the main loop to run the application
if __name__ == "__main__":
    app.mainloop()
