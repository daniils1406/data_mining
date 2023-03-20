import re
import whois
from courlan import check_url
import psycopg2
from psycopg2 import OperationalError
from telethon import TelegramClient
from telethon.tl.types import Channel
from urllib.parse import urlparse
import collections
import matplotlib 
from matplotlib import pyplot as plt 

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt



postgres_name = 'vk'
postgres_user = 'postgres'
postgres_password = 'Landrover2013'
postgres_host = '127.0.0.1'
postgres_port = '5432'


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connect = None
    try:
        connect = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connect



connection = create_connection(postgres_name, postgres_user, postgres_password, postgres_host, postgres_port)

G = nx.Graph()
connection.autocommit = True
cursor = connection.cursor()
cursor.execute(f"SELECT DISTINCT vkuser FROM friends;")
fromPoint = cursor.fetchall()

matrix=[0]*len(fromPoint)
for i in range (len(fromPoint)):
     matrix[i]=[0]*len(fromPoint)

for i in range(len(fromPoint)):
    G.add_node(fromPoint[i][0])
    cursor.execute(f"SELECT friend FROM friends WHERE vkuser='{fromPoint[i][0]}';")
    toPoint=cursor.fetchall()
    value=1/len(toPoint)
    for j in range (len(toPoint)):
        if(toPoint[j] in fromPoint):
                G.add_edge(fromPoint[i][0],toPoint[j][0])
                matrix[fromPoint.index(toPoint[j])][i]=value
        



vector=[1/len(fromPoint)]*len(fromPoint)

U0=np.array(vector)



U_past_has_alpha = []
while True:
    vector = 0.8 * (np.dot(matrix, vector)) + 0.2 * U0
    # print('Un: ', U)
    if str(vector) == str(U_past_has_alpha):
        break
    U_past_has_alpha = vector
# print('Un converge to: ', vector)
for i in range (len(vector)):
     print(vector[i],fromPoint[i][0])
     cursor.execute(f"INSERT INTO data VALUES ({vector[i]},{fromPoint[i][0]})")


nx.draw(G, with_labels=1, node_color='g')
plt.show()