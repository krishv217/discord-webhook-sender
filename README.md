# discord-webhook-sender
A multi-webhook customizable message sender with support for embeds, images and role pinging.

To use:
1. Install required packages using `pip install -r requirements.txt`
2. Enter your Discord bot token and customize embed features (headers, footers, thumbnails, etc.) in DiscordWHSender.py
3. Run DiscordWHSender.py

Supported commands:
• `!<message>` - Send embed message to all webhooks
• `&<message>` - Send normal message to all webhooks
• `$current` - Show current image URL
• `$setimage <url>` - Set image URL for embeds
• `$clearimage` - Clear current image
• `$reload` - Reload webhook configuration from JSON
• `$help` - Show the help message

If you have any issues, feel free to DM me on Discord @ `.krik`
