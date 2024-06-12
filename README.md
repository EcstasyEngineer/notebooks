# notebooks

This repository serves as a collection of scratchpad Jupyter notebooks (`.ipynb` files) and scripts. It is intended for experimental and exploratory programming tasks.

## Setting up the Virtual Environment in VSCode

To set up the virtual environment in VSCode, follow these steps:

1. Open the command palette by pressing `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS).
2. Type "Python: Create Environment" and select it from the list.
3. Choose the option to create the environment using `venv` and `requirements.txt`.
4. Specify the path to the `requirements.txt` file in your project directory.
5. Press Enter to create the virtual environment.

Next, you need to add the SSH command and configure the remote origin URL. Here's an example:
```bash
git remote add origin git@github.com:[repo]
```

Additionally, don't forget to set your Git username and email. You can do this by running the following commands:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Make sure to replace "Your Name" and "your.email@example.com" with your actual name and email address.

Note: Insert the following line under the `[core]` section in your Git configuration file (`~/.gitconfig` or `.git/config`):
```bash
sshCommand = ssh -i ~/.ssh/[private_key]
```
