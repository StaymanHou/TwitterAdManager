import requests
import Config
from time import sleep
import logging
import re

class TwitterSession(object):
    """A Twitter Session object. Contains a :class:`Lib.TwitterAccount.TwitterAccount` object 
        and a :class:`requests.session` object. It also maintains auth_token and root_url 
        after login. :attr:`is_login` holds the status of the session whether it's login or not.
        You can use it just as a :class:`requests.session`.

            >>> ts = TwitterSession(twitterAccount)
            >>> url = ...
            >>> r = ts.get(url)
            >>> payload = {...}
            >>> r = ts.post(url, payload)
        
        It will guarantee to login the twitter account before :func:`get()` 
        and :func:`post()`. So you do not have to call 
        :func:`Lib.TwitterSession.TwitterSession.login`. You can get the auth_token
        and the root_url by calling :func:`Lib.TwitterSession.TwitterSession.get_auth_token` 
        and :func:`Lib.TwitterSession.TwitterSession.get_root_url`. They will alse guarantee the login.
        **Do not** try to access auth_token and root_url directly. It will be a empty 
        string before login.
    """

    account = None
    session = None
    is_login = False
    waiting_time = 0
    initial_time = 0
    increase_ratio = 0
    load_interval = 0
    auth_token = ''
    root_url = ''

    def __init__(self, account):
        super(TwitterSession, self).__init__()
        self.account = account
        self.session = requests.Session()
        config = Config.get()
        self.initial_time = config.getint('General', 'initial_retry_waiting_time')
        self.increase_ratio = config.getint('General', 'retry_waiting_time_increase_ratio')
        self.load_interval = config.getint('General', 'load_interval')

    def get(self, url, **kwargs):
        """Commit a get requests with :attr:`self.session`.
            It will guarantee to login first.
        """
        self.login()
        return self.session.get(url, **kwargs)

    def post(self, url, **kwargs):
        """Commit a post requests with :attr:`self.session`.
            It will guarantee to login first.
        """
        self.login()
        return self.session.post(url, **kwargs)

    def get_root_url(self):
        """Return the :attr:`self.root_url`.
            It will guarantee to login first.
        """
        self.login()
        return self.root_url

    def get_auth_token(self):
        """Return the :attr:`self.auth_token`.
            It will guarantee to login first.
        """
        self.login()
        return self.auth_token

    def login(self):
        """Reset the :attr:`self.session` and use the session to login
            Infinite loop with an increasing retry waiting time 
            until successful login.
            It calls :func:`Lib.TwitterSession.TwitterSession.commit_login` to commit login.
            Please invoke this method at the begining of other method
            to make sure the login status.
        """
        while not self.is_login:
            self.session = requests.Session()
            if self.commit_login() == 0:
                self.waiting_time = 0
                self.is_login = True
                logging.info('@%s: login succeeded!'%self.account.username)
                return
            if self.waiting_time == 0:
                self.waiting_time = self.initial_time
            else:
                self.waiting_time *= self.increase_ratio
            logging.warning('@%s: login failed. retry in %d sec'%(self.account.username, self.waiting_time))
            sleep(self.waiting_time)
        
    def commit_login(self):
        """Return 0 if success, otherwise return none zero. Commit login 
            and perform the behavior.
        """
        # visit login page and get authenticity_token
        url = 'https://ads.twitter.com/login'
        try:
            r = self.session.get(url)
        except Exception, e:
            logging.warning('login warning -1: /login page request error | %s'%str(e))
            return -1
        if r.status_code!=200:
            logging.warning('login warning -2: /login page unexpected response | Status code: %d'%r.status_code)
            return -2
        m = re.search('<meta name="csrf-token" content="(.+?)"',r.text)
        if m is None:
            logging.warning('login warning -3: /login page cant find csrf-token')
            return -3
        self.auth_token = m.group(1)
        sleep(self.load_interval)
        # post username and password to session page to login
        url = 'https://ads.twitter.com/session' 
        payload = {'user_identifier': self.account.username,
                   'redirect_after_login': '',
                   'password': self.account.password,
                   'authenticity_token': self.auth_token}  
        try:
            r = self.session.post(url, data=payload)
        except Exception, e:
            logging.warning('login warning -4: /session page request error | %s'%str(e))
            return -4
        if r.status_code!=200:
            logging.warning('login warning -5: /session page unexpected response | Status code: %d'%r.status_code)
            return -5
        m = re.search('<title id="page_title">Sign in - Twitter Ads</title>',r.text)
        if m is not None:
            logging.warning('login warning -6: please check you username and password')
            return -6
        sleep(self.load_interval)
        # visit accounts page to get account root url
        url = 'https://ads.twitter.com/accounts'
        try:
            r = self.session.get(url)
        except Exception, e:
            logging.warning('login warning -7: /accounts page request error | %s'%str(e))
            return -7
        if r.status_code!=200:
            logging.warning('login warning -8: /accounts page unexpected response')
            return -8
        m = re.search('<li class=\'active \'><a href="(.+?)/campaigns">Campaigns</a></li>',r.text)
        if m is None:
            logging.warning('login warning -9: /accounts page cant find Account settings for root url')
            return -9
        self.root_url = 'https://ads.twitter.com'+m.group(1)
        sleep(self.load_interval)
        return 0
