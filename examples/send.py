from webhook_client import WebhookClient, Embed
import datetime

client = WebhookClient(
    webhook_url="HOOK_URL",
    username="github.com/elijahgives",
    avatar_url="https://cdn.discordapp.com/attachments/906585612663009314/906624383152431234/gift-gif.gif"
        )

embed = Embed(
    title='Hello from embed!',
    description='Example embed from [webhook-client](https://github.com/elijahgives/webhook-client).',
    timestamp=datetime.datetime.utcnow()
)
embed.add_field(name='Field #1', value="Description for `Field #1`.")
embed.set_image(url="https://cdn.discordapp.com/attachments/906585612663009314/906624383152431234/gift-gif.gif")

client.send('Hello world', embeds=[embed], tts=False)