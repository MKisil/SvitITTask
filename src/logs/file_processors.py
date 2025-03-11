import zipfile
from io import BytesIO
from abc import ABC, abstractmethod


class FileProcessor(ABC):
    @abstractmethod
    def process(self, file) -> list:
        pass


class TextFileProcessor(FileProcessor):
    def process(self, file):
        content = file.read()
        return content.decode().splitlines()


class ZipFileProcessor(FileProcessor):
    def process(self, file):
        logs = []
        with zipfile.ZipFile(BytesIO(file.read())) as zf:
            for filename in zf.namelist():
                with zf.open(filename) as f:
                    logs += f.read().decode().splitlines()
        return logs
