import pandas
import sqlite3

class Searching:
	'''
		Searches a match for the given query for the parameter

		Instance Variables :
			@query : String, Pattern entered by the user to be matched
			@parameter : String, Column name in the database whose value will be matched by the qwery.
						 Contains only two values - COURSE_CODE and COURSE_TITLE
			@cursor : Database (sqlite3) cursor object

		Instance Methods :
			__init__ : Instantiates the instance of the class
			search : matches the query with the given parameter
	'''
	def __init__(self, parameter):
		self.parameter = parameter
		self.lecture, self.tutorial, self.practical = [], [], []

	def search(self, query, cursor):

		cursor.execute ( "SELECT {} FROM courses WHERE {} LIKE ?".format(self.parameter, self.parameter), ('%' + query + '%',))
		match_list = cursor.fetchall()  #This will print all the matched strings 

		self.Print_(match_list)  #only for command line
		prompt = input(' match number :')	
		match_parameter = match_list[prompt] #This is the desired course_code/course_title
		match_id = cursor.execute("SELECT _rowid_ FROM courses WHERE {} = ?".format(self.parameter), match_parameter).fetchall()[0] 
		
		cursor.execute("SELECT * FROM courses WHERE _rowid_ >= ? ", match_id )
		result_list = [cursor.fetchone()] #contains the complete details of the course
		
		try:
			next_record = cursor.fetchone()
			while (not next_record[0]):
				result_list.append(next_record)
				next_record = cursor.fetchone()		  
		except: ##add excpetion type
			pass
		finally:
			#self.Print_(result_list)
			pass

		details_df = pandas.DataFrame(result_list)
		tut_index, prac_index = -1, -1

		for index in range (len(details_df[1])) :
			if (details_df[1][index].lower() == 'practical') :
				prac_index = index
			elif (details_df[1][index].lower() == 'tutorial') :
				tut_index = index

		if (tut_index == -1) :
			if (prac_index == -1):
				self.lecture = details_df
			else :
				self.practical = details_df[prac_index : ]
				self.lecture = details_df[ : prac_index]
		else:
			if (prac_index == -1):
				self.lecture = details_df[ : tut_index]
				self.tutorial = details_df[tut_index : ]
			else :
				self.lecture = details_df[ : prac_index]
				self.practical = details_df[prac_index : tut_index]
				self.tutorial = details_df[tut_index : ]


	def Print_ (self, list_):
		for i in range(len(list_)):
			print i, list_[i]

		if not list_ : 
			pass
			#print 'Sorry, No searches where found.'


db = sqlite3.connect('courses.db')
cursor = db.cursor()

while True:
	course_title_search = Searching('COURSE_TITLE')
	print
	print 
	query = raw_input("Enter your query : ")
	course_title_search.search(query, cursor)
