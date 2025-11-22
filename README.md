# MLBB Patcher Tool

This project contains a Python script to generate a patch file for modifying Mobile Legends: Bang Bang (MLBB) assets. The script allows users to select various modifications, which are then compiled into a `patch.dat` file.

## Features

-   **User-Friendly Interface:** A simple command-line menu to select desired hacks.
-   **Patch Generation:** Creates a `patch.dat` file based on user selections.
-   **Supported Modifications:**
    -   Unlock All Skins
    -   Drone View (High, Medium, Low)
    -   Map Hack (Show enemies on map)

## How It Works

The `patcher.py` script prompts the user for their MLBB User ID and Server ID. It then presents a menu of available cheats. Based on the user's selection, it constructs a binary patch file (`patch.dat`).

This `patch.dat` file is designed to be placed in the game's data directory (`Android/data/com.mobile.legends/files/dragon2017/assets/`). When the game launches, it reads this patch file, and the modifications are loaded into the game.

## Usage Guide

### Part 1: Generating the Patch File with Termux

1.  **Install Prerequisites:**
    Open Termux and install Python and Git:
    ```bash
    pkg update && pkg upgrade -y
    pkg install python git -y
    ```

2.  **Clone the Repository:**
    ```bash
    git clone https://github.com/johnderrickos12-pixel/mlbb-patcher.git
    cd mlbb-patcher
    ```

3.  **Run the Patcher:**
    ```bash
    python patcher.py
    ```
    Follow the on-screen prompts to enter your account details and select the desired cheats. A `patch.dat` file will be generated in the current directory.

### Part 2: Injecting the Patch with ZArchiver

1.  **Install ZArchiver** from the Google Play Store and grant file access permissions.

2.  **Copy the Patch File:**
    -   In ZArchiver, navigate to the Termux folder where you ran the script (e.g., `/data/data/com.termux/files/home/mlbb-patcher/`).
    -   Long-press on `patch.dat` and select "Copy".

3.  **Paste into MLBB Directory:**
    -   Navigate to `Android/data/com.mobile.legends/files/dragon2017/assets/`.
    -   Paste the `patch.dat` file, choosing to "REPLACE" the existing file if prompted.

4.  **Clear Cache & Launch:**
    -   Go to your device's Settings -> Apps -> Mobile Legends.
    -   "Force Stop" the app, then go to "Storage" and "Clear cache".
    -   Launch the game to see the changes.

**Disclaimer:** Modifying game files is against the terms of service of most games, including MLBB. Use this tool at your own risk.
