import disnake
import asyncio
from disnake.ext import commands
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

intents = disnake.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

bot = commands.InteractionBot(intents=intents)


def dbCon():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )

def insertMsgsInDb(guild_id, msg_data):
    if not msg_data:
        return
    db = dbCon()
    cursor = db.cursor()

    cursor.executemany(
        "INSERT INTO messages (channel_id, guild_id, author_id, content, created_at) VALUES (%s, %s, %s, %s, %s)",
        msg_data
    )

    db.commit()
    cursor.close()
    db.close()
    print(f"Inserted {len(msg_data)} messages into database.")


@bot.event
async def on_ready():
    print(f"{bot.user} has connected.")

    guild = bot.guilds[0]
    print(f"Bot is running on {guild.name}")

    last_message_ids = {}

    while True:
        for channel in guild.text_channels:
            print(f"Fetching from #{channel.name}...")

            last_message_id = last_message_ids.get(channel.id)
            fetched_messages = []
            msg_data = []

            try:
                if last_message_id:
                    async for msg in channel.history(
                            limit=100,
                            before=disnake.Object(id=last_message_id),
                            oldest_first=False
                    ):
                        fetched_messages.append(msg)
                else:
                    async for msg in channel.history(limit=100, oldest_first=False):
                        fetched_messages.append(msg)

                if fetched_messages:
                    last_message_ids[channel.id] = fetched_messages[-1].id

                    for msg in fetched_messages:
                        if msg.content:
                            msg_data.append((
                                msg.channel.id,
                                guild.id,
                                msg.author.id,
                                msg.content,
                                msg.created_at
                            ))

                    insertMsgsInDb(guild.id, msg_data)

                print(f"Fetched {len(fetched_messages)} messages from {channel.name}")

            except disnake.Forbidden:
                print(f"Missing permissions for {channel.name}")
            except Exception as e:
                print(f"Error fetching from {channel.name}: {e}")

        print("Cycle complete.\n")
        await asyncio.sleep(6)


if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))
