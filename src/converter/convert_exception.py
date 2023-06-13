class ConvertException(Exception):
    def __init__(self, file_format: str):
        self.msg = f"Format {file_format.upper()} unsupported"

    def __str__(self):
        return self.msg
