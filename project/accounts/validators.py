from django.core.exceptions import ValidationError


class ContainSymbolsValidator(object):
    def __init__(self, symbols: str, min_digits: int = 0):
        self.symbols = symbols
        self.min_digits = min_digits

    def validate(self, password: str, user=None):
        if sum(password.count(sym) for sym in self.symbols) < self.min_digits:
            raise ValidationError(
                f"The password must contain at least {self.min_digits} symbols: {self.symbols}",
                code='password_no_symbol',
            )

    def get_help_text(self):
        return f"Your password must contain at least {self.min_digits} symbols: {self.symbols}"
