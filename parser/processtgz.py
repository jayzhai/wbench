#!/bin/python -u

__author__ = "jay.zhai@gmail.com"

import tarfile

def average(arr):
    length = len(arr)
    fltarr = [float(_s) for _s in arr]
    return "{:.2f}".format(sum(fltarr)/length)

def stddev(arr):
    length = len(arr)
    fltarr = [float(_s) for _s in arr]
    m = sum(fltarr)/length
    d = .0
    for i in fltarr:d+=(i-m)**2
    return (d*(1.0/length))**0.5


vms = []
boottimearr = []
uptimearr = []
tgz = tarfile.open('../data/16vmlocalssd.tar.gz', "r:gz")
tgzcontent = tgz.getmembers()
for ti in tgzcontent:
    print ti.name
    if ti.name.find("boot") > -1:
        bootinfo = tgz.extractfile(ti)

line = bootinfo.readline()
while line:
    #print line,
    line = bootinfo.readline()
    if line.startswith("vm"):
        _line = line.split("\t")
        vms.append(_line[0].strip())
        boottimearr.append(_line[1].strip())
        uptimearr.append(_line[2].strip())
print str(vms)
print "average boot time:" + str(average(boottimearr))
#print "average up time:" + str(average(uptimearr))
bootinfo.close()

tgz.close()
