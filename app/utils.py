from flask import url_for
from wtforms.fields import Field
from wtforms.widgets import HiddenInput
from wtforms.compat import text_type

def register_template_utils(app):
    """Register Jinja 2 helpers (called from __init__.py)."""

    @app.template_test()
    def equalto(value, other):
        return value == other

    @app.template_global()
    def is_hidden_field(field):
        from wtforms.fields import HiddenField
        return isinstance(field, HiddenField)

    app.add_template_global(locale)
    app.add_template_global(index_for_role)

def locale(tag):
        from app.wakkerdam.models.constants.Localization import Localization
        from flask_login import current_user

        # @returns text for tag with CU's language, else English
        if current_user.is_authenticated:
            language = current_user.getLanguage()
        else:
            language = "en_US"
        localization = Localization.query.filter_by(tag=tag, language=language).first()
        if localization == None:
            raise Exception(f"Text could not be found for tag: {tag} and language: {language}")
        return localization.text

def index_for_role(role):
    return url_for(role.index)


class CustomSelectField(Field):
    widget = HiddenInput()

    def __init__(self, label='', validators=None, multiple=False,
                 choices=[], allow_custom=True, **kwargs):
        super(CustomSelectField, self).__init__(label, validators, **kwargs)
        self.multiple = multiple
        self.choices = choices
        self.allow_custom = allow_custom

    def _value(self):
        return text_type(self.data) if self.data is not None else ''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist[1]
            self.raw_data = [valuelist[1]]
        else:
            self.data = ''
