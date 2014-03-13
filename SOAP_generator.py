import os

#SOAP file generator
#Alexander Stein 2014, CIS 454: Bioinformatics, University of Oregon
#
#DESCRIPTION
#	Python script for generating files with differing parameters. The functions aren't really
#important to look at for out needs unless you're curious about how they work. What is
#important is the main function at the bottom which you can edit to generate different 
#SOAP scripts.
#	There are four editable parameters, and this program works by iterating through and
#generating files with combinations of all of the inputed lists of values you supply. So
#if your list length are 4, 2, 1, and 5, 40 different scripts will be generated, for
#example, so wariness will have to be exercised so that you don't end up generating
#very large volumes of scripts on accident that you may not end up using.
#
#USAGE
#	Go down to the main function at the bottom and edit your parameters. Then from there
#all you need to do is run the script with python.
#Files will be outputted to a subfolder, "SOAP_generator_out".
#
#
#Variable parameters:
#
#	(int) pair_num_cutoff:
#		Minimum amount of times a sequence of base pairs can overlap before two contigs
#		can be joined.
#	(int) map_len:
#		The minimum length of the overlapping sequences of bases. Minimum value is 5.
#	(int) kmerFreqCutoff:
#		Maximum frequency that kmers may appear before being cut off.
#	(int) kmerLength:
#		The size of the kmers. Input is a number from 13 to 127.
######################################################
#				       SETUP						 #
######################################################

#Some "constants"
#Read in template from file.
f = open('SOAP_template.txt' , 'r')
scriptTemplate = f.read()
f.close()
f = open('config_template.txt' , 'r')
configTemplate = f.read()	
f.close()
######################################################
#				     FUNCTIONS						 #
######################################################

def outputScript(pair_num_cutoff, map_len,kmerFreqCutoff, kmerLength):
	'''
	description:
		Generates a soapdenovo script 
	args:
		(int) pair_num_cutoff:
			Minimum amount of times a sequence of base pairs can overlap before two contigs
			can be joined.
		(int) map_len:
			The minimum length of the overlapping sequences of bases. Minimum value is 5.
		(int) kmerFreqCutoff:
			Maximum frequency that kmers may appear before being cut off.
		(int) kmerLength:
			The size of the kmers. Input is a number from 13 to 127.
	return:
		Generates a .sh and config file with name of the format 
		soap_<pair_num_cutoff>_<map_len>_<kmerFreqCutoff>_<kmerLength>.sh
	'''
	#Validate input
	if kmerLength < 13 or kmerLength > 127:
		raise ValueError('kmerLength not between 13 and 127. Recieved value: ' + str(kmerLength))
	else:
		print ("Generating script with kmerFreqCutoff = " + str(kmerFreqCutoff) + " and kmerLength = " + str(kmerLength))
	

	
	#Needs name of config file
	configName = 'config_%d_%d.txt' % (pair_num_cutoff, map_len)
	#Output folder
	outFolder = 'Results_%d_%d_%d_%d' % (pair_num_cutoff, map_len, kmerFreqCutoff, kmerLength)
	#Create new file
	scriptFile = open('soap_%d_%d_%d_%d.sh' % (pair_num_cutoff, map_len,kmerFreqCutoff, kmerLength), 'w+')
	scriptFile.write(scriptTemplate % {'kmerFreqCutoff':str(kmerFreqCutoff), 
	                                   'kmerLength':str(kmerLength), 
	                                   'config':configName, 
	                                   'out':outFolder})
	scriptFile.close()


def outputConfig(pair_num_cutoff, map_len):
	'''
	description:
		Generates a soapdenovo configuration file. 
	args:
		(int) pair_num_cutoff:
			Minimum amount of times a sequence of base pairs can overlap before two contigs
			can be joined. If given 2-plet, the first will go to the paired-end library 
			and the 2nd will go to the mate pair.
		(int) map_len:
			The minimum length of the overlapping sequences of bases. Minimum value is 5.
	return:
		Generates a config file with name of the format 
		config_<pair_num_cutoff>_<map_len>.sh
	'''
	#Validate input
	if map_len < 5:
		raise ValueError('map_len cannot be less than 5. Recieved value: ' + str(map_len))
	else:
		print ("Generating config with pair_num_cutoff = " + str(pair_num_cutoff) + " and map_len = " + str(map_len))
	
	#Create new file
	configFile = open('config_%s_%s.txt' % (str(pair_num_cutoff), str(map_len)), 'w+')
	try:
		configFile.write(configTemplate % {'pair_num_cutoff':str(pair_num_cutoff), 'map_len':str(map_len)})
	except:
		configFile.close()

def generateScripts(pairNums, map_lens, freqCutoffs, kmerLens):
	'''
	description:
		Runs through all of the lists, generating scripts with each of the parameter permutations.
	args:
		(int list) pairNums:
			List of pair_num_cutoff values.
		(int list) map_lens:
			List of map_len values.
		(int list) freqCutoffs:
			List of kmerFreqCutoff values.
		(int list) kmerLens:
			List of kmerLength values.
	return:
		Generates a .sh and config file with name of the format 
		soap_<pair_num_cutoff>_<map_len>_<kmerFreqCutoff>_<kmerLength>.sh
		config_<pair_num_cutoff>_<map_len>.sh
	'''
	#Make new directory for the files if one doesn't exist
	try:
		os.chdir('SOAP_generator_out')
	except OSError:
		os.makedirs('SOAP_generator_out')
		os.chdir('SOAP_generator_out')
	
	print ("Generation started...")
	#Outputting config files
	for i in pairNums:
		for j in map_lens:
			outputConfig(i, j)
	#Outputting .sh files
	for i in pairNums:
		for j in map_lens:
			for k in freqCutoffs:
				for l in kmerLens:
					outputScript(i, j,k,l)


######################################################
#						MAIN						 #
######################################################
#Main function. Runs the script.
if __name__ == "__main__":
		
	#EDIT THESE VALUES IN ORDER TO GENERATE YOUR SCRIPTS
	#40_34_23_30
	pairNums	= [5,7]		#Min number of times paired/matched
	map_lens	= [31,35]	#Minimum overlap amount
	freqCutoffs = [0]		#Maximum kmer frequency cap
	kmerLens	= [45,53,61]		#Kmer length
	print 'Starting up script...'
	generateScripts(pairNums, map_lens, freqCutoffs, kmerLens)
