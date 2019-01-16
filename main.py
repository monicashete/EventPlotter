import db_connect as dbConnect
import plot
import argparse

def db_init(name):
    db_obj = dbConnect.Database(name)
    db_parser = dbConnect.DataParser(db_obj)

    return db_parser


def plot_events(db_parser, date, x_label, y_label, title):
    x_list = list()
    y_list = list()

    db_parser.get_events_data(date)
    db_parser.build_event_plot_list(x_list, y_list)

    p_obj = plot.PlotGraph(x_list, y_list)
    p_obj.name_plot(x_label, y_label, title)
    p_obj.plot_graph()

    return


def main():

    db_parser = db_init('graphData')
    plot_events(db_parser, '2015-02-13', "disruption intervals",
                "number of events", "hours vs disruption frequency")

    return


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Plot data for disruption \
             events for a particular date')
    main()
