import sys, pathlib, os, asyncio
#
#
# async def start_webApp():
#     print('Web App Started')
#     os.system('python3 webApp/webApp_start.py')
#     print('Web App Stopped')
#
#
# async def start_tg_bot():
#     print('Tg Bot Started')
#     os.system('python3 bot/main.py')
#     print('Tg Bot Stopped')
#
#
# async def main():
#     await asyncio.gather(*[asyncio.create_task(i) for i in [start_webApp(), start_tg_bot()]])
#
#
# if __name__ == '__main__':
#     print(os.name)
#     if os.name == 'nt':
#         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     asyncio.run(main())
if __name__ == '__main__':
    os.system('python3 bot/main.py | python3 webApp/webApp_start.py')