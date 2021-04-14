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

class MIMETypeError(Exception):
    def __init__(self):
        super().__init__("html and plain can't be set at same time.")