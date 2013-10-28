#!/bin/python -u

__author__ = "jzhai"

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
    return "{:.2f}".format((d*(1.0/length))**0.5)

def extractcontent(tgzfile, entryfilename):
    tgz = tarfile.open(fileobj=tgzfile, mode='r:gz')
    ct = tgz.getmember(entryfilename)
    return tgz.extractfile(ct)

def printfile(file):
    line = file.readline()
    while line:
        print line,
        line = file.readline()

vms = []
boottimearr = []
uptimearr = []
testddfiles = []
testmysqlfiofiles = []
testvideoiofiles = []
tgz = tarfile.open('../data/16vmlocalssd.tar.gz', "r:gz")
tgzcontent = tgz.getmembers()
for ti in tgzcontent:
    print ti.name
    if ti.name.find("boot") > -1:
        bootinfo = tgz.extractfile(ti)
    if ti.name.find("test-dd") > -1:
        testddfiles.append(ti)
    if ti.name.find("test-mysqlfio") > -1:
        testmysqlfiofiles.append(ti)
    if ti.name.find("test-videoio") > -1:
        testvideoiofiles.append(ti)

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
print "average boot time:" + str(average(boottimearr)) + "s, stdev:" + str(stddev(boottimearr))
#print "average up time:" + str(average(uptimearr))
bootinfo.close()

for tddti in testddfiles:
    #print tddti.name
    tddfile = tgz.extractfile(tddti)
    res = extractcontent(tddfile, "./test-dd.res")
    printfile(res)

tgz.close()
