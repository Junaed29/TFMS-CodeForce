from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class MaximumLengthValidator:
    def __init__(self, max_length=16):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(
                _("This password must contain at most %(max_length)d characters."),
                code='password_too_long',
                params={'max_length': self.max_length},
            )

    def get_help_text(self):
        return _(
            "Your password must contain at most %(max_length)d characters."
            % {'max_length': self.max_length}
        )

class AlphanumericValidator:
    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            raise ValidationError(
                _("This password must contain at least one letter and one number."),
                code='password_no_alphanumeric',
            )

    def get_help_text(self):
        return _("Your password must contain at least one letter and one number.")
