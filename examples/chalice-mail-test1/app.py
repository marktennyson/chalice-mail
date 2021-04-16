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
# mail.is_ses = True
# mail.aws_region= 'ap-south-1'
mail.template_dir = _baseDir/'templates'
mail.attachment_dir = _baseDir/'attachments'
mail.login()

@app.route('/')
def index():
    msg = Message(mail)
    msg.subject = "this is the subject"
    msg.add_recipient("aniketsarkar@yahoo.com")
    msg.plain = "Aniket"
    msg.html = "<h1>This is the HTML Message.</h1>"
    # msg.html = msg.render_template('text.html', email="aniketsarkarkorea@gmail.com")
    mail.send_email(msg)
    return {'message':'email sended successfully'}
