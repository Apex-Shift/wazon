# main.py
import sys
from ui.cli import run_cli
from ui.gui import run_gui

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        print("[*] Launching Wazon GUI Dashboard...")
        run_gui()
    else:
        print("[*] Launching Wazon CLI Mode...")
        run_cli()