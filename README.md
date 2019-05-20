# Slackbot
Lightweight class for using python to interact with Slack by utilising the great [slackclient](https://github.com/slackapi/python-slackclient)!

The main benefit is the ability to use emails inplace of channel ID's and have the message always be sent in the channel between a user and the bot instead of in the Slackbot channel.
This was just made quickly for my team to use and I thought to share it before any internal integration, so I hope this helps get you off to a quick start.

### Set Up

- Install [slackclient](https://github.com/slackapi/python-slackclient)
- Set up a [Slack App](https://api.slack.com/slack-apps)
- Set up a bot on the 'Bot Users' tab on `https://api.slack.com/apps/YOUR-APP-ID`
- Go to 'OAuth & Permissions' and enable the following scopes
```
channels:history
channels:read
chat:write:bot
groups:read
im:read
incoming-webhook
mpim:read
files:read
files:write:user
bot
users:read
users:read.email
```
### Optional Token Set Up
We will be using the `Bot User OAuth Access Token`

_If you wish to extend this class you may need to use your `OAuth Access Token` for some methods._

Slackbot defaults to read your token from the JSON file `/Users/YOU/Credentials/slack.json`. Create this folder and file as below.
```
{
  "token": "xoxb-29XXXXXXXX-64XXXXXXXXXX-euXXXXXXXXXXXXXXXXXXXXXX"
}
```
If not; you can give your token manually when initialising an instance of Slackbot with `Slackbot(token=TOKEN)`, but this is not recommended for safety.

### Quick Guide

First initialise an instance of Slackbot with a `Bot User OAuth Access Token`.

```
slackbot = Slackbot()
```

You can easily send messages from within Slack. 
The `channel` can be a user email, channel name (#example), channel ID, chat ID or user ID. 
An email is probably the easiest to use and it can be found under a users profile. 
These messages will come from the bot account you have created for the app.
```
slackbot.send_message('Hello, World!', 'USER-EMAIL')
```

If a user does not yet have an IM ID with your bot, it will open an IM channel and send an automated onboarding message to the user with their user ID and IM ID. 
You can test this onboarding message by running

```
slackbot._send_onboarding_message('YOUR-SLACK-EMAIL')
```

You can send a file to a user by providing a file path.

```
slackbot.send_file('../hello.txt', 'USER-EMAIL')
```
