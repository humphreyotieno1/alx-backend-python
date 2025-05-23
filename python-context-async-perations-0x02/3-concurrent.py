import asyncio
import aiosqlite

async def async_fetch_users():
    """Fetch all users from the database"""
    async with aiosqlite.connect('users.db') as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            print("All users:")
            for row in results:
                print(dict(row))
            return results

async def async_fetch_older_users():
    """Fetch users older than 40"""
    async with aiosqlite.connect('users.db') as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            results = await cursor.fetchall()
            print("\nUsers over 40:")
            for row in results:
                print(dict(row))
            return results

async def fetch_concurrently():
    """Run both queries concurrently"""
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())