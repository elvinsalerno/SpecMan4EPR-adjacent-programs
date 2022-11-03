

from data_objects_class import load_data
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib

#This is for testing only this script
filename_list=[r'C:\Users\esalerno\Google Drive\MagLab\LuPO4_Eu2plus\Eu2LuPO4_5K_15dB_t2_3.312T_T2']



font = {'family' : 'Verdana',
        'weight' : 'normal',
        'size'   : 12}
plt.rc('font', **font)


def create_data_objects(filename_list):
    data_objects=[]

    print('data loaded:')

    x_axis_data_types=[]
    for i in range (0,len(filename_list)):
        data_objects.append(load_data(filename_list[i]))
        #Load and do first integration with these baseline and integration limits
        data_objects[i].update_data_fcn(0,1000e-9,0,1000e-9,'*1')

        x_axis_data_types.append(data_objects[i].units_list[0])

        print(filename_list[i])
        #print('number of traces ',i, ' ', len(data_objects[i].data_in[0]))
        print('data structure', data_objects[i].I_or_T, np.shape(data_objects[i].data_in),'\n')
    #check if all objects have identical x axes, give a warning if not
    if all (element == x_axis_data_types[0] for element in x_axis_data_types):
        pass
    else:
        print ("the objects don't all have identical experimental axes...")
        print(*x_axis_data_types,sep=', ')

    return data_objects



def plot_the_transients(data_objects,i1,i2,bl1,bl2,DPI_in=100,magn_or_reim=False,plot_v_lines_in=True):
    if magn_or_reim==True:
        return plot_the_re_im_transients(data_objects,i1,i2,bl1,bl2,DPI=DPI_in,plot_vlines=plot_v_lines_in)
    else:
        return plot_the_magn_transients(data_objects,i1,i2,bl1,bl2,DPI=DPI_in,plot_vlines=plot_v_lines_in)



def plot_the_re_im_transients(data_objects,i1,i2,bl1,bl2,DPI=100,plot_vlines=True):
    plt.close(1)
    fig, axs = plt.subplots(2, sharex=True,num=1,figsize=(3.25,2.25), dpi=DPI)

    #this plots transients of re and im
    for i in range (0,len(data_objects)):
        if data_objects[i].I_or_T=='T':
            for j in range(0,len(data_objects[i].data_BL_corr)):
                #axs[j].set_title(data_objects[i].signal_labels[j])
                colors = cm.rainbow(np.linspace(0.,1, len(data_objects[i].data_BL_corr[j])))
                for k in range(0,len(data_objects[i].data_BL_corr[j])):
                    axs[j].plot(data_objects[i].transient_axis/1e-9,data_objects[i].data_BL_corr[j,k].T,color=colors[k])

                if plot_vlines==True:
                    axs[j].vlines(bl1*1e9,np.amin(data_objects[i].data_BL_corr),np.amax(data_objects[i].data_BL_corr),color='b')
                    axs[j].vlines(bl2*1e9,np.amin(data_objects[i].data_BL_corr),np.amax(data_objects[i].data_BL_corr),color='b')
                    axs[j].vlines(i1*1e9,np.amin(data_objects[i].data_BL_corr),np.amax(data_objects[i].data_BL_corr),color='r',linestyles='dashed')
                    axs[j].vlines(i2*1e9,np.amin(data_objects[i].data_BL_corr),np.amax(data_objects[i].data_BL_corr),color='r',linestyles='dashed')
                else:
                    pass
                axs[j].set_xlabel(data_objects[i].signal_labels[j])


                #Label the y axes
                axs[j].set_ylabel(data_objects[i].signal_labels[j])

    plt.xlabel('ns')

    plt.subplots_adjust(bottom=0.25,left=0.25)

    return fig

def plot_the_magn_transients(data_objects,i1,i2,bl1,bl2,DPI=100,plot_vlines=True):
    plt.close(1)
    #fig = plt.figure(num=2,figsize=(3.25,2.25), dpi=DPI)
    fig, axs = plt.subplots(1, sharex=True,num=1,figsize=(3.25,2.25), dpi=DPI)
    #this returns the magnitude
    def magn_fcn(data_in_arr):
        for i in range(0,len(data_in_arr)):
            if i==0:
                magn = (data_in_arr[i])**2
            else:
                magn += (data_in_arr[i])**2
        magn=np.sqrt(magn)
        return magn

    for i in range (0,len(data_objects)):
        if data_objects[i].I_or_T=='T':
            magn_data=magn_fcn(data_objects[i].data_BL_corr)
            colors = cm.rainbow(np.linspace(0.,1, np.shape(magn_data)[0]))
            for j in range(0,np.shape(magn_data)[0]):
                plt.plot(data_objects[i].transient_axis/1e-9,magn_data[j].T,color=colors[j])

            if plot_vlines==True:
                plt.vlines(bl1*1e9,np.amin(magn_data),np.amax(magn_data),color='b')
                plt.vlines(bl2*1e9,np.amin(magn_data),np.amax(magn_data),color='b')
                plt.vlines(i1*1e9,np.amin(magn_data),np.amax(magn_data),color='r',linestyles='dashed')
                plt.vlines(i2*1e9,np.amin(magn_data),np.amax(magn_data),color='r',linestyles='dashed')
            else:
                pass


    plt.xlabel('ns')#data_objects[0].units_list[0])
    plt.ylabel('magnitude')
    plt.subplots_adjust(bottom=0.25,left=0.25)

    return fig


def magn_fcn(data_in_arr):
    for i in range(0,len(data_in_arr)):
        if i==0:
            magn = (data_in_arr[i])**2
        else:
            magn += (data_in_arr[i])**2
    magn=np.sqrt(magn)
    return magn


def toggle_norm(data_objects,):
    for i in range (0,len(data_objects)):  
        data_objects[i].normalize= not data_objects[i].normalize
        data_objects[i].set_active_integ_data()

def toggle_re_im_magn(data_objects,):
    for i in range (0,len(data_objects)):  
        data_objects[i].im_re_magn= not data_objects[i].im_re_magn
        data_objects[i].set_active_integ_data()

def toggle_avg_exp(data_objects,):
    for i in range (0,len(data_objects)):
        data_objects[i].avg_exp= not data_objects[i].avg_exp
        data_objects[i].set_active_integ_data()  

def toggle_fourier(data_objects,freq_add,fourier_freq):
    for i in range (0,len(data_objects)):
        data_objects[i].fourier_on= not data_objects[i].fourier_on
        update_fourier(data_objects,freq_add,fourier_freq)
def update_fourier(data_objects,freq_add,fourier_freq):
    for i in range (0,len(data_objects)):
        data_objects[i].fourier_freq_add=freq_add
        data_objects[i].fourier_freq=fourier_freq
        data_objects[i].do_fourier()

        #data_objects[i].set_active_integ_data()


def plot_integrated(data_objects,DPI=100,x_label_in=False,fit_data='None',guess=[],timescale='none'):
    plt.close(3)
    #this plots the integrated

    fig, axs = plt.subplots(1, sharex=True,num=3,figsize=(3.25,2.25), dpi=DPI)

    for i in range (0,len(data_objects)):   
        #print(np.shape(data_objects[i].active_integ_data))
        for j in range(0,len(data_objects[i].active_integ_data)):
            #exp_axes is the first axis after the transient, or first if its integrated
            plt.plot(data_objects[i].exp_axis_modded,data_objects[i].active_integ_data[j])
    
    #This method also works
    """
    for i in range(0,len(data_objects)):
        if len(np.shape(data_objects[i].active_integ_data))==2:
            #pass
            for j in range(0,len(data_objects[i].active_integ_data)):
                plt.plot(data_objects[i].exp_axis_modded[:],data_objects[i].active_integ_data[j][:])

        elif len(np.shape(data_objects[i].active_integ_data))==3:
            xxx=np.array(data_objects[i].active_integ_data)
            xxx=np.swapaxes(xxx,1,2)
            for j in range(0,np.shape(data_objects[i].active_integ_data)[0]):
                for k in range (0,np.shape(data_objects[i].active_integ_data)[2]):
                    plt.plot(data_objects[i].exp_axis_modded[:], xxx[j,k,:])
    """

    if x_label_in!=False:
        plt.xlabel(x_label_in)
    elif data_objects[0].fourier_on==True:
        plt.xlabel(data_objects[0].fourier_freq)
    else:# x_label_in==False:
        plt.xlabel(data_objects[0].units_list[0])



    plt.ylabel('intensity')
    plt.subplots_adjust(bottom=0.25,left=0.25)
    #fig.subplots_adjust(bottom=0.2,left=0.2)

    #fit_data_and_plot(data_objects,fit_data=fit_data,guess=guess,timescale=timescale)
    if fit_data!='None':
        handle_fitted(data_objects,fit_data=fit_data,guess=guess,timescale=timescale)

    return fig

def handle_fitted(data_objects,fit_data='None',guess=[],timescale='none'):    
    for i in range(0,len(data_objects)):
        data_objects[i].fit_fcn_handler(fit_data=fit_data,guess=guess,timescale=timescale)
        for j in range(0,len(data_objects[i].fitted_x_arr)):
            plt.plot(data_objects[i].fitted_x_arr[j],data_objects[i].fitted_y_arr[j],'r--')

def swap_IR(data_objects):    
    for i in range(0,len(data_objects)):
        #print('yes')
        if data_objects[i].I_or_T == "T" and len (np.shape(data_objects[i].data_in))==3 and np.shape(data_objects[i].data_in)[0]==2:
            data_objects[i].swap_IR()


def save_fig_fcn(figurino,filename_to_save="saved_figure"):
    from PIL import Image
    from io import BytesIO
    #plt.tight_layout(rect=(0,0,1,1))
    #or use to adjust frame of saved photo:

    fig=figurino
    #fig.subplots_adjust(bottom=0.2,left=0.2)
    
    # save figure
    # (1) save the image in memory in PNG format
    png1 = BytesIO()

    fig.savefig(png1, format='png',bbox_inches='tight')
    # (2) load this image into PIL
    png2 = Image.open(png1)
    
    ##################################
    import os
    #Get directory where this script is running,
    #Then add '\figures' to it for desired directory
    MYDIR = [(os.path.dirname(__file__)),'figures']
    MYDIR =  '\\'.join(MYDIR)
    # If folder doesn't exist, then create it.
    if not os.path.isdir(MYDIR):
        os.makedirs(MYDIR)
        print("created folder : ", MYDIR)
    else:
        pass
        #print(MYDIR, "folder already exists.")
    #################################
    Image_directory=MYDIR
        
    
    Image_name=filename_to_save#'gaussian3'
    #print("%s is %d years old." % fig1xlim)
    filenamecont1="".join(["\\",Image_name])
    filenamecont2=Image_directory+filenamecont1+'.tiff'
    # (3) save as TIFF
    png2.save(filenamecont2)
    png1.close()

    print('file saved as: ', filenamecont2)

    ###############################################################################

def save_data_fcn(data_objects):
    ##############################################################################
    ##############################save file out###################################
    
    for i in range(0,len(data_objects)):
        ##################################
        import os
        #Get directory where this script is running,
        #Then add '\data_out' to it for desired directory
        MYDIR = [(os.path.dirname(__file__)),'data_out']
        MYDIR =  '\\'.join(MYDIR)
        # If folder doesn't exist, then create it.
        if not os.path.isdir(MYDIR):
            os.makedirs(MYDIR)
            print("created folder : ", MYDIR)
        else:
            pass
            #print(MYDIR, "folder already exists.")
        #################################

        input_directory=MYDIR

        filenameout=(os.path.basename(data_objects[i].filename))
        filenameout1="".join(["\\",filenameout])
        filenameoutcomby=input_directory+filenameout1+'_out.txt'

        print('file saved:',filenameoutcomby)
        if data_objects[i].im_re_magn==False:
            data_labels=['magnitude']
        else:
            data_labels=data_objects[i].signal_labels
        
        if len(np.shape(data_objects[i].active_integ_data))==2:
            a=np.array(data_objects[i].active_integ_data).T
            a=np.insert(a,0,data_objects[i].exp_axis_modded,axis=1)

            #this is the header
            HEAD=data_objects[i].units_list[0]+','+",".join(data_labels)


            f = open(filenameoutcomby, "w")
            np.savetxt(f, a, delimiter=',',header=HEAD,comments='n_signals,n_x,n_y\n'+','.join(map(str,np.shape(data_objects[i].active_integ_data)))+',1'+'\n')#, header=column_names, comments="")
            f.close()

        elif len(np.shape(data_objects[i].active_integ_data))==3:
            a=[]

            xxx=np.array(data_objects[i].active_integ_data)
            xxx=np.swapaxes(xxx,1,2)
            for j in range(0,np.shape(data_objects[i].active_integ_data)[2]):
                for k in range (0,np.shape(data_objects[i].active_integ_data)[0]):
                    a.append(xxx[k,j,:])
            a=np.array(a).T
            a=np.insert(a,0,data_objects[i].exp_axis_modded,axis=1)

            data_labels=(data_labels)*np.shape(data_objects[i].active_integ_data)[2]

            HEAD=data_objects[i].units_list[0]+','+",".join(data_labels)
            f = open(filenameoutcomby, "w")
            np.savetxt(f, a, delimiter=',', header=HEAD,comments='n_signals,n_x,n_y\n'+','.join(map(str,np.shape(data_objects[i].active_integ_data)))+'\n')#comments='(x),(y)*'+str(np.shape(data_objects[i].active_integ_data)[2])+'\n')
            f.close()

def save_trans_data_fcn(data_objects):
    ##############################################################################
    ##############################save file out###################################
    
    for i in range(0,len(data_objects)):
        ##################################
        import os
        #Get directory where this script is running,
        #Then add '\data_out' to it for desired directory
        MYDIR = [(os.path.dirname(__file__)),'data_out']
        MYDIR =  '\\'.join(MYDIR)
        # If folder doesn't exist, then create it.
        if not os.path.isdir(MYDIR):
            os.makedirs(MYDIR)
            print("created folder : ", MYDIR)
        else:
            pass
            #print(MYDIR, "folder already exists.")
        #################################

        input_directory=MYDIR

        filenameout=(os.path.basename(data_objects[i].filename))
        filenameout1="".join(["\\",filenameout])
        filenameoutcomby=input_directory+filenameout1+'_trans_out.txt'

        print('file saved:',filenameoutcomby)
        data_labels=data_objects[i].signal_labels

        if data_objects[i].I_or_T=='T':
            a=[]
            xxx=np.array(data_objects[i].data_in)
            for j in range(0,np.shape(xxx)[0]):
                for k in range (0,np.shape(xxx)[1]):
                    a.append(xxx[j,k,:])
            a=np.array(a).T
            a=np.insert(a,0,data_objects[i].transient_axis,axis=1)
            data_labels=(data_labels)*np.shape(xxx)[1]
            HEAD='s'+','+",".join(data_labels)
            f = open(filenameoutcomby, "w")

            x_axis=", ".join(map(str,(data_objects[i].exp_axes[0].tolist())[:]))
            units=data_objects[i].units_list[0]
            if units [-1]=='s':
                units='s'

            np.savetxt(f, a, delimiter=',', header=HEAD,comments='experimental axis: '+str(units)+'\n'+'n_signals,n_x,n_y\n'+','.join(map(str,np.shape(xxx)))+'\n'+x_axis+'\n')#comments='(x),(y)*'+str(np.shape(data_objects[i].active_integ_data)[2])+'\n')
            f.close()
        else:
            print('file not transient')
        

if __name__=='__main__':
    data_objects=create_data_objects(filename_list)
    #swap_IR(data_objects)
    plot_the_re_im_transients(data_objects,0,100e-9,0,100e-9)
    #plot_the_magn_transients(data_objects)
    #plot_integrated(data_objects)
    #plot_plotly(data_objects)
    #toggle_re_im_magn(data_objects)
    #plot_integrated(data_objects,fit_data='t2',guess=[],timescale='ns')
    #fit_data_and_plot(data_objects,fit_data='t2',guess=[],timescale='ns')

    plt.show()
    plt.close()
    #save_trans_data_fcn(data_objects)

    #save_fig_fcn(plot_the_magn_transients(data_objects,0,100e-9,0,100e-9,DPI=300))




