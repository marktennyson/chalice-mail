from .errors import TemplateNotFoundError, InsufficientError, SMTPLoginError, MIMETypeError
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from jinja2 import Template
from .mail import Mail

class Message:
    def __init__(self, mail:Mail, subject:str=None,
                sender:str=None,
                recipients:list=None,
                body:str=None,
                html:str=None,
                cc:list=None,
                bcc:list=None,
                attachments=None,
                reply_to:str=None):
        self.mail:Mail = mail
        self.subject = subject 
        self.recipients = recipients or list()
        self.body = body 
        self.html = html
        self.cc = cc or list()
        self.bcc = bcc or list()
        self.attachments = attachments
        self.reply_to = reply_to
    
    def _mimetext(self):
        if self.body is not None and self.html is not None: raise MIMETypeError #both mimetype can't be set at same time.
        if self.body is not None and self.html is None: return MIMEText(self.body, 'plain')
        if self.html is not None and self.body is None: return MIMEText(self.html, 'html')

    def _make_message(self):
        message:MIMEMultipart = MIMEMultipart()
        message.attach(self._mimetext())
        message['Subject'] = self.subject
        message['From'] = self.mail.username
        message['To'] = ", ".join(self.recipients)
        return message

    def add_recipient(self, recipient=None) -> None:
        if recipient is None: return None
        if isinstance(recipient, list): self.recipients.extend(recipient)
        if isinstance(recipient,str): self.recipients.append(recipient)

    def to_string(self) -> str: return self._make_message().as_string() #it returns the string representation of the message instance.

    def _send_email(self):pass
