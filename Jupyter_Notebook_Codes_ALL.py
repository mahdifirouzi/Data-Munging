# First Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

# Read CSV File For RAW Heating And Electrical Consumption Pattern From Scraped Data
df = pd.read_csv("C:\\Users\\PowerMan\\Desktop\\KASR\Final\\Code and data\\Data\\Whole_scraped_data\\Total-Load-Whole-Premise.csv")
# Delete additional datas in RAW File
# Delete Extra Columns
df.drop('Date Start',axis=1,inplace=True)
df.drop('(Weekdays) or (Weekends and Holidays)',axis=1,inplace=True)
df.drop('Demand',axis=1,inplace=True)
# Delete Extra Raws
# Create an index to filter raws faster than normal for loop!
df['keep']=np.where( df['City'] == 'City', 1, 0)
df=df[df['keep']==0]
# Delete Auxilary index Column
df.drop('keep',axis=1,inplace=True)
# Change data type to float
df[['HR1','HR2','HR3','HR4','HR5','HR6','HR7','HR8','HR9','HR10','HR11','HR12','HR13','HR14','HR15','HR16','HR17','HR18','HR19','HR20','HR21','HR22','HR23','HR24']] = df[['HR1','HR2','HR3','HR4','HR5','HR6','HR7','HR8','HR9','HR10','HR11','HR12','HR13','HR14','HR15','HR16','HR17','HR18','HR19','HR20','HR21','HR22','HR23','HR24']].astype('float64')
# Convert Sqft To Sqm Sqft/10.764=Sqm
sqft_coef = 10.76391041671
#Convert wh/Sqft  To wh/Sqm
df.loc[:,'HR1':'HR24']=df.loc[:,'HR1':'HR24']/(sqft_coef)
# Create 2 Column for State And City
df['city_name'] = df.iloc[:, 0]
df['city_state'] = df.iloc[:, 0]
# Split City and State
for i in range (0,120450):
    ct = df.iloc[i, 0]
    ct = ct.split(',', 1)
    ctname  = ct[0]
    ctstate = ct[1]
    df.iloc[i, 28] = ctname
    df.iloc[i, 29] = ctstate
# Save File step1
df.to_csv(path_or_buf="C:\\Users\\PowerMan\\Desktop\\KASR\\Final\\Code and data\\Codes\\datamunging\\step1.csv")
########################################################################################################
########################################################################################################
########################################################################################################
# Read New Modified CSV File
df = pd.read_csv("C:\\Users\\PowerMan\\Desktop\\KASR\\Final\\Code and data\\Codes\\datamunging\\step1.csv")
# Delete Old Index Column
df.drop('Unnamed: 0',axis=1,inplace=True)
#Create Day index
day=[]
for i in range (1,331):
    for j in range (1,366):
        day.append(j)
day_no=pd.Series(day)
df['day_num']=day_no
#Load Cities List
ct = pd.read_csv("C:\\Users\\PowerMan\\Desktop\\KASR\\Final\\Code and data\\Codes\\datamunging\\sourcecity.csv")
df['climate']= df['city_name']
df['city_no']= df['city_name']
df[['city_name','city_no','climate']] = df[['city_name','city_no','climate']].astype(str)
climate=[]
city_no=[]
#Extract Data from source ct climate and city numbers
for i in range (0,120450):
    cit = str(df.iloc[i, 28])
    cit=cit.lower()
    for j in range (0,55):
        ctt=ct.iloc[j, 2]
        ctt=ctt.lower()
        if cit==ctt:
            df.iloc[i,30] = ct.iloc[j, 3]
            df.iloc[i,31] = ct.iloc[j, 0]
# Save File step2
df.to_csv(path_or_buf="C:\\Users\\PowerMan\\Desktop\\KASR\\Final\\Code and data\\Codes\\datamunging\\step2.csv")
##################################################################################################
# Read New Modified CSV File
df = pd.read_csv("C:\\Users\\PowerMan\\Desktop\\KASR\\Final\\Code and data\\Codes\\datamunging\\step2.csv")
# Delete Old Index Column
df.drop('Unnamed: 0',axis=1,inplace=True)
# Delete Extra Column
df.drop('city_no',axis=1,inplace=True)
# Delete Extra Column
df.drop('City',axis=1,inplace=True)
# Delete Extra Column
df.drop('city_state',axis=1,inplace=True)
# Rearreng colmns
data_colm=['date','load_type','building_type','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','city','climate','city_no']
df.columns=data_colm
#Create Day index
day=[]
for i in range (1,331):
    for j in range (1,366):
        day.append(j)
day_no=pd.Series(day)
df['day_num']=day_no
# Create A Column For Each Day Sum Of Loads
df['sum_day']= df.loc[:, '1':'24'].sum(axis=1)
# Sort Columns
new_order = [27,29,28,0,30,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,31]
df = df[df.columns[new_order]]
# Change Name of Load Types
df['load_type'] = df.load_type.map({'Electric':'Energy','Fossil Fuel':'Electric'})
# Save File step3
df.to_csv(path_or_buf="C:\\Users\\PowerMan\\Desktop\\KASR\\Final\\Code and data\\Codes\\datamunging\\step3.csv")
#######################################################################################
# Step 3
# Read New Modified CSV File
df = pd.read_csv("C:\\Users\\PowerMan\\Desktop\\KASR\\Final\\Code and data\\Codes\\datamunging\\step3.csv")
# Delete Old Index Column
df.drop('Unnamed: 0',axis=1,inplace=True)
# Reduce File size
df['building_type']=df.building_type.map({'Office, Large':4,'Office, Medium':3,'Office, Small':1})
# Seprate Electrical and Energy
en=df.loc[df.load_type=='Energy'].copy()
el=df.loc[df.load_type=='Electric'].copy()
he=df.loc[df.load_type=='Electric'].copy()
he['load_type'] = he.load_type.map({'Electric':'Heat'})
he.drop('sum_day',axis=1,inplace=True)
# Save File step4
en.to_csv(path_or_buf="C:\\Users\\PowerMan\\Desktop\\KASR\\Final\\Code and data\\Codes\\datamunging\\step4en.csv")
el.to_csv(path_or_buf="C:\\Users\\PowerMan\\Desktop\\KASR\\Final\\Code and data\\Codes\\datamunging\\step4el.csv")
he.to_csv(path_or_buf="C:\\Users\\PowerMan\\Desktop\\KASR\\Final\\Code and data\\Codes\\datamunging\\step4he.csv")
###############################################################################################################
# Read New Modified CSV File
he = pd.read_csv("C:\\Users\\PowerMan\\Desktop\\KASR\\Final\\Code and data\\Codes\\datamunging\\step4he.csv")
# Delete Old Index Column
he.drop('Unnamed: 0',axis=1,inplace=True)
for i in range (0,60225):
    for j in range (7,31):
        if he.iloc[i,j]<0:
            he.iloc[i,j]=0
he['sum_day']= he.loc[:, '1':'24'].sum(axis=1)
# Save File step5
he.to_csv(path_or_buf="C:\\Users\\PowerMan\\Desktop\\KASR\\Final\\Code and data\\Codes\\datamunging\\step5he.csv")
############################################################################################################
# Step 6
# Read New Modified CSV File
he = pd.read_csv("C:\\Users\\PowerMan\\Desktop\\KASR\\Final\\Code and data\\Codes\\datamunging\\step5he.csv")
el = pd.read_csv("C:\\Users\\PowerMan\\Desktop\\KASR\\Final\\Code and data\\Codes\\datamunging\\step5el.csv")
#en = pd.read_csv("C:\\Users\\PowerMan\\Desktop\\KASR\\Data\\Pandas\\RAW_Mannaged\\step5en.csv")

# Delete Old Index Column
he.drop('Unnamed: 0',axis=1,inplace=True)
el.drop('Unnamed: 0',axis=1,inplace=True)

alll = pd.read_csv("C:\\Users\\PowerMan\\Desktop\\KASR\\Final\\Code and data\\Codes\\datamunging\\annuallysum.csv")
sumey1=[]
sumey3=[]
sumey4=[]

sumhy1=[]
sumhy3=[]
sumhy4=[]

for j in range (0,165,3):
    c = j  * 365
    jj=j/3
    jj=int(jj)

    sumey1.append(0)
    sumey3.append(0)
    sumey4.append(0)
    sumhy1.append(0)
    sumhy3.append(0)
    sumhy4.append(0)



    city_name = el.iloc[ c, 0]
    city_climate=el.iloc[ c,2]
    city_number=el.iloc[ c,1]
    alll.iloc[j,1]= city_name
    alll.iloc[j,2]= city_climate
    alll.iloc[j,0]= city_number

    alll.iloc[j+1, 1] = city_name
    alll.iloc[j+1, 2] = city_climate
    alll.iloc[j+1, 0] = city_number

    alll.iloc[j+2, 1] = city_name
    alll.iloc[j+2, 2] = city_climate
    alll.iloc[j+2, 0] = city_number

    alll.iloc[j, 3]   = 1
    alll.iloc[j+1, 3] = 3
    alll.iloc[j+2, 3] = 4

    for i in range (0,360):
        sumey4[jj]= el.iloc[i+c, 31]      +   sumey4[jj]
        sumey3[jj]= el.iloc[i+c + 1, 31]  +   sumey3[jj]
        sumey1[jj]= el.iloc[i+c+ 2, 31]  +  sumey1[jj]

        sumhy4[jj]= he.iloc[i+c, 31]      +    sumhy4[jj]
        sumhy3[jj]= he.iloc[i+c + 1, 31]  +    sumhy3[jj]
        sumhy1[jj]= he.iloc[i+c + 2, 31]  +    sumhy1[jj]
    alll.iloc[j,     4] = sumhy1[jj]
    alll.iloc[j + 1, 4] = sumhy3[jj]
    alll.iloc[j + 2, 4] = sumhy4[jj]
    alll.iloc[j,     5] = sumey1[jj]
    alll.iloc[j + 1, 5] = sumey3[jj]
    alll.iloc[j + 2, 5] = sumey4[jj]
    alll.iloc[j,     6] = sumey1[jj]+sumhy1[jj]
    alll.iloc[j + 1, 6] = sumey3[jj]+sumhy3[jj]
    alll.iloc[j + 2, 6] = sumey4[jj]+sumhy4[jj]


alll.loc[:,'heat':'energy']=alll.loc[:,'heat':'energy']/(1000)
######################################################################################################
# step 7
warnings.simplefilter(action='ignore', category=FutureWarning)
# Read New Modified CSV File
he = pd.read_csv("C:\\Users\\PowerMan\\Desktop\\KASR\\Data\\Pandas\\RAW_Mannaged\\he_sorted_971012_1054.csv")
el = pd.read_csv("C:\\Users\\PowerMan\\Desktop\\KASR\\Data\\Pandas\\RAW_Mannaged\\el_sorted_971012_1054.csv")
coef = pd.read_csv("C:\\Users\\PowerMan\\Desktop\\KASR\\Data\\Pandas\\Eng_Analysed\\Coefficents.csv")
# Delete Old Index Column
he.drop('Unnamed: 0',axis=1,inplace=True)
el.drop('Unnamed: 0',axis=1,inplace=True)
el0B = el.loc[(el.climate=='1A')&(el.city=='Miami')]
el1A = el.loc[(el.climate=='1A')&(el.city=='Miami')]
el1B = el.loc[(el.climate=='1A')&(el.city=='Miami')]
el2A = el.loc[(el.climate=='2A')&(el.city=='Austin')]
el2B = el.loc[(el.climate=='2B')&(el.city=='Phoenix')]
el3A = el.loc[(el.climate=='3A')&(el.city=='Charlotte')]
el3B = el.loc[(el.climate=='3B')&(el.city=='Las Vegas')]
el4A = el.loc[(el.climate=='4A')&(el.city=='Newark')]
el4B = el.loc[(el.climate=='4B')&(el.city=='Amarillo')]
el4C = el.loc[(el.climate=='4C')&(el.city=='Medford')]
el5A = el.loc[(el.climate=='5A')&(el.city=='Cleveland')]
el5C = el.loc[(el.climate=='5A')&(el.city=='Cleveland')]

el0B .loc[:,'1':'24']=el0B .loc[:,'1':'24']*(coef.iloc[0,2])
el1A .loc[:,'1':'24']=el1A .loc[:,'1':'24']*(coef.iloc[1,2])
el1B .loc[:,'1':'24']=el1B .loc[:,'1':'24']*(coef.iloc[2,2])
el2A .loc[:,'1':'24']=el2A .loc[:,'1':'24']*(coef.iloc[3,2])
el2B .loc[:,'1':'24']=el2B .loc[:,'1':'24']*(coef.iloc[4,2])
el3A .loc[:,'1':'24']=el3A .loc[:,'1':'24']*(coef.iloc[5,2])
el3B .loc[:,'1':'24']=el3B .loc[:,'1':'24']*(coef.iloc[6,2])
el4A .loc[:,'1':'24']=el4A .loc[:,'1':'24']*(coef.iloc[7,2])
el4B .loc[:,'1':'24']=el4B .loc[:,'1':'24']*(coef.iloc[8,2])
el4C .loc[:,'1':'24']=el4C .loc[:,'1':'24']*(coef.iloc[9,2])
el5A .loc[:,'1':'24']=el5A .loc[:,'1':'24']*(coef.iloc[10,2])
el5C .loc[:,'1':'24']=el5C .loc[:,'1':'24']*(coef.iloc[11,2])

he0B = he.loc[(he.climate=='1A')&(he.city=='Miami')]
he1A = he.loc[(he.climate=='1A')&(he.city=='Miami')]
he1B = he.loc[(he.climate=='1A')&(he.city=='Miami')]
he2A = he.loc[(he.climate=='2A')&(he.city=='Austin')]
he2B = he.loc[(he.climate=='2B')&(he.city=='Phoenix')]
he3A = he.loc[(he.climate=='3A')&(he.city=='Charlotte')]
he3B = he.loc[(he.climate=='3B')&(he.city=='Las Vegas')]
he4A = he.loc[(he.climate=='4A')&(he.city=='Newark')]
he4B = he.loc[(he.climate=='4B')&(he.city=='Amarillo')]
he4C = he.loc[(he.climate=='4C')&(he.city=='Medford')]
he5A = he.loc[(he.climate=='5A')&(he.city=='Cleveland')]
he5C = he.loc[(he.climate=='5A')&(he.city=='Cleveland')]

he0B .loc[:,'1':'24']=he0B .loc[:,'1':'24']*(coef.iloc[0,3])
he1A .loc[:,'1':'24']=he1A .loc[:,'1':'24']*(coef.iloc[1,3])
he1B .loc[:,'1':'24']=he1B .loc[:,'1':'24']*(coef.iloc[2,3])
he2A .loc[:,'1':'24']=he2A .loc[:,'1':'24']*(coef.iloc[3,3])
he2B .loc[:,'1':'24']=he2B .loc[:,'1':'24']*(coef.iloc[4,3])
he3A .loc[:,'1':'24']=he3A .loc[:,'1':'24']*(coef.iloc[5,3])
he3B .loc[:,'1':'24']=he3B .loc[:,'1':'24']*(coef.iloc[6,3])
he4A .loc[:,'1':'24']=he4A .loc[:,'1':'24']*(coef.iloc[7,3])
he4B .loc[:,'1':'24']=he4B .loc[:,'1':'24']*(coef.iloc[8,3])
he4C .loc[:,'1':'24']=he4C .loc[:,'1':'24']*(coef.iloc[9,3])
he5A .loc[:,'1':'24']=he5A .loc[:,'1':'24']*(coef.iloc[10,3])
he5C .loc[:,'1':'24']=he5C .loc[:,'1':'24']*(coef.iloc[11,3])

el0B['climate'] = el0B.climate.map({'1A':'0B'})
el1A['climate'] = el1A.climate.map({'1A':'1B'})
el5C['climate'] = el5C.climate.map({'5A':'5C'})

he0B['climate'] = he0B.climate.map({'1A':'0B'})
he1A['climate'] = he1A.climate.map({'1A':'1B'})
he5C['climate'] = he5C.climate.map({'5A':'5C'})

el10B = el0B.loc[(el0B.building_type==1)]
el11A = el1A.loc[(el1A.building_type==1)]
el11B = el1B.loc[(el1B.building_type==1)]
el12A = el2A.loc[(el2A.building_type==1)]
el12B = el2B.loc[(el2B.building_type==1)]
el13A = el3A.loc[(el3A.building_type==1)]
el13B = el3B.loc[(el3B.building_type==1)]
el14A = el4A.loc[(el4A.building_type==1)]
el14B = el4B.loc[(el4B.building_type==1)]
el14C = el4C.loc[(el4C.building_type==1)]
el15A = el5A.loc[(el5A.building_type==1)]
el15C = el5C.loc[(el5C.building_type==1)]

he10B = he0B.loc[(he0B.building_type==1)]
he11A = he1A.loc[(he1A.building_type==1)]
he11B = he1B.loc[(he1B.building_type==1)]
he12A = he2A.loc[(he2A.building_type==1)]
he12B = he2B.loc[(he2B.building_type==1)]
he13A = he3A.loc[(he3A.building_type==1)]
he13B = he3B.loc[(he3B.building_type==1)]
he14A = he4A.loc[(he4A.building_type==1)]
he14B = he4B.loc[(he4B.building_type==1)]
he14C = he4C.loc[(he4C.building_type==1)]
he15A = he5A.loc[(he5A.building_type==1)]
he15C = he5C.loc[(he5C.building_type==1)]

el30B = el0B.loc[(el0B.building_type==3)]
el31A = el1A.loc[(el1A.building_type==3)]
el31B = el1B.loc[(el1B.building_type==3)]
el32A = el2A.loc[(el2A.building_type==3)]
el32B = el2B.loc[(el2B.building_type==3)]
el33A = el3A.loc[(el3A.building_type==3)]
el33B = el3B.loc[(el3B.building_type==3)]
el34A = el4A.loc[(el4A.building_type==3)]
el34B = el4B.loc[(el4B.building_type==3)]
el34C = el4C.loc[(el4C.building_type==3)]
el35A = el5A.loc[(el5A.building_type==3)]
el35C = el5C.loc[(el5C.building_type==3)]

he30B = he0B.loc[(he0B.building_type==3)]
he31A = he1A.loc[(he1A.building_type==3)]
he31B = he1B.loc[(he1B.building_type==3)]
he32A = he2A.loc[(he2A.building_type==3)]
he32B = he2B.loc[(he2B.building_type==3)]
he33A = he3A.loc[(he3A.building_type==3)]
he33B = he3B.loc[(he3B.building_type==3)]
he34A = he4A.loc[(he4A.building_type==3)]
he34B = he4B.loc[(he4B.building_type==3)]
he34C = he4C.loc[(he4C.building_type==3)]
he35A = he5A.loc[(he5A.building_type==3)]
he35C = he5C.loc[(he5C.building_type==3)]

el40B = el0B.loc[(el0B.building_type==4)]
el41A = el1A.loc[(el1A.building_type==4)]
el41B = el1B.loc[(el1B.building_type==4)]
el42A = el2A.loc[(el2A.building_type==4)]
el42B = el2B.loc[(el2B.building_type==4)]
el43A = el3A.loc[(el3A.building_type==4)]
el43B = el3B.loc[(el3B.building_type==4)]
el44A = el4A.loc[(el4A.building_type==4)]
el44B = el4B.loc[(el4B.building_type==4)]
el44C = el4C.loc[(el4C.building_type==4)]
el45A = el5A.loc[(el5A.building_type==4)]
el45C = el5C.loc[(el5C.building_type==4)]

he40B = he0B.loc[(he0B.building_type==4)]
he41A = he1A.loc[(he1A.building_type==4)]
he41B = he1B.loc[(he1B.building_type==4)]
he42A = he2A.loc[(he2A.building_type==4)]
he42B = he2B.loc[(he2B.building_type==4)]
he43A = he3A.loc[(he3A.building_type==4)]
he43B = he3B.loc[(he3B.building_type==4)]
he44A = he4A.loc[(he4A.building_type==4)]
he44B = he4B.loc[(he4B.building_type==4)]
he44C = he4C.loc[(he4C.building_type==4)]
he45A = he5A.loc[(he5A.building_type==4)]
he45C = he5C.loc[(he5C.building_type==4)]

writer = pd.ExcelWriter("C:\\Users\\PowerMan\\Desktop\\KASR\\Data\\Pandas\\Eng_Analysed\\Climate_0B.xlsx")
el10B.to_excel(writer,'el10B')
el30B.to_excel(writer,'el30B')
el40B.to_excel(writer,'el40B')
he10B.to_excel(writer,'he10B')
he30B.to_excel(writer,'he30B')
he40B.to_excel(writer,'he40B')
writer.save()

writer = pd.ExcelWriter("C:\\Users\\PowerMan\\Desktop\\KASR\\Data\\Pandas\\Eng_Analysed\\Climate_1A.xlsx")
el11A.to_excel(writer,'el11A')
el31A.to_excel(writer,'el31A')
el41A.to_excel(writer,'el41A')
he11A.to_excel(writer,'he11A')
he31A.to_excel(writer,'he31A')
he41A.to_excel(writer,'he41A')
writer.save()

writer = pd.ExcelWriter("C:\\Users\\PowerMan\\Desktop\\KASR\\Data\\Pandas\\Eng_Analysed\\Climate_1B.xlsx")
el11B.to_excel(writer,'el11B')
el31B.to_excel(writer,'el31B')
el41B.to_excel(writer,'el41B')
he11B.to_excel(writer,'he11B')
he31B.to_excel(writer,'he31B')
he41B.to_excel(writer,'he41B')
writer.save()

writer = pd.ExcelWriter("C:\\Users\\PowerMan\\Desktop\\KASR\\Data\\Pandas\\Eng_Analysed\\Climate_2A.xlsx")
el12A.to_excel(writer,'el12A')
el32A.to_excel(writer,'el32A')
el42A.to_excel(writer,'el42A')
he12A.to_excel(writer,'he12A')
he32A.to_excel(writer,'he32A')
he42A.to_excel(writer,'he42A')
writer.save()

writer = pd.ExcelWriter("C:\\Users\\PowerMan\\Desktop\\KASR\\Data\\Pandas\\Eng_Analysed\\Climate_2B.xlsx")
el12B.to_excel(writer,'el12B')
el32B.to_excel(writer,'el32B')
el42B.to_excel(writer,'el42B')
he12B.to_excel(writer,'he12B')
he32B.to_excel(writer,'he32B')
he42B.to_excel(writer,'he42B')
writer.save()

writer = pd.ExcelWriter("C:\\Users\\PowerMan\\Desktop\\KASR\\Data\\Pandas\\Eng_Analysed\\Climate_3A.xlsx")
el13A.to_excel(writer,'el13A')
el33A.to_excel(writer,'el33A')
el43A.to_excel(writer,'el43A')
he13A.to_excel(writer,'he13A')
he33A.to_excel(writer,'he33A')
he43A.to_excel(writer,'he43A')
writer.save()

writer = pd.ExcelWriter("C:\\Users\\PowerMan\\Desktop\\KASR\\Data\\Pandas\\Eng_Analysed\\Climate_3B.xlsx")
el13B.to_excel(writer,'el13B')
el33B.to_excel(writer,'el33B')
el43B.to_excel(writer,'el43B')
he13B.to_excel(writer,'he13B')
he33B.to_excel(writer,'he33B')
he43B.to_excel(writer,'he43B')
writer.save()

writer = pd.ExcelWriter("C:\\Users\\PowerMan\\Desktop\\KASR\\Data\\Pandas\\Eng_Analysed\\Climate_4A.xlsx")
el14A.to_excel(writer,'el14A')
el34A.to_excel(writer,'el34A')
el44A.to_excel(writer,'el44A')
he14A.to_excel(writer,'he14A')
he34A.to_excel(writer,'he34A')
he44A.to_excel(writer,'he44A')
writer.save()

writer = pd.ExcelWriter("C:\\Users\\PowerMan\\Desktop\\KASR\\Data\\Pandas\\Eng_Analysed\\Climate_4B.xlsx")
el14B.to_excel(writer,'el14B')
el34B.to_excel(writer,'el34B')
el44B.to_excel(writer,'el44B')
he14B.to_excel(writer,'he14B')
he34B.to_excel(writer,'he34B')
he44B.to_excel(writer,'he44B')
writer.save()

writer = pd.ExcelWriter("C:\\Users\\PowerMan\\Desktop\\KASR\\Data\\Pandas\\Eng_Analysed\\Climate_4C.xlsx")
el14C.to_excel(writer,'el14C')
el34C.to_excel(writer,'el34C')
el44C.to_excel(writer,'el44C')
he14C.to_excel(writer,'he14C')
he34C.to_excel(writer,'he34C')
he44C.to_excel(writer,'he44C')
writer.save()

writer = pd.ExcelWriter("C:\\Users\\PowerMan\\Desktop\\KASR\\Data\\Pandas\\Eng_Analysed\\Climate_5A.xlsx")
el15A.to_excel(writer,'el15A')
el35A.to_excel(writer,'el35A')
el45A.to_excel(writer,'el45A')
he15A.to_excel(writer,'he15A')
he35A.to_excel(writer,'he35A')
he45A.to_excel(writer,'he45A')
writer.save()

writer = pd.ExcelWriter("C:\\Users\\PowerMan\\Desktop\\KASR\\Data\\Pandas\\Eng_Analysed\\Climate_5C.xlsx")
el15C.to_excel(writer,'el15C')
el35C.to_excel(writer,'el35C')
el45C.to_excel(writer,'el45C')
he15C.to_excel(writer,'he15C')
he35C.to_excel(writer,'he35C')
he45C.to_excel(writer,'he45C')
writer.save()
