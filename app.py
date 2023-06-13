import streamlit as st
import PyPDF2
import pandas as pd
import re
import pandas as pd
import numpy as np
import openpyxl
from openpyxl import load_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.cbook import get_sample_data
import matplotlib.cbook as cbook


#https://drive.google.com/drive/folders/15isTTRs3Ans4VJnLrSMRMsClB-iu7man?usp=sharing

def depth_start(t):
    return re.findall('^[0-9][0-9]:[0-9][0-9]\s[0-9][0-9]:[0-9][0-9]\s[0-9]:[0-9][0-9].([0-9.]+)', t)

# method to extract depth end
def depth_end(t):
    return re.findall('^[0-9][0-9]:[0-9][0-9]\s[0-9][0-9]:[0-9][0-9]\s[0-9]:[0-9][0-9]\s[0-9.]+.([0-9.]+)', t)

def hole_section(t):
    return re.findall('^[0-9][0-9]:[0-9][0-9]\s[0-9][0-9]:[0-9][0-9]\s[0-9]:[0-9][0-9]\s[0-9][0-9][0-9.]+\s[0-9][0-9][0-9.]+.([0-9.]+)', t)

def csg_rawsize(t):
    for m in re.finditer('Casing Last Size .([0-9.+]*)', t):
        return (m.group())

def csg_rawdepth(t):
    for m in re.finditer('Set MD .([0-9.+]*)', t):
        return (m.group())
def losses_raw(t):
    for m in re.finditer('losses.*([0-9.]+)', t):
        return (m.group())
    
def losses11(t):
    return re.findall('losses.([\d+-?.]+)', t)
def kick_raw(t):
    for m in re.finditer('flow at.*([0-9.]+)', t):
        return (m.group())
    
# extrace losses rate or losses 
def kick(t):
    return re.findall('kill mud.*(ppg+', t)
            
def kick1(t):
        for m in re.finditer('(kill mud.*+)', t):
            return (m.group())  
def losses1(t):
    try:
        return re.findall('losses\srate:.([\d+-?.]+)', t)
    except:   
        pass
# Extracting unit of measurement
def unit_of_measurement(t):
    word_list = t.split()
    return word_list[-1]
st.title("AUTOMATED OFFSET WELL ANALYSIS")
st.header("UPLOAD DOR'S HERE")
st.subheader("IN THIS VERSION-I OFFSET WELL ANALYSIS PROGRAM SHOWCASE, DDR FORMAT IS LIMITED.")
st.subheader("SMALL WORK MANUAL -")
st.subheader("KINDLY FIND THE BELOW LINK TO LIMITED DDR FORMAT IN DRIVE")
st.subheader("1) DOWNLOAD THE FOLDER ")
st.subheader("2) UNZIP IT ")
st.subheader("3) UPLOAD THE ENTIRE FOLSER IN THE DRAG AND DROP OBJECT BELOW (REMEMBER TO UPLOAD UNZIPPED 'FOLDER')")
def main():
    parent_text = ""
    summary = []
    csg_size = []
    csd = []
    losses = []
    l2 = []
    l=[]
    df_notes = pd.DataFrame()
    result = st.file_uploader("Upload", type="pdf",accept_multiple_files=True)
    result1 = st.button("ANALYSE")
    if result1:
        st.header("PROCESSING")
        st.text("It may take couple of minutes .....")
        for r in result:
            pdf_reader = PyPDF2.PdfReader(r)
            text = ""
            parent_text = ""
            data = pd.DataFrame()
            data1= pd.DataFrame()
            data2= pd.DataFrame()
            for pagenum in range(pdf_reader.numPages):
                pageobj = pdf_reader.getPage(pagenum)
                text += pageobj.extract_text() 
                #print(text)
                #text= text.replace("\n"," ")
                #print(text)
                text= text.replace("\n"," ")
                #parent_text = text
                datal = pd.DataFrame()
                lines = text.split("\n")
                non_empty_lines = [line for line in lines if line.strip() != ""]
                text = ""
                for line in non_empty_lines:
                    text += line + "\n"
                        # removing commas in between numericals and equal signs and double spaces
                    text = text.replace(',', '')
                    text = text.replace('=', '')
                    text = text.replace('(in)','')
                    text = text.replace('Set MD (ft)', 'Set MD')
                        #text = text.replace('Casing Last Size (in)', 'Casing Last Size')
                    text = text.replace(" - ", '\n')
                    text = re.sub(' +', ' ', text)
                    x = []
                    parent_text= text
                    
            for m in re.findall('24 Hours Summary(.*?)24 Hours Forecast', text):
                summary.append(m)
            for r in re.findall('Casing Last Size(.*?)Set MD', text):
                csg_size.append(r)
            for r in re.findall('Set MD(.*?)Next Size', text):
                csd.append(r)
            for u in re.finditer('[0-9][0-9]:[0-9][0-9]\s[0-9][0-9]:[0-9][0-9]\s[0-9]', text):
                l.append(u.start())  
            datal.append(l)
            p1 = l[0]
            p2 = l[1]
            a = 1
                
            for i in l[1:]:
                l2.append(text[p1:p2])
                #print(data1)
                print("-----------------------LOADING--------------------------------------")
                p1 = p2
                a = a+1
                try:
                    p2 = l[a]
                except:
                    pass
                data_l2 = pd.DataFrame({"notes":l2})
        df_notes = data_l2        
        data["SUMMARY"] = summary
        data = data.drop_duplicates(subset="SUMMARY")
        data1["CASING-SIZE"] = csg_size
        data1 = data1.drop_duplicates(subset = "CASING-SIZE")
        data1 = data1.dropna()
        data2["CSD"] = csd
        data2 = data2.drop_duplicates(subset = "CSD")
        data2 = data2.dropna()
        dat=pd.concat([data1,data2],axis=1)
        r = dat.shape[0]
        r = range(0,8)
        t = []
        for x  in r:
            t.append(x)
        index = t
        dati = pd.DataFrame()
        dati['INDEX'] = index
        dat = pd.concat([dat,dati],axis=1)
        dat.set_index("INDEX",inplace=True)
        X_axis = [2,2,np.NaN,np.NaN,3,3,np.NaN,np.NaN,4,4,np.NaN,np.NaN,5,5,np.NaN,np.NaN,6,6,np.NaN,np.NaN,7,7,np.NaN,np.NaN,8,8,np.NaN,np.NaN] 
        Y_axis = [0,dat.iloc[1,1],np.NaN,np.NaN,0,dat.iloc[2,1],np.NaN,np.NaN,0,dat.iloc[3,1],np.NaN,np.NaN,0,dat.iloc[4,1],np.NaN,np.NaN,0,dat.iloc[5,1],np.NaN,np.NaN,0,dat.iloc[6,1],np.NaN,np.NaN,0,dat.iloc[7,1],np.NaN,np.NaN]
        datt= pd.DataFrame()
        datt1= pd.DataFrame()
        datt2= pd.DataFrame()
        datt1['X-axis'] = X_axis
        y1 = []
        for j in range(0,datt1.shape[0]):
            y1.append(j)
        datt1['no'] = y1  
        datt2['Y-axis'] = Y_axis
        datt = pd.concat([datt1,datt2],axis=1)
        
        t1 = []
        
        for r in range(2,datt.shape[0]+2):
            t1.append(r)
        datt['S X axis'] = t1
        datt = pd.concat([data2,datt],axis=1)
        data_l2 = data_l2.dropna()   
        data_l2  = data_l2.drop_duplicates(subset='notes')
        df_notes = data_l2
        
        
        Search_for_These_values = ['losses', 'losses rate'] #creating list
        
        pattern = '|'.join(Search_for_These_values) 
        df_losses = df_notes
        df_losses['losses_available'] = df_notes['notes'].str.contains(pattern)
        
        # Remove the rows that does not contain the word losses
        
        df_losses = df_losses[df_losses.losses_available == True]

        df_losses['time_from'] = df_losses.notes.str[0:5]

        df_losses['time_to'] = df_losses.notes.str[6:11]

        df_losses['duration'] = df_losses.notes.str[12:17]

        df_losses['depth_start'] = df_losses.notes.apply(lambda x: depth_start(x))
        df_losses['depth_start']  = df_losses['depth_start'].str.join(', ')

        try:
            df_losses['depth_start']  = df_losses['depth_start'].astype(float)
        except:
            pass

        df_losses['depth_end'] = df_losses.notes.apply(lambda x: depth_end(x))
        df_losses['depth_end']  = df_losses['depth_end'].str.join(', ')
        try:
            df_losses['depth_end']  = df_losses['depth_end'].astype(float)
        except:
            pass
        df_losses['losses_raw'] = df_losses.notes.apply(lambda x: losses_raw(x))
        df_losses['dummy_index'] = df_losses.index

        Search_for_These_values1 = ['losses', 'losses rate'] #creating list

        pattern1 = '|'.join(Search_for_These_values1) 

        df_losses['losses_test'] = df_losses['losses_raw'].str.contains(pattern1)
        df_losses = df_losses[df_losses.losses_test == True]

        df_losses.loc[df_losses.losses_raw.str.contains('rate'), 'dummy'] = 'Yes'

        df_losses1 = df_losses[df_losses.dummy != 'Yes']
        df_losses2 = df_losses[df_losses.dummy == 'Yes']
        df_losses1 = df_losses1.reset_index()
        df_losses2 = df_losses2.reset_index()

        df_losses1['loss'] = df_losses1['losses_raw'].apply(lambda x: losses11(x))

        df_losses2['loss'] = df_losses2.losses_raw.apply(lambda x: losses1(x))

        def types(t):
            
                pass

        def emptt():
            
                pass
                

        df_losses_final = pd.concat([df_losses1, df_losses2])

        df_losses_final = df_losses_final.sort_values(by='dummy_index', ascending=True)
        df_losses_final['loss']  = df_losses_final['loss'].str.join(', ')

        
        Search_for_These_values2 = ['1','2','3','4','5','6','7','8','9','0']
        pattern2 = '|'.join(Search_for_These_values2) 
        df_losses_final['losses_available1'] = df_losses_final['loss'].str.contains(pattern2)
        df_losses_final = df_losses_final[df_losses_final.losses_available1 == True]

        
        df_losses = df_losses_final
        df_losses['L X axis'] = 1.7
        df_losses = df_losses.drop_duplicates(subset = 'depth_start')
        #df_losses['depth_start'] = df_losses['depth_start'].astype(float)
        #df_losses.depth_start = df_losses.depth_start.fillna(value=np.nan,inplace=True)
        #df_losses = df_losses.dropna(subset='depth_start',inplace=True)
        
        #df_losses.to_excel("tttt.xlsx")
        
        
        #### well controll
        
        Search_for_These_values4 = ['well flow', 'kick' , 'kill' , 'well control'] #creating list

        pattern4 = '|'.join(Search_for_These_values4) 
        df_kick = df_notes
        df_kick['flow_available'] = df_kick['notes'].str.contains(pattern4)

        # Remove the rows that does not contain the word losses

        df_kick = df_kick[df_kick.flow_available == True]

        df_kick['time_from'] = df_kick.notes.str[0:5]

        df_kick['time_to'] = df_kick.notes.str[6:11]

        df_kick['duration'] = df_kick.notes.str[12:17]

        df_kick['depth_start'] = df_kick.notes.apply(lambda x: depth_start(x))
        df_kick['depth_start']  = df_kick['depth_start'].str.join(', ')

        try:
            df_kick['depth_start']  = df_kick['depth_start'].astype(float)
        except:
            pass

        df_kick['depth_end'] = df_kick.notes.apply(lambda x: depth_end(x))
        df_kick['depth_end']  = df_kick['depth_end'].str.join(', ')
        try:
            df_kick['depth_end']  = df_kick['depth_end'].astype(float)
        except:
            pass
        df_kick['kick_raw'] = df_kick.notes.apply(lambda x: kick_raw(x))
        df_kick['kick_available1'] = df_kick['kick_raw'].str.contains(pattern2)
        df_kick = df_kick[df_kick.kick_available1 == True]
        df_kick['W X axis'] = 1.4
        df_kick = df_kick.drop_duplicates(subset = 'depth_start')                
        
                
        #### Fish
        
        Search_for_These_values5 =  ['fish', 'left in hole' , 'fishing' , 'L I H' ] #creating list

        pattern5 = '|'.join(Search_for_These_values5) 
        df_fish = df_notes
        df_fish['fish_available'] = df_fish['notes'].str.contains(pattern5)

        # Remove the rows that does not contain the word losses

        df_fish = df_fish[df_fish.fish_available == True]

        df_fish['time_from'] = df_fish.notes.str[0:5]

        df_fish['time_to'] = df_fish.notes.str[6:11]

        df_fish['duration'] = df_fish.notes.str[12:17]

        df_fish['depth_start'] = df_fish.notes.apply(lambda x: depth_start(x))
        df_fish['depth_start']  = df_fish['depth_start'].str.join(', ')

        try:
            df_fish['depth_start']  = df_fish['depth_start'].astype(float)
        except:
            pass

        df_fish['depth_end'] = df_fish.notes.apply(lambda x: depth_end(x))
        df_fish['depth_end']  = df_fish['depth_end'].str.join(', ')
        try:
            df_fish['depth_end']  = df_fish['depth_end'].astype(float)
        except:
            pass
        #df_fish['fish_raw'] = df_fish.notes.apply(lambda x: fish_raw(x))
        #df_fish['fish_available1'] = df_fish['fish_raw'].str.contains(pattern2)
        #df_fish = df_fish[df_fish.fish_available1 == True]
        df_fish['F X axis'] = 1.1
        df_fish = df_fish.drop_duplicates(subset = 'depth_start')
                
        
        
        ### graph
        datt = datt.sort_values(by=['no'],ascending=True)
        dfl = pd.DataFrame()
        dfl['depth_start'] = df_losses['depth_start']
        dfl['L X axis'] = df_losses['L X axis']
         
        dfw = pd.DataFrame()
        #dfw = df_kick[['depth_start','W X axis']]
        dfw['depth_start'] = df_kick['depth_start']
        dfw['W X axis'] = df_kick['W X axis']
        
        dff = pd.DataFrame()
        #dff = df_fish[['depth_start','F X axis']]
        dff['depth_start'] = df_fish['depth_start']
        dff['F X axis'] = df_fish['F X axis']
        
        dft = pd.DataFrame()
        #dft = datt[['X-axis','Y-axis','CSD','S X axis']]
        dft['X-axis'] = datt['X-axis']
        dft['Y-axis']= datt['Y-axis']
        dft['S X axis'] = datt['S X axis']
        dft['CSD'] = datt['CSD']
        
        dft['X-axis'] = pd.to_numeric(dft['X-axis'],downcast='float')
        dft['Y-axis'] = pd.to_numeric(dft['Y-axis'],downcast='float')
        dft['S X axis'] = pd.to_numeric(dft['S X axis'],downcast='float')
        #dft['CSD'] = pd.to_numeric(dft['CSD'],downcast='float')
        
        #dfl = dfl.fillna(value=np.nan,inplace=True)
        #dfl = dfl.dropna(subset='depth_start',inplace=True)
        
        #dfl = pd.DataFrame()
        #dfw = pd.DataFrame()
        #dff = pd.DataFrame()
        
        dfl['depth_start'] = pd.to_numeric(dfl['depth_start'],downcast='float')
        dfw['depth_start'] = pd.to_numeric(dfw['depth_start'],downcast='float')
        dff['depth_start'] = pd.to_numeric(dff['depth_start'],downcast='float')
        
        dfl['L X axis'] = pd.to_numeric(dfl['L X axis'],downcast='float')
        dfw['W X axis'] = pd.to_numeric(dfw['W X axis'],downcast='float')
        dff['F X axis'] = pd.to_numeric(dff['F X axis'],downcast='float')
        
        dtr = pd.DataFrame()
        dtr['S X axis'] = dft['X-axis'] 
        dtr['CSD'] = dft["Y-axis"]
        dtr = dtr.dropna()
        dtr = dtr[dtr['CSD']!=0.0]
        
        graph, ax = plt.subplots(1)
        xf = (dff[['F X axis']])
        yf = (dff[['depth_start']])
        xc = (dft[['X-axis']])
        yc = (dft[['Y-axis']])
        xw = (dfw[['W X axis']])
        yw = (dfw[['depth_start']])
        x = (dtr[['S X axis']])
        xl =((dfl[['L X axis']]))
        y = (dtr[['CSD']])
        yl = (dfl[['depth_start']])
        ax.scatter(xl,yl,marker='X',label = 'Losses',color = 'y')
        ax.scatter(xw,yw,marker='X',label = 'Well control',color='r')
        ax.scatter(xf,yf,marker='X',label = 'Fish',color = 'brown')
        ax.scatter(x,y,marker=9,label = 'Shoe',color="k")
        ax.plot(xc,yc,color='k')
        ax.invert_yaxis()
        ax.axes.xaxis.set_visible(False)
        leg = ax.legend(loc='lower right',frameon=False);
        #plt.show()
        #plt.savefig("STICK CHART--t.jpg")
        
        summaryshow = pd.DataFrame()
        summaryshow['SUMMARY'] = data["SUMMARY"]
        qw = []
        for er in range(1,summaryshow.shape[0]+1):
            qw.append(er)
        summaryshow['DAYS'] = qw
        summaryshow = summaryshow.set_index("DAYS")
        lossshow = df_losses[['depth_start','depth_end','losses_raw']]
        lossshow['depth_start'] = pd.to_numeric(lossshow['depth_start'],downcast='signed')
        lossshow = lossshow.dropna(subset='depth_start')
        lossshow = lossshow.set_index("depth_start")
        
        
        
        kickshow = df_kick[['depth_start','depth_end','kick_raw']]
        kickshow['depth_start'] = pd.to_numeric(kickshow['depth_start'],downcast='signed')
        kickshow = kickshow.dropna(subset='depth_start')
        kickshow = kickshow.set_index("depth_start")
        
        
        
        fishshow = df_fish[['depth_start','depth_end']]
        fishshow = fishshow.set_index("depth_start")
        st.text("COMPLETED ....")
        st.text("STICK-CHART")
        st.pyplot(plt)
        #sum_button = st.button("SUMMARY OF THE WELL")
        #if sum_button:
        st.text("LOSS-SUMMARY")
        st.dataframe(lossshow)
        st.text("KICK-SUMMARY")
        st.dataframe(kickshow)
        st.text("SUMMARY OF THE WELL")
        st.table(summaryshow)
            
        #sum1_button = st.button("LOSSES")
        #if sum1_button:
        
        
        #sum_button2 = st.button("KICK-SUMMARY")
        #if sum_button2:
        
            
        #sum_button3 = st.button("FISH-SUMMARY")
        #if sum_button3:
        #st.dataframe(fishshow)
        
      
main()
