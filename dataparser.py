class DataParser(object):
    """
    >>> parse = DataParser()
    >>> file_str = "empid=D011\\ngender=M\\nage=29"
    >>> parse.parse_raw_data(file_str)
    >>> d_d = parse.get_data()
    >>> d_d[0]['empid']
    'D011'
    """
    def __init__(self):
        self.__data_dicts = []

    # depricated
    def get_data(self):
        return self.__data_dicts

    def parse_raw_data(self, file_str):
        data_list = self._to_list(file_str)
        data_dict = self._to_dict(data_list)
        self.__data_dicts.append(data_dict)

    def _to_list(self, file_str):
        """
        >>> DataParser()._to_list("empid=D011\\ngender=M\\nage=29")
        ['empid=D011', 'gender=M', 'age=29']
        """
        data_list = file_str.split()
        return data_list

    def _to_dict(self, data_list):
        """
        >>> x = DataParser()._to_dict(['empid=D011', 'gender=M', 'age=29'])
        >>> x['age']
        '29'
        """
        data_dict = dict(pair.split('=') for pair in data_list)
        return data_dict

    def scrub_db_list(self, db_list):
        """
        >>> DataParser().scrub_db_list([(14,), (25,)])
        [14, 25]
        """
        clean_list = []
        for item in db_list:
            clean_list.append(item[0])
        return clean_list

if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
