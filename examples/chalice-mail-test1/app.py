from chalice import Chalice
from os import getenv
from dotenv import load_dotenv
from chalice_mail import Mail, Message
from pathlib import Path
from os import path
load_dotenv()

app = Chalice(app_name='chalice-mail-test1')
_baseDir = Path(path.realpath(__file__)).parent
mail = Mail(app)
mail.is_smtp = True
mail.smtp_using_tls = True
mail.username = getenv('email_username')
mail.password = getenv('email_password')
mail.smtp_server = 'smtp.gmail.com'
mail.smtp_port = 587
mail.template_dir = _baseDir/'templates'
mail.attachment_dir = _baseDir/'attachments'
mail.login()

@app.route('/')
def index():
    msg = Message(mail)
    msg.subject = "this is the subject"
    # msg.recipients = ['aniketsarkar@yahoo.com']
    msg.add_recipient("aniketsarkarkorea@gmail.com")
    # msg.add_recipient(["aniket@cloodon.com"])
    # msg.html = "<h1>Hello World</h1>"
    msg.html = msg.render_template('text.html', email="aniketsarkarkorea@gmail.com")
    # msg.body = "Aniket"
    msg.add_attachment(['aniket.jpg', 'attachments.txt'])
    mail.send_email(msg)
    return {'message':'email sended successfully'}
