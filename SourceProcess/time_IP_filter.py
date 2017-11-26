#!/bin/python

import datetime
import logging

logging.basicCofing(level=logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')

timelist = ['16:00:00','16:30:00','17:00:00','17:30:00','18:00:00','18:30:00','19:00:00','19:30:00','20:00:00']
timeoutputlist = []
datetimelist = []

InnerIP_list = ['166.111','59.66','101.5','101.6','183.172','183.173','118.229']
fin = open('0517.txt','r')

for time in timelist:
    timestrl = '2017-05-17 '+time
    timeoutputlist.append('./timefiles/'+ time + '.txt')
    datetimelist.append(datetime.datetime.strptime(timestrl,'%Y-%m-%d %H:%M:%S'))

print datetimelist[8]

IPlist = [{},{},{},{},{},{},{},{},{}]
line = fin.readline()
while line:
    line = fin.readline()
    try:
        items = line.split(',')
        time = items[5]
        dstIP = items[4]
        rttavg = items[6]
        timeTuple = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')

        IPdetails = dstIP.split('.')
        IPprefix = '.'.join(IPdetails[0:2])
        if IPprefix in InnerIP_list:
            continue

        flag = 10
        for i in range(9):
            if timeTuple > datetimelist[i]:
                continue
            if timeTuple < datetimelist[i]:
                continue
            flag = i
            break

        if flag > 8:
            continue

        i = flag
        if dstIP in IPlist[i]:
            IPlist[i][dstIP].append((time,rttavg))
        if dstIP not in IPlist[i]:
            IPlist[i][dstIP] = [(time,rttavg)]

    except IndexError:
        fin.close()
        break


for i in range(9):
    foutstr = timeoutputlist[i]
    fout = open(foutstr,'w')
    for ip in IPlist[i]:
        prtline = [ip]
        for item in IPlist[i][ip]:
            prtline.append('('+','.join(item)+')')
        fout.write(' '.join(prtline)+'\n')

    fout.close()



        

