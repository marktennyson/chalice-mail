from ._errors import TemplateNotFoundError, Jinja2ContextDataError
from jinja2 import Template, exceptions

def render_template(template_file, **context) -> str:
    try: 
        with open(template_file, 'r') as f:
            template:Template = Template(f.read())
            return template.render(context)
    except FileNotFoundError: raise TemplateNotFoundError(template_file)
    except exceptions.UndefinedError: raise Jinja2ContextDataError
