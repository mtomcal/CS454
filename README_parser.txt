SOAP_parser.py Instructions
	This program can be just run as `python SOAP_parser.py` with default settings, or it
	can be run with up to three other arguments given. These arguments, in order are:
		-The path of the directory which contains the SOAP output folders of the format
		 Results_####
		-The path to the template file the program will base the output off of
		-The filename to give to the outputted file.
	In short, the usage is:
		SOAP_parser.py <Soap out folder> <Outputted file template> <Outputted file name>
	In order, the default settings are:
		/ibrix/home7/stein2/Bioinformatics/out/
		dataTemplate.txt
		SOAP_stats.txt
	If any statistics files aren't found, generating errors, these will manifest in the 
	form of negative numbers in the output file.
Templating:
	In the template file, you can choose how to set the outputs by putting them in the
	format %(attribute)s. The $()s surrounding the name of the attribute is used by 
	Python to make a format string. Here are all the available attributes to choose from.
		contigs
			The number of contigs
		kmerFreqCutoff
			Cutoff number for the frequency of kmers
		kmerLength
			The length of the kmers
		longestScaffold
			The longer scaffold
		map_len
			The minimum overlap amount for combining sequences
		n
			The number of N's
		N50
			N50 of scaffolds
		N90
			N90 of scaffols
		pair_num_cutoff
			How many times a pair of sequences can overlap before being considered for
			combination
		percentScaffolds
			Percentage of outputs that are scaffolds. (scaffolds/(scaffolds+singletons))
		scaffolds
			Number of scaffolds
		scaffoldsAndSingletons
			Number of scaffolds and singletons
		scaffoldsOver100K
			Number of scaffolds over 100K base pairs in length
		scaffoldsOver10K
			Number of scaffolds over 10K in length
		scaffoldsOver1K
			Number of scaffolds over 1K in length
		scaffoldsOver1M
			Number of scaffolds over 1M in length
		scaffoldsOver500
			Number of scaffolds over 500 in length
		singletons
			Number of singletons
		sizeWithN
			Size of output with N's
		sizeWithoutN
			Size without N's included