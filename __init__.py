import sys, pathlib, os, asyncio

if __name__ == "__main__":
    if sys.platform.startswith("win"):
        os.system("python bot_start.py | python webApp_start.py")
    else:
        os.system("python3 bot_start.py | python3 webApp_start.py")
