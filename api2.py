"""
@Avinash Reddy Penugonda


"""

import os
import time                     #import libraries

try:
    import psutil;              #import third party libraries for CPU metrics
except ImportError:
    print("problem in importing psutil...Exiting...");
    sys.exit();

try:
    import datadog;             #import datadog libraries for API calls
except ImportError:
    print("problem in importing datadog...Exiting...");
    sys.exit();

from datadog import initialize,api
options={
    'api_key':'YOUR API KEY',   #api key initialization
    }
initialize(**options)

def staticParameters():                             #function for static parameters that are almost constant
    apiCall('my.system.cpu',psutil.cpu_count(logical=True))
    apiCall('my.system.processes',numProcess())

def numProcess():                                   #function to get the number of processes running in the system
    count=0
    for proc in psutil.process_iter():
        try:
            count=count+1
        except psutil.NoSuchProcess:
            pass
    return(count)

def avgThreeParam(array):                           #function which takes ans nx3 matrix and adds up each column to find the average value
    load=[0,0,0]
    for i in range(len(array)):
        load[0]+=array[i][0]                        #add the columns for average
        load[1]+=array[i][1]
        load[2]+=array[i][2]
    for i in range(len(array[0])):
        load[i]=load[i]/(len(array)*os.cpu_count()) #final step= sum/(num of measurements) and I also normalize the CPU load to 1
    return (load);
    
def avgOneParam(array):                             #function to find an average of an array of elements                            
    util=0;
    for i in range(len(array)):
        util+=array[i]
    util=util/len(array)
    return (util)   
    
def apiCall(met,val):                               #call to the API
    api.Metric.send([{'metric':met,'points':val,'host':"python",'tags':["version:1"]}])

def clearCollector(array):                          #to clear the array after 10 seconds from previous data to store new data
    for i in array:
        i.clear()

def nonEmpty(array):                                # to check if data is collected or not
    if len(array)>0:
        return (True)
    else:
        return(False)
    
#load_Arr[0]
#cpu_util[1]
#mem_used[2]
#swap_used[3]
#disk_used[4]
collector=[[],[],[],[],[]]                      #each sub-array is to continuously append similar metrics which are later calculated for average
t1=time.time();
interval=10                                     #time interval to aggregate the data

while(True):                                    #infinite loop
    staticParameters();
    data_reads_in=psutil.disk_io_counters(perdisk=False)[0]         #finds the number of reads in at the start and also at the end to find reads/sec
    data_writes_out=psutil.disk_io_counters(perdisk=False)[1]
    net_pack_out=psutil.net_io_counters()[2]                        #finds the number of packes sent at the start and also at the end to find packets sent/sec
    net_pack_in=psutil.net_io_counters()[3] 
    while((time.time()-t1)<=interval):                              #condition to aggregate data for 10 sec
        collector[0].append(list(os.getloadavg()))
        collector[1].append(psutil.cpu_percent(interval=0.5, percpu=False))     #find the current metric value and append it to the array
        collector[2].append(psutil.virtual_memory()[2])
        collector[3].append(psutil.swap_memory()[3])
        collector[4].append(psutil.disk_usage('/')[3])
        time.sleep(2)                                                   #sleep for 2 seconds
    t1=time.time()
    
    if(nonEmpty(collector[0])):                                 #condition to see if array is not empty, to prevent any exceptions of array indexing
        avg=avgThreeParam(collector[0])                         #call the average function
        apiCall('my.system.load1',avg[0])
        apiCall('my.system.load5',avg[1])                       #Api calls
        apiCall('my.system.load15',avg[2])
        print("Avg Cpu load calculated and sent!")

    if(nonEmpty(collector[1])):                                 #condition to see if array is not empty, to prevent any exceptions of array indexing
        apiCall('my.system.cpuUtil',avgOneParam(collector[1]))  #call the averagae function and api call
        print("Avg Cpu Utilization calculated and sent!")       

    if(nonEmpty(collector[2])):
        apiCall('my.system.memoryUsed',avgOneParam(collector[2]))
        print("Avg Memory utilization calculated and sent!")
    
    if(nonEmpty(collector[3])):
        apiCall('my.system.swapUsed',avgOneParam(collector[3]))
        print("Avg swap memory utiliation calculated and sent!")
        
    if(nonEmpty(collector[4])):
        apiCall('my.system.diskUsed',avgOneParam(collector[4]))
        print("Disk utilization sent!")

    if(data_reads_in >0 and data_writes_out >0):
        apiCall('my.system.dataReadsIn',(psutil.disk_io_counters(perdisk=False)[0]-data_reads_in)/(interval+2))     #find avg read in/sec and write out/sec
        apiCall('my.system.dataWritesOut',(psutil.disk_io_counters(perdisk=False)[1]-data_writes_out)/(interval+2))
        print("Avg read in/sec and write out/sec calculated and sent!")

    if(net_pack_in>0 and net_pack_out >0):
        apiCall('my.system.packetsIn',(psutil.net_io_counters()[3]-net_pack_in)/(interval+2))
        apiCall('my.system.packetsOut',(psutil.net_io_counters()[2]-net_pack_out)/(interval+2))
        print("Avg packets in/sec, packets out/sec calculated and sent!")
    clearCollector(collector)                                   #function call to clear the arrays for a new set of measurements
    print("\n")
