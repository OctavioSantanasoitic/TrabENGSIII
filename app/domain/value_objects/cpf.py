import re


class Cpf:

    def __init__(self, cpf) -> None:
        self.cpf_raw = cpf
        self.cpf = Cpf.parse(cpf) \
            if Cpf.validate(cpf) \
            else None

    @classmethod
    def parse(cls, value: str):
        return ''.join(re.findall(r'\d', str(value or '')))

    def format(self):
        if not self.cpf:
            return None
        return '{}.{}.{}-{}'.format(self.cpf[:3], self.cpf[3:6], self.cpf[6:9], self.cpf[9:])

    def to_str(self):
        return self.cpf

    @classmethod
    def validate(cls, cpf: str):
        cpf_numbers = Cpf.parse(cpf)
        if len(cpf_numbers) != 11:
            return False

        unique_characters = set(cpf_numbers)
        if len(unique_characters) < 2:
            return False

        return True
