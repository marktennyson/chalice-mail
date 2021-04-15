from smtplib import SMTP, SMTP_SSL
from .errors import *
from chalice import Chalice
from jinja2 import Template, exceptions
from pathlib import Path
from ssl import create_default_context

class Mail:
    def __init__(self, c_app:Chalice, 
            username:str=None, 
            password:str=None, 
            smtp_server:str=None, 
            smtp_port:int=None, 
            is_smtp:bool=None, 
            is_ses:bool=None, 
            smtp_using_ssl:bool=None, 
            smtp_using_tls:bool=None, 
            template_dir:str=None,
            attachment_dir:str=None) -> None:
        self.username:str = username
        self.password:str = password
        self.smtp_server:str = smtp_server
        self.smtp_port:int = smtp_port
        self.is_smtp:bool = is_smtp
        self.is_ses:bool = is_ses
        self.smtp_using_ssl:bool = smtp_using_ssl
        self.smtp_using_tls:bool = smtp_using_tls
        self.template_dir:str = template_dir
        self.attachment_dir:str = attachment_dir
        self.c_app = c_app
        if self.smtp_using_ssl: self.smtp_using_tls = False
        elif self.smtp_using_tls: self.smtp_using_ssl = False
        if self.is_smtp: self._configure_smtp()
    
    def _check_none(self,var:list) -> list: return [val for val in var if val == None]
    
    def _configure_smtp(self):
        if self.smtp_using_ssl: self.smtp_using_tls = False
        elif self.smtp_using_tls: self.smtp_using_ssl = False
        if not self.is_smtp or self.is_smtp == '': raise InsufficientError('is_smtp')
        if not self.username or self.username == '': raise InsufficientError('username')
        if not self.password or self.password == '': raise InsufficientError('password')
        if not self.smtp_server or self.smtp_server == '': raise InsufficientError('smtp_server')
        if not self.smtp_port or self.smtp_port == '': raise InsufficientError('smtp_port')
        if not self.smtp_using_ssl and not self.smtp_using_tls: raise InsufficientError('smtp_using_ssl, smtp_using_tls')
        if self.smtp_using_tls: # for smtp using start_tls
            self.smtp = SMTP(self.smtp_server, self.smtp_port)
            self.smtp.ehlo()
            self.smtp.starttls()
        elif self.smtp_using_ssl: # for smtp using start_ssl
            self.smtp = SMTP_SSL(self.smtp_server, self.smtp_port)
        try: self.smtp.login(self.username, self.password)
        except Exception as e: raise SMTPLoginError([self.username, self.password], e)
    
    def login(self): self._configure_smtp()

    def send_email(self, message):
        self.smtp.sendmail(self.username, message.recipients, message.to_string())

    def render_template(self, template_file, **context) -> str:
        if not self.template_dir: raise InsufficientError('template_dir')
        try: 
            with open(Path(self.template_dir)/template_file, 'r') as f:
                template:Template = Template(f.read())
                return template.render(context)
        except FileNotFoundError: raise TemplateNotFoundError(template_file)
        except exceptions.UndefinedError: raise Jinja2ContextDataError