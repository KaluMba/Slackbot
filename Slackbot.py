import os
import re
import slack
import pandas

from pathlib import Path

def is_email(text):
    """
    Parameters
    ----------
    text: string
        text to test

    Returns
    -------
    boolean
        whether the input text is an email
    """
    return bool(re.match(r"^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", text))

class Slackbot:
    """Handles Slack interactions"""

    def __init__(self, token=None):
        if token is None:
            home = str(Path.home())
            self.token = dict(pandas.read_json(
                path_or_buf=f'{home}/Credentials/slack.json',
                typ='series'))['token']
        else:
            self.token = token
        self.client = slack.WebClient(token=self.token)
        self.ims = self.client.im_list()['ims']
        self.ims_users = [x['user'] for x in self.ims]

    def _get_im_ID(self, user):
        if user['id'] in self.ims_users:
            return [x['id'] for x in self.ims if x['user'] == user['id']][0]

    def _refresh_ims(self):
        self.ims = self.client.im_list()['ims']
        self.ims_users = [x['user'] for x in self.ims]

    def _construct_onboarding_message(self, user):
        if user['id'] not in self.ims_users:
            self.client.im_open(user=user['id'])
            self._refresh_ims()

        profile = user['profile']
        msg = (
            f'Ahoy, {profile["real_name"]}!\n\n'
            f'Your Slack ID is {user["id"]}\n')

        im = [x['id'] for x in self.ims if x['user'] == user['id']][0]
        msg = msg + f"Our IM ID is {im}"
        return msg

    def _send_onboarding_message(self, email):
        user = self.client.users_lookupByEmail(email=email)['user']
        msg = self._construct_onboarding_message(user)
        return self.send_message(msg, user['id'])

    def _im_open(self, user):
        """Opens a private channel between a user and the bot"""
        im = self._get_im_ID(user)
        if not im:
            self.client.im_open(user=user['id'])
            self._refresh_ims()
            im = self._get_im_ID(user)
            self._send_onboarding_message(user['profile']['email'])
            return im
        return im

    def send_message(self, msg: str, channel: str):
        """
        Sends a message to a given channel on Slack

        Parameters
        ----------
        msg : string
            The message to send
        channel : str
            Email or #channel

        Returns
        -------
        response : SlackResponse
            assert response['ok']
            response['message']
        """
        if is_email(channel):
            user = self.client.users_lookupByEmail(email=channel)['user']
            channel = self._im_open(user=user)
        response = self.client.chat_postMessage(
            text=msg,
            channel=channel)
        assert response['ok']
        assert response['message']['text'] == msg
        return response

    def send_file(self,
                  file,
                  channel,
                  title='',
                  msg=''):
        """
        Sends a file to a given channel on Slack

        Parameters
        ----------
        file : string
            relative file path
        channel : string
            channel name or ID
        title : string
            optional title
        msg : string
            optional message

        Returns
        -------
        response : SlackResponse
            assert response['ok']
            response['message']
        """
        if is_email(channel):
            user = self.client.users_lookupByEmail(email=channel)['user']
            channel = self._im_open(user=user)
        response = self.client.files_upload(
            channels=channel,
            file=file,
            initial_comment=msg,
            title=title)
        assert response['ok']
        return response
