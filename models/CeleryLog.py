import hashlib
import os


class CeleryLog(object):
    @staticmethod
    def message_hash(text):
        return hashlib.md5(text.encode()).hexdigest()

    @staticmethod
    def get_logs(start=0, end=9):
        file_name = 'celery.log'

        if not os.path.exists('./' + file_name) or os.path.getsize('./' + file_name) == 0:
            return None

        with open('./' + file_name, "r+", encoding="utf-8") as file:
            file.seek(0, os.SEEK_END)
            chars_num = file.tell()
            pos = 0
            file.seek(0, os.SEEK_END)
            chars_num = file.tell()
            pos = 0

            while True:
                file.seek(pos, os.SEEK_SET)
                line = (file.readline())
                pos += len(line)

                if pos >= chars_num:
                    break

            while True:
                file.seek(pos, os.SEEK_SET)
                line = (file.readline())
                pos += len(line)

                if pos >= chars_num:
                    break
