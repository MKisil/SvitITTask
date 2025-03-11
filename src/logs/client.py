from fastapi import UploadFile, Depends
from sqlalchemy.orm import Session
import magic

from src.config import settings
from src.database import get_db
from src.logs.elastic import ElasticsearchClient
from src.logs.file_processors import TextFileProcessor, ZipFileProcessor
from src.logs.parser import LogParser


class LogClient:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.es_client = ElasticsearchClient()
        self.log_parser = LogParser()

    def process_upload(self, file: UploadFile, user_id: int):
        mime = magic.Magic(mime=True)
        content = file.file.read(1024)
        content_type = mime.from_buffer(content)
        file.file.seek(0)

        processor = self._get_processor(content_type)
        log_lines = processor.process(file.file)

        print(log_lines)

        parsed_logs = []
        for line in log_lines:
            parsed_log = self.log_parser.parse(line, user_id)
            if parsed_log:
                parsed_logs.append(parsed_log)

        if parsed_logs:
            self.es_client.index_logs(parsed_logs)

    def _get_processor(self, content_type: str):
        if content_type == 'text/plain':
            return TextFileProcessor()
        elif content_type == 'application/zip':
            return ZipFileProcessor()
        else:
            raise ValueError("Unsupported file type")

    def search_user_logs(self, user_id, start_time=None, end_time=None, keyword=None, level=None):
        return self.es_client.search_user_logs(
            user_id=user_id,
            start_time=start_time,
            end_time=end_time,
            keyword=keyword,
            level=level
        )
