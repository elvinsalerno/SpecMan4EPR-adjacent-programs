
#This is for testing only this script
input_directory=r'C:\Users\esalerno\Google Drive\MagLab\LuPO4_Eu2plus'
input_filename='Eu2LuPO4_5K_15dB_ELDOR_93.5to94.5GHz_ctr94GHz'


#input_directory=r"C:\Users\esalerno\Google Drive\MagLab\short_biradical_wintyer_break\1mM"
#input_filename="ChirpEcho_4dB_93.5to94.5_t90_1.6us_100Kshots_holeat94.02"

input_directory=r"C:\Users\esalerno\Google Drive\MagLab\Miguel\MG-III-530_Gd3_C3\MG_VIII_530_Gd3_1percent\Round4\12202022\hole_burning_definitive"
input_filename="Boldenhausen_Fourier_det_obs93.5to94.5GHz_15dB_3.67T_center94.0Ghz_Amp0.4_varypumpFreq_93.5to94.1GHz_pumpamp0.5"

filename_in=input_directory+'\\'+input_filename

#filename_in="C:/Users/evsal/Google Drive/MagLab/Frank_Natia/CoAPSO_1uM_08092022/08162022/5uM_CoPhen_50K_10dB_pfT1_08162022_5"

import matplotlib.pyplot as plt
import numpy as np
from load_exp_SpecMan import load_exp_fcn
from load_d01_SpecMan import load_binary_fcn
import re





class load_data():
    def __init__(self, filename_in):
        self.filename=filename_in
        #print('filename',self.filename)
        
        self.axes_list,self.units_list,self.transient_line,self.sampling,self.sampling_units=load_exp_fcn(self.filename)

        self.n_signals=len(self.transient_line)-5
        self.I_or_T=self.transient_line[2]

        if self.n_signals==2:
            self.signal_labels=['real','imag']
        else:
            self.signal_labels=self.transient_line[5:]

        self.data_in=load_binary_fcn(self.filename)[0]
        self.exp_dimensionality=load_binary_fcn(self.filename)[1]
        self.integrated_arr=[]
        self.data_BL_corr = self.data_in.copy()
        self.baseline_indices=[100,200]
        self.integration_indices=[0,100]
        self.integrated_arr_norm=[]

        self.normalize=False
        self.im_re_magn=False
        self.avg_exp=False
        self.active_integ_data=[]

        self.fourier_on=False
        self.fft_xf=[]
        self.fft_yf=[]
        self.fourier_freq_add=0
        self.fourier_freq="GHz"

        
        #Dictionary defining essential unit orders
        self.units_indices={"p":1e-12,"n":1e-9,"u":1e-6,"m":1e-3,"k":1e3,"M":1e6,"G":1e9}


        if self.I_or_T=='T':
            self.exp_axes=self.axes_list.copy()[1:]
            self.transient_axis=self.axes_list.copy()[0]
            self.transient_max=np.amax(self.data_in)
            self.transient_min=np.amin(self.data_in)
            self.exp_axis_modded=self.exp_axes.copy()
        if self.I_or_T=='I':
            self.exp_axes=self.axes_list.copy()
            self.transient_max=1
            self.transient_min=0
        


    #get the magnitude of an array given two+ other components (eg re+im)
    def magn_fcn(self,data_in_arr):
        for i in range(0,len(data_in_arr)):
            if i==0:
                magn = (data_in_arr[i])**2
            else:
                magn += (data_in_arr[i])**2
        magn=np.sqrt(magn)
        return magn


    #fcn to find the index of number in array which is closest to specified
    def closest_idx_fcn(self,input_arr,specified):
        specific_value=min(input_arr, key=lambda x:abs(x-specified))
        index_desired, = np.where(input_arr == specific_value)
        return index_desired
    def closest_idx_baseline(self,baseline_lim_1,baseline_lim_2):
        baseline_indices=[]
        baseline_indices.append(self.closest_idx_fcn(self.transient_axis,baseline_lim_1)[0])
        baseline_indices.append(self.closest_idx_fcn(self.transient_axis,baseline_lim_2)[0])
        self.baseline_indices=baseline_indices
    def closest_idx_integration(self,integration_lim_1,integration_lim_2):
        integration_indices=[]
        integration_indices.append(self.closest_idx_fcn(self.transient_axis,integration_lim_1)[0])
        integration_indices.append(self.closest_idx_fcn(self.transient_axis,integration_lim_2)[0])
        self.integration_indices=integration_indices        


    #function to apply baseline correction given the data, the x values, and the baseline limits
    def apply_baseline_correction(self):
        for i in range(0,self.n_signals):
            for j in range(0,len(self.data_in[i])):
                points_for_averaging=self.data_in[i,j,self.baseline_indices[0]:self.baseline_indices[1]]
                avg=np.mean(points_for_averaging)
                self.data_BL_corr[i,j]=self.data_in[i,j]-avg
        

    def apply_integration_fcn(self,data_arr):
        temp_integrated_arr=[]
        for j in range(0,len(data_arr)):
            points_for_integration=data_arr[j,self.integration_indices[0]:self.integration_indices[1]]
            integs=np.sum(points_for_integration)
            temp_integrated_arr.append(integs)
        return np.array(temp_integrated_arr)
    

    def swap_IR(self):
        self.data_in[[0,1]]=self.data_in[[1,0]]

    def do_integration(self):
        if self.I_or_T=="T":
            temp_integs=[]
            for i in range(0,len(self.data_BL_corr)):
                temp_integs.append(self.apply_integration_fcn(self.data_BL_corr[i]))
            temp_integs.append(self.apply_integration_fcn(self.magn_fcn(self.data_BL_corr)))
            self.integrated_arr=np.array(temp_integs)
        elif self.I_or_T=='I':
            self.integrated_arr=self.data_in.copy()
            self.integrated_arr=np.append(self.integrated_arr,np.array([self.magn_fcn(self.data_in)]),axis=0)
            self.integrated_arr=self.integrated_arr.transpose((0, 2, 1))

    def set_active_integ_data(self):
        
        if self.im_re_magn==True: #If true plot im/re
            if self.normalize==True:
                self.active_integ_data=self.integrated_arr[0:-1]
                maximum=np.amax(self.active_integ_data)
                self.active_integ_data = self.active_integ_data/maximum

            else:
                self.active_integ_data=self.integrated_arr[0:-1]
        else:
            if self.normalize==True:
                self.active_integ_data=[self.integrated_arr[-1]]
                maximum=np.amax(self.active_integ_data)
                self.active_integ_data = self.active_integ_data/maximum

            else:
                self.active_integ_data=[self.integrated_arr[-1]]

        if self.fourier_on==True and self.I_or_T=='T':
            self.do_fourier()
            self.active_integ_data=self.fft_yf
            if self.normalize==True:
                self.active_integ_data=self.active_integ_data/np.amax(self.active_integ_data)
        else:
            pass

    
        if self.avg_exp==True:
            if len(np.shape(self.active_integ_data)) >=3:
                self.active_integ_data=np.mean(self.active_integ_data,axis=2)
            elif self.fourier_on==True:
                self.active_integ_data=[np.mean(self.active_integ_data,axis=0)]
        else:
            pass

    def set_n_traces(self,first_trace=str(0),last_trace=str(-1)):
        first_trace=first_trace.replace(" ", "")
        last_trace=last_trace.replace(" ", "")

        #If they're not numbers, then set from 0:end
        if first_trace.isdigit()==False or first_trace=='':
            first_trace='0'
        if last_trace.isdigit()==False or last_trace=='':
            last_trace='-1'
        if first_trace=='0' and last_trace=='-1':
            pass
        else:
            xxx=[]
            for i in range(0,len(self.active_integ_data)):
                xxx.append(self.active_integ_data[i][int(first_trace):int(last_trace)])
            self.exp_axis_modded=self.exp_axis_modded[int(first_trace):int(last_trace)]
            self.active_integ_data=np.array(xxx)
        #if using fourier data then just set it to fft_xf
        if self.fourier_on==True:
            self.exp_axis_modded=self.fft_xf[0]#self.transient_axis[self.integration_indices[0]:self.integration_indices[1]]
    ###########################


    #Program to see if units are specified, if so then return the conversion
    #If not then return 1
    def check_units(self,string_in):
        if string_in in self.units_indices:
            return self.units_indices[string_in]
        else:
            return 1

    #############################

    def fourier_fcn(self,times_in,re_in,im_in,sampling=500e-12,f_add=94,frequency='GHz'):    
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
        
        freq_dict={"THz":1e12,"GHz":1e9,"MHz":1e6,"kHz":1e3,"Hz":1}

        xf=xf/freq_dict[frequency]+f_add
        
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

    def do_fourier(self):
        self.fft_xf=[]
        self.fft_yf=[]
        if self.I_or_T=='I':
            return
        else:
            pass

        for i in range(0,np.shape(self.data_in)[1]):
            #print(self.data_in[i][0][0:100])
            xf,yf=self.fourier_fcn(self.transient_axis[self.integration_indices[0]:self.integration_indices[1]],self.data_in[0][i][self.integration_indices[0]:self.integration_indices[1]],self.data_in[1][i][self.integration_indices[0]:self.integration_indices[1]],self.sampling,self.fourier_freq_add,self.fourier_freq)
            self.fft_xf.append(xf)
            self.fft_yf.append(yf)
        self.fft_xf=np.array(self.fft_xf)
        self.fft_yf=np.array(self.fft_yf)
        #for j in range(0,len(data_arr)):
        #    points_for_integration=data_arr[j,self.integration_indices[0]:self.integration_indices[1]]

    def str_to_math(self,innumb,stringaling):
        #Remove the whitespace
        stringaling=stringaling.replace(" ", "")
        #split the string into a list of operators and numbers
        res = re.findall(r'[0-9\.]+|[^0-9\.]+', stringaling)
        #split the list pairwise 
        www=[res[i:i+2] for i in range(0, len(res), 2)]
        numby=innumb
        for i in range(0, len(www)):
            if 'e-' in www[i][0]:
                numby=numby*10**(-float(www[i][1]))
            elif 'e' in www[i][0]:
                numby=numby*10**(float(www[i][1]))
            elif "*" in www[i][0]:
                numby=numby*float(www[i][1])
                #*=float(www[i][1])
            elif "/" in www[i][0]:
                numby=numby/float(www[i][1])
            elif "+" in www[i][0]:
                numby=numby+float(www[i][1])
            elif "-" in www[i][0]:
                numby=numby-float(www[i][1])
        return numby

    def modify_integ_x_axis(self,string_in):
        #change the x axis, take the data in and copy it, then see if the matching units 
        #are relevant 
        #print(self.fft_xf)
        if self.fourier_on==True:
            self.exp_axis_modded=self.fft_xf#np.array(self.transient_axis)
            self.exp_axis_modded=self.str_to_math(self.exp_axis_modded,string_in)
        else:
            self.exp_axis_modded=self.str_to_math(self.exp_axes[0].copy()/self.check_units(self.units_list[0][0]),string_in)



    def update_data_fcn(self,bl1,bl2,il1,il2,mathstring,first_trace_in=str(0),last_trace_in=str(-1)):
        if self.I_or_T=="T":
            self.closest_idx_baseline(bl1,bl2)
            self.apply_baseline_correction()
            self.closest_idx_integration(il1,il2)

        #update_fourer

        self.do_integration()
        self.modify_integ_x_axis(mathstring)
        self.set_active_integ_data()
        
        self.set_n_traces(first_trace_in,last_trace_in)

    def fit_fcn_handler(self,fit_data='t2',guess=[],timescale='none'):
        self.fitted_x_arr=[]
        self.fitted_y_arr=[]
        if len(np.shape(self.active_integ_data))==2:
            print(self.filename)
            for j in range(0,len(self.active_integ_data)):
                print('dataset',j)
                fitted_x,fitted_y=self.fit_t1_t2(self.exp_axis_modded[:],self.active_integ_data[j][:],fit_data=fit_data,guess=guess,timescale=self.units_list[0])
                self.fitted_x_arr.append(fitted_x)
                self.fitted_y_arr.append(fitted_y)

        elif len(np.shape(self.active_integ_data))==3:
            xxx=np.array(self.active_integ_data)
            xxx=np.swapaxes(xxx,1,2)
            print(self.filename)
            for j in range(0,np.shape(self.active_integ_data)[0]):
                for k in range (0,np.shape(self.active_integ_data)[2]):
                    print('dataset',j, k)
                    fitted_x,fitted_y=self.fit_t1_t2(self.exp_axis_modded[:], xxx[j,k,:],fit_data=fit_data,guess=guess,timescale=self.units_list[0])
                    self.fitted_x_arr.append(fitted_x)
                    self.fitted_y_arr.append(fitted_y)


    def fit_t1_t2(self,x_data,y_data,fit_data='no',guess=[],timescale='ns'):
        if fit_data=='t1' or fit_data=='t2':
            if len(guess)!=3:
                if timescale=='us':
                    guess=[6,1000, 1]
                elif timescale=='ms':
                    guess=[6,0.001,1]
                else:
                    guess=[6,1000,1]
                    
        if fit_data=='2t1' or fit_data=='2t2':
            if len(guess)!=5:
                if timescale=='us':
                    guess=[0.6,3, 1.5, 0.4, 2]
                elif timescale=='ms':
                    guess=[0.6,0.001,1,0.4,0.002 ]
                else:
                    guess=[0.6,3000,3, 0.4, 2000]

        if fit_data=='t2':
            def expon(t,N0,k,c):
                return N0*np.exp(-t/k)+c
        elif fit_data=='t1':
            def expon(t,N0,k, c):
                return -N0*np.exp(-t/k) + c
        elif fit_data=='2t1':
            def expon(t,N0_1,k1, c,N0_2,k2):
                return -(N0_1/(N0_1+N0_2))*np.exp(-t/k1) - (N0_2/(N0_1+N0_2))*np.exp(-t/k2) + c
        elif fit_data=='2t2':
            def expon(t,N0_1,k1,c,N0_2,k2):
                return (N0_1/(N0_1+N0_2))*np.exp(-t/k1)+(N0_2/(N0_1+N0_2))*np.exp(-t/k2)+c


        times_sim=np.linspace(x_data[0],x_data[-1],1000)
        Boundz=(0,np.inf)

        if fit_data=='t1' or fit_data=='t2' or fit_data=='2t2' or fit_data=='2t1':
            from scipy.optimize import curve_fit
                
            pars, pcov = curve_fit(expon,x_data,y_data, p0=guess,bounds=Boundz,maxfev=1000000)#,bounds=(0,np.inf),maxfev=3800)
        
            if fit_data=='t1' or fit_data=='t2':
                plt.plot(times_sim,expon(times_sim,*pars),'r--')#,label=str(round(pars[1],2))+' '+timescale )
                print('N_0 =',pars[0],'\n','rate1 =',pars[1]**-1,'\n' , 'lifetime =',pars[1],'\n','C =',pars[2],'\n')

                print('error of lifetime = ', np.sqrt(np.diag(pcov))[1])
                
            elif fit_data=='2t2' or fit_data=='2t1':
                plt.plot(times_sim,expon(times_sim,*pars),'r--')#,label=str(round(pars[1],2))+', '+str(round(pars[4],2))+' '+timescale )
                print('N0_1 =',pars[0],'(',pars[0]/(pars[0]+pars[4]),')','\n','rate_1 =',pars[1]**-1, '\n' , 'lifetime_1 =',pars[1],'\n','*******************','\n','N0_2 =',pars[4],'(',pars[4]/(pars[0]+pars[4]),')','\n','rate_2 =',pars[4]**-1,'\n','lifetime_2 =',pars[4],'\n','*****************','\n','C =',pars[2],'\n')
            
            
            else:
                pass
            #plt.legend()
            return times_sim,expon(times_sim,*pars)
        else:
            return False











if __name__=='__main__':
    xxx=load_data(filename_in)
    print(filename_in)
    xxx.im_re_magn=True
    #xxx.avg_exp=False
    xxx.fourier_on=True
    xxx.avg_exp=True
    #xxx.do_fourier()
    #xxx.modify_integ_x_axis('')
    xxx.swap_IR()
    xxx.set_active_integ_data()
    xxx.update_data_fcn(000e-9,10000e-9,0e-9,1500e-9,'*1','0','-1')


    print(np.shape(xxx.fft_xf))
    print(np.shape(xxx.exp_axis_modded))
    print(np.shape(xxx.active_integ_data))
    print(np.shape(xxx.fft_yf))
    for i in range(0,len(xxx.active_integ_data)):
        #plt.plot(xxx.exp_axes[0],xxx.integrated_arr_norm[i])
        plt.plot(xxx.exp_axis_modded,xxx.active_integ_data[i])
        #plt.plot(xxx.fft_xf[i],xxx.fft_yf[i])
    plt.show()
    plt.close()


