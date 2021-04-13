class TemplateNotFoundError(Exception):
    def __init__(self, templateName:str=None):
        self.templateName:str = templateName
        self.message = '{0} not found at template folder'.format(self.templateName)
        super().__init__(self.message)

class InsufficientError(Exception):
    def __init__(self, message:str) -> None:
        self.message:str = message
        super().__init__(self.message)

class SMTPLoginError(Exception):
    def __init__(self, loginCreds:list) -> None:
        self.loginCreds:list = loginCreds
        self.message = 'failed to login with: '+', '.join(self.loginCreds)
        super().__init__(self.message)