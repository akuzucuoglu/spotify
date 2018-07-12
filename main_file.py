# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 16:36:21 2018

@author: ahmet.kuzucuoglu
"""

#1. Build the connection
import cx_Oracle
dsn_tns = cx_Oracle.makedsn('IDB-10256.roketsan.com.tr', '1521', service_name='XE')
conn = cx_Oracle.connect(user='HR', password='HR', dsn=dsn_tns)


#2. SQL: Insertion
#insert edilecek row'lar rows listesine eklenir.
rows = [ (1, 1,'first asdasd isa K' ),
         (2, 2,'second' ),
         (3, 3,'third'),
         (4, 4,'fourth') ]

#Insertion işlemi için cursor açılır ve işlem gerçekleştirilir.
cur_insert = conn.cursor()
cur_insert.bindarraysize = 4
cur_insert.setinputsizes(int, 4000)
cur_insert.executemany("INSERT INTO xx_ahmet(id1,id2,data) VALUES(:1,:2,:3)", rows)
cur_insert.close()
conn.commit()

# Now query the results back
cur_select = conn.cursor()
cur_select.execute('select * from xx_ahmet')
res = cur_select.fetchall()
print(res)               
cur_select.close()

print('hello')

rows
my_RowList
