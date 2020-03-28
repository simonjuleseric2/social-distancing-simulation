import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import math
import random


def Move_around(x_limit,y_limit, list_movers, df):

    for i in list_movers:
        if (df.loc[i,'infected']==2) or (df.loc[i,'infected']==4) : 
            list_movers.remove(i)
            
        df.loc[i,'X'], df.loc[i,'Y'] = (df.loc[i,'X']+random.uniform(1,x_limit/4))%x_limit, (df.loc[i,'Y']+random.uniform(1,y_limit/4))%y_limit
        
    return df
        #df.loc[i,'X'], df.loc[i,'Y']=np.random.uniform(0, s, size=(1, 2))

def get_range(x1, y1, x2, y2):
    Dist = math.sqrt((x1-x2)**2+(y1-y2)**2)
    return Dist

def interaction(Day, df, patient_previous, distance_limit, R_I):
    succeptibles=df.loc[df['infected']==0]
    infected=df.loc[df['infected']==1]
    for i in succeptibles.index:
        x1, y1=succeptibles.loc[i,'X'], succeptibles.loc[i,'Y']
        for j in infected.index:
            x2, y2=infected.loc[j,'X'], infected.loc[j,'Y']
            distance_xy=get_range(x1, y1, x2, y2)
            if distance_xy<distance_limit:
                df, status=infect(i, df, Day, R_I)
                if status==1:
                    break # Avoid more unnecessary calculation if target already infected
                         
    return df
                    

                    
def infect(Person, df, Day, R_I):
    if random.random()<R_I and Day>3 and df.loc[Person,'infected']==0:
        status=1
        df.loc[Person,'infected'] = status
        df.loc[Person,'Day']=Day
    else:
        status=0
            
    return df, status


def kill(df):
    #samplesize = math.floor(len(df[df['Covid-19']==1])*.005+len(df[df['Covid-19']==2])*.005)
    samplesize = math.floor(len(df[df['infected']==1])*.01)
    if samplesize>len(df[df['infected']==1]): 
        return
    df.loc[df[df['infected']==1].sample(n = samplesize).index.values.tolist(),'infected']=4
    return df

def resolve(df, Day):
    df.loc[(df['Day']<Day-10) & (df['infected']==1) ,'infected'] = 3
    #df.loc[(df['Day']<Day-21) & (df['Covid-19']==2) ,'Covid-19'] = 3
    return df
    


def Count(Day, df, Stat):
    
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
samplesize2 = math.floor(population*0.10)
list_movers2 = df2.sample(n = samplesize2).index.values.tolist() #deffine index of people who are moving around

Stat1 = pd.DataFrame(columns='Healthy,infected,Cured,Dead'.split(','))
Stat2 = pd.DataFrame(columns='Healthy,infected,Cured,Dead'.split(','))

    
t=60
Day=0
R_I=0.4 #Infection Rate

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
    
    df1=Move_around(x_limit, y_limit, list_movers1, df1)
    df2=Move_around(x_limit, y_limit, list_movers2, df2)
    
    
    df1=interaction(Day, df1, patient_previous1, distance_limit, R_I)
    df2=interaction(Day, df2, patient_previous2, distance_limit, R_I)
    
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
    plt.xlabel('Days')
    plt.ylabel('Cases')
    
    plt.legend(['Susceptible', 'Infectious', 'Dead', 'Recovered'])
    
    plt.subplot(224)
    plt.plot(Stat2.index, Stat2['Healthy'], 'b')
    plt.plot(Stat2.index, Stat2['infected'], 'r')
    plt.plot(Stat2.index, Stat2['Dead'], 'k')
    plt.plot(Stat2.index, Stat2['Cured'], 'g')
    plt.xlabel('Days')
    plt.ylabel('Cases')
    
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
   