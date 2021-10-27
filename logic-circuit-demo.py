# Copyright 2021 by naru fox
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from dimod.reference.samplers import ExactSolver
from dwave.system import DWaveSampler, EmbeddingComposite
from TextFormatter import TextFormatter
from datetime import datetime
import time


print("Quantum Solver Engine")
print("Copyright (c) 2021 naru fox")
print("All Rights Reserved\n\n")
print("Staring Program...")
import dwavebinarycsp

print("defining binToDec")
def binToDec(inNum):
    numberx=inNum
    dec_number= int(numberx, 2)
    return (dec_number)
    #print('The decimal conversion is:', dec_number)
    #print(type(dec_number))

print("Defining Logic Circuit")

def logic_circuit(a,b,c,d,e,f,g):
    str1=str(a)+str(b)+str(c)+str(d)+str(f)+str(g)
    num1=binToDec(str1)
    num2=num1*num1
    output1=num2==49
    
    return (output1)
print("Setting up custom text format...")
cprint = TextFormatter()
cprint.cfg('g', 'k', 'b')
cprint.out("Success!")
print("Setting csp var")
csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
print("csp adding constraint")
csp.add_constraint(logic_circuit, ['a', 'b', 'c', 'd','e','f','g'])

print("converting to bqm")
print("Started "+str(datetime.now()))
start = time.time()

# Convert the binary constraint satisfaction problem to a binary quadratic model
bqm = dwavebinarycsp.stitch(csp)
done = time.time()
print("Finished in "+str(done-start))
print("Completed "+str(datetime.now()))

print("printing bqm\n")

cprint.cfg('m', 'k', 'b')
cprint.out(bqm)
print("\n")
print("making sampler")
sampler = EmbeddingComposite(DWaveSampler())
print("making sampleset")
print("Started "+str(datetime.now()))

start = time.time()
samplesize=10
print("Samplesize is "+str(samplesize))
sampleset = sampler.sample(bqm, num_reads=samplesize, label='output')
done = time.time()
print("Finished in "+str(done-start))
print("Completed "+str(datetime.now()))

print("printing sampleset")
print("<SAMPLESET>\n")
cprint.cfg('b', 'k', 'b')

cprint.out(sampleset)

print("\n</END OF SAMPLESET>")
cprint.cfg('b', 'k', 'b')
cprint.out("Completed "+str(datetime.now()))