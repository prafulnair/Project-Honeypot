import psutil
from datetime import datetime
import pandas as pd


# =======================================================
flag = 0

for proc in psutil.process_iter():
    try:
        pName = proc.name()
        pID = proc.pid
        pstr = str(pName)+"\n"  #+":::"+str(pID)
        print(pstr)
        #first time write entire file
        if flag == 0:
            file1 = open("NORMAL_MODE_processes.txt","w")
            file1.write(pstr)
            file1.close()
            flag = 1
        else:
            file1 = open("NORMAL_MODE_processes.txt","a")
            file1.write(pstr)
            file1.close()

    except Exception as e:
        raise
    else:
        pass
    finally:
        pass

# =======================================================



def compare(File1,File2):
    with open(File1,'r') as f:
        d=set(f.readlines())


    with open(File2,'r') as f:
        e=set(f.readlines())

    open('file3.txt','w').close() #Create the file

    with open('file3.txt','a') as f:
        for line in list(d-e):
           f.write(line)

file1 = "SAFE_MODE_processes.txt"
file2 = "NORMAL_MODE_processes.txt"
compare(file2,file1)



def get_size(bytes):
    """
    Returns size of bytes in a nice format
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return(f"{bytes:.2f}{unit}B")
        bytes /= 1024
processes = []
i=0

file = open('file3.txt','r')
 # read file line by line

Lines = file.readlines() 
count = 0
procsName = []
# Strips the newline character 
for line in Lines: 
    # print(line.strip())
    print("Line{}: {}".format(count, line.strip()))
    count +=1
    procsName.append(line.strip())

# end of reading file


for process in psutil.process_iter():
    
    if(process.name() in procsName):
        with process.oneshot():
            pid = process.pid
            name = process.name()
            create_time = datetime.fromtimestamp(process.create_time())
            i=i+1
            print(i,".",name,"\n")

            try:
                cores = len(process.cpu_affinity())
            except psutil.AccessDenied:
                cores = 0

            cpu_usage = process.cpu_percent(interval=0.4)
            status = process.status()

            try:
                nice = int(process.nice())
            except psutil.AccessDenied:
                nice = 0

            try:
                memory_usage = process.memory_percent()
                #memory_usage = process.memory_full_info().uss
            except psutil.AccessDenied:
                memory_usage = 0
            #counting process total, written bytes
            io_counters = process.io_counters()
            read_bytes = io_counters.read_bytes
            write_bytes = io_counters.write_bytes

            #get number of total threads taken by this process
            n_threads = process.num_threads()

            try:
                username = process.username()
            except psutil.AccessDenied:
                username = "Cant retrieve information"


        processes.append({
            'pid': pid, 'name': name, 'create_time' : create_time, 'cores' : cores, 'cpu_usage' : cpu_usage,
            'status' : status, 'nice' : nice, 'memory_usage' : memory_usage, 'read_bytes' : read_bytes,
            'write_bytes' : write_bytes, 'n_threads':n_threads, 'usernames' : username
        })

print("---------printing suspected Process Details------------")
print(processes)
print("-------------------------------------------------------")

    #using pandasdataframe to covert this process list
df = pd.DataFrame(processes)
# set the process id as index of a process
df.set_index('pid', inplace=True)
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Process Viewer & Monitor")
    parser.add_argument("-c", "--columns", help="""Columns to show,
                                                available are name,create_time,cores,cpu_usage,status,nice,memory_usage,read_bytes,write_bytes,n_threads,username.
                                                Default is name,cpu_usage,memory_usage,read_bytes,write_bytes,status,create_time,nice,n_threads,cores.""",
                        default="name,cpu_usage,memory_usage,read_bytes,write_bytes,status,create_time,nice,n_threads,cores")
    parser.add_argument("-s", "--sort-by", dest="sort_by", help="Column to sort by, default is memory_usage .", default="memory_usage")
    parser.add_argument("--descending", action="store_true", help="Whether to sort in descending order.")
    parser.add_argument("-n", help="Number of processes to show, will show all if 0 is specified, default is 25 .", default=25)

    # parse arguments
    args = parser.parse_args()
    columns = args.columns
    sort_by = args.sort_by
    descending = args.descending
    n = int(args.n)

    # sort rows by the column passed as argument
    df.sort_values(sort_by, inplace=True, ascending=not descending)
    # pretty printing bytes
    df['memory_usage'] = df['memory_usage'].apply(get_size)
    df['write_bytes'] = df['write_bytes'].apply(get_size)
    df['read_bytes'] = df['read_bytes'].apply(get_size)
    # convert to proper date format
    df['create_time'] = df['create_time'].apply(datetime.strftime, args=("%Y-%m-%d %H:%M:%S",))
    # reorder and define used columns
    df = df[columns.split(",")]
    # print
    if n == 0:
        print(df.to_string())
    elif n > 0:
        print(df.head(n).to_string())



