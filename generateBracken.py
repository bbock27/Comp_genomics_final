import os

bracken_dir_path = "/data/mschatz1/bbock4/Bracken-master"
kraken_dir_path = "/data/mschatz1/bbock4/kraken2-master"
kraken_db_path = "/data/mschatz1/bbock4/kraken2-master/standard_db"
bbock_path = "/data/mschatz1/bbock4"
count = 0
command = "/data/mschatz1/bbock4/kraken2-master/kraken2 --db /data/mschatz1/bbock4/kraken2-master/standard_db --threads 48 --gzip-compressed --paired "
for file in os.listdir("./classifications"):
	bracken_command = bracken_dir_path + "/bracken " + "-d " + kraken_db_path + " -i "
	if("report" in file and "bracken" not in file):
		bracken_command += bbock_path + "/classifications/" + file + " -o " + bbock_path + "/bracken_reports/" + file.split(".")[0] + ".bracken -r 100 -l S -t 48" 
		# command = command + " /data/mschatz1/bbock4/reads_by_sample/" + directory + "/" + file
		print(bracken_command)
	count += 1
	# count += 1
	# if(count > 2):
	# 	break
# command = command + " | tee /data/mschatz1/bbock4/classifications/" + directory + ".txt"
	# print(command)
print(count)