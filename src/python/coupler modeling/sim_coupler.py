import argparse
import setup_sim


#Define the parser
parser = argparse.ArgumentParser(description = 'Coupler Model Parameters')


#Define the help messages
R1_help = 'Resistance per unit length of input coupler branch (default: %(default)s)'
R2_help = 'Resistance per unit length of output coupler branch (default: %(default)s)'
Rc_help = 'Coupling resistance per unit length (default: %(default)s)'
N_help =  'Number of sections used in simulation. Related to the total branch resistance as R1_total = R1*N  (default: %(default)s)'
RL1_help = 'Load resistance at the output of the input branch  (default: %(default)s)'
RL2_help = 'Load resistance at the output of the output branch  (default: %(default)s)'
Iin_help ='Input current used in simulatio (default: %(default)s)'
outpath_help='Path used to store the output netlist and simulations folder (default: %(default)s'


#Define the parser arguments
parser.add_argument('-R1',metavar='R1_value',default='1k'  ,help=R1_help)
parser.add_argument('-R2',metavar='R2_value',default='1k'  ,help=R2_help)
parser.add_argument('-Rc',metavar='Rc_value',default='100k',help=Rc_help)
parser.add_argument('-N' ,metavar='N_value' ,default=100   ,help=N_help,type=int)
parser.add_argument('-RL1',metavar='RL1_value',default='1k',help=RL1_help)
parser.add_argument('-RL2',metavar='RL2_value',default='1k',help=RL2_help)
parser.add_argument('-Iin',metavar='Iin_Value',default='100u',help=Iin_help)
parser.add_argument('-o','--output_path',metavar='output_path',default='../output',help=outpath_help)

#Define the local variables as parsed
input_params = parser.parse_args()
R1 = input_params.R1
R2 = input_params.R2
Rc = input_params.Rc
N = input_params.N
RL1 = input_params.RL1
RL2 = input_params.RL2
Iin = input_params.Iin
output_path = input_params.output_path

#Verbose the output
print(input_params)
print('Graphene coupler simulation\n\n\n')
print('##############################################')
print('Running simulation with the following options:')
print('R1: '+R1)
print('R2: '+R2)
print('Rc: '+Rc)
print('N: '+str(N))
print('RL1: '+RL1)
print('RL2: '+RL2)
print('I_in: '+Iin)
print('Output Path: '+output_path)

#Generate the netlist
setup_sim.create_scs(R1=R1,R2=R2,RL1=RL1,RL2=RL2,Rc=Rc,N=N,I_in=Iin,outputPath=output_path)
print('Setup simulation sucessfully.\n')

print('Running simulation')
setup_sim.runSim(outputPath=output_path)
