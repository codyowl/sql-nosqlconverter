import json
import MySQLdb
import pymongo
from pymongo import MongoClient
import os
from collections import OrderedDict


username = raw_input("Enter Your Mysql Username :")

passwd = raw_input("Enter Your Mysql Password :")

db = raw_input("Enter Your Mysql database name :")

table = raw_input("Enter Your Mysqt table name :")

db_connect = MySQLdb.connect(user=username, passwd=passwd, db=db)

cursor = db_connect.cursor()

#for getting column name
query = "SELECT * FROM %s" % table
cursor.execute(query)

column_name = [i[0] for i in cursor.description]

print column_name


query2 = "SELECT * FROM %s;" % (table)
cursor.execute(query2)
fetcher = cursor.fetchall()

print "printing from the fetcher"
print fetcher
result = []

#appending dict values to result by filtering null values
for row in fetcher:
	row = dict(zip(column_name, row))
	row = { key:value for key,value in row.items() if ( key in column_name and ( value != None ) or key not in column_name )}
	result.append(row)
    	
#print result
print "printing from result"


jsondumper = json.dumps(result, indent=4)

#print jsondumper

#writing it to json file

filename = ("%s.json") % (table)

fileopener = open(filename, 'w')
fileopener.write(jsondumper)
fileopener.close()
db_connect.close()
print "Done !!  your mysql db has been converted into a json file"

print "######################################################"

print "-------------------------------------------------------"
print "Converting to Mongodb....."

mongo_db_name = raw_input("Enter Your MongodbName :")
mongo_collection_name = raw_input("Enter Your Collection Name :")

importcommand = "mongoimport --db" + " " +  mongo_db_name + " --collection" + " " + mongo_collection_name + " --type json" + " --file" + " " + filename  + " --jsonArray"

print importcommand
os.system(importcommand)

print "Your Db " + mongo_db_name + " has been migrated at " + mongo_db_name + "!" 

 





