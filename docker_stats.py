import csv
import time

import docker

cli = docker.from_env()

running_containers = cli.containers.list()

with open('sim_data.csv', 'w') as data_file:
    print('Writing docker data to file')
    for i in range(0,5):
        for container in running_containers:
            stats = cli.containers.get(container.name).stats(stream=False)
            memory_usage = stats["memory_stats"]["usage"] - stats["memory_stats"]["stats"]["inactive_file"]
            memory = float(memory_usage/1024)/1000 # convert memory to MiB

            writer = csv.writer(data_file)
            writer.writerow([container.name, memory])
            print([container.name, memory])
        time.sleep(1)
        print('Stats data written')
    print('Docker data written to file')
print('You can now view the memory information')
