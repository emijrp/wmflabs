#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2014 emijrp
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import MySQLdb
import sys

query = "SELECT ss_total_edits FROM site_stats WHERE 1"
if len(sys.argv) > 1:
	query = sys.argv[1]

conn = MySQLdb.connect(host='s3.labsdb', db='meta_p', read_default_file='~/replica.my.cnf', use_unicode=True)
cursor = conn.cursor()
cursor.execute("SELECT lang, family, slice, dbname FROM wiki WHERE 1;")
result = cursor.fetchall()
families = [
    "wikibooks", 
    "wikipedia", 
    "wiktionary", 
    "wikimedia", 
    "wikiquote", 
    "wikisource", 
    "wikinews", 
    "wikiversity", 
    "commons", 
    "wikispecies", 
    "wikidata", 
    "wikivoyage"
    ]

for row in result:
    lang = row[0]
    family = row[1]
    if family not in families:
        continue
    dbserver = row[2]
    dbname = row[3]+'_p'
    
    try:
        conn2 = MySQLdb.connect(host=dbserver, db=dbname, read_default_file='~/replica.my.cnf', use_unicode=True)
        cursor2 = conn2.cursor()
        cursor2.execute(query)
        result2 = cursor2.fetchall()
        for row2 in result2:
            edits = int(row2[0])
            print dbname, dbserver, edits

        cursor2.close()
        conn2.close()
    except:
        print "Error in", dbserver, dbname
