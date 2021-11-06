from core import WebhookClient, Embed
import datetime

client = WebhookClient(
    webhook_url="https://discord.com/api/webhooks/906585629092102144/36t_wa8PuYUYsngE8D7rMumVVdQvrV4LiBROon3Ftslw2aWYhLJriXm9k_xWY71iDruj",
    username="github.com/elijahgives",
    avatar_url="https://cdn.discordapp.com/attachments/906585612663009314/906624383152431234/gift-gif.gif"
        )

embed = Embed(
    title='Hello, world.',
    description='This is a test embed from DiscordWebhook by ElijahGives.',
    timestamp=datetime.datetime.utcnow()
)
embed.add_field(name='Field #1', value="Description for `Field #1`.")
embed.add_field(name='Field #2', value="Description for `Field #2`.")
embed.set_image(url="https://cdn.discordapp.com/attachments/906585612663009314/906624383152431234/gift-gif.gif")

client.send('Hello world', embeds=[embed])