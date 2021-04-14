from .errors import *
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email.encoders import encode_base64
from jinja2 import Template, exceptions
from pathlib import Path

class Message:
    def __init__(self, mail, subject:str=str(),
                sender:str=str(),
                recipients:list=list(),
                body:str=str(),
                html:str=str(),
                cc:list=list(),
                bcc:list=list(),
                reply_to:str=str()):
        self.mail = mail
        self.subject = subject 
        self.sender  = sender
        self.recipients = recipients
        self.body = body 
        self.html = html
        self.cc = cc
        self.bcc = bcc
        self._attachments:list = list()
        self.reply_to = reply_to
    
    def _mimetext(self):
        if self.body and self.html: raise MIMETypeError #both mimetype can't be set at same time.
        if self.body and not self.html: return MIMEText(self.body, 'plain')
        if self.html and not self.body: return MIMEText(self.html, 'html')

    def _make_message(self) -> MIMEMultipart:
        message:MIMEMultipart = MIMEMultipart()
        message.attach(self._mimetext())
        message['Subject'] = self.subject
        message['From'] = self.sender or self.mail.username
        message['To'] = ", ".join(self.recipients)
        if len(self._attachments) > 0: 
            for attachment in self._attachments: message.attach(attachment)
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

    def add_attachment(self, attachment_file):
        if not self.mail.attachment_dir: raise InsufficientError('attachment_dir')
        if isinstance(attachment_file, str): self._attach_attachments_with_ins(attachment_file)
        if isinstance(attachment_file, list):
            for attachment in attachment_file: self._attach_attachments_with_ins(attachment)

    def to_string(self) -> str: return self._make_message().as_string() #it returns the string representation of the message instance.