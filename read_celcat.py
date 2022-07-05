import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

from matplotlib.ticker import FormatStrFormatter


## SUPPLY
df_tec_supply=pd.read_csv("./data/tec_supply.csv",encoding='utf-8',delimiter=';')
df_tec=pd.read_csv("./data/tec1.csv",encoding='utf-8',delimiter=';')

dfplot = pd.DataFrame({'Counts': df_tec_supply.Counts.values,'Counts_back': df_tec_supply.Counts_back.values}, index=df_tec_supply.Time)

fig, ax=plt.subplots(tight_layout=True)
dfplot.plot.bar(figsize=(15,8),width=0.6, ax=ax)
#ax.plot(dfplot.Counts)
#ax.plot(dfplot.Counts_back)
ax.grid(True, lw=0.1)

#plt.subplots_adjust(bottom=0.20)
#ax.set_xticks()
ax.legend(['De CV vers ST','De ST vers CV'])
ax.set_xlabel('Temps')
ax.set_ylabel('Capacité bus')
ax.set_title('Offre TEC')

#fig.savefig("./results/offre_TEC.pdf")
fig.savefig("./results/offre_TEC.jpg", bbox_inches='tight', dpi=400)


## DEMAND
bins = pd.IntervalIndex.from_tuples([(7*60+30, 8*60), (8*60, 8*60+15), (8*60+15, 8*60+30),(8*60+30, 8*60+45),(8*60+45,9*60),(9*60,9*60+15)],dtype='interval[int32]')

# cbins per 15 mins and per hour
cbins=np.array([7*60+30,8*60,8*60+15,8*60+30,8*60+45,9*60,9*60+15])

supply=np.zeros((bins.shape[0],))
cc=pd.cut(df_tec.time_adjusted, bins)
df_tec['span']=pd.cut(df_tec.time_adjusted, bins)

for i in range(cbins.shape[0]-1):
    #supply[i]=np.sum(df_tec[df_tec.span.to_string()==str(bins[i])].Capacity.values)
    supply[i]=np.sum(df_tec[(df_tec.time_adjusted>=cbins[i])&(df_tec.time_adjusted<cbins[i+1])].Capacity.values)

df=pd.read_csv("./celcat/celcat_data_JANV.csv",encoding='utf-8',delimiter=';')
df.sum_grp.values[np.isnan(df.sum_grp.values)]=0

days=np.zeros((df.values.shape[0],))
time=np.zeros((df.values.shape[0],))
week_ref=np.zeros((df.values.shape[0],))

for i in range(df.values.shape[0]):
    day=int(df.start_time[i].split(' ')[0].split('/')[0])
    month=int(df.start_time[i].split(' ')[0].split('/')[1])
    year=int(df.start_time[i].split(' ')[0].split('/')[2])
    hour=int(df.start_time[i].split(' ')[1].split(':')[0])
    minute=int(df.start_time[i].split(' ')[1].split(':')[1])
    second=int(df.start_time[i].split(' ')[1].split(':')[2])
    days[i]=int(dt.datetime(year, month, day, hour, minute, second, 173504).weekday())
    time[i]=hour*60+minute
    week_ref[i]=dt.datetime(year, month, day, hour, minute, second, 173504).isocalendar()[1]

df['dow']=days
df['time']=time
df['week']=week_ref

unq,cnt=np.unique(df['week'].values,return_counts=True)

# zone nord
print(df[(df.site_name=='Liege Sart-Tilman - Agora')
| (df.site_name=='Liege Sart-Tilman - Village')
| (df.site_name=='Liege Sart-Tilman - Polytech')].site_name)

# zone sud
print(df[(df.site_name=='Liege Sart-Tilman - Hopital')
| (df.site_name=='Liege Sart-Tilman - Blanc Gravier')
| (df.site_name=='Liege Sart-Tilman - Vallee')].site_name)

boo1=(df.site_name=='Liege Sart-Tilman - Agora')|(df.site_name=='Liege Sart-Tilman - Village')|(df.site_name=='Liege Sart-Tilman - Polytech')
boo2=(df.site_name=='Liege Sart-Tilman - Hopital')|(df.site_name=='Liege Sart-Tilman - Blanc Gravier')|(df.site_name=='Liege Sart-Tilman - Vallee')
boo_tot=boo1|boo2

# temporal resolution = 15 mins
days=np.array([0,1,2,3,4,5])
times=np.array([8*60,8*60+15,8*60+30,8*60+45,9*60,9*60+15])
time_labels=['07:45-08:00','08:00-08:15','08:15-08:30','08:30-08:45','08:45-09:00','09:00-09:15']
day_labels=['Lundi','Mardi','Mercredi','Jeudi','Vendredi']

n=10
ratio_nord=1.

#supply=np.array([735+110,480,295,660,700,550]) # until 8h00, 8h15, 8h30, 8h45, 9h00
demand_weeks_north=np.zeros((n,))
demand_weeks_south=np.zeros((n,))

retard=0
offset=9+retard
st_week=1

for i in range(5): # days
    fig=plt.figure(i+2,figsize=(20,10))
    fig.suptitle(day_labels[days[i]], fontsize=20)
    for j in range(6): # times
        for k in range(n):
            #demand_weeks[k]=0.37*np.sum(df[(df.dow==days[i])&(df.time<times[j]+1)&(df.time>=(times[j]-15+1))&(df.week==(k+38))&boo_tot].sum_grp)
            demand_weeks_south[k]=0.26*np.sum(df[(df.dow==days[i])&((df.time-offset)<times[j]+1)&((df.time-offset)>=(times[j]-15+1))&(df.week==(k+st_week))&boo2].sum_grp)
            demand_weeks_north[k]=0.43*np.sum(df[(df.dow==days[i])&(df.time<(times[j]+1))&(df.time>=(times[j]-15+1))&(df.week==(k+st_week))&boo1].sum_grp)
            #demand_weeks[k]=0.43*np.sum(df[(df.dow==days[i])&(df.time<(times[j]+1))&(df.time>=(times[j]-15+1))&(df.week==(k+38))&boo1].sum_grp)
            #demand_weeks[k]=0.4*np.sum(df[(df.dow==days[i])&(df.time>times[j])&(df.week==(k+38))].sum_grp)

        plt.subplot(2,3,j+1)
        p1=plt.bar(np.arange(demand_weeks_north.shape[0]),demand_weeks_north)
        p2=plt.bar(np.arange(demand_weeks_south.shape[0]),demand_weeks_south,bottom=demand_weeks_north)
        p3=plt.plot(np.ones((len(demand_weeks_north),))*supply[j]*ratio_nord,'k',linewidth=2.)
        p4=plt.plot(np.ones((len(demand_weeks_north),))*np.mean(demand_weeks_north),'b--',linewidth=2.)
        p5=plt.plot(np.ones((len(demand_weeks_north),))*np.mean(demand_weeks_south),'r--',linewidth=2.)

        plt.ylim(0,2000)

        plt.grid(True,linewidth=0.1)
        plt.title(time_labels[j])
        #plt.xlabel('Numéro de semaine (' + days[i] + '= jour de référence)')
        plt.xlabel('Semaine')
        plt.ylabel('Nombre d\'étudiants')
        plt.legend((p1[0], p2[0],p3[0], p4[0],p5[0]), ('Nord', 'Sud','Offre TP','Moyenne nord','Moyenne sud'))
        #plt.legend(['Offre TP','Demande moyenne','Demande'])
        #ticks=np.linspace(38-37,52-37,n).astype(int).astype(str)
        ticks=(np.arange(n)+1).astype(int).astype(str)
        plt.xticks(np.arange(len(ticks)), ticks,rotation=45)
        wspace = .5
        hspace = .5
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=wspace, hspace=hspace)
    fig.savefig("./results/Q2_2020_"+str(days[i])+"_qh.png", dpi=fig.dpi)
plt.show()
