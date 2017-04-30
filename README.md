# Datadog-metrics
Learn and use Datadog monitoring tools for CPU performance metrics
attps://github.ctantly collect CPU performance metrics and sends it to Datadog API to visuvalize the data and get useful results

Packages & Libraries used: psutil, datadog, time, os
VM's used: Mac, Two EC2 Containers(test load and python script are run as background process to monitor the metrics continuously)

Goal: to design an Acitivy monitor similar to the one in MAC and deploy it on many Virtual server machines, see them in action and learn Datadog.

Assumptions:
1. Tested on Macbook and Linux
2. One data point sent to Datadog every ~15 seconds (granularity can be increased but I don't think we require to send data so frequently, also it overloads the system)
3. the metric values are collected with a time period of 2 sec and averaged at the tenth second and sent to the API
4. If ther is a problem in collecting a metric, I skipped that datapoint and sent other metrics to the API

Metrics measured:
    CPU utilization (%)
    CPU Load time for 1 min, 5 min and 15 minutes
    Percentage of Memory utilization (RAM & Swap memory)
    number of processors
    Total disk utilization(%)
    Number of processes running currently
    Number of packets sent and received per sec
    Number of reads and writes per sec
    
Features:
1. Works on Linux /Mac
2. Measures the hardware specs: CPU, Memory, Network, I/O, Disk
3. Monitors to monitor any drastic change in any metric and sends a mail if it's above the threshold
4. Events triggerd to the dashboard
5. Markers to help better understand the visuvalization
6. Better knowledge on Infrastructure, Host map

Worked on:
1. used StatsD server (Datadog agent) to send the metrics at first stage of the project
2. Wrote a python script which sends almost the same type of metrics from my Mac later.
3. Integrated three custom Activity monitors using HTTP API and one using Datadog StatsD server(Datadog agent):
    a. EC2 Custom Activity Monitor -- Java instance [less CPU load] is a EC2 ubuntu instance that runs the script and load as background processes [continuous data on Datadog].
    b. EC2 Custom Activity Monitor -- Python instance [high CPU load] is a EC2 ubuntu instance that runs the script and load as background processes [continuous data Datadog].
    c. Mac Activity Monitor -- The script from my Mac is not run continuously
    d. Activity Monitor using StatsD server (Datadog agents by defualt sends the CPU metris on which the agent is running, so didn't create a custom dashboard)
4. EC2 Custom Activity Monitor -- Java instance [less CPU load] has a low test load running along with the python script measuring the metrics continuously and sending it to the API
5. EC2 Custom Activity Monitor -- Python instance [high CPU load] has a high test load running along with the python script measuring the metrics continuously and sending it to the API.
6. Mac Activity Monitor -- sends the metrics of my Mac to the Datadog
7. Could not find time to work on Integrations but would love to if I find some time before Thursday.

Conclusion:
Impressed by Datadog and it's ease of use, libraries, integrations and capabilities
