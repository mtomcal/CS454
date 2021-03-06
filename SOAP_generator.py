import os
import re
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
#		can be joined. May contain tuples for differentiated
#		mate pair and paired end values. Paired end is first element, mate pair, second.
#	(int) map_len:
#		The minimum length of the overlapping sequences of bases. Minimum value is 5. May contain 
#		tuples for differentiated mate pair and paired end values. Paired end is first 
#		element, mate pair, second.
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
	

	
	#Needs name of config file and sanitize
	configName = sanitize('config_%s_%s.txt' % (str(pair_num_cutoff), str(map_len)))
	#Output folder and sanitize
	outFolder = sanitize('Results_%s_%s_%d_%d' % (str(pair_num_cutoff), str(map_len), kmerFreqCutoff, kmerLength))
	#Create new file and sanitize name
	filename = sanitize('soap_%s_%s_%d_%d.sh' % (str(pair_num_cutoff), str(map_len),kmerFreqCutoff, kmerLength))
	scriptFile = open(filename, 'w+')
	scriptFile.write(scriptTemplate % {'kmerFreqCutoff':sanitize(str(kmerFreqCutoff)), 
	                                   'kmerLength':sanitize(str(kmerLength)), 
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
	
	#Create new file and sanitize for shell
	filename = 'config_%s_%s.txt' % (str(pair_num_cutoff), str(map_len))
	configFile = open(sanitize(filename), 'w+')
	try:
		#Tuple detected
		configFile.write(configTemplate % {'pair_num_cutoff_PE':str(pair_num_cutoff[0]),'map_len_PE':str(map_len[0]),
		                                   'pair_num_cutoff_MP':str(pair_num_cutoff[1]),'map_len_MP':str(map_len[1])})
	except:
		#No Tuple
		configFile.write(configTemplate % {'pair_num_cutoff_PE':str(pair_num_cutoff),'map_len_PE':str(map_len),
		                                   'pair_num_cutoff_MP':str(pair_num_cutoff),'map_len_MP':str(map_len)})
		pass
	configFile.close()

def generateScripts(pairNums, map_lens, freqCutoffs, kmerLens):
	'''
	description:
		Runs through all of the lists, generating scripts with each of the parameter permutations.
	args:
		(int list) pairNums:
			List of pair_num_cutoff values. May contain tuples for differentiated
			mate pair and paired end values. Paired end is first element, mate pair, second.
		(int list) map_lens:
			List of map_len values. May contain tuples for differentiated
			mate pair and paired end values. Paired end is first element, mate pair, second.
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

def sanitize(toClean):
	'''
	Utility used to clean names up for Unix
	'''
	toClean = re.sub('[,]','-', toClean)
	toClean = re.sub('[() ]','', toClean)
	return toClean
######################################################
#						MAIN						 #
######################################################
#Main function. Runs the script.
if __name__ == "__main__":
		
	#EDIT THESE VALUES IN ORDER TO GENERATE YOUR SCRIPTS
	#40_34_23_30
	pairNums	= [(5,7),(7,11)]		#Min number of times paired/matched
	map_lens	= [(31,33),(35,37)]	#Minimum overlap amount
	freqCutoffs = [0]		#Maximum kmer frequency cap
	kmerLens	= [49,55,63]		#Kmer length
	print 'Starting up script...'
	generateScripts(pairNums, map_lens, freqCutoffs, kmerLens)
