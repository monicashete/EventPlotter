#!usr/bin/python

import MySQLdb
from collections import defaultdict


class Database:

    def __init__(self, name):
        self._connect = MySQLdb.connect(
            user='root', host='localhost', database=name)
        self._cursor = self._connect.cursor()

    def db_read(self, query):
        self._cursor.execute(query)
        data = self._cursor.fetchall()
        return data

    def db_write(self, sql, val):
        self._cursor.execute(sql, val)
        self._connect.commit()

    def db_close(self):
        self._connect.close()


class DataParser:

    def __init__(self, db):
        self.db_obj = db
        self.user_dict = defaultdict(list)
        self.intrvl_user_dict = defaultdict(list)
        self.event_dict = defaultdict(list)

    def populate_interval_dict(self, id, date_time):
        if (date_time.hour <= 12):
            interval = date_time.hour
            self.intrvl_user_dict[interval].append(
                (str(id), str(date_time.time())))
            if (date_time.minute >= 40):
                self.intrvl_user_dict[interval +
                                      1].append((str(id), str(date_time.time())))
        else:
            interval = date_time.hour - 12
            self.intrvl_user_dict[interval].append(
                (str(id), str(date_time.time())))
            if (date_time.minute >= 40 and date_time.hour != 23):
                #print ("MON: hour: "+ str(date_time.hour) + " id "+ str(id) + "time: " + str(date_time.time()))
                self.intrvl_user_dict[interval +
                                      1].append((str(id), str(date_time.time())))

    def print_event_dict(self):

        print("Printing raw event data: ")
        for id, val in self.event_dict.items():
            print ("id: " + str(id) + "     date: " + str(val))

        print("Printing processed interval based event data: ")
        for interval, data in sorted(self.intrvl_user_dict.items()):
            print ("int: " + str(interval), data)



    def get_events_data(self, date):
        query = "select product_id,disruption_date from \
                    network_disruptions where disruption_date like '%" + date + "%'"

        event_rows = self.db_obj.db_read(query)

        for row in event_rows:
            #data is tuple
            self.event_dict[row[0]].append(row[1])
            # populate interval dict with interval<--->(id,time) for a date
            self.populate_interval_dict(row[0], row[1])

        return

    def build_event_plot_list(self, x_list, y_list):
        # create a list of intervals and corresponding counts
        # sort interval keys
        for interval, data in sorted(self.intrvl_user_dict.items()):
            x_list.append(interval)
            y_list.append(len(data))

        return

    def fill_users(self):
        self.db_obj._cursor.execute(
            "SELECT user_id,login_date FROM user_activity")
        user_rows = self.db_obj._cursor.fetchall()
        #data is tuple
        for row in user_rows:
            self.user_dict[row[0]] = row[1]
        return
