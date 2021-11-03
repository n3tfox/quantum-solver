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
import array as arr
import json
import numpy as nmpy
import pickle



print("Quantum Solver Engine")
print("Copyright (c) 2021 naru fox")
print("All Rights Reserved\n\n")
print("Staring Program...")
import dwavebinarycsp

print("Defining vars")

varNames=['a', 'b', 'y', 'z']

outNames=['a','b','y','z']
samplesize=10



print("defining binToDec")
def binToDec(inNum):
    numberx=inNum
    dec_number= int(numberx, 2)
    return (dec_number)
    #print('The decimal conversion is:', dec_number)
    #print(type(dec_number))

print("Defining Logic Circuit")

#old circuit
#    str1=str(a)+str(b)+str(c)+str(d)+str(f)+str(g)
#    num1=binToDec(str1)
#    num2=num1*num1
#    output1=num2==49
#  
def logic_circuit(a,b,y,z):
    and1=a and b
    or1=a or b
    not1=not and1
    and2=not1 and or1
    out1=and2
    carry1=and1

    return ((out1==y) and (carry1==z))
print("Setting up custom text format...")
cprint = TextFormatter()
cprint.cfg('g', 'k', 'b')
cprint.out("Success!")
print("Setting csp var")
csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
print("csp adding constraint")

csp.add_constraint(logic_circuit, varNames)

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






print("Samplesize is "+str(samplesize))
sampleset = sampler.sample(bqm, num_reads=samplesize, label='output')
done = time.time()
print("Finished in "+str(done-start))
print("Completed "+str(datetime.now()))

print("printing sampleset")
print("<SAMPLESET>\n")
cprint.cfg('b', 'k', 'b')

cprint.out(sampleset)
cprint.out(type(sampleset))

print("\n</END OF SAMPLESET>")
cprint.cfg('b', 'k', 'b')

#for sample, energy in sampleset.data(varNames):
#    print(sample, csp.check(sample), energy)


print("Starting Packing Into CSV")
valid, invalid, datas = 0, 0, []
for datum in sampleset.data(['sample', 'energy', 'num_occurrences']):
    if (csp.check(datum.sample)):
        valid = valid+datum.num_occurrences
        for i in range(datum.num_occurrences):
            datas.append((datum.sample, datum.energy, '1'))
    else:
        invalid = invalid+datum.num_occurrences
        for i in range(datum.num_occurrences):
            datas.append((datum.sample, datum.energy, '0'))
print(valid, invalid)
print(datas)
print(datas[0][0])
data=sampleset
print(data)
firstLen=len(data)
i=0
tableHeaders = []
def joinaList(list1):
    j=0
    outLine=""
    while j<len(list1):
        outLine=outLine+str(list1[j])
        if not (j==(len(list1)-1)):
            outLine=outLine+","
        j=j+1
    j=0
    return outLine
def joinBoxes(list1,callable1):
    j=0
    outLine=""
    while j<len(list1):
        outLine=outLine+str(callable1(list1[j]))
        if not (j==(len(list1)-1)):
            outLine=outLine+","
        j=j+1
    j=0
    return outLine

print(type(sampleset))
outName=str(datetime.now()).replace(" ","_")+"-results";
# Writing to sample.txt
with open(outName+".txt", "w") as outfile:
    outfile.write(str(sampleset))


#som = SOM_CLASS()

fileObject = open(outName+".bin", "wb")

pickle.dump(sampleset, fileObject)
#som = pickle.load(fileObject)
#som.work()
fileObject.close()

print("Binary data is found at "+outName+".bin");
print("Text data is found at "+outName+".txt");
cprint.out("Completed "+str(datetime.now()))
