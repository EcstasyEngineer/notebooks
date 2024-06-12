# notebooks

This repository serves as a collection of scratchpad Jupyter notebooks (`.ipynb` files) and scripts. It is intended for experimental and exploratory programming tasks.

## Setting up the Virtual Environment in VSCode

To create a virtual environment and install the necessary dependencies from `requirements.txt`, follow these steps in Visual Studio Code:

1. Open the terminal in VSCode (`Ctrl+``).
2. Ensure you are in the root directory of the project.
3. Create a virtual environment:
    - On Windows, run: `python -m venv .venv`
    - On macOS/Linux, run: `python3 -m venv .venv`
4. Activate the virtual environment:
    - On Windows, run: `.venv\Scripts\activate`
    - On macOS/Linux, run: `source .venv/bin/activate`
5. Install the requirements: `pip install -r requirements.txt`

After following these steps, your virtual environment should be set up with all the dependencies listed in `requirements.txt`, and you can start using or developing the notebooks and scripts in this repository.