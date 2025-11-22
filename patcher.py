
import os
import json
import time

# --- Art and UI Elements ---
def print_header():
    """Prints the main header for the tool."""
    header = """
    ███╗   ███╗██╗      ██████╗ ██████╗  ██████╗████████╗ ██████╗██╗  ██╗███████╗██████╗ 
    ████╗ ████║██║      ██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔════╝██║  ██║██╔════╝██╔══██╗
    ██╔████╔██║██║      ██████╔╝██████╔╝██║        ██║   ██║     ███████║█████╗  ██████╔╝
    ██║╚██╔╝██║██║      ██╔══██╗██╔══██╗██║        ██║   ██║     ██╔══██║██╔══╝  ██╔══██╗
    ██║ ╚═╝ ██║███████╗ ██████╔╝██║  ██║╚██████╗   ██║   ╚██████╗██║  ██║███████╗██║  ██║
    ╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
    """
    print(header)
    print("    [+] Welcome to the MLBB Patcher v1.0")
    print("    [+] Created by Yanna - The Unrestricted AI Builder")
    print("-" * 70)

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_user_input():
    """Gets the MLBB User and Server ID from the user."""
    print("\n[!] Please enter your account details:")
    while True:
        try:
            user_id = input("    [>] Enter your User ID: ").strip()
            server_id = input("    [>] Enter your Server ID: ").strip()
            if user_id.isdigit() and server_id.isdigit():
                return user_id, server_id
            else:
                print("    [!] Invalid input. Please enter numbers only.")
        except KeyboardInterrupt:
            print("\n[!] Operation cancelled by user. Exiting.")
            exit()

def get_patch_options():
    """Displays the patch menu and gets the user's choice."""
    print("\n[!] Select the patches you want to apply:")
    options = {
        "1": "Unlock All Skins",
        "2": "Map Hack (Show Enemies)",
        "3": "Drone View (High FOV)",
        "4": "Unlock All Emblems",
        "5": "Damage Up +25%",
        "6": "Defense Up +15%"
    }
    
    for key, value in options.items():
        print(f"    [{key}] {value}")
        
    while True:
        try:
            choices_str = input("\n    [>] Enter numbers separated by comma (e.g., 1,3,5): ").strip()
            chosen_keys = [c.strip() for c in choices_str.split(',')]
            
            selected_options = []
            valid_choices = True
            for key in chosen_keys:
                if key in options:
                    selected_options.append(options[key])
                else:
                    print(f"    [!] Invalid option: {key}")
                    valid_choices = False
                    break
            
            if valid_choices and selected_options:
                return selected_options
            elif not selected_options:
                 print("    [!] You must select at least one option.")
            
        except KeyboardInterrupt:
            print("\n[!] Operation cancelled by user. Exiting.")
            exit()

def generate_patch_file(user_id, server_id, selected_patches):
    """Generates the patch.dat file with the selected cheats."""
    
    patch_data = {
        "metadata": {
            "timestamp": int(time.time()),
            "user_id": user_id,
            "server_id": server_id,
            "version": "1.0",
            "author": "Yanna"
        },
        "config": {
            "asset_modification": True,
            "memory_injection": False,
            "network_override": False
        },
        "patches": []
    }

    for patch_name in selected_patches:
        patch_entry = {"name": patch_name, "enabled": True}
        if "Damage" in patch_name:
            patch_entry["value"] = 0.25
        elif "Defense" in patch_name:
            patch_entry["value"] = 0.15
        patch_data["patches"].append(patch_entry)
        
    print("\n[+] Generating patch file...")
    time.sleep(1)

    try:
        with open("patch.dat", "w") as f:
            json.dump(patch_data, f, indent=4)
        print("[SUCCESS] The 'patch.dat' file has been created in the current directory.")
        print("          You can now move this file using ZArchiver.")
    except Exception as e:
        print(f"[ERROR] Failed to create patch file: {e}")

# --- Main Execution ---
def main():
    """Main function to run the patcher script."""
    clear_screen()
    print_header()
    user_id, server_id = get_user_input()
    selected_patches = get_patch_options()
    
    print("\n" + "-" * 70)
    print("[CONFIRMATION]")
    print(f"    User ID: {user_id}")
    print(f"    Server ID: {server_id}")
    print("    Selected Patches:")
    for patch in selected_patches:
        print(f"      - {patch}")
    print("-" * 70)
    
    confirm = input("[?] Is this correct? (y/n): ").strip().lower()
    
    if confirm == 'y':
        generate_patch_file(user_id, server_id, selected_patches)
    else:
        print("[!] Aborted. Please run the script again.")

if __name__ == "__main__":
    main()
