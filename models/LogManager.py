import linecache
import os
from models.ClientConfigManager import ClientConfigManager


class LogManager(object):
    def __init__(self, client_name):
        self.client_name = client_name

    @staticmethod
    def get_list_of_dir(dir_, ext=None):
        res = []

        for file_name in os.listdir(dir_):
            if ext is None:
                res.append(file_name)
            elif file_name.endswith(ext):
                res.append(file_name)

        return res

    def get_list(self):
        base_dir = ClientConfigManager(self.client_name).project_base_dir
        res = LogManager.get_list_of_dir(base_dir, ext='.log')
        dir_ = base_dir + '/conf_xml'
        res += LogManager.get_list_of_dir(dir_, ext='.xml')
        dir_ = base_dir + '/temp'
        res += LogManager.get_list_of_dir(dir_)

        return res

    def get_file_name(self, index):
        return self.get_list()[index]

    def read_content(self, index, counter=0):
        file_name = self.get_file_name(index)

        lines = []
        for x in range(counter*50, (counter+1)*50):
            lines.append(linecache.getline(file_name, x))
        return "\n".join(lines)

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
