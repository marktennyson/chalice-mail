chalice-mail
======================================

.. module:: chalice-mail

One of the most basic functions in a web application is the ability to send
emails to your users.

The **Chalice-Mail** extension provides a simple interface to set up SMTP as well as the SES(Simple Emial Server) with your
`Chalice`_ serverless application and to send messages from your views and scripts.

Links
-----

* `documentation <https://packages.python.org/Flask-Mail/>`_
* `source <https://github.com/marktennyson/chalice-mail>`_

Installing Chalice-Mail
-------------------------

Install with **pip** and **easy_install**::

    pip install chalice-mail

or download the latest version from version control::

    git clone https://github.com/marktennyson/chalice-mail.git
    cd chalice-mail
    python setup.py install


.. Configuring Chalice-Mail
.. ----------------------

.. **Chalice-Mail** is configured through the standard Flask config API. These are the available
.. options (each is explained later in the documentation):

.. * **MAIL_SERVER** : default **'localhost'**

.. * **MAIL_PORT** : default **25**

.. * **MAIL_USE_TLS** : default **False**

.. * **MAIL_USE_SSL** : default **False**

.. * **MAIL_DEBUG** : default **app.debug**

.. * **MAIL_USERNAME** : default **None**

.. * **MAIL_PASSWORD** : default **None**

.. * **MAIL_DEFAULT_SENDER** : default **None**

.. * **MAIL_MAX_EMAILS** : default **None**

.. * **MAIL_SUPPRESS_SEND** : default **app.testing**

.. * **MAIL_ASCII_ATTACHMENTS** : default **False**

.. In addition the standard Flask ``TESTING`` configuration option is used by **Flask-Mail**
.. in unit tests (see below).

Emails are managed through a ``Mail`` instance::

   from chalice import Chalice
   from chalice_mail import Mail

   app = Chalice(app_name='app')
   mail = Mail(app)
   mail.is_smtp = True
   mail.smtp_using_tls = True
   mail.username = "someone@example.com"
   mail.password = "world's_top_secret_password"
   mail.smtp_server = 'smtp.example.com'
   mail.smtp_port = 587
   mail.login()


Sending messages
----------------

To send a message first create a ``Message`` instance::

    from chalice_mail import Message

    @app.route("/")
    def index():

        msg = Message("Hello",
                      sender="from@example.com",
                      recipients=["to@example.com"])

You can set the recipient emails immediately, or individually::

    msg.recipients = ["you@example.com"]
    msg.add_recipient("somebodyelse@example.com")

If you have set ``username`` you don't need to set the message
sender explicity, as it will use this configuration value by default::

    msg = Message("Hello",
                  recipients=["to@example.com"])

The message can contain a body and/or HTML::

    msg.body = "testing"
    msg.html = "<b>testing</b>"

Finally, to send the message, you use the ``Mail`` instance configured with your Flask application::

    mail.send(msg)

Simple Example => Using SMTP TLS
--------------------------------

send emails using the tls encryption::

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

Simple Example => Using SMTP SSL
--------------------------------
send email using smtp ssl encryption::

   from chalice import Chalice
   from chalice_mail import Mail, Message

   app = Chalice(app_name='app')
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

Simple Example => Using SES
--------------------------------
send uisng aws ses service::

   from chalice import Chalice
   from chalice_mail import Mail, Message

   app = Chalice(app_name='app')
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

Email with Html
---------------
send email using html raw_data::

   from chalice import Chalice
   from chalice_mail import Mail, Message

   app = Chalice(app_name='app')
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

Email with HTML Rendering
-------------------------
send email with html rendering::

   from chalice import Chalice
   from chalice_mail import Mail, Message
   from pathlib import Path
   from os import path

   app = Chalice(app_name='app')
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

Email with Attachments
-----------------------
send email with attachments::

   from chalice import Chalice
   from chalice_mail import Mail, Message
   from pathlib import Path
   from os import path

   app = Chalice(app_name='app')
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

See the `API`_ for details.


API
---

.. module:: chalice_mail

.. autoclass:: Mail
   :members: send_email, render_template, login



.. autoclass:: Message
   :members: add_recipient, add_attachment, render_template, to_string, to_bytes

.. _GitHub: http://github.com/marktennyson/chalice-mail