from templateGame import Game
import asyncio

async def main():
    game = Game()
    game.load_data()
    while game.running:
        game.tick()
        await asyncio.sleep(0)

if __name__ == '__main__':
    asyncio.run(main())