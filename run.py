import asyncio
from bot import main  # Импортируем основную функцию из bot.py

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('The bot was stopped')
