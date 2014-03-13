#Alexander Stein 2014
#CIS 454: Bioinformatics
#Retrieves relevant information from SOAP outputs in the ACISS work directory.

import sys
import os
import re

class SOAPParser:
	def __init__(self, outPath, template='dataTemplate.txt', statsOutputFile='SOAP_stats.txt'):
		'''
		Constructor
		Args:
			outPath:
				The path to the director holding the results folders
			template:
				A template file to style the output
			statsOutputFile:
				The name of the file that the statistics will be outputted into
		'''
		self.outputsFolder = outPath
		self.template = open(template,'r').read()
		self.statsOut = statsOutputFile
	def fetchAttribute(self, sourceFile, attribute, lastOccurence=True):
		'''
		Fetch attribute from a data file.
		Args:
			sourceFile:
				A string or a file object with the information to be searched
			attribute:
				The attribute to search for.
			lastOccurence:
				If stat appears multiple times, grab first if false, last if true.
		'''
		try:		#If given file
			sourceFile = sourceFile.read()
		except:		#String
			#Nothing needs to be done
			pass
		#regex
		regex = '%s[^0-9]*([0-9]*)' % attribute
		results = re.findall(regex, sourceFile)
		
		#Pops off last result
		if lastOccurence:
			return results.pop()
		else:
			return results.pop(0)
		
	def parse(self):
		'''
		Begins parser
		Args:
			(void)
		'''
		print 'Beginning parser...'
		os.chdir(self.outputsFolder)
		#Clear file for writing
		print 'Writing to ' + self.statsOut + '...'
		open(self.statsOut,'w').close()
		#get list of folders.
		folders = os.listdir('.')
		folders = filter(isResults,list(folders))
		for folder in folders:
			print 'Processing folder' + folder + '...'
			self.processFolder(folder)
		print 'Finished!'
	
	def processFolder(self,folder):
		'''
		Grabs data from folder
		Args:
			folder:
				Name of folder to be process
		'''
		#Go inside folder
		os.chdir(folder)
		#Intitialize attributes dictionary
		attributes = {'pair_num_cutoff':-1,'map_len':-1,'kmerFreqCutoff':-1,
		              'sizeWithN':-1, 'sizeWithoutN':-1,
		              'kmerLength':-1,'contigs':-1,'longestScaffold':-1,'singletons':-1,
		              'n':-1,'scaffolds':-1,'N50':-1,'N90':-1, 'scaffoldsAndSingletons':-1,
		              'scaffoldsOver1M':-1, 'scaffoldsOver1K':-1, 'scaffoldsOver10K':-1,
		              'scaffoldsOver100K':-1, 'scaffoldsOver500':-1, 'percentScaffolds':-1}
		
		#Parse folder name
		folderArgs = folder.split("_")
		attributes['pair_num_cutoff'] = folderArgs[1]
		attributes['map_len'] = folderArgs[2]
		attributes['kmerFreqCutoff'] = folderArgs[3]
		attributes['kmerLength'] = folderArgs[4]
		
		#Get file data and parse.
		
		
		
		try:
			#Open err log
			errLog = open('A_k33_2.err.log','r').read()
			#Parse the error log data
			attributes['N50'] = self.fetchAttribute(errLog,'N50')
			attributes['N90'] = self.fetchAttribute(errLog,'N90')
			attributes['scaffolds'] = self.fetchAttribute(errLog,'Scaffold number')
			attributes['longestScaffold'] = self.fetchAttribute(errLog,'Longest scaffold')
			attributes['scaffoldsAndSingletons'] = self.fetchAttribute(errLog,'Scaffold and singleton number')
		except:
			print 'Error: "A_k33_2.err.log" not found'
		try:
			#Open scafStats
			scaffStat = open('out.scafStatistics','r').read()
			#Parse the scafStatistics file
			attributes['contigs'] = self.fetchAttribute(scaffStat,'Contig_Num')
			attributes['sizeWithN'] = self.fetchAttribute(scaffStat,'Size_includeN',False)
			attributes['sizeWithoutN'] = self.fetchAttribute(scaffStat,'Size_withoutN',False)
			attributes['n'] = int(attributes['sizeWithN']) - int(attributes['sizeWithoutN'])
			attributes['scaffoldsOver1M'] = self.fetchAttribute(scaffStat,'scaffolds>1M')
			attributes['scaffoldsOver1K'] = self.fetchAttribute(scaffStat,'scaffolds>1K')
			attributes['scaffoldsOver10K'] = self.fetchAttribute(scaffStat,'scaffolds>10K')
			attributes['scaffoldsOver100K'] = self.fetchAttribute(scaffStat,'scaffolds>100K')
			attributes['scaffoldsOver500'] = self.fetchAttribute(scaffStat,'scaffolds>500')
			attributes['singletons'] = self.fetchAttribute(scaffStat,'Singleton_Num')
			attributes['percentScaffolds'] = str(float(attributes['scaffolds'])/float(attributes['singletons']))
		except:
			print 'Error "out.scafStatistics" not found'
		#Go back out of folder
		os.chdir('..')
		self.outputResult(attributes)
	
	def outputResult(self, attributes):
		'''
		Outputs a sections of results for certain inputs
		Args:
			attributes:
				A dictionary of attribute:value pairs
		'''
		file = open(self.statsOut,'a')
		output = self.template
		output = output % attributes
		file.write(output)
		file.close()
		#TODO

		
def isResults(inputFolder):
	'''
	Utility function for filter() finds SOAP result folders for completed runs
	'''
	return re.search('Results_', inputFolder)
	
	
if __name__ == '__main__':
	#Defaults
	outPath = '/ibrix/home7/stein2/Bioinformatics/out/' 
	template='sample_dataTemplate.txt'
	statsOutputFile='SOAP_stats.txt'
	
	#Check for command line args
	if len(sys.argv) == 4:
		outPath = sys.argv[1]
		template = sys.argv[2]
		statsOutputFile = sys.argv[3]
	elif len(sys.argv) == 3:
		outPath = sys.argv[1]
		template = sys.argv[2]
	elif len(sys.argv) == 2:
		if sys.argv[1] == '-h' or sys.argv[1] == '--help':
			print('Usage: SOAP_parser.py <Soap out folder> <Outputted file template> <Outputted file name>')
			exit()
		outPath = sys.argv[1]
	elif len(sys.argv) == 1:
		pass
	parser = SOAPParser(outPath,template,statsOutputFile)
	parser.parse()
	#ACISS path '/ibrix/home7/stein2/Bioinformatics/out/'