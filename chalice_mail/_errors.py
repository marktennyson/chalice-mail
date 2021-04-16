class TemplateNotFoundError(Exception):
    def __init__(self, templateName:str=None):
        self.templateName:str = templateName
        self.message = '{0} not found at template folder'.format(self.templateName)
        super().__init__(self.message)

class InsufficientError(Exception):
    def __init__(self, field:str) -> None:
        self.message:str = field+ " is the required field"
        super().__init__(self.message)

class SMTPLoginError(Exception):
    def __init__(self, loginCreds:list, errorMessage:str=None) -> None:
        self.loginCreds:list = loginCreds
        self.message = 'failed to login with: '+', '.join(self.loginCreds)+". Response from smtp server: "+str(errorMessage)
        super().__init__(self.message)

class ServerTypeError(Exception):
    def __init__(self) -> None:
        super().__init__("please choose only one between smtp and ses.")

class Jinja2ContextDataError(Exception):
    def __init__(self) -> None:
        super().__init__("templating jinja2 format is not valid.")

class AttachmentNotFoundError(Exception):
    def __init__(self, attachment_file):
        self.message = "{0} not found at attachments folder".format(attachment_file)
        super().__init__(self.message)

class SESError(Exception):
    def __init__(self, message): 
        super().__init__("failed to send ses email.because: "+str(message))