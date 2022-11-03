# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 18:09:46 2021

@author: hiper
"""








input_directory=r"C:\Users\evsal\Google Drive\MagLab\Jon_fft_data"
input_filename="Jon_off_combined"

input_directory=r"C:\Users\evsal\Google Drive\MagLab\short_biradical_wintyer_break\1mM"
input_filename="ChirpEcho_4dB_93.5to94.5_t90_1.6us_100Kshots_holeat94.02"


Col=[0,1]



#cutoff_ind=[0,900]

f_add=94.

#time between samples, in picoseconds
sampling=500




###############################################################################
###############################################################################
###############################################################################
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np




filetype='.dat'

filename_in="".join(["\\",input_filename])
filename_comby=input_directory+filename_in+filetype

print(filename_comby)

font = {'family' : 'Verdana',
        'weight' : 'normal',
        'size'   : 12}
plt.rc('font', **font)


fig = plt.figure(num=2,figsize=(3.25,2.25), dpi=300)

raw_data = np.genfromtxt(filename_comby,skip_header=1)#,delimiter=',')



    
#def fourier_func(Col): 
def fourier_fcn(times_in,re_in,im_in,sampling=500e-12,f_add=94):    
    times=times_in
    data_im=im_in
    data_re=re_in
    
    T=sampling
    
    data = [data_im[i]+ 1j* data_re[i] for i in range(len(data_im)) ]  
        
    from scipy.fft import fft, fftfreq
    # Number of sample points
    N = len(times)

    y =data-np.mean(data)
    yf = fft(y)
    
    xf = fftfreq(N, T)#[:N//2]
    
    yf = np.fft.fftshift(yf)
    xf = np.fft.fftshift(xf)
    
    xf=xf/1e9+f_add
    
    yf=(np.sqrt(np.real(yf)**2+np.imag(yf)**2))
    
    fix_zero_point=f_add
    fix_zero='on'
    if fix_zero=='on':
        idx = np.where(xf == fix_zero_point)[0][0]
        avg_point = (yf[idx - 1] + yf[idx +1])/2
        yf = np.where(xf == fix_zero_point , avg_point , yf)

    else:
        pass
    return xf,yf

    
xfL=[]
yfL=[]


for i in Col:
    times=raw_data[:,0]
    data_im=raw_data[:,2*i+1]
    data_re=raw_data[:,2*i+2]
    

    x,y=fourier_fcn(times,data_im,data_re,500e-12,94)
    xfL.append(x)
    yfL.append(y)
    

for i in range(0,len(xfL)):
    #plt.plot(xxx.exp_axes[0],xxx.integrated_arr_norm[i])
    #plt.plot(xxx.exp_axis_modded,xxx.active_integ_data[i])
    plt.plot(xfL[i],yfL[i])
    plt.xlabel("GHz")
    plt.ylabel('intensity')

    




###################################
"""

plt.figure(1)


plt.plot(times_list[0],im_list[-1],label='last_trace_re')
plt.plot(times_list[0],re_list[-1],label='last_trace_im')
plt.legend()
#plt.show()
#plt.xlim(0,5e-7)



plt.vlines(times_list[0][cutoff_ind[0]],min(im_list[-1]),max(re_list[-1]),'k',zorder=10)
plt.vlines(times_list[0][cutoff_ind[1]],min(im_list[-1]),max(re_list[-1]),'k',zorder=9)
#plt.xlim(0,0.25e-6)





plt.figure(3)
plt.plot(cut_times_list[0],cut_re_list[0])
plt.plot(cut_times_list[0],cut_im_list[0])
##################################


xf_list=np.array(xf_list)
xf_list=np.mean(xf_list,axis=0)

yf_list=np.array(yf_list)
yf_list=np.mean(yf_list,axis=0)

theta_list=np.array(theta_list)
theta_list=np.mean(theta_list,axis=0)




if normalize_on=='on':
    yf_list=yf_list/max(yf_list)
else:
    pass


# remove 94GHz frequency
'''
idx = np.where(xf_list == 94.0)
xf_list = xf_list[xf_list  != 94.0]
yf_list = np.delete(yf_list , idx)

'''
# replace zero frequency point by the average
if fix_zero=='on':
    idx = np.where(xf_list == fix_zero_point)[0][0]
    avg_point = (yf_list[idx - 1] + yf_list[idx +1])/2
    yf_list = np.where(xf_list == fix_zero_point , avg_point , yf_list)
    
    idx_theta = np.where(xf_list == fix_zero_point)[0][0]
    avg_theta=(theta_list[idx_theta - 1] + theta_list[idx_theta +1])/2
    theta_list=np.where(xf_list == fix_zero_point , avg_theta , theta_list)
    
else:
    pass


#deal with angle between im and re


fig = plt.figure(num=123,figsize=(3.25,2.25), dpi=300)
plt.figure(123)
plt.plot(xf_list,abs(theta_list*180/np.pi))
#plt.xlim(93.9,94.1)
plt.xlim(xlim)
plt.xlabel('GHz')
plt.ylabel('theta (deg)')

print((theta_list)*(180/np.pi))








#plt.ylim(0,3)
plt.figure(2)
plt.plot(xf_list, yf_list, '-b')
#plt.xlim(70,110)
#plt.xlim(-.2,.2)
#plt.ylim(0,6)
plt.xlabel("GHz")
plt.ylabel('intensity')



if print_data=='on':
    print('\nxf\n')
    print(*xf_list,sep=',')
    print('\n')
    print('yf\n')
    print(*yf_list,sep=',')
else:
    pass

sum_y=np.sum(yf_list)


plt.xlim(xlim)



x_axis_label='GHz'

"""
plt.show()