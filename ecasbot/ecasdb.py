#!/usr/bin/python3
# coding=utf-8

import sqlite3


class ASDbClass:
    def adduser(self, userid, joindate):
        # Attaching to database...
        con = sqlite3.connect(self.DbName)
        cs = con.cursor()

        # Add new user to our database...
        cs.execute('INSERT INTO as_users (NN, UserID, JoinDate, MsgCount) VALUES (NULL, ?, ?, ?)', (userid, joindate, '0'))

        # Write to database...
        con.commit()

        # Close connection...
        con.close()

    def __init__(self, dbn):
        self.DbName = dbn
