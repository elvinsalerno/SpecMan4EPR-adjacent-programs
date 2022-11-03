# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 11:42:28 2022

@author: esalerno
"""


import numpy as np
import matplotlib.pyplot as plt



#This is for testing only this script
input_directory=r'C:\Users\evsal\Google Drive\MagLab\LuPO4_Eu2plus'
input_filename='Eu2LuPO4_5K_15dB_ELDOR_93.5to94.5GHz_ctr94GHz'
filename_in=input_directory+'\\'+input_filename






def load_binary_fcn(filename_in):
    filename_in=filename_in+'.d01'
    f = open(filename_in, "r")
    a = np.fromfile(f, dtype=np.uint32,count=1000)
    f.close()
    #print(a)

    ndim1=a[0]
    dformat=a[1]

    if dformat==1:
      sformat='float32'
    else:
      sformat='double'




    dstrms=[]
    ntotal=1

    #because first two are general info, and data is contained in each subsequent set of 6
    num_header=2+ndim1*6

    dim_info=[]
    for i in range(0,ndim1):
        dim_info.append(a[2+i*6:2+(i+1)*6])
    dim_info=np.array(dim_info)
    
    #print(dim_info)

    


    #print(sformat)
    f = open(filename_in, "r")
    b = np.fromfile(f, dtype='float32',offset=0)
    b=b[num_header:]
    #print(b[0],b[6000*201:6000*201+10])



    data_in=[]


    for i in range(0,ndim1):#len(dim_info)):
        
        data_offset=np.sum(dim_info[0:i,5])
        #print(data_offset)
        data_temp=[]

        for k in range(0,dim_info[i,2]):
            data_temp.append(b[dim_info[i,1]*k+data_offset:dim_info[i,1]*(k+1)+data_offset])
        data_in.append(data_temp)

    data_in=np.array(data_in)
    #print(data_in)
    return data_in, dim_info

if __name__=="__main__":
    data=load_binary_fcn(filename_in)
    print(np.shape(data))
    for i in range(0,np.shape(data)[0]):
        for j in range(0,np.shape(data)[1]):
            plt.plot(data[i][j])

    #plt.show()
    plt.close()

#fig = plt.figure(num=3,figsize=(3.25,2.25), dpi=300)
#import matplotlib.cm as cm
#colors = cm.rainbow(np.linspace(0.,1, 201))







