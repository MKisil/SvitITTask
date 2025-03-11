import re
from datetime import datetime


class LogParser:
    def __init__(self):
        self.pattern = re.compile(
            r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) '  # timestamp
            r'([A-Z]+)\s+'  # log level
            r'(.+)'  # message
        )

    def parse(self, log_line, user_id):
        match = self.pattern.match(log_line)
        if not match:
            return None

        timestamp_str, level, message = match.groups()
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')

        log_doc = {
            'timestamp': timestamp,
            'level': level,
            'message': message,
            'user_id': user_id
        }

        return log_doc
