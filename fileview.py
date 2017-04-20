from view import View
from glob import glob
import os


class FileView(View):
    def __init__(self):
        super(View, self).__init__()

    def get(self, line):
        """
        >>> file_list = FileView().get('')
        ['data.txt', 'data2.txt', 'data3.txt', 'datalist.txt', 'file.txt']
        >>> file_list[0]
        'empid=D011\\ngender=m\\nage=29\\nsales=722\\nbmi=normal\\nsalary=320\\nbirthday=23-11-1987'
        """
        if line:
            flag = line.split()
            if flag[0] == 'cwd':
                print(os.getcwd())
                contents = os.listdir(os.getcwd())
                for item in contents:
                    if item[-4:] != '.txt' and item[-3:] != '.py' and item[-3:] != '.db':
                        print(item)
            elif len(flag) == 1:
                try:
                    directory = './' + line
                    os.chdir(directory)
                    print(os.getcwd())
                except Exception as e:
                    print('fview:', e)
        else:
            raw_file_list = []
            filename_list = glob('*.txt')
            print(filename_list)
            for file in filename_list:
                with open(file, 'r') as f:
                    contents = f.read()
                    data_sets = contents.split("\n\n")
                    for data_set in data_sets:
                        raw_file_list.append(data_set)
            return raw_file_list

    def set(self, **kwargs):
        # TODO: write data to file?
        pass

if __name__ == '__main__':
    import doctest

    doctest.testmod()
