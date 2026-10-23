# Interactive Algorithm Visualizer

**DAA Mini-Project** — an interactive web application for learning sorting and searching algorithms.

## Features

- Visualize Bubble Sort, Selection Sort, Insertion Sort, Merge Sort, Quick Sort and Heap Sort.
- Visualize Linear Search and Binary Search.
- Generate random arrays or enter a custom array.
- Adjust animation speed.
- Display comparisons, swaps, writes, and algorithm time.
- Explain best-, average-, worst-case time complexity and space complexity.
- Verify sorting output.

## Technology Stack

- Python
- Streamlit
- Plotly

## Requirements

- Python 3.10 or newer recommended
- Internet connection for installing packages (not needed every time the app runs)

## Run locally

1. Download or clone this repository.
2. Open the project folder in a terminal.
3. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

4. Activate it on Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   On Windows Command Prompt:

   ```cmd
   .venv\Scripts\activate.bat
   ```

   On macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

5. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

6. Run the application:

   ```bash
   python -m streamlit run app.py
   ```

7. Open the local URL printed in the terminal, usually `http://localhost:8501`.

## DAA Concepts

This project demonstrates sorting and searching, divide and conquer, recursion, operation counting, and theoretical time/space complexity.

## Notes

- Binary Search automatically sorts the input before searching.
- Runtime measurements vary by hardware and execution environment.
- The app is intended as an educational demonstration; operation counts are useful alongside runtime measurements.

## Author

Student DAA Mini-Project
