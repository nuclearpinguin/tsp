import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from random import randint
import math
from itertools import permutations
import random
import os

CURRENT_PATH = os.getcwd()
COORDS_FILE_NAME ="cities.csv"
TIMES_FILE_NAME = "paths.csv"
WORKTIME_FILE_NAME = "time.csv"
NEIGHBOURS_TABLE_FILE_PATH ="neighbours_table2.csv"
CITIES_NUMBER = 600

def is_neighbour(row1,row2):
    if (row1[1] == row2[1] and abs(int(row1[2]) - int(row2[2])) == 1) or \
       (row1[2] == row2[2] and abs(int(row1[1]) - int(row2[1])) == 1):
        return 1.0
    return 0.0

def generate_random_times(neighbours_table):
    rows = np.array([1,2,3])
    city_names = []
    for i in range(len(neighbours_table)):
        city_names.append("Miasto_"+str(i))
    for i in range(len(city_names)):
        name1 = city_names[i]
        for j in range(i+1,len(city_names)):
            name2 = city_names[j]
            if neighbours_table[i][j] == 1.0:
                rows = np.vstack((rows,[name1,name2,randint(1, 18)]))
    rows = np.delete(rows, (0), axis=0)
    df_to_save2 = pd.DataFrame(data=rows, columns=["city_from","city_to","time"])
    df_to_save2.to_csv(TIMES_FILE_NAME,sep=',',index = False)
    
def generate_neighbours_table(array):
    neighbours_table = np.zeros((array.shape[0],array.shape[0]))
    for i in range(len(array)):
        row1 = array[i]
        for j in range(i,len(array)):
            row2 = array[j]
            neighbours_table[i][j] = is_neighbour(row1,row2)
    # columns = list(row[0] for row in array)
    # df_to_save = pd.DataFrame(data=neighbours_table, index=columns,columns=columns)
    # df_to_save.to_csv(NEIGHBOURS_TABLE_FILE_PATH ,sep=',')
    return neighbours_table
               
def generate_coordinates_table(cities_no):
    rows = np.array([0,0,"String",0])
    city_names = []
    for i in range(cities_no):
        city_names.append("Miasto_"+str(i))
    dims = list(i for i in range(math.ceil(math.sqrt(cities_no))))
    coords = get_all_permutations(dims)
    random.shuffle(coords)
    i = 0
    for coord in coords:
        if i >= len(city_names):
            break
        rows = np.vstack((rows,[city_names[i],coord[0],coord[1],randint(1, 18)]))
        i += 1
    rows = np.delete(rows, (0), axis=0)
    df_to_save = pd.DataFrame(data=rows,columns=["city_name","x","y","quantity"])
    df_to_save.to_csv(COORDS_FILE_NAME ,sep=',',index = False)
    return rows
                
def get_all_permutations(dims):
    perm = []
    for i in dims:
        for j in dims:
            perm.append((i,j))
    return perm        


def generate_worktime (high):
  worktime=[]
  worktime.append(randint(20,high))
  df_to_save = pd.DataFrame(data=worktime,columns=["time"])
  df_to_save.to_csv(WORKTIME_FILE_NAME ,sep=',',index = False)
  return worktime



coordinates = generate_coordinates_table(88)
neighbours_table = generate_neighbours_table(coordinates)
generate_random_times(neighbours_table)
generate_worktime(101)