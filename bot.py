from pyrogram import Client
from pyrogram.errors import FloodWait, PeerIdInvalid
import time

# Replace these with your own API details
API_ID = "22359038"
API_HASH = "b3901895dc193c30c808ba4f1b550ed0"
SESSION_NAME = "test"  # Can be any session name

# Initialize the Pyrogram client
app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)

async def remove_banned_users(channel_username):
    """
    Unbans all banned users from a group or channel.
    """
    async with app:
        try:
            # Ensure we "meet" the channel first
            chat = await app.get_chat(channel_username)
            print(f"Successfully accessed channel/group: {chat.title}")
        except PeerIdInvalid:
            print("Error: The channel or group is invalid, or the user hasn't interacted with it yet.")
            return

        # Fetch all banned members
        async for banned_member in app.get_chat_members(channel_username, filter="banned"):
            try:
                # Unban the member
                await app.unban_chat_member(channel_username, banned_member.user.id)
                print(f"Unbanned: {banned_member.user.first_name} (ID: {banned_member.user.id})")
                time.sleep(1)  # Respect rate limits

            except FloodWait as e:
                print(f"FloodWait: Sleeping for {e.value} seconds")
                time.sleep(e.value)
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    target_channel = input("Enter the username or ID of the group/channel: ")
    app.run(remove_banned_users(target_channel))
