
import numpy as np



#This is for testing only this script
input_directory=r'C:\Users\evsal\Google Drive\MagLab\LuPO4_Eu2plus'
input_filename='Eu2LuPO4_5K_15dB_ELDOR_93.5to94.5GHz_ctr94GHz'
filename_in=input_directory+'\\'+input_filename


def load_exp_fcn(filename_in):
    filename_in=filename_in+'.exp'

    #Create a list of strings with each [section]
    sections_list=[]
    with open(filename_in) as f:
        for line in f:
            if line.startswith('[') and ']' in line:
                #If this is the first time through, then temp doesnt exist yet and there will be an exception, 
                # do not append here
                try: 
                    sections_list.append(temp)
                except:
                    pass
                temp=[]
            temp.append(line) 




    #Find the [sweep] section in the sections list
    #make it into a list of lists
    sweep_section=[]
    for i in sections_list:
        if '[sweep]' in i[0]:
            #Start from index 1 to skip [sweep] heading
            for j in range(1,len(i)):
                j=i[j].replace('sweep','sweep ')
                j=j.replace('\n','')
                j=j.replace(',',' ')
                j=j.split(' ')
                sweep_section.append(j)

    #get the variable names from the sweepn line in[sweep] section
    #and append to a list
    #Dont get the ones with S ("Sum axis")
    #dont get the ones with P ("Parmeters axis")
    variables_list=[]
    for i in sweep_section:
        if i[0]=='sweep' and i[3]!='P' and i[3]!='S':
            variables_list.append([i[6],i[4]])
    variables_list=np.array(variables_list)

    #Get transient line from [sweep] section
    for i in sweep_section:
        if i[0]=='transient':
            transient_line=i

    




    #Find the [params] section in the sections list
    #Make it into a list of lists of strings 
    params_section=[]
    for i in sections_list:
        if '[params]' in i[0]:
            #start from 1 to avoid grabbing "[params]"line
            for j in range(1,len(i)):
                #separate the string as desired
                j=i[j]
                j=j.replace('\n','')
                j=j.replace(',',' ')
                j=j.replace(';',' ;')
                j=j.replace('  ',' ')
                j=j.split(' ')
                params_section.append(j)



    #Get the relevant parameters lines, make into a list
    #Choose by which contain the 
    params_scan_list=[]
    for i in params_section:
        if i[0] in variables_list[:,0]:
            params_scan_list.append(i)

    
   
    #Dictionary defining essential unit orders
    units_indices={"p":1e-12,"n":1e-9,"u":1e-6,"m":1e-3,"k":1e3,"M":1e6,"G":1e9}

    #Program to see if units are specified, if so then return the conversion
    #If not then return 1
    def check_units(string_in):
        if string_in in units_indices:
            return units_indices[string_in]
        else:
            return 1

    
    #get the sampling from parameters
    sampling=1
    sampling_units='x'
    for i in params_section:
        if sampling==1:
            if i[0] == "Sampling":
                #print(i)
                sampling_units=i[3]
                sampling=float(i[2])*check_units(i[3][0])
        else:
            pass



    if transient_line[2]=='T':
        I_or_T='T'
        sampling_axis=np.arange(0,sampling*int(transient_line[3]),sampling)
        sampling_axis=sampling_axis[0:int(transient_line[3])]
    else:
        I_or_T='I'
    


    #######################################################################
    ######Define function for experimental axis based on type detcected####
    #######################################################################


    def step_fcn(list_input,n_steps):
        start_value=float(list_input[2])*check_units(list_input[3][0])
        step_size=float(list_input[5])*check_units(list_input[6][0])

        #print(list_input)
        units=list_input[3]

        #Generate the x-values from the information gathered
        #for i in range(0,n_steps):
        x_values=np.array([start_value+i*step_size for i in range(0,int(n_steps))])
        #x_values=x_values/check_units(list_input[3][0])
        return x_values, units

    def array_in_fcn(list_input,n_steps):
        x_values=[]
        def is_number(s):
            try:
                float(s)
                return True
            except ValueError:
                return False

        for i in list_input:
            if is_number(i):
                x_values.append(float(i))
        
        #This should be more dynamic, needs
        return np.array(x_values),"integer"


    def logto_fcn(list_input,n_steps):
        start_value=float(list_input[2])*check_units(list_input[3][0])
        stop_value=float(list_input[5])*check_units(list_input[6][0])


        units=list_input[3]
        #Generate the x-values from the information gathered
        #for i in range(0,n_steps):
        x_values=np.geomspace(start_value,stop_value,num=int(n_steps))
        #x_values=x_values/check_units(list_input[3][0])
        return x_values,units

    def to_fcn(list_input,n_steps):
        start_value=float(list_input[2])*check_units(list_input[3][0])
        stop_value=float(list_input[5])*check_units(list_input[6][0])


        units=list_input[3]
        #Generate the x-values from the information gathered
        #for i in range(0,n_steps):
        x_values=np.linspace(start_value,stop_value,num=int(n_steps))
        #x_values=x_values/check_units(list_input[3][0])
        return x_values,units

    #Make function to read from [params] line how the exp axis is generated
    def determine_axis_vals(list_input):
        if 'logto' in list_input:
            exp_type='logto'
        elif 'to' in list_input:
            exp_type='to'
        elif 'step' in list_input:
            exp_type='step'
        else:
            exp_type='array_in'
        return (exp_type)


    if I_or_T=='T':
        axes_list=[sampling_axis]
    else:
        axes_list=[]


    units_list=[]
    #This will determine what kind of function is necessary and execute it
    for i in range(0,len(params_scan_list)):
        #could also just do if 'logto' in params_scan_list[i]:
        if determine_axis_vals(params_scan_list[i])=='step':
            outlist=step_fcn(params_scan_list[i],variables_list[i,1])
        elif determine_axis_vals(params_scan_list[i])=='array_in':
            outlist=array_in_fcn(params_scan_list[i],variables_list[i,1])   
        elif determine_axis_vals(params_scan_list[i])=='logto':
            outlist=logto_fcn(params_scan_list[i],variables_list[i,1])  
        elif determine_axis_vals(params_scan_list[i])=='to':
            outlist=to_fcn(params_scan_list[i],variables_list[i,1])   
        else:
            print("EXP READ ERROR")
        axes_list.append(outlist[0])
        units_list.append(outlist[1])

        
    #print(np.shape(units_list))

    return axes_list,units_list,transient_line, sampling, sampling_units


#print(np.shape(units_list))

if __name__ == "__main__":
    exp_info=load_exp_fcn(filename_in)
    #print(len(exp_info[0]))
    print(len(exp_info[0][0]))
    print(exp_info[3])
    print(exp_info[4])
    #print(exp_info[3])


