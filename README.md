<h1>One of the most basic functions in a web application is the ability to send emails to your users fully serverlessly.</h1>
# Maintainers wanted
<!-- [Apply within](https://github.com/github-tools/github/issues/539) -->

# Chalice-Mail

<!-- [![Downloads per month](https://img.shields.io/npm/dm/github-api.svg?maxAge=2592000)][npm-package]
[![Latest version](https://img.shields.io/npm/v/github-api.svg?maxAge=3600)][npm-package]
[![Gitter](https://img.shields.io/gitter/room/github-tools/github.js.svg?maxAge=2592000)][gitter]
[![Travis](https://img.shields.io/travis/github-tools/github.svg?maxAge=60)][travis-ci]
[![Codecov](https://img.shields.io/codecov/c/github/github-tools/github.svg?maxAge=2592000)][codecov] -->

The `Chalice-Mail` extension provides a simple interface to set up SMTP and AWS SES(Simple Email Service) with your Chalice application and to send messages from your views and scripts.
source code available at: <a href="https://github.com/marktennyson/chalice-mail">Github Repo</a>

## Usage
##### Using SMTP => TLS Encryption
```python
from chalice import Chalice
from chalice_mail import Mail, Message

app = Chalice(app_name='chalice-mail-test1')
mail = Mail(app)
mail.is_smtp = True
mail.smtp_using_tls = True
mail.username = "someone@example.com"
mail.password = "world's_top_secret_password"
mail.smtp_server = 'smtp.example.com'
mail.smtp_port = 587
mail.login()

@app.route('/send-smtp-mail')
def send_smtp_mail():
    msg = Message(mail)
    msg.subject = "this is the subject"
    msg.add_recipient("aniketsarkar@yahoo.com")
    msg.plain = "This is the email body."
    mail.send_email(msg)
    return {'message':'email sended successfully'}

```
##### Using SMTP => SSL Encryption
```python
from chalice import Chalice
from chalice_mail import Mail, Message

app = Chalice(app_name='chalice-mail-test1')
mail = Mail(app)
mail.is_smtp = True
mail.smtp_using_ssl = True
mail.username = "someone@example.com"
mail.password = "world's_top_secret_password"
mail.smtp_server = 'smtp.example.com'
mail.smtp_port = 465
mail.login()

@app.route('/send-smtp-mail')
def send_smtp_mail():
    msg = Message(mail)
    msg.subject = "this is the subject"
    msg.add_recipient("aniketsarkar@yahoo.com")
    msg.plain = "This is the email body."
    mail.send_email(msg)
    return {'message':'email sended successfully'}

```
##### Using SES(Simple Email Service)
```python
from chalice import Chalice
from chalice_mail import Mail, Message

app = Chalice(app_name='chalice-mail-test1')
mail = Mail(app)
mail.username = "someone@example.com"
mail.aws_region = "ap-south-1"
"""
please provide the value of 'mail.aws_secret_id' 
and 'mail.aws_secret_key' if you want to set the AWS 
Iam user manually.
"""
mail.login()

@app.route('/send-smtp-mail')
def send_smtp_mail():
    msg = Message(mail)
    msg.subject = "this is the subject"
    msg.add_recipient("aniketsarkar@yahoo.com")
    msg.plain = "This is the email body."
    mail.send_email(msg)
    return {'message':'email sended successfully'}

```
##### Using SMTP => Email with HTML
```python
from chalice import Chalice
from chalice_mail import Mail, Message

app = Chalice(app_name='chalice-mail-test1')
mail = Mail(app)
mail.is_smtp = True
mail.smtp_using_tls = True
mail.username = "someone@example.com"
mail.password = "world's_top_secret_password"
mail.smtp_server = 'smtp.example.com'
mail.smtp_port = 587
mail.login()

@app.route('/send-smtp-mail')
def send_smtp_mail():
    msg = Message(mail)
    msg.subject = "this is the subject"
    msg.add_recipient("aniketsarkar@yahoo.com")
    """ 
    Simply pass the html value to the html variable of Message instance.
    """
    msg.html = "<h1>This is the email body.</h1>"
    mail.send_email(msg)
    return {'message':'email sended successfully'}

```
##### Using SMTP => Email with HTML rendering
```python
from chalice import Chalice
from chalice_mail import Mail, Message
from pathlib import Path
from os import path

app = Chalice(app_name='chalice-mail-test1')
_baseDir = Path(path.realpath(__file__)).parent
mail = Mail(app)
mail.is_smtp = True
mail.smtp_using_tls = True
mail.username = "someone@example.com"
mail.password = "world's_top_secret_password"
mail.smtp_server = 'smtp.example.com'
mail.smtp_port = 587
mail.template_dir = _baseDir/'templates' # required if using template rendering.
mail.login()

@app.route('/send-smtp-mail')
def send_smtp_mail():
    msg = Message(mail)
    msg.subject = "this is the subject"
    msg.add_recipient("aniketsarkar@yahoo.com")
    context={}
    """
    This package comes with the jinja2 based template rendering system.
    Simpley use the 'render_template()' function to rend the html file.
        'render_template()' functions takes the html file name as arguments 
    and the context as well as.
    """
    msg.html = mail.render_template('index.html', context)
    mail.send_email(msg)
    return {'message':'email sended successfully'}

```
##### Using SMTP => Email with attachments
```python
from chalice import Chalice
from chalice_mail import Mail, Message
from pathlib import Path
from os import path

app = Chalice(app_name='chalice-mail-test1')
_baseDir = Path(path.realpath(__file__)).parent
mail = Mail(app)
mail.is_smtp = True
mail.smtp_using_tls = True
mail.username = "someone@example.com"
mail.password = "world's_top_secret_password"
mail.smtp_server = 'smtp.example.com'
mail.smtp_port = 587
mail.attachment_dir = _baseDir/'attachments' # required if using attachments.
mail.login()

@app.route('/send-smtp-mail')
def send_smtp_mail():
    msg = Message(mail)
    msg.subject = "this is the subject"
    msg.add_recipient("aniketsarkar@yahoo.com")
    msg.plain = "This is the email body."
    """
    Use the 'add_attachments()' function to add the attachments 
    with the message instance. Don't forget to put the attachments 
    on the attachments folder.
        'add_attachments()' function basically takes list or str data 
    type as argument. If you want to add only one attachment just pass 
    the attachment name. If you want to add more than one attachments use a list.
    """
    msg.add_attachments(['python.png', 'README.rst'])
    mail.send_email(msg)
    return {'message':'email sended successfully'}

```

## Installation
`chalice-mail` is available from `pypi`.
#### install using pip
```shell
pip install chalice-mail
```
#### install from source code
```shell
git clone https://github.com/marktennyson/chalice-mail && cd chalice-mail
python setup.py install --user
```

## Compatibility
`chalice-mail` is compatiable with python3.6 and higher versions.
Not compatiable for Python version 2.


## Contributing

We welcome contributions of all types!