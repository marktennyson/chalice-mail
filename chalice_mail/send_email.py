from os import getcwd
from smtplib import SMTP
from .errors import TemplateNotFoundError, InsufficientError, SMTPLoginError
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from jinja2 import Template


class SendEmail:
    def __init__(self, username:str=None, password:str=None, smtpServer:str=None, smtpPort:int=None, 
            is_smtp:bool=None, is_ses:bool=None, is_using_ssl:bool=None, is_using_tls:bool=None) -> None:
        self.message:MIMEMultipart = MIMEMultipart()
        self.username:str = username
        self.password:str = password
        self.smtpServer:str = smtpServer
        self.smtpPort:int = smtpPort
        self.is_smtp:bool = is_smtp
        self.is_ses:bool = is_ses
        self.is_using_ssl:bool = is_using_ssl
        self.is_using_tls:bool = is_using_tls
        if self.is_using_ssl: self.is_using_tls = False
        if self.is_using_tls: self.is_using_ssl = False
        if self.is_smtp: self._configure_smtp()
    
    def _check_none(self,var:list) -> list: return [val for val in var if val == None]
    
    def _configure_smtp(self):
        _required_none_var:list = self._check_none([self.username, self.password, self.smtpServer, 
                    self.smtpPort, self.is_using_ssl, self.is_using_tls])
        if len(_required_none_var) > 0: raise InsufficientError(", ".join(_required_none_var)+"are the required fields. please provide the sufficient data.")
        self.smtp = SMTP(self.smtpServer, self.smtpPort)
        self.smtp.ehlo()
        if self.is_using_ssl: self.smtp.startssl()
        elif self.is_using_tls: self.smtp.starttls()
        try: self.smtp.login()
        except: raise SMTPLoginError