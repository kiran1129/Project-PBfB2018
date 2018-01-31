#! /usr/bin/env python

#A python script for searches in an SQL database

#Preparations before the interactions with the user start
#--------------------------------------------------------

#load the modules needed
import MySQLdb		#for the interactions with MySQL

#make a connection to the SQL server
MyConnection = MySQLdb.connect( host = "localhost", user = "root", passwd = "PBfB2018", db = "lactis")
MyCursor = MyConnection.cursor()

#preparing to write the results in a file
ResultFileName = "SearchResults.txt"
ResultFile = open(ResultFileName, 'w')


#Interaction with the user - getting the variables for the search
#----------------------------------------------------------------

#print an introduction to the script for the user
StartingPrompt='''This is a search engine for the database "lactis.sql"

You can search among the following fields:

* device\t*location\t*owner\t*species\t*strain
* plasmid\t*info\t*abm(antibiotic marker)\t*genotype\t*datum

Please choose only one field. 
'''
print StartingPrompt

##Get the columns to be searched
#-------------------------------

#save the search field
SearchField = raw_input("In which field do you want to search?\n")

#Check the search term and request new input until it matches the mySQL format (small letters)
SearchFieldList=['device','location','owner','species','strain','plasmid','info','abm(antibiotic marker)','abm','abm (antibiotic marker)','genotype','datum']

while SearchField not in SearchFieldList:
        SearchField=raw_input("Field not recognized. Input has to be in small letters. Please type again!\n")

#the ambigous input for the antibiotic marker is reformatted for the mySQL command
if SearchField == 'abm(antibiotic marker)' or SearchField == 'abm (antibiotic marker)':
        SearchField = 'abm'

#save the search term
SearchTerm = raw_input("Please enter your search term. You can use % as a wildcard.\n")

#Also add variations to the searchterm (all caps, all minor)
SearchTermList = [SearchTerm]

SearchTermList.append(SearchTerm.upper())
SearchTermList.append(SearchTerm.lower())


##Ask whether the results should be sorted according to a certain column
#-----------------------------------------------------------------------

#Any sorting?
print "Do you want to sort the results?"
SortYN = raw_input("Yes/No\t")

#A list with possible answers to the input request
SortYList = ['Yes','yes','Y','y','YES','Ja','ja','J','j']

#if sorting, ask for the column
if SortYN in SortYList:
        SearchSort = raw_input("According to what column do wou want to sort your results?")

	#Check the input for the sorting column
	while SearchSort not in SearchFieldList:
        	SearchSort=raw_input("Field not recognized. Input has to be in small letters. Please type again!\n")



#Create several mySQL search commands
#------------------------------------

#A list to collect all the possible commands for mySQL depending on the different search terms
SQLSearchList=[]

#Loop through the Search terms created above
for term in SearchTermList:
	if SortYN not in SortYList:
		#mySQL command without sorting
		SQL = "SELECT device,location,owner,species,strain,plasmid,info,abm,genotype,datum FROM lactis WHERE %s LIKE '%s';" % (SearchField, term)
		SQLSearchList.append(SQL)		#add the commands to the mySQL command list
		print SQL	#developping line
	else:
		#mySQL command with sorting
		SQL = "SELECT device,location,owner,species,strain,plasmid,info,abm,genotype,datum from lactis WHERE %s LIKE '%s' ORDER BY %s;" % (SearchField, term, SearchSort)
		SQLSearchList.append(SQL)		#add the commands to the mySQL command list
		print SQL	#developping line


#Header of the screen output
#---------------------------

#print "Your SQL Search: ", SQL			#prints the command as check
#print
#print "Number of hits: %d " % SQLresultTotal
#print
print "-----------------------------------------------------------------------------------------------"
print "Device    \tLocation\towner\tspecies\tstrain\tplasmid\tinfo\tabm\tgenotype\tdatum"
print "-----------------------------------------------------------------------------------------------"
print


#The header of the file
#----------------------

#ResultFile.write("\n 
#Your SQL Search: ")
#ResultFile.write(SQL)
#ResultFile.write("\n
#Number of hits: ")
#ResultFile.write(str(SQLresultTotal))
ResultFile.write("""\n
-----------------------------------------------------------------------------------------------
Device    \tLocation\towner\tspecies\tstrain\tplasmid\tinfo\tabm\tgenotype\tdatum
-----------------------------------------------------------------------------------------------

""")


#Executing the different commands
#--------------------------------

#A list that will collect the results
SQLresultList = []
SQLresultTotal = 0

for term in SQLSearchList:
	print term
        SQLresult=MyCursor.execute(term)         #executes the command and collects the results
	print SQLresult
        SQLresultTotal = SQLresultTotal + SQLresult
	FirstResults=MyCursor.fetchall()         #variable that contains the search results
	SQLresultList.append(FirstResults)       #appends the collected results to a list
	for Index in range(SQLresult):
		#create a list with all entries of one query
		entry=[FirstResults[Index][0],FirstResults[Index][1],FirstResults[Index][2],FirstResults[Index][3],FirstResults[Index][4],FirstResults[Index][5],FirstResults[Index][6],FirstResults[Index][7],FirstResults[Index][8],FirstResults[Index][9]]
		#print the list for the current line
		ResultLine = "{e[0]}\t{e[1]}\t{e[2]}\t{e[3]:15}\t{e[4]:15}\t{e[5]}\t{e[6]}\t{e[7]}\t{e[8]}\t{e[9]}".format(e=entry)
		print ResultLine
		#write the line to the destination file
		ResultFile.write(ResultLine+"\n")

#print SQLresultList[0]
print SQLresultList[0][0]


#Print the Search results at the end, if there are more than 20 results
if SQLresult >20:
	print "--------------------------------------------------------------------------------------------------"
        print "Device    \tLocation\towner\tspecies\tstrain\tplasmid\tinfo\tabm\tgenotype\tdatum"
        print "--------------------------------------------------------------------------------------------------"
	#print
	#print "Your SQL Search: ", SQL                  #prints the command as check
	print
	print "Number of hits: %d " % SQLresultTotal
	print
	print "--------------------------------------------------------------------------------------------------"


#close the written file
ResultFile.close()

#close the conncection to the SQL server
MyCursor.close()
MyConnection.close()
