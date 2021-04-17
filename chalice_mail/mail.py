from smtplib import SMTP, SMTP_SSL
from jinja2 import Template, exceptions
from pathlib import Path
from boto3 import client
from botocore.exceptions import ClientError
from ._errors import *

class Mail:
    """Manages email messaging

    :param is_smtp: set True if want to send email using smtp server.
    :param is_ses: set True if want to send email using aws ses.
    :param username: smtp login username, required if using smtp.
    :param password: smtp login password, required if using smtp.
    :param smtp_server: smtp server name, required if using smtp.
    :param smtp_port: smtp port number, required if using smtp.
    :param aws_secret_id: aws IAM user secret id, required if want to pass creds manually.
    :param aws_secret_key: aws IAM user secret key, required if want to pass creds manually.
    :param aws_region: deafult region for aws ses, required if using ses.
    :param smtp_using_ssl: set it True if want to send email using ssl based encryption.
    :param smtp_using_tls: set it True if want to send email using tls based encryption.
    :param template_dir: default location for all html templates, required if want to rend html template.
    :param attachment_dir: default location for all attachments, required if want to send email with attachments.
    """
    def __init__(self, is_smtp:bool=None, 
            is_ses:bool=None,
            username:str=None, 
            password:str=None,
            smtp_server:str=None, 
            smtp_port:int=None, 
            aws_secret_id:str=None, 
            aws_secret_key:str=None, 
            aws_region:str=None,   
            smtp_using_ssl:bool=None, 
            smtp_using_tls:bool=None, 
            template_dir:str=None, 
            attachment_dir:str=None) -> None: 
        self.is_smtp:bool = is_smtp # required if using smtp.
        self.is_ses:bool = is_ses # required if using ses.
        self.username:str = username # required for both smtp and ses.
        self.password:str = password # required if using smtp.
        self.aws_secret_id = aws_secret_id # required if somebody want to pass the creds manually.
        self.aws_secret_key = aws_secret_key # required if somebody want to pass the creds manually.
        self.aws_region = aws_region # required is using ses.
        self.smtp_server:str = smtp_server # required if using smtp.
        self.smtp_port:int = smtp_port # required if using smtp.
        self.smtp_using_ssl:bool = smtp_using_ssl # required if using smtp for ssl.
        self.smtp_using_tls:bool = smtp_using_tls # required if using smtp for tls.
        self.template_dir:str = template_dir # required if somebody wants to send email with template rendering.
        self.attachment_dir:str = attachment_dir # required if somebody wants to send email with attachments.
        if self.smtp_using_ssl: self.smtp_using_tls = False
        elif self.smtp_using_tls: self.smtp_using_ssl = False
        if self.is_smtp: self._configure_smtp()
        
    def _configure_smtp(self) -> None:
        if self.smtp_using_ssl: self.smtp_using_tls = False
        elif self.smtp_using_tls: self.smtp_using_ssl = False
        if not self.is_smtp or self.is_smtp == '': raise InsufficientError('is_smtp')
        if not self.username or self.username == '': raise InsufficientError('username')
        if not self.password or self.password == '': raise InsufficientError('password')
        if not self.smtp_server or self.smtp_server == '': raise InsufficientError('smtp_server')
        if not self.smtp_port or self.smtp_port == '': raise InsufficientError('smtp_port')
        if not self.smtp_using_ssl and not self.smtp_using_tls: raise InsufficientError('smtp_using_ssl, smtp_using_tls')
        if self.smtp_using_tls: # for smtp using start_tls
            self.smtp:SMTP = SMTP(self.smtp_server, self.smtp_port)
            self.smtp.ehlo()
            self.smtp.starttls()
        elif self.smtp_using_ssl: # for smtp using start_ssl
            self.smtp:SMTP_SSL = SMTP_SSL(self.smtp_server, self.smtp_port)
        try: self.smtp.login(self.username, self.password)
        except Exception as e: raise SMTPLoginError([self.username, self.password], e)
        
    def _configure_ses(self) -> None: 
        if not self.is_ses: raise InsufficientError('is_ses')
        if not self.aws_region: raise InsufficientError('aws_region')
        if self.aws_secret_id and not self.aws_secret_key: raise InsufficientError('aws_secret_key')
        if self.aws_secret_key and not self.aws_secret_id: raise InsufficientError('aws_secret_id')
        if self.aws_secret_id and self.aws_secret_key: 
            self.ses = client('ses', aws_access_key_id=self.aws_secret_id, 
                    aws_secret_access_key=self.aws_secret_key, region_name=self.aws_region)
        else: self.ses = client('ses', region_name=self.aws_region)

    def login(self) -> None: 
        """create the smtp or ses client object """
        
        if self.is_smtp: self._configure_smtp()
        elif self.is_ses: self._configure_ses()

    def _send_ses_mail(self, message) -> bool:
        try: 
            _ = self.ses.send_email(
                Destination={
                    'ToAddresses': list(message.send_to),
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': 'utf-8',
                            'Data': message.to_string(),
                        },
                    },
                    'Subject': {
                        'Charset': 'utf-8',
                        'Data': message.subject,
                    },
                },
                Source=message.sender or self.username,
            )
            return True
        except ClientError as e: raise SESError(e)

    def send_email(self, message) -> None:
        """Sends a single message instance.

        :param message: a Message instance.
        :required: please select at least one server option between `is_smtp` or `is_ses`
        """
        if self.is_ses and self.is_smtp: raise ServerTypeError
        if not self.username and not message.sender: raise InsufficientError('username or sender')
        if self.is_smtp: self.smtp.sendmail(message.sender or self.username, message.send_to, message.to_string())
        if self.is_ses: self._send_ses_mail(message)

    def render_template(self, template_file, **context) -> str:
        """
        render the html templates with context data using the super-power of Jinja2.

        :param template_file: html file name.
        :param **context: context params for template rendering.
        """
        if not self.template_dir: raise InsufficientError('template_dir')
        try: 
            with open(Path(self.template_dir)/template_file, 'r') as f:
                template:Template = Template(f.read())
                return template.render(context)
        except FileNotFoundError: raise TemplateNotFoundError(template_file)
        except exceptions.UndefinedError: raise Jinja2ContextDataError
