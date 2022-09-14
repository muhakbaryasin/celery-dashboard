import linecache
import os
from models.ClientConfigManager import ClientConfigManager


class LogManager(object):
    def __init__(self, client_name):
        self.client_name = client_name

    @staticmethod
    def _count_generator(reader):
        b = reader(1024 * 1024)
        while b:
            yield b
            b = reader(1024 * 1024)

    @staticmethod
    def count_total_lines(file_):
        with open(file_, 'rb') as fp:
            c_generator = LogManager._count_generator(fp.raw.read)
            count = sum(buffer.count(b'\n') for buffer in c_generator)
            return count + 1

    @staticmethod
    def get_list_of_dir(dir_, ext=None, need_full_path=True):
        if dir_[-1] != '/':
            dir_ = dir_ + '/'

        res = []

        for file_name in os.listdir(dir_):
            file_ = (dir_ + file_name) if need_full_path else file_name
            if ext is None:
                res.append(file_)
            elif file_name.endswith(ext):
                res.append(file_)

        return res

    def get_list(self, need_full_path=True):
        base_dir = ClientConfigManager(self.client_name).project_base_dir
        res = LogManager.get_list_of_dir(base_dir, ext='.log', need_full_path=need_full_path)
        dir_ = base_dir + '/conf_xml'
        res += LogManager.get_list_of_dir(dir_, ext='.xml', need_full_path=need_full_path)
        dir_ = base_dir + '/temp'
        res += LogManager.get_list_of_dir(dir_, need_full_path=need_full_path)

        return res

    def get_total_lines_of(self, index):
        file_ = self.get_file_name(index)

        return LogManager.count_total_lines(file_)

    def get_file_name(self, index):
        return self.get_list()[index]

    def read_content(self, index, line_end_no=None):
        file_name = self.get_file_name(index)

        if line_end_no is None:
            line_end_no = self.get_total_lines_of(index)

        lines_start_no = 0 if line_end_no - 50 < 0 else line_end_no - 50

        lines = ""
        for x in range(lines_start_no, line_end_no):
            lines += linecache.getline(file_name, x)
        return lines

    def tail_file(self, index, nlines):
        file_name = self.get_file_name(index)

        with open(file_name) as qfile:
            qfile.seek(0, os.SEEK_END)
            endf = position = qfile.tell()
            linecnt = 0

            while position >= 0:
                qfile.seek(position)
                next_char = qfile.read(1)
                if next_char == "\n" and position != endf - 1:
                    linecnt += 1

                if linecnt == nlines:
                    break
                position -= 1

            if position < 0:
                qfile.seek(0)

            return qfile.read()
