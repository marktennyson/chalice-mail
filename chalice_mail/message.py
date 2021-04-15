from .errors import *
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email.encoders import encode_base64
from email.utils import formatdate, make_msgid
from jinja2 import Template, exceptions
from pathlib import Path
from time import time

class Message:
    def __init__(self, mail, subject:str=str(),
                sender:str=str(),
                recipients:list=list(),
                plain:str=str(),
                html:str=str(),
                cc:list=list(),
                bcc:list=list(),
                reply_to:str=str(),
                timedate:time=None,
                extra_headers:dict=None):
        self.mail = mail
        self.subject:str = subject 
        self.sender:str  = sender
        self.recipients:list = list(recipients) if not isinstance(recipients, list) else recipients
        self.plain:str = plain 
        self.html:str = html
        self.cc:list = cc
        self.bcc:list = bcc
        self._attachments:list = list()
        self.reply_to:str = reply_to
        self.timedate:str = formatdate(timedate) if timedate else formatdate(time())
        self.msg_id:str = make_msgid()
        self.extra_headers:dict = extra_headers
    
    @property
    def send_to(self):
        return set(self.recipients) | set(self.bcc or ()) | set(self.cc or ())

    # def _mimetext(self):
    #     if not self.plain and not self.html: raise InsufficientError('plain or html')
    #     if self.plain and not self.html: return MIMEText(self.plain, 'plain')
    #     if self.html and not self.plain: return MIMEText(self.html, 'html')
    #     if self.html and self.plain:

    def _make_message(self) -> MIMEMultipart:
        message:MIMEMultipart = MIMEMultipart()
        # message.attach(self._mimetext())
        if self.plain: message.attach(MIMEText(self.plain, 'plain'))
        if self.html: message.attach(MIMEText(self.html, 'html'))
        if not self.plain and not self.html: raise InsufficientError('plain or html')
        message['Subject'] = self.subject
        message['From'] = self.sender or self.mail.username
        message['Date'] = self.timedate
        message['Message-ID'] = self.msg_id
        if len(self.recipients) < 0: raise InsufficientError('recipients')
        message['To'] = ", ".join(self.recipients)
        if self.cc : message['Cc'] = ", ".join(self.cc) if isinstance(self.cc, list) else self.cc
        if self.bcc : message['Bcc'] = ", ".join(self.bcc) if isinstance(self.bcc, list) else self.bcc
        if self.reply_to: message['Reply-To'] = self.reply_to
        if len(self._attachments) > 0: 
            for attachment in self._attachments: message.attach(attachment)
        if self.extra_headers:
            for key, value in self.extra_headers.items():
                message[key] = value
        return message

    def add_recipient(self, recipient=None) -> None:
        if recipient is None: return None
        if isinstance(recipient, list): self.recipients.extend(recipient)
        if isinstance(recipient,str): self.recipients.append(recipient)

    def render_template(self, template_file, **context) -> str:
        if not self.mail.template_dir: raise InsufficientError('template_dir for Mail')
        try: 
            with open(Path(self.mail.template_dir)/template_file, 'r') as f:
                template:Template = Template(f.read())
                return template.render(context)
        except FileNotFoundError: raise TemplateNotFoundError(template_file)
        except exceptions.UndefinedError: raise Jinja2ContextDataError

    def _attach_attachments_with_ins(self, attachment_file) -> None:
        payload = MIMEBase('application', 'octet-stream')
        try:
            with open(Path(self.mail.attachment_dir)/attachment_file, 'rb') as f:
                payload.set_payload(f.read())
                encode_base64(payload)
                payload.add_header('Content-Disposition', 'attachment', filename=attachment_file)
                self._attachments.append(payload)
        except FileNotFoundError: raise AttachmentNotFoundError(attachment_file)

    def add_attachment(self, attachment_file) -> None:
        if not self.mail.attachment_dir: raise InsufficientError('attachment_dir')
        if isinstance(attachment_file, str): self._attach_attachments_with_ins(attachment_file)
        if isinstance(attachment_file, list):
            for attachment in attachment_file: self._attach_attachments_with_ins(attachment)

    def to_string(self) -> str: return self._make_message().as_string() #it returns the string representation of the message instance.