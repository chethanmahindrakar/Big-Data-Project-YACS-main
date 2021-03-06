# YACS PROJECT
# worker.py file

'''
Authors:
Ameya Bhamare           PES1201800351
Atmik Ajoy              PES1201800189              
Chethan Mahindrakar     PES1201801126
Dhanya Gowrish          PES1201800965

PES University
'''

import matplotlib.pyplot as plt
import statistics
import datetime
import numpy as np
import time
import matplotlib.pyplot as plt


def task_calc():
    starting_time = dict()
    ending_time = dict()
    task_times = dict()
    task_time_list = []
    i=1

    while(i!=4):
        log_file = open(r"logs/worker"+str(i)+".txt", "r")
        lines = log_file.readlines()

        for line in lines:
            try:
                split_1 = line.split("\t") 
                time_stamp = datetime.datetime.strptime(split_1[0][0:-1], '%Y-%m-%d %H:%M:%S.%f')
                
                
                split_2 = split_1[1].split("->")       
                split_2[0] = split_2[0].strip()
                split_2[1] = split_2[1][0:-1].strip()[1:]
                

                if ((split_2[0] == "Worker has finished executing task") or (split_2[0] == "Worker received task")):
                    split_3 = split_2[1].split(',')                  
                    task_id = split_3[1].split(':')[1].split(']')[0]
                                    
                    if (split_2[0] == "Worker has finished executing task"):                 
                        ending_time[task_id] = time_stamp
                    
                    if (split_2[0] == "Worker received task"):
                        starting_time[task_id] = time_stamp
                    
                    if ((task_id in starting_time) and (task_id in ending_time)):
                        task_times[task_id] = (ending_time[task_id] - starting_time[task_id])
                        
                        task_time_list.append(task_times[task_id].total_seconds())
            except:
                continue
        
        log_file.close()
        i+=1        
    # end of while
                    
    print("MEAN EXECUTION TIME OF TASKS = ", statistics.mean(task_time_list), 'seconds') 
    print("MEDIAN EXECUTION TIME OF TASKS = ", statistics.median(task_time_list), 'seconds') 


def job_calc():
    start_time = dict()
    end_time = dict()
    job_task_times = dict()
    job_time_list = []

    # find job completion times         
    with open("logs/master.txt", 'r') as f:
        lines = f.readlines()
        for line in lines:
            try:
                split_1 = line.split("\t") 
                
                timestamp_string = split_1[0][0:-1]
                time_stamp = datetime.datetime.strptime(timestamp_string, '%Y-%m-%d %H:%M:%S.%f')
                        
                split_4 = split_1[1].split("->")      
                split_4[0] = split_4[0].strip()
                split_4[1] = split_4[1][0:-1].strip()[1:]
                
                if ((split_4[0] == "Job has finished execution") or (split_4[0] == "Job request has been received")):

                    if (split_4[0] == "Job has finished execution"):
                        split_3 = split_4                 
                        job_id = split_3[1].split(':')[1].split(']')[0]
                        end_time[job_id] = time_stamp

                    if (split_4[0] == "Job request has been received"):      
                        job_id = split_4[1].split(',')[0].split(':')[1]
                        start_time[job_id] = time_stamp

                    if ((job_id in start_time) and (job_id in end_time)):
                        job_task_times[job_id] = end_time[job_id] - start_time[job_id]
                        job_time_list.append(job_task_times[job_id].total_seconds())
            except:
                continue
                    
                
    print("\nMEAN EXECUTION TIME OF JOBS = ", statistics.mean(job_time_list), 'seconds') 
    print("MEDIAN EXECUTION TIME OF JOBS = ", statistics.median(job_time_list), 'seconds')



def plot_graph():
    #plot graphs
    wrkr_1=1
    wrkr_2=2
    wrkr_3=3
    x = {wrkr_1:[], wrkr_2:[], wrkr_3:[]}
    y = {wrkr_1:[], wrkr_2:[], wrkr_3:[]}
    count_tasks_per_worker = {1:0, 2:0, 3:0}

    with open("logs/master.txt", 'r') as log_file:
        lines = log_file.readlines()    
        split_1 = lines[0].split("\t") 
        time_stamp = datetime.datetime.strptime(split_1[0][0:-1], '%Y-%m-%d %H:%M:%S.%f')
        starting_time = time_stamp
        for worker_id in x:
            x[worker_id].append(0)
            y[worker_id].append(0)
        
        for line in lines:
            try:
                if line.strip() != '':
                    split_1 = line.split("\t") 
                    time_stamp = datetime.datetime.strptime(split_1[0][0:-1], '%Y-%m-%d %H:%M:%S.%f')

                    split_2 = split_1[1].split("->")       
                    split_2[0] = split_2[0].strip()
                    split_2[1] = split_2[1][0:-1].strip()[1:]
                    
                    if ((split_2[0] == "Received update from worker") or (split_2[0] == "Worker has been sent task") ):
                        split_3 = split_2[1].split(',')               
                        worker_id = int(split_3[0].split(':')[1])
                        
                        if (split_2[0] == "Received update from worker"):
                            count_tasks_per_worker[worker_id] -= 1
                            x[worker_id].append((time_stamp - starting_time).total_seconds())
                            y[worker_id].append(count_tasks_per_worker[worker_id])

                        if (split_2[0] == "Worker has been sent task"):
                            count_tasks_per_worker[worker_id] += 1
                            x[worker_id].append((time_stamp - starting_time).total_seconds())
                            y[worker_id].append(count_tasks_per_worker[worker_id])
            except:
                continue
       


    # Plotting the graph
    fig, ax = plt.subplots(figsize=(30, 5))
    ax.plot(x[1], y[1], color='orange', label="Worker-1")
    ax.plot(x[2], y[2], color='red', label="Worker-2")
    ax.plot(x[3], y[3], color='purple', label="Worker-3")
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Number of Tasks')
    ax.set_title('GRAPH => Number of Tasks VS Time')
    legend = ax.legend(loc='upper left', shadow=False, fontsize='large')
    plt.show()



if __name__=='__main__':
    task_calc()
    job_calc()
    plot_graph()