import linecache
import os


class LogManager(object):
    @staticmethod
    def get_list_of_dir(dir_, ext=None):
        res = []

        for file_name in os.listdir(dir_):
            if ext is None:
                res.append(file_name)
            elif file_name.endswith(ext):
                res.append(file_name)

        return res

    @staticmethod
    def get_list():
        dir_ = './'
        res = LogManager.get_list_of_dir(dir_, ext='.log')
        dir_ = './conf_xml'
        res += LogManager.get_list_of_dir(dir_, ext='.xml')
        dir_ = './temp'
        res += LogManager.get_list_of_dir(dir_)

        return res

    @staticmethod
    def get_file_name(index):
        return LogManager.get_list()[index]

    @staticmethod
    def read_content(index, counter=0):
        file_name = LogManager.get_file_name(index)

        lines = []
        for x in range(counter*50, (counter+1)*50):
            lines.append(linecache.getline(file_name, x))
        return "\n".join(lines)

    @staticmethod
    def tail_file(index, nlines):
        file_name = LogManager.get_file_name(index)

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

            print(qfile.read(), end='')
