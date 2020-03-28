import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import math
import random


def Move(x_limit,y_limit, list_movers, df):
    for i in list_movers:
        if (df.loc[i,'infected']==2) or (df.loc[i,'infected']==4) : 
            list_movers.remove(i)
            
        df.loc[i,'X'], df.loc[i,'Y'] = (df.loc[i,'X']+random.uniform(1,x_limit/3))%x_limit, (df.loc[i,'Y']+random.uniform(1,y_limit/3))%y_limit
        
    return df
        #df.loc[i,'X'], df.loc[i,'Y']=np.random.uniform(0, s, size=(1, 2))

def check(i,j, df, patient_previous, distance_limit):
    try:
        Dist = math.sqrt((df.loc[i,'X']-df.loc[j,'X'])**2+(df.loc[i,'Y']-df.loc[j,'Y'])**2)
        flag = ((patient_previous[i]==1) ^ (patient_previous[j]==1)) and Dist<distance_limit
    except:
        print(type(df))
        print(df)
    
    return flag
    
def interact(Day, df, patient_previous, distance_limit):

    for i in range(len(df)):
        for j in range(i):
            #print('xxx')
            #print(type(df))
            if check(i,j, df, patient_previous, distance_limit):
                if (df.loc[i,'infected']==0) :
                
                    df=infect(i, df, Day)
                    
                else:
                
                    df=infect(j, df, Day)
    return df
                    
                    
def infect(Person, df, Day):

    if random.random()>0.25 and Day>3 : 
        return df
    if df.loc[Person,'infected']==0:
        df.loc[Person,'infected'], df.loc[Person,'Day'] = 1, Day                    
    return df

def kill(df):
    
    #global df
    
    #samplesize = math.floor(len(df[df['Covid-19']==1])*.005+len(df[df['Covid-19']==2])*.005)
    samplesize = math.floor(len(df[df['infected']==1])*.01)
    if samplesize>len(df[df['infected']==1]): 
        return
    df.loc[df[df['infected']==1].sample(n = samplesize).index.values.tolist(),'infected']=4
    return df

def resolve(df, Day):
    #global df, Day
    df.loc[(df['Day']<Day-10) & (df['infected']==1) ,'infected'] = 3
    #df.loc[(df['Day']<Day-21) & (df['Covid-19']==2) ,'Covid-19'] = 3
    return df
    


def Count(Day, df, Stat):
    #global df, Stat
    
    List = list(df['infected'])
    
    Stat.loc[Day,'Healthy'] = List.count(0)
    Stat.loc[Day,'infected'] = List.count(1)    
    Stat.loc[Day,'Cured'] = List.count(3)
    Stat.loc[Day,'Dead'] = List.count(4)
     
    return Stat


x_limit, y_limit=35,35                  
distance_limit = 1.0 # Distance limit for infection event

population=1000

df1 = pd.DataFrame(columns='X,Y,infected,Day'.split(','))
df2 = pd.DataFrame(columns='X,Y,infected,Day'.split(','))

coord=np.random.uniform(0, x_limit, size=(population, 2))
#x=np.random.randint(0, s, size=(n, 2))
df1['infected'] = np.zeros((population), dtype=int)
df1['X'], df1['Y']=coord[:, 0], coord[:, 1]
df2['infected'] = np.zeros((population), dtype=int)
df2['X'], df2['Y']=coord[:, 0], coord[:, 1]

samplesize1 = math.floor(population*0.7)
list_movers1 = df1.sample(n = samplesize1).index.values.tolist() #deffine index of people who are moving around
samplesize2 = math.floor(population*0.03)
list_movers2 = df2.sample(n = samplesize2).index.values.tolist() #deffine index of people who are moving around

Stat1 = pd.DataFrame(columns='Healthy,infected,Cured,Dead'.split(','))
Stat2 = pd.DataFrame(columns='Healthy,infected,Cured,Dead'.split(','))

    
t=60
Day=0


#Patient 0:
p0=random.randrange(population)
df1.iloc[p0, 2]=1
df2.iloc[p0, 2]=1
Stat1=Count(Day, df1, Stat1)
Stat2=Count(Day, df2, Stat2)

patient_previous1 = list(df1['infected'])
patient_previous2 = list(df2['infected'])
ims = []
for i in range(0, t):
    
    Day +=1
    
    df1=kill(df1)
    df1=resolve(df1, Day)
    df2=kill(df2)
    df2=resolve(df2, Day)
    
    df1=Move(x_limit, y_limit, list_movers1, df1)
    df2=Move(x_limit, y_limit, list_movers2, df2)
    
    
    df1=interact(Day, df1, patient_previous1, distance_limit)
    df2=interact(Day, df2, patient_previous2, distance_limit)
    
    Stat1=Count(Day, df1, Stat1)
    patient_previous1 = list(df1['infected'])
    
    Stat2=Count(Day, df2, Stat2)
    patient_previous2 = list(df2['infected'])
    
    
    healthy_loc1=df1.loc[df1['infected']==0]
    sick_loc1=df1.loc[df1['infected']==1]
    hosp_loc1=df1.loc[df1['infected']==2]
    Cured_loc1=df1.loc[df1['infected']==3]
    
    healthy_loc2=df2.loc[df2['infected']==0]
    sick_loc2=df2.loc[df2['infected']==1]
    hosp_loc2=df2.loc[df2['infected']==2]
    Cured_loc2=df2.loc[df2['infected']==3]
    
    fig = plt.figure()
    plt.subplot(221)
    plt.scatter(healthy_loc1['X'], healthy_loc1['Y'], 2, 'b')
    plt.scatter(sick_loc1['X'], sick_loc1['Y'], 2, 'r')
    plt.scatter(Cured_loc1['X'], Cured_loc1['Y'], 2, 'g')
    plt.xticks([])
    plt.yticks([])
    plt.title('Standard')
    
    plt.subplot(222)
    plt.scatter(healthy_loc2['X'], healthy_loc2['Y'], 2, 'b')
    plt.scatter(sick_loc2['X'], sick_loc2['Y'], 2, 'r')
    plt.scatter(Cured_loc2['X'], Cured_loc2['Y'], 2, 'g')
    plt.xticks([])
    plt.yticks([])
    plt.title('Movement restriction')
    
    plt.subplot(223)
    plt.plot(Stat1.index, Stat1['Healthy'], 'b')
    plt.plot(Stat1.index, Stat1['infected'], 'r')
    plt.plot(Stat1.index, Stat1['Dead'], 'k')
    plt.plot(Stat1.index, Stat1['Cured'], 'g')
    
    plt.legend(['Susceptible', 'Infectious', 'Dead', 'Recovered'])
    
    plt.subplot(224)
    plt.plot(Stat2.index, Stat2['Healthy'], 'b')
    plt.plot(Stat2.index, Stat2['infected'], 'r')
    plt.plot(Stat2.index, Stat2['Dead'], 'k')
    plt.plot(Stat2.index, Stat2['Cured'], 'g')
    
    plt.legend(['Susceptible', 'Infectious', 'Dead', 'Recovered'])
    
    #data=np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    fig.canvas.draw()
    #data=np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    data=np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    #plt.show()
    
    ims.append(data)
    plt.clf()
    plt.cla()

from moviepy.editor import ImageSequenceClip #Somehow doesn't work if put at the top, possible conflict with matplotlib

clip = ImageSequenceClip(ims, fps=3)
clip.write_gif('simulation.gif', fps=3)
clip.write_videofile('simulation.mp4', fps=3) 
   