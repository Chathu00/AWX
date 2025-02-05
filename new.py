
import os
import psutil
import shutil
import datetime

# Fetch files from a specific directory
def fetch_files(source_path, destination_path):
    try:
        if os.path.exists(source_path):
            shutil.copy(source_path, destination_path)
            print(f"File copied from {source_path} to {destination_path}")
        else:
            print(f"Source file does not exist: {source_path}")
    except Exception as e:
        print(f"Error fetching file: {e}")

# Scrape log file and fetch logs for a specific duration
def scrape_logs(log_file, start_time, end_time):
    try:
        if not os.path.exists(log_file):
            print(f"Log file not found: {log_file}")
            return
        
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M")
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M")
        
        with open(log_file, "r") as file:
            logs = file.readlines()

        print(f"\nLogs from {start_time} to {end_time}:\n")
        for line in logs:
            if any(keyword in line for keyword in [start_time.strftime("%Y-%m-%d %H:%M"), end_time.strftime("%Y-%m-%d %H:%M")]):
                print(line.strip())

    except Exception as e:
        print(f"Error reading log file: {e}")

# Check for high CPU and Memory usage
def check_high_memory_cpu(threshold_cpu=50, threshold_memory=500):
    print("\nChecking high CPU and memory usage processes...\n")
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            cpu_usage = proc.info['cpu_percent']
            mem_usage = proc.info['memory_info'].rss / (1024 * 1024)  # Convert bytes to MB
            
            if cpu_usage > threshold_cpu or mem_usage > threshold_memory:
                print(f"High Usage Process: {proc.info}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

#Kill a process by PID
def kill_process(pid):
    try:
        process = psutil.Process(pid)
        process.terminate()
        print(f"Process {pid} terminated successfully.")
    except psutil.NoSuchProcess:
        print(f"Process {pid} not found.")
    except Exception as e:
        print(f"Error terminating process {pid}: {e}")

#Check disk utilization
def check_disk_utilization():
    disk_usage = psutil.disk_usage('/')
    print(f"\n Disk Usage: {disk_usage.percent}%\n")

#Execute all tasks
if __name__ == "__main__":
    # Example Usage
    fetch_files("C:/logs/app.log", "./app.log")
    scrape_logs("C:/logs/app.log", "2025-02-01 10:00", "2025-02-01 12:00")
    check_high_memory_cpu()
    check_disk_utilization()

    # Example: Killing a process (Replace with actual PID)
    kill_process(1884)  
