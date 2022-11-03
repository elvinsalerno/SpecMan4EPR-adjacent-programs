import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import *
from tkinter import Label
#from typing_extensions import Self
from object_manager_SpecMan import *
import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import os.path
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
import sys
from tkinter import Tk, Button, Frame
from tkinter.scrolledtext import ScrolledText

import re





filename_list=[r'C:\Users\esalerno\Google Drive\MagLab\LuPO4_Eu2plus\Eu2LuPO4_5K_15dB_t2_3.312T_T2',\
r'C:\Users\esalerno\Google Drive\MagLab\Frank_Natia\CoAPSO_1uM_08092022\08162022\5uM_CoPhen_50K_10dB_pfT1_08162022_5']


# plot function is created for 
# plotting the graph in 
# tkinter window







class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('1000x800')
        self.title('Read SpecMan .d01 and .exp files')

        self.i1=0
        self.i2=1000e-9
        self.bl1=0
        self.bl2=1000e-9

        self.filenames=[]

        self.normalize=False
        self.im_re_magn=False
        self.vlines=True
        self.avg_exp=False
        self.fourier_on=False

        # place a button on the root window
        ttk.Button(self,
                text='Open files',
                command=lambda:[self.open_file_dialog()]
                ).place(x=20, y=90)#grid(row=0,column=1)#,expand=True)
        
        ttk.Button(self,
                text='Clear',
                command=lambda:[self.clear_file_entry_box()]
                ).place(x=20, y=130)#grid(row=0,column=1)#,expand=True)

        ttk.Button(self,
                text='Load',
                command=lambda:[self.open_data_protocol()]
                ).place(x=170, y=90)#grid(row=0,column=1)#,expand=True)

        ttk.Button(self,
                text='Update',width=20,
                command=lambda:[self.update_plots()]
                ).place(x=750, y=250)#grid(row=0,column=1)#,expand=True)

        ttk.Button(self,
                text='Plotly',width=20,
                command=lambda:[self.plot_plotly_fcn(self.data_objects)]
                ).place(x=20, y=550)#grid(row=0,column=1)#,expand=True)
        
        ttk.Button(self,
                text='Swap imag/real',width=20,
                command=lambda:[self.swap_IR_tkinter(self.data_objects)]
                ).place(x=20, y=600)#grid(row=0,column=1)#,expand=True)


 

        save_figure_filename_label = Label(self, text="save figure filename",)
        save_figure_filename_label.place(x=20, y=170)

        self.save_figure_filename = Entry(self,width=15,font=('TkDefaultFont 20'))
        self.save_figure_filename.place(x=20, y=205)#grid(column=0, row=0)

        ttk.Button(self,
                text='Save transient figure',width=20,
                command=lambda:[self.save_transient_figure()]
                ).place(x=20, y=300)#grid(row=0,column=1)#,expand=True)

        ttk.Button(self,
                text='Save integrated figure',width=20,
                command=lambda:[self.save_integ_figure()]
                ).place(x=20, y=250)#grid(row=0,column=1)#,expand=True)
        
        self.toggle_norm_button=ttk.Button(self,
                text='not normalized',width=20,
                command=lambda:[self.normalize_integ_plot()]
                )
        self.toggle_norm_button.place(x=750, y=300)#grid(row=0,column=1)#,expand=True)

        self.toggle_imremagn_button=ttk.Button(self,
                text='magn',width=20,
                command=lambda:[self.re_im_magn_fcn()]
                )
        self.toggle_imremagn_button.place(x=750, y=400)#grid(row=0,column=1)#,expand=True)

        self.toggle_avg_exp_button=ttk.Button(self,
                text='not averaged',width=20,
                command=lambda:[self.average_fcn()]
                )
        self.toggle_avg_exp_button.place(x=750, y=450)#grid(row=0,column=1)#,expand=True)


        self.toggle_vlines_button=ttk.Button(self,
                text='vlines on',width=20,
                command=lambda:[self.vlines_fcn()]
                )
        self.toggle_vlines_button.place(x=750, y=350)#grid(row=0,column=1)#,expand=True)

        self.toggle_fourier_button=ttk.Button(self,
                text='Fourier off',width=18,
                command=lambda:[self.apply_fourier()]
                )
        self.toggle_fourier_button.place(x=525, y=515)#grid(row=0,column=1)#,expand=True)

         

        save_figure_filename_label = Label(self, text=u"ctr freq \u2193",)
        save_figure_filename_label.place(x=540, y=570)



        self.data_objects=[]

        data_entry_inst = Label(self, text="file paths as comma separated plain text",font=('TkDefaultFont 12'))
        data_entry_inst.place(x=5, y=5)

        #text entry box for filenames
        self.temp_in_txt = Entry(self,width=20,font=('TkDefaultFont 20'))
        self.temp_in_txt.insert(0, "C:/Users/esalerno/Google Drive/MagLab/short_biradical_wintyer_break/1mM/ChirpEcho_4dB_93.5to94.5_t90_1.6us_100Kshots_holeat94.02")
        self.temp_in_txt.place(x=2, y=40)#grid(column=0, row=0)

        set_baseline_lims = Label(self, text="baseline limits (ns) 1, 2")
        set_baseline_lims.place(x=750, y=0)
        set_baseline_lims.config(fg= "blue")

        self.bl1_txt = Entry(self,width=5,font=('TkDefaultFont 20'))
        self.bl1_txt.place(x=750, y=40)#grid(column=0, row=0)

        self.bl2_txt = Entry(self,width=5,font=('TkDefaultFont 20'))
        self.bl2_txt.place(x=850, y=40)#grid(column=0, row=0)

        set_integ_lims = Label(self, text="integration limits (ns) 1, 2")
        set_integ_lims .place(x=750, y=80)
        set_integ_lims .config(fg= "red")

        #text entry boxes for bl correction limits, integration limits
        self.i1_txt = Entry(self,width=5,font=('TkDefaultFont 20'))
        self.i1_txt.place(x=750, y=120)#grid(column=0, row=0)

        self.i2_txt = Entry(self,width=5,font=('TkDefaultFont 20'))
        self.i2_txt.place(x=850, y=120)#grid(column=0, row=0)

        first_trace_label = Label(self, text="first trace")
        first_trace_label.place(x=750, y=160)
        self.first_trace_entry = Entry(self,width=5,font=('TkDefaultFont 20'))
        self.first_trace_entry.place(x=750, y=190)#grid(column=0, row=0
        self.first_trace_entry.insert(0, "0")

        last_trace_label = Label(self, text="last trace")
        last_trace_label.place(x=850, y=160)
        self.last_trace_entry = Entry(self,width=5,font=('TkDefaultFont 20'))
        self.last_trace_entry.place(x=850, y=190)#grid(column=0, row=0)
        self.last_trace_entry.insert(0, "end")

        describe_x_label_label = Label(self, text="desired x-axis label")
        describe_x_label_label.place(x=270, y=480)
        self.x_label_in = Entry(self,width=15,font=('TkDefaultFont 20'))
        self.x_label_in.place(x=270, y=520)#grid(column=0, row=0)

        describe_ops_label = Label(self, text="x-axis operations (read->):\n *x  /x  +x  -x  *xex  *xe-x",font=("Arial", 12))
        describe_ops_label.place(x=270, y=560)
        self.math_ops_in = Entry(self,width=15,font=('TkDefaultFont 20'))
        self.math_ops_in.place(x=270, y=610)#grid(column=0, row=0)

        #########################save data out########################
        ttk.Button(self,
                text='Save integrated .txt',width=20,
                command=lambda:[save_data_fcn(self.data_objects)]
                ).place(x=20, y=350)#grid(row=0,column=1)#,expand=True)

        ttk.Button(self,
                text='Save transient .txt',width=20,
                command=lambda:[save_trans_data_fcn(self.data_objects)]
                ).place(x=20, y=400)#grid(row=0,column=1)#,expand=True)

        ######################open new window for matplotlib plot########################
        #self.plottt()
        #self.plot_new_window=ttk.Button(self,
        #        text='plot new winder',
        #        command=lambda:[self.plottt()]
        #       )
        #self.plot_new_window.place(x=800, y=600)#grid(row=0,column=1)#,expand=True)

        self.new_plot_window_int = ttk.Button(self, text="Open integrated plot",width=20,  command=lambda:[self.new_plot_window_fcn(which_plot='integrated')])
        self.new_plot_window_int.place(x=20, y=500)
        
        self.new_plot_window_trans = ttk.Button(master=self, text="Open transient plot", width=20, command=lambda:[self.new_plot_window_fcn(which_plot='transient')])
        self.new_plot_window_trans.place(x=20, y=450)

        ####################Fit t1t2 options
        OPTIONS = ["None","t1","t2","2t1","2t2"] 

        self.fit_type = StringVar(self)
        self.fit_type.set(OPTIONS[0]) # default value

        w = OptionMenu(self, self.fit_type, *OPTIONS)
        w.place(x=750, y=530)
        self.global_fit_type='None'
        self.fit_guess=[]

        self.enter_fit_guess = Entry(self,width=15,font=('TkDefaultFont 20'))
        self.enter_fit_guess.place(x=750, y=580)#grid(column=0, row=0)
        #self.enter_fit_guess.insert(0, "end")

        self.fit_data = Label(self, text="fit t1 or t2")
        self.fit_data.place(x=750, y=495)

        self.fit_label = Label(self, text="")
        self.fit_label.place(x=730, y=620)

        self.okaybutton = ttk.Button(self, text="Confirm", command=self.update_fit)
        self.okaybutton.place(x=850, y=530)

        ####################fourier options

        FREQ_OPTIONS = ["THz","GHz","MHz","kHz","Hz"] 

        self.enter_add_number = Entry(self,width=10,font=('TkDefaultFont 20'))
        self.enter_add_number.place(x=550, y=610)#grid(column=0, row=0)

        self.fft_freq = StringVar(self)
        self.fft_freq.set(FREQ_OPTIONS[1]) # default value

        self.freq_choice = OptionMenu(self, self.fft_freq, *FREQ_OPTIONS)
        self.freq_choice.place(x=630, y=560)

        self.frequency_chosen="GHz"
        self.number_to_add=0

        ###########for console in gui###################
        self.log_widget = ScrolledText(self, height=9, width=135, font=("consolas", "10", "normal"))
        self.log_widget.place(x=10, y=650)
        self.redirect_logging()


    def update_fit(self):
        for i in range(0,len(self.data_objects)):
            self.data_objects[i].update_data_fcn(self.bl1,self.bl2,self.i1,self.i2,self.math_ops_in.get(),self.first_trace_entry.get(),self.last_trace_entry.get())

        self.global_fit_type=self.fit_type.get()

        if self.global_fit_type=='t1' or self.global_fit_type=='t2':
            self.fit_label['text']='amplitude, lifetime, constant'
        elif self.global_fit_type=='2t1' or self.global_fit_type=='2t2':
            self.fit_label['text']='A1,lifetime1,c,A2,lifetime2'
        else: 
            self.fit_label['text']=''
        
        temp_fit_guess=self.enter_fit_guess.get()

        temp_fit_guess=temp_fit_guess.replace(" ", "")
        temp_fit_guess=temp_fit_guess.split(',')
        if len (self.fit_guess)>0:
            try:
                "because it may not be written as a number"
                self.fit_guess=[float(i) for i in temp_fit_guess]
            except:
                print('enter only numbers and commas as guess')

        if self.global_fit_type=='t1' or self.global_fit_type=='t2':
            if len (self.fit_guess)!=3 and len (self.fit_guess)!=0:
                print('wrong guess format for ',self.global_fit_type,'\nshould have 3 comma separated inputs')
        if self.global_fit_type=='t21' or self.global_fit_type=='2t2':
            if len (self.fit_guess)!=5 and len (self.fit_guess)!=0:
                print('wrong guess format for ',self.global_fit_type,'\nshould have 5 comma separated inputs')
        
        self.update_plots()

    def clear_file_entry_box(self):
        self.temp_in_txt.delete(0, END)

    def normalize_integ_plot(self):
        self.normalize= not self.normalize
        if self.normalize==True:
            self.toggle_norm_button['text']='Normalized'
        else:
            self.toggle_norm_button['text']='Not Normalized'
        toggle_norm(self.data_objects)
        self.update_plots()
    
    def re_im_magn_fcn(self):
        self.im_re_magn= not self.im_re_magn
        if self.im_re_magn==True:
            self.toggle_imremagn_button['text']='im/re'
        else:
            self.toggle_imremagn_button['text']='magn'
        toggle_re_im_magn(self.data_objects)
        self.update_plots()

    def average_fcn(self):
        self.avg_exp= not self.avg_exp
        if self.avg_exp==True:
            self.toggle_avg_exp_button['text']='averaged'
        else:
            self.toggle_avg_exp_button['text']='not averaged'
        toggle_avg_exp(self.data_objects)
        self.update_plots()    
    
    def apply_fourier(self):
        print('***adjust fourier cutoff with integration limits\n***baseline does nothing for fourier transform\n')

        #Change the transient plot to im/re to be clear about where data is coming from
        if self.im_re_magn==False:
            self.re_im_magn_fcn()


        self.fourier_on= not self.fourier_on
        if self.fourier_on==True:
            self.toggle_fourier_button['text']='fourier on'
        else:
            self.toggle_fourier_button['text']='fourier off'


        self.update_fourier_info()
        toggle_fourier(self.data_objects,self.number_to_add,self.frequency_chosen)
        self.update_plots()    
            
    def vlines_fcn(self):
        self.vlines= not self.vlines
        if self.vlines==True:
            self.toggle_vlines_button['text']='vlines on'
        else:
            self.toggle_vlines_button['text']='vlines off'

        self.make_the_plots()

    def swap_IR_tkinter(self,data_objects):
        swap_IR(data_objects)
        self.update_plots()  



    def update_plots(self):
        
        #for the math operations to x axis
        #check if the input contains a legitimate number, return 
        #the value if so, return False if not
        def isnumeric(value):
            x=re.findall('\d*\.?\d+',value)
            if len(x)>1:
                return False
            else:
                pass
            try:
                float(x[0])
                return float(x[0])
            except:
                return False


        #If the value is not numeric, use preset values
        # for baseline and integration limits, otherwise take input
        if not isnumeric(self.i1_txt.get()):
            self.i1=0
        else:
            self.i1=isnumeric(self.i1_txt.get())*1e-9

        if not isnumeric(self.i2_txt.get()):
            self.i2=1000e-9
        else:
            self.i2=isnumeric(self.i2_txt.get())*1e-9

        if not isnumeric(self.bl1_txt.get()): 
            self.bl1=0
        else:
            self.bl1=isnumeric(self.bl1_txt.get())*1e-9

        if not isnumeric(self.bl2_txt.get()):
            self.bl2=1000e-9
        else:
            self.bl2=isnumeric(self.bl2_txt.get())*1e-9


        self.update_fourier_info()
        update_fourier(self.data_objects,self.number_to_add,self.frequency_chosen)

        for i in range(0,len(self.data_objects)):
            self.data_objects[i].update_data_fcn(self.bl1,self.bl2,self.i1,self.i2,self.math_ops_in.get(),self.first_trace_entry.get(),self.last_trace_entry.get())
        
        
        '''
        #***********Plot integrated figure*****************
        self.integrated_fig = FigureCanvasTkAgg(plot_integrated(self.data_objects),  master = self)  
        self.integrated_fig.draw()
            # placing the canvas on the Tkinter window
        self.integrated_fig.get_tk_widget().place(x=350, y=400)#grid(row=2, column=4)#, ipadx=40, ipady=20)    
        '''
        self.make_the_plots()
    
    
    def update_fourier_info(self):
        #get floats from string and check if its numeric
        def isnumeric(value):
            x=re.findall('\d*\.?\d+',value)
            if len(x)>1:
                return False
            else:
                pass
            try:
                float(x[0])
                return float(x[0])
            except:
                return False

        self.frequency_chosen=self.fft_freq.get()
       
        if not isnumeric(self.enter_add_number.get()):
            self.number_to_add=0
        else:
            self.number_to_add=isnumeric(self.enter_add_number.get())

    def  plot_plotly_fcn(self,data_objects):
            #import plotly.express as px
            #import plotly.graph_objects as go
            #import plotly.io as pio
            #import numpy as np


            plotly_fig = go.Figure()
            for i in range(0,len(data_objects)):
                if len(np.shape(data_objects[i].active_integ_data))==2:
                    for j in range(0,len(data_objects[i].active_integ_data)):
                        plotly_fig.add_trace(go.Scatter(x=data_objects[i].exp_axis_modded[:], y=data_objects[i].active_integ_data[j][:],
                                        #marker_color='rgba(0.5,0.5,0.5,0.5)',
                                        mode='lines',))
                                    #name=name_list[i]))
                elif len(np.shape(data_objects[i].active_integ_data))==3:
                    xxx=np.array(data_objects[i].active_integ_data)
                    xxx=np.swapaxes(xxx,1,2)
                    for j in range(0,np.shape(data_objects[i].active_integ_data)[0]):
                        for k in range (0,np.shape(data_objects[i].active_integ_data)[2]):
                            plotly_fig.add_trace(go.Scatter(x=data_objects[i].exp_axis_modded[:], y=xxx[j,k,:],
                                    #marker_color='rgba(0.5,0.5,0.5,0.5)',
                                    mode='lines',))
                                    #name=name_list[i]))

            plotly_fig.update_yaxes(title='intensity')

            if len(self.x_label_in.get())>0 and self.x_label_in.get()[0]!=' ':
                plotly_fig.update_xaxes(title=self.x_label_in.get())
            else:
                if len(self.data_objects[0].units_list[0])>0:
                    plotly_fig.update_xaxes(title=self.data_objects[0].units_list[0])
                else:
                    pass
                    #plotly_fig.update_xaxes(title=self.data_objects[0].units_list[0])

            plotly_fig.show()


    def save_transient_figure(self):
        save_fig_fcn(plot_the_transients(self.data_objects,self.i1,self.i2,self.bl1,self.bl2,magn_or_reim=self.im_re_magn,DPI_in=300,plot_v_lines_in=self.vlines),filename_to_save=self.save_figure_filename.get()+'_transient')

    def save_integ_figure(self):
        #get x-label 
        if len(self.x_label_in.get())>0 and self.x_label_in.get()[0]!=' ':
            x_label_integ=self.x_label_in.get()
        else:
            x_label_integ=False
        save_fig_fcn(plot_integrated(self.data_objects,DPI=300,x_label_in=x_label_integ,fit_data=self.global_fit_type,guess=self.fit_guess),filename_to_save=self.save_figure_filename.get()+'_integrated')

    def make_the_plots(self):
        #***********Plot re im transient figure*****************


        self.re_im_trans_fig = FigureCanvasTkAgg(plot_the_transients(self.data_objects,self.i1,self.i2,self.bl1,self.bl2,magn_or_reim=self.im_re_magn,plot_v_lines_in=self.vlines),  master = self)  
        #self.re_im_trans_fig.set_figwidth(10)
        self.re_im_trans_fig.draw()
        # placing the canvas on the Tkinter window
        self.re_im_trans_fig.get_tk_widget().place(x=350, y=10)#grid(row=0, column=4)#, ipadx=40, ipady=20)


        #***********Plot integrated figure*****************
        #get x-label 
        if len(self.x_label_in.get())>0 and self.x_label_in.get()[0]!=' ':
            x_label_integ=self.x_label_in.get()
        else:
            x_label_integ=False

        self.integrated_fig = FigureCanvasTkAgg(plot_integrated(self.data_objects,x_label_in=x_label_integ,fit_data=self.global_fit_type,guess=self.fit_guess),  master = self)  
        
        self.integrated_fig.draw()
        # placing the canvas on the Tkinter window
        self.integrated_fig.get_tk_widget().place(x=350, y=250)#grid(row=2, column=4)#, ipadx=40, ipady=20)    


    def open_data_protocol(self):
        filenames_list =  str(self.temp_in_txt.get())
        filenames_list = filenames_list.split(",")

        #Get rid of any empty strings
        while("" in filenames_list):
            filenames_list.remove("")

        for i in range(0,len(filenames_list)):
            #Get rid of leading white space in string
            if filenames_list[i][0]==' ':
                filenames_list[i]=filenames_list[i][1:]
            #strip the filetype
            if filenames_list[i][-4:]=='.dat' or filenames_list[i][-4:]=='.exp' or filenames_list[i][-4:]=='.d01':
                filenames_list[i]= filenames_list[i][:-4]

        #Remove duplicates from the list
        self.filenames = []
        [self.filenames.append(x) for x in filenames_list if x not in self.filenames]
        if len(filenames_list)!=len(self.filenames):
            print('***you only need to select one of each file, ignoring extensions***')

        #Check if the files desired actually exist
        files_exist=[]
        for x in self.filenames:
            if os.path.isfile(x+'.d01') and os.path.isfile(x+'.exp'):
                files_exist.append(True)
            elif os.path.isfile(x+'.d01') and not os.path.isfile(x+'.exp'): 
                files_exist.append(False)
                print(x + '.exp file not found')
            elif os.path.isfile(x+'.exp') and not os.path.isfile(x+'.d01'):
                files_exist.append(False)
                print(x + '.d01 file not found')
            else:
                files_exist.append(False)
                print(x+'.d01 \nand\n', x + '.exp files not found')

            
        self.normalize=False
        self.im_re_magn=False
        self.vlines=True
        self.toggle_norm_button['text']='Not Normalized'
        self.toggle_imremagn_button['text']='magn'
        self.toggle_vlines_button['text']='vlines on'
         
        if all(files_exist):  
            self.data_objects=create_data_objects(self.filenames)
            for i in range(0,len(self.data_objects)):
                self.data_objects[i].update_data_fcn(self.bl1,self.bl2,self.i1,self.i2,self.math_ops_in.get(),self.first_trace_entry.get(),self.last_trace_entry.get())
            self.make_the_plots()
        else:
            pass
            #print('file does not exist')



    def open_file_dialog(self):
        filetypes = (
            ('All files', '*.*'),
            ('text files', '*.txt')
        )
        filenames = fd.askopenfilenames(
            title='Open files',
            initialdir='/',
            filetypes=filetypes)

        the_string=str(filenames[:])[1:-1]
        the_string = the_string.replace("'", "")

        self.temp_in_txt.insert(0, the_string)#+",")

    ########################print console in gui#######################
    #This will print to console
    #Type command self.reset_logging() to activate 
    def reset_logging(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
    #This will print conosole in GUI
    #This command is called in __init__ to normally print to GUI
    def redirect_logging(self):
        logger = PrintLogger(self.log_widget)
        sys.stdout = logger
        sys.stderr = logger
    

    #####################To open new window for figures####################

    def new_plot_window_fcn(self,which_plot='integrated'):
        #Create a new top level window
        new_window = tk.Toplevel()
        tk.Label(master=new_window).pack() #, text="This is a new window"

        def plottt():
            #***********get x-axis label for integrated figure*****************
            #get x-label 
            if len(self.x_label_in.get())>0 and self.x_label_in.get()[0]!=' ':
                x_label_integ=self.x_label_in.get()
            else:
                x_label_integ=False
            # creating the Tkinter canvas
            # containing the Matplotlib figure
            if which_plot=='integrated':        
                canvas = FigureCanvasTkAgg(plot_integrated(self.data_objects,DPI=300,x_label_in=x_label_integ,fit_data=self.global_fit_type,guess=self.fit_guess),
                                        master = new_window)  
            else: #ie if which_plot=='integrated':
                canvas = FigureCanvasTkAgg(plot_the_transients(self.data_objects,self.i1,self.i2,self.bl1,self.bl2,DPI_in=300,magn_or_reim=self.im_re_magn,plot_v_lines_in=self.vlines),
                        master = new_window)  
            canvas.draw()
            # placing the canvas on the Tkinter window
            canvas.get_tk_widget().pack()
            # creating the Matplotlib toolbar
            toolbar = NavigationToolbar2Tk(canvas,
                                        new_window)
            toolbar.update()
            # placing the toolbar on the Tkinter window
            canvas.get_tk_widget().pack()
        plottt()
  









#Need this class to print console to gui
class PrintLogger():  # create file like object #did say PrintLogger(object)???

    def __init__(self, textbox):  # pass reference to text widget
        self.textbox = textbox  # keep ref

    def write(self, text):
        self.textbox.insert("end", text)  # write text to textbox
        self.textbox.see("end")  # scroll to end

    def flush(self):  # needed for file like object
        pass









if __name__ == "__main__":
    app = App()
    app.mainloop()

    def on_closing():
        #close the tkinter window
        app.destroy()
    app.protocol("WM_DELETE_WINDOW", on_closing)

