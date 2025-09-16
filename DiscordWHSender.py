import discord
from discord_webhook import DiscordWebhook, DiscordEmbed
import asyncio
from threading import Thread
import json
import os

# change token
TOKEN = "Discord Bot Token"

intents = discord.Intents.default()
intents.message_content = True  

client = discord.Client(intents=intents)

# Global variable for image URL - add if you want a default img every time
image = ""

# Configuration variables - customize these for your use case
EMBED_TITLE = "Information Alert"
EMBED_COLOR = 15207950  # Can also use hex: 0xE8034E
AUTHOR_NAME = "Bot Name"
AUTHOR_URL = "https://example.com"
AUTHOR_ICON = "https://example.com/author-icon.png"
THUMBNAIL_URL = "https://example.com/thumbnail.png"
FOOTER_TEXT = "Footer Text | example.com"
FOOTER_ICON = "https://example.com/footer-icon.png"

# Load webhook configuration from JSON file
def load_webhook_config():
    """Load webhook configuration from webhooks.json"""
    try:
        with open('webhooks.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ webhooks.json file not found! Creating a default one...")
        # Create default config if file doesn't exist
        default_config = {
            "group1": {
                "name": "Default Group",
                "wh": "YOUR_WEBHOOK_URL_HERE",
                "role": 1234567890
            }
        }
        with open('webhooks.json', 'w') as f:
            json.dump(default_config, f, indent=2)
        print("✅ Default webhooks.json created. Please update it with your webhook URLs.")
        return default_config
    except json.JSONDecodeError:
        print("❌ Error parsing webhooks.json. Please check the JSON format.")
        return {}

# Load webhook info from JSON file
info = load_webhook_config()

def embed_webhook(webhook, image_url, content, role=None):
    """Send an embed webhook message"""
    try:
        if role:
            wh = DiscordWebhook(url=webhook, content=f'<@&{role}>')
        else:
            wh = DiscordWebhook(url=webhook)
        
        # Create embed object for webhook
        embed = DiscordEmbed(
            title=EMBED_TITLE, 
            description=content, 
            color=EMBED_COLOR
        )
        
        # Set author
        embed.set_author(
            name=AUTHOR_NAME, 
            url=AUTHOR_URL, 
            icon_url=AUTHOR_ICON
        )
        
        # Set thumbnail
        embed.set_thumbnail(url=THUMBNAIL_URL)
        
        # Set footer
        embed.set_footer(
            text=FOOTER_TEXT, 
            icon_url=FOOTER_ICON
        )
        
        # Add image if provided
        if image_url:
            embed.set_image(url=image_url)
        
        # Add embed object to webhook
        wh.add_embed(embed)
        response = wh.execute()
        return response
    except Exception as e:
        print(f"Error sending embed webhook: {e}")

def normal_webhook(webhook, desc, role=None):
    """Send a normal webhook message"""
    try:
        if role:
            wh = DiscordWebhook(url=webhook, content=f'<@&{role}>\n{desc}')
        else:
            wh = DiscordWebhook(url=webhook, content=desc)
        
        response = wh.execute()
        return response
    except Exception as e:
        print(f"Error sending normal webhook: {e}")

@client.event
async def on_ready():
    """Event triggered when bot is ready"""
    print(f"{client.user} is now online!")
    print(f"Bot ID: {client.user.id}")
    print(f"Discord.py version: {discord.__version__}")

@client.event
async def on_message(message):
    """Event triggered when a message is sent"""
    global image, info
    
    # Ignore messages from the bot itself
    if message.author == client.user:
        return
    
    # Embed webhook command
    if message.content.startswith('!'):
        content = message.content[1:]  # Remove the '!' prefix
        
        try:
            # Send to all configured webhooks
            for group_key in info:
                webhook_url = info[group_key]["wh"]
                role_id = info[group_key]["role"]
                
                # Use threading to avoid blocking
                Thread(
                    target=embed_webhook, 
                    args=(webhook_url, image, content, role_id)
                ).start()
            
            await message.channel.send("✅ Embed message sent to all webhooks.")
        except Exception as e:
            await message.channel.send(f"❌ Error sending embed message: {e}")

    # Regular webhook command
    elif message.content.startswith('&'):
        desc = message.content[1:]  # Remove the '&' prefix
        
        try:
            # Send to all configured webhooks
            for group_key in info:
                webhook_url = info[group_key]["wh"]
                role_id = info[group_key]["role"]
                
                # Use threading to avoid blocking
                Thread(
                    target=normal_webhook, 
                    args=(webhook_url, desc, role_id)
                ).start()
            
            await message.channel.send("✅ Message sent to all webhooks.")
        except Exception as e:
            await message.channel.send(f"❌ Error sending message: {e}")

    # Show current image command
    elif message.content.startswith('$current'):
        if image:
            await message.channel.send(f"📷 Current image: {image}")
        else:
            await message.channel.send("📷 No image currently set.")
    
    # Set image command
    elif message.content.startswith('$setimage '):
        new_image = message.content[10:]  # Remove '$setimage ' prefix
        image = new_image.strip()
        await message.channel.send(f"✅ Image set to: {image}")
    
    # Clear image command
    elif message.content.startswith('$clearimage'):
        image = ""
        await message.channel.send("✅ Image cleared.")
    
    # Help command
    elif message.content.startswith('$help'):
        help_text = """
**Bot Commands:**
• `!<message>` - Send embed message to all webhooks
• `&<message>` - Send normal message to all webhooks
• `$current` - Show current image URL
• `$setimage <url>` - Set image URL for embeds
• `$clearimage` - Clear current image
• `$reload` - Reload webhook configuration from JSON
• `$help` - Show this help message
        """
        await message.channel.send(help_text)
    
    # Reload webhook configuration
    elif message.content.startswith('$reload'):
        info = load_webhook_config()
        await message.channel.send(f"✅ Webhook configuration reloaded. Found {len(info)} webhook groups.")

async def main():
    """Main function to run the bot"""
    try:
        await client.start(TOKEN)
    except discord.LoginFailure:
        print("❌ Invalid token provided!")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    # Run the bot
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")