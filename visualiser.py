import pygal


# TODO: would be nice to build titles in a separate function!
class Visualiser(object):
    def __init__(self):
        self.__charts = {'-b': pygal.Bar(),
                         '-l': pygal.Line(),
                         '-p': pygal.Pie(),
                         '-r': pygal.Radar()}

    def display_chart(self, arg, data):
        obj = self.__charts[arg]
        chart = self.build_chart(obj, data)
        chart.render_in_browser()

    def build_chart(self, obj, data):
        chart = obj
        title_builder = []
        for key, data_list in data.items():
            title_builder.append(key + ' vs ')
            chart.add(key, data_list)
            chart.title = ''.join(title_builder)[:-4]
        return chart

    def is_valid_flag(self, input_param):
        result = False
        if input_param in self.__charts:
            result = True
        return result
