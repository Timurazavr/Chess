import sys, pathlib, os, asyncio

if __name__ == '__main__':
    asyncio.gather(*[asyncio.create_task(os.system(i)) for i in ['python3 webApp/webApp_start.py', 'python3 bot/main.py']])
