class Serializer(object):

    def serialize(self, line, db_contents):
        try:
            import pickle
            args = line.split()
            if len(args) == 1 and args[0] != '-r':
                # write
                filename = args[0] + '.pickle'
                if db_contents:
                    with open(filename, 'wb') as p_file:
                        pickle.dump(db_contents, p_file)
                    print('-- Database pickled!\n\t-> as filename: {}.'.format(filename))
                else:
                    raise Exception('* Database is empty. Nothing to serialize.')
            elif len(args) == 2 and args[0] == '-r':
                # read
                filename = args[1] + '.pickle'
                try:
                    with open(filename, 'rb') as p_file:
                        data = pickle.load(p_file)
                    output = "\n".join(str(i) for i in data)
                    print(output)
                except Exception as e:
                    print(e)
            else:
                raise Exception("* Invalid parameters.\n-- Type 'help serialize' for more details.")
        except Exception as e:
            print(e)