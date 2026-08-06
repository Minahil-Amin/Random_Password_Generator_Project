# 🔐 Random Password Generator

A beautiful, modern, and responsive desktop application for generating secure, customizable random passwords. This project is built using Python and the modern **CustomTkinter** GUI library. 

It is designed to be highly beginner-friendly, adhering strictly to procedural/functional programming paradigms (no object-oriented classes or complex concepts), making it the perfect learning resource or portfolio project for students and Python beginners.

---

## 🎨 User Interface Preview

### Features and Layout
- **Modern Dark Theme**: Styled with neon purple and blue accent colors, featuring rounded corners and custom styling.
- **Double-Panel Design**: Includes a left sidebar for **Password History** and a right panel for password generation configurations.
- **Dynamic Password Strength Indicator**: Visual 3-segment color bar updating from **Weak (Red)** to **Medium (Orange)** to **Strong (Green)** based on password length.
- **Synchronized Slider & Input**: A length slider and text entry box that are fully synchronized with real-time input validation.
- **Show/Hide Toggle**: A toggle button to easily mask (`*`) or reveal the password.
- **Cybersecurity Quotes**: Dynamic cybersecurity quotes displayed at the bottom of the application.

---

## ⚙️ Technologies Used

- **Language**: Python 3.12+
- **GUI Engine**: CustomTkinter (built on top of Tkinter)
- **Standard Library Modules**: 
  - `random` (for password characters selection)
  - `string` (for pulling alphabet, numbers, and symbols pools)
  - `tkinter` (for MessageBox and PhotoImage support)

---

## 📚 Python Concepts Used

This application showcases standard beginner and intermediate concepts:
- **Variables & Data Types**: Storing lists, configurations, booleans, and string values.
- **Functions**: Structured code block organization for readability and reusability (e.g. generation, clipboard operations, UI synchronization).
- **Control Flow**:
  - `if-else` blocks for character selection configurations and strength check thresholds.
  - `try-except` blocks for handling missing file/icon assets without crashing the application.
- **Loops**: For-loops used to build the randomized password character by character.
- **Lists & Strings**: Slicing list history, appending, checking membership, and string concatenation.
- **GUI Event Binding**: Synchronizing slider movement (`command`) and text field key releases (`<KeyRelease>`).
- **Timers**: Utilizing `after()` for non-blocking visual feedback (e.g. "✓ Password Copied!" auto-fades).

---

## 📂 Folder Structure

```text
RandomPasswordGenerator/
│
├── main.py               # Main application code with GUI layout and logic
├── requirements.txt      # Project library dependencies list
├── README.md             # Project documentation and guide
├── assets/
│     └── icon.png        # Padlock logo/app icon asset
└── screenshots/          # folder containing app screenshots
```

---

## 🚀 Installation & Running Guide

### 1. Clone or Download the Repository
Make sure you have downloaded all the files into a single directory named `RandomPasswordGenerator`.

### 2. Open the Project in VS Code
Open your system's PowerShell and navigate to the project folder, then open it in VS Code:
```powershell
cd "d:\1st INTERN\DECODE Project 3.1 Random Password Generator"
code .
```

### 3. Install Dependencies in VS Code
Open the integrated terminal in VS Code (using `Ctrl + ` ` ` or **Terminal > New Terminal** from the top menu) and run:
```powershell
pip install -r requirements.txt
```

### 4. Run the Application
From the same terminal, execute:
```powershell
python main.py
```

---

## 🛠️ How it Works

1. **Length Input**: Enter a number between `4` and `50` or move the slider.
2. **Options**: Check or uncheck which characters to include. The generator prevents generating a password if zero checkboxes are checked!
3. **Generate**: Click **⚡ Generate Password**. The app loops `length` times, picking a random character from your chosen settings pool using `random.choice()`.
4. **Copy**: Click **📋 Copy** to add the password to your clipboard.
5. **Clear**: Click **🧹 Clear** to reset inputs, checkboxes, and output back to defaults.
6. **Recent History**: The left sidebar shows up to 5 recently generated passwords. Click any of them to instantly copy it to your clipboard!

---

## 🔮 Future Improvements

If you wish to expand this project further, here are some recommended features to implement:
- **Export to CSV**: Save generated passwords directly to a local text/CSV file.
- **Exclude Similar Characters**: Add a setting to skip confusing letters like `o`, `O`, `0`, `l`, `I`, `1`.
- **Advanced Strength Meter**: Incorporate character entropy calculations to rate passwords based on complexity rather than just length.
- **Theme Switcher**: Allow users to switch between Light Mode and Dark Mode dynamically.

---

## 👤 Author
Developed with ❤️ for educational purposes. Feel free to use and modify this project for your portfolio!
