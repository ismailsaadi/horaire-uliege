import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

#print(dt.datetime(2019, 12, 30, 23, 59, 59, 173504).isocalendar()[1])
#print(dt.datetime(2019, 6, 30, 00, 30, 00, 173504).weekday())

df_tec_supply=pd.read_csv("./data/tec_supply.csv",encoding='utf-8',delimiter=';')
print(df_tec_supply.columns)
print(df_tec_supply.Time)
print(df_tec_supply.Counts_back)

df_tec=pd.read_csv("./data/tec1.csv",encoding='utf-8',delimiter=';')
print(df_tec.columns)
print(df_tec)

dfplot = pd.DataFrame({'Counts': df_tec_supply.Counts.values,'Counts_back': df_tec_supply.Counts_back.values}, index=df_tec_supply.Time)
ax=dfplot.plot.bar(figsize=(15,8),width=0.6)
plt.grid(True,linewidth=0.1)
plt.subplots_adjust(bottom=0.20)
plt.xticks(rotation=80)
plt.legend(['De CV vers ST','De ST vers CV'])
plt.xlabel('Temps')
plt.ylabel('Capacité bus')
plt.title('Offre TEC')
fig=ax.get_figure()
fig.savefig("./results/offre_TEC.png", dpi=fig.dpi)
#plt.show()



print(np.array([8*60,8*60+15,8*60+30,8*60+45,9*60,9*60+15]))

bins = pd.IntervalIndex.from_tuples([(7*60+30, 8*60), (8*60, 8*60+15), (8*60+15, 8*60+30),(8*60+30, 8*60+45),(8*60+45,9*60),(9*60,9*60+15)],dtype='interval[int32]')

# cbines per 15 mins and per hour
cbins=np.array([7*60+30,8*60,8*60+15,8*60+30,8*60+45,9*60,9*60+15])
#cbins=np.array([7*60,8*60,9*60,10*60])

supply=np.zeros((bins.shape[0],))
cc=pd.cut(df_tec.time_adjusted, bins)
print(cc)

df_tec['span']=pd.cut(df_tec.time_adjusted, bins)


print(bins[1])
print(df_tec.span[3])
print(df_tec.span.values[3])
print(df_tec.span)

print(cbins)
for i in range(cbins.shape[0]-1):
    print(df_tec.span.to_string())
    print(str(bins[i]))
    print(df_tec.span.to_string()==str(bins[i]))
    #print(df_tec.columns)
    #print(str(bins[i]).dtype)
    #print(pd.IntervalIndex.from_tuples([bins[i]]))
    #supply[i]=np.sum(df_tec[df_tec.span.to_string()==str(bins[i])].Capacity.values)
    supply[i]=np.sum(df_tec[(df_tec.time_adjusted>=cbins[i])&(df_tec.time_adjusted<cbins[i+1])].Capacity.values)

print(supply)
print(np.array([735+110,480,295,660,700,550]))
#print(np.sum(supply))
print(np.sum(np.array([735+110,480,295,660,700,550])))

df=pd.read_csv("./celcat/celcat_data_JANV.csv",encoding='utf-8',delimiter=';')
print(df.columns)
print(df.values.shape[0])
print(df.site_name)

print(np.isnan(df.sum_grp.values))
df.sum_grp.values[np.isnan(df.sum_grp.values)]=0
print(df.sum_grp.values)

#df.sum_grp.plot(kind='hist')
#plt.grid(True,linewidth=0.1)
#plt.show()

#for i in range()


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
print(df.columns)
print(df)
print(df.start_time)





#plt.show()

unq,cnt=np.unique(df['week'].values,return_counts=True)
print(unq)
print(cnt)

print(df.sum_grp)
print(df.default_capacity)
print(df.start_time)
print(df.site_name)

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

print(boo1)

# fig,axs=plt.subplots(1,1,figsize=(20,10))
# unq,cnt=np.unique(df[boo_tot&(df.dow==0)&(df.week==39)].time.values,return_counts=True)
# axs.bar(np.arange(len(cnt)),cnt,width=0.35)
#
# plt.sca(axs)
# plt.xticks(np.arange(len(cnt)),unq/60,rotation=45)


#axs.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))

#axs.xticks(np.arange(len(cnt)),unq/60,rotation=45)
#axs.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
#plt.show()

# &(df.sum_grp>100)



# temporal resolution = 15 mins
days=np.array([0,1,2,3,4,5])
times=np.array([8*60,8*60+15,8*60+30,8*60+45,9*60,9*60+15])
time_labels=['07:45-08:00','08:00-08:15','08:15-08:30','08:30-08:45','08:45-09:00','09:00-09:15']
day_labels=['Lundi','Mardi','Mercredi','Jeudi','Vendredi']
print(times)

# temporal resolution = 60 mins
# days=np.array([0,1,2,3,4,5])
# times=np.array([8*60,9*60,10*60]) # only end time specified
# time_labels=['07:00-08:00','08:00-09:00','09:00-10:00']
# day_labels=['Lundi','Mardi','Mercredi','Jeudi','Vendredi']
# print(times)


n=10
#+295
#ratio_nord=0.65
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


# for i in range(5): # days
#     fig=plt.figure(i+2,figsize=(20,5))
#     fig.suptitle(day_labels[days[i]], fontsize=20)
#     for j in range(3): # times
#         for k in range(n):
#             #demand_weeks[k]=0.37*np.sum(df[(df.dow==days[i])&(df.time<times[j]+1)&(df.time>=(times[j]-15+1))&(df.week==(k+38))&boo_tot].sum_grp)
#             demand_weeks_south[k]=0.26*np.sum(df[(df.dow==days[i])&((df.time-offset)<times[j]+1)&((df.time-offset)>=(times[j]-60+1))&(df.week==(k+st_week))&boo2].sum_grp)
#             demand_weeks_north[k]=0.43*np.sum(df[(df.dow==days[i])&(df.time<(times[j]+1))&(df.time>=(times[j]-60+1))&(df.week==(k+st_week))&boo1].sum_grp)
#
#             #demand_weeks[k]=0.43*np.sum(df[(df.dow==days[i])&(df.time<(times[j]+1))&(df.time>=(times[j]-15+1))&(df.week==(k+38))&boo1].sum_grp)
#
#             #demand_weeks[k]=0.4*np.sum(df[(df.dow==days[i])&(df.time>times[j])&(df.week==(k+38))].sum_grp)
#
#         plt.subplot(1,3,j+1)
#
#
#
#         p1=plt.bar(np.arange(demand_weeks_north.shape[0]),demand_weeks_north)
#         p2=plt.bar(np.arange(demand_weeks_south.shape[0]),demand_weeks_south,bottom=demand_weeks_north)
#         p3=plt.plot(np.ones((len(demand_weeks_north),))*supply[j]*ratio_nord,'k',linewidth=2.)
#         p4=plt.plot(np.ones((len(demand_weeks_north),))*np.mean(demand_weeks_north),'b--',linewidth=2.)
#         p5=plt.plot(np.ones((len(demand_weeks_north),))*np.mean(demand_weeks_south),'r--',linewidth=2.)
#
#         #plt.ylim(0,2000)
#
#         plt.grid(True,linewidth=0.1)
#         plt.title(time_labels[j])
#         #plt.xlabel('Numéro de semaine (' + days[i] + '= jour de référence)')
#         plt.xlabel('Semaine')
#         plt.ylabel('Nombre d\'étudiants')
#         plt.legend((p1[0], p2[0],p3[0], p4[0],p5[0]), ('Nord', 'Sud','Offre TP','Moyenne nord','Moyenne sud'))
#         #plt.legend(['Offre TP','Demande moyenne','Demande'])
#         #ticks=np.linspace(38-37,52-37,n).astype(int).astype(str)
#         ticks=(np.arange(n)+1).astype(int).astype(str)
#         plt.xticks(np.arange(len(ticks)), ticks,rotation=45)
#         wspace = .5
#         hspace = .5
#     plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=wspace, hspace=hspace)
#     fig.savefig('/Users/ismailsaadi/FNRS research/scheduling/results/Q2_2020_'+str(days[i])+'_hh.png', dpi=fig.dpi)

plt.show()
