import os






for directory in next(os.walk('./reads_by_sample'))[1]:
	count = 0
	command = "/data/mschatz1/bbock4/kraken2-master/kraken2 --db /data/mschatz1/bbock4/kraken2-master/standard_db --threads 48 --gzip-compressed --report /data/mschatz1/bbock4/classifications/" + directory + ".report --paired "
	for file in os.listdir("./reads_by_sample/" + directory):
		if("_1" in file or "_2" in file):
			command = command + " /data/mschatz1/bbock4/reads_by_sample/" + directory + "/" + file
			count += 1
	command = command + " | tee /data/mschatz1/bbock4/classifications/" + directory + ".txt"
	print(command)

