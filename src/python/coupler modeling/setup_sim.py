"""
Created on Thu Aug 03 16:13:45 2017

@author: momar
"""
import numpy as np
import matplotlib.pyplot as plt
import os,subprocess
from scipy.io import savemat

def create_scs(R1='1k',R2='1k',RL1='1k',RL2='1k',Rc='100k',N=100,I_in='1u',outputPath='../output'):
    """
    Creates a Spectre netlist to simulate the graphene coupler model. 
    All the Spectre model parameters are given as string except the number of
    sections which is an integer
    
    Parameters:
    -----------
    R1: string , optional (default = '1k')
        Resistance of each section in first branch
    R2: string , optional (default = '1k')
        Resistance of each section in second branch
    RL1: string , optional (default = '1k')
        Resistance of first branch load resistance
    RL2: string , optional (default = '1k')
        Resistance of second branch load resistance
    Rc: string , optional (default = '100k')
        Coupling resistance per unit length
    N: int, optional (default = 100)
        Number of sections used in the simulation
    I_in: string , optional (default = '1u')
        Input current applied to first branch
    outputPath: string, optional (default ='./output')
        Path to directory to save output files and netlist
    """
    filename = os.path.join(outputPath,'input.scs')
    runFile = os.path.join(outputPath,'runSimulation')
    runCommand = 'spectre ./input.scs -format psfascii'
    
    header = "simulator lang=spectre\n"
    header += "global 0\n"
    header += "parameters RL1="+RL1+" RL2="+RL2+" R1="+R1+" R2="+R2+" Rc="+Rc+" \n"
    
    body = ""
    for i in range(N):
        body += "R1_"+str(i)+" (v1_"+str(i)+" v1_"+str(i+1)+") resistor r="+R1+" \n" #Distributed R1
        body += "R2_"+str(i)+" (v2_"+str(i)+" v2_"+str(i+1)+") resistor r="+R2+" \n" #Distributed R2
        body += "Rc_"+str(i)+" (v1_"+str(i)+" v2_"+str(i)+") resistor r="+Rc+" \n" #Distributed Rc
    
    body += "RL1 (v1_"+str(N)+" v1_gnd) resistor r="+RL1+" \n" #Load resistance 1 to probe dc source
    body += "RL2 (v2_"+str(N)+" v2_gnd) resistor r="+RL2+" \n" #Load resistance 2 to probe dc source
    body += "VL1 (v1_gnd 0) vsource dc=0 type=dc \n" #Probe 1 DC source
    body += "VL2 (v2_gnd 0) vsource dc=0 type=dc \n" #Probe 2 DC source
    body += "Iin (0 v1_0) isource dc="+I_in+" type=dc \n" #Stimulus input source
    
    simOptions =  "simulatorOptions options reltol=1e-3 vabstol=1e-6 iabstol=1e-12 temp=27 "
    simOptions += "tnom=27 scalem=1.0 scale=1.0 gmin=1e-12 rforce=1 maxnotes=5 maxwarns=5 "
    simOptions += "digits=5 cols=80 pivrel=1e-3 sensfile=\"../psf/sens.output\" checklimitdest=psf \n" 
    simOptions += "dcOp dc write=\"spectre.dc\" maxiters=150 maxsteps=10000 annotate=status\n"
    simOptions += "dcOpInfo info what=oppoint where=rawfile \n"
    simOptions += "modelParameter info what=models where=rawfile \n"
    simOptions += "element info what=inst where=rawfile \n"
    simOptions += "outputParameter info what=output where=rawfile \n"
    simOptions += "designParamVals info what=parameters where=rawfile \n"
    simOptions += "primitives info what=primitives where=rawfile \n"
    simOptions += "subckts info what=subckts  where=rawfile \n"
    #simOptions += "save all \n"
    simOptions += "saveOptions options save=allpub currents=all \n"
    
    #Write the file to the output
    print('Writing the SCS file')
    with open(filename,"w") as scs_file:
        scs_file.write(header)
        scs_file.write(body)
        scs_file.write(simOptions)
    print('Done\n\n')
    
    print('Writing simulation script')
    with open(runFile,"w") as cmd_file:
        cmd_file.write(runCommand)
    print('Done\n\n')

    print('Setting simulation script permissions')
    os.chmod(runFile,0o777)
    print('Done\n\n')
    return None



def runSim(outputPath='../output'):
    """
    """
    init_dir = os.getcwd()
    os.chdir(outputPath)
    process = subprocess.Popen(['tcsh','./runSimulation'],stdout=subprocess.PIPE)
    
    #Redirect the pipe to the screen
    while process.poll() is None:
        l = process.stdout.readline()
        print(l)
    print(process.stdout.read()) #Flush any final line
    os.chdir(init_dir)
    read_dcOp()
    return None

def read_dcOp(dcOpFile='../output/input.raw/dcOp.dc',plotData = True,saveMatlab=True,matPath='../output/dcOpData.mat',verbose_err = False):
    """
    """
    
    #Initialize the returns
    V1=np.array([])
    V1_idx = np.array([])
    
    V2=np.array([])
    V2_idx = np.array([])
    
    R1=np.array([])
    R1_idx = np.array([])
    
    R2=np.array([])
    R2_idx = np.array([])
    
    Rc=np.array([])
    Rc_idx = np.array([])
    
    errLog = '' #Error log

    with open(dcOpFile,'r') as f:
        for line in f:
            if not line[0] == '#': #Not a comment line
                small_case = line.lower()
                small_case = small_case.split()
                if len(small_case[0])>1: #Line with spacing
                    #Get the element name after removing non essential characters
                    #Format--> "elemId_nodeId[optional:Number]"
                    elem_tag = small_case[0].strip('\"') #Remove the "
                    elem_tag = elem_tag.split(':')[0] #Keep only name before terminal name if any
                    elem_tag = elem_tag.split('_') #First index is name, other is number
                    try:
                        elem_id = elem_tag[0]
                        elem_idx = elem_tag[1]
                        elem_val = float(small_case[2])
                        elem_idx = int(elem_idx)
                        if elem_id == 'v1':
                            V1 = np.append(V1,elem_val)
                            V1_idx = np.append(V1_idx,elem_idx)
                        if elem_id == 'v2':
                            V2 = np.append(V2,elem_val)
                            V2_idx = np.append(V2_idx,elem_idx)
                        if elem_id == 'r1':
                            R1 = np.append(R1,elem_val)
                            R1_idx = np.append(R1_idx,elem_idx)
                        if elem_id == 'r2':
                            R2 = np.append(R2,elem_val)
                            R2_idx = np.append(R2_idx,elem_idx)
                        if elem_id == 'rc':
                            Rc = np.append(Rc,elem_val)
                            Rc_idx = np.append(Rc_idx,elem_idx)
                    except:
                        errLog+='No match found for '+line
    
    if plotData:
        #Plot the data
        plt.figure()
        plt.title('Voltage')
        plt.plot(V1_idx,V1,V2_idx,V2)
        plt.legend(('V1','V2'))
        
        plt.figure()
        plt.title('Current')
        plt.plot(R1_idx,R1,R2_idx,R2,Rc_idx,Rc)
        plt.legend(('R1','R2','Rc'))
    
    if saveMatlab:
        #Create the variable dictionary
        varsDict = {'R1_idx':R1_idx,'R1':R1,'R2_idx':R2_idx,'R2':R2,'Rc_idx':Rc_idx,'Rc':Rc} #Current
        varsDict.update({'V1_idx':V1_idx,'V1':V1,'V2_idx':V2_idx}) #Voltages
        savemat(matPath,varsDict)
   
    if verbose_err:
        print(errLog)
    plt.show()
    return V1_idx,V1,V2_idx,V2,R1_idx,R1,R2_idx,R2,Rc_idx,Rc
