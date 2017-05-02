import pygal


# TODO: would be nice to build titles in a separate function!
class Visualiser(object):
    def __init__(self):
        self.__funcs = {'-b': lambda x: self.display_bar(x),
                        '-l': lambda x: self.display_line(x),
                        '-p': lambda x: self.display_pie(x),
                        '-r': lambda x: self.display_radar(x)}
        # self.__objs = {'-b': BarVisualiser(),
        #                 '-l': BarVisualiser(),
        #                 '-p': BarVisualiser(),
        #                 '-r': BarVisualiser()}

    def display_chart(self, input_param, data_set_dict):
        self.__funcs[input_param](data_set_dict)
        # self.__objs[input_param].display('x')

    def display_bar(self, data_dict):
        title_builder = []
        title = ""
        bar_chart = pygal.Bar()
        for key, data_list in data_dict.items():
            title_builder.append(key + ' vs ')
            title = ''.join(title_builder)
            bar_chart.add(key, data_list)
        bar_chart.title = title[:-4]
        bar_chart.render_in_browser()  # opens default web browser

    def display_line(self, data_dict):
        title_builder = []
        title = ""
        line_chart = pygal.Line()
        for key, data_list in data_dict.items():
            title_builder.append(key + ' vs ')
            title = ''.join(title_builder)
            line_chart.add(key, data_list)
        line_chart.title = title[:-4]
        line_chart.render_in_browser()

    def display_pie(self, data_dict):
        title_builder = []
        title = ""
        pie_chart = pygal.Pie()
        for key, data_list in data_dict.items():
            title_builder.append(key + ' vs ')
            title = ''.join(title_builder)
            pie_chart.add(key, data_list)
        pie_chart.title = title[:-4]
        pie_chart.render_in_browser()

    def display_radar(self, data_dict):
        title_builder = []
        title = ""
        radar_chart = pygal.Radar()
        for key, data_list in data_dict.items():
            title_builder.append(key + ' vs ')
            title = ''.join(title_builder)
            radar_chart.add(key, data_list)
        radar_chart.title = title[:-4]
        radar_chart.render_in_browser()
