import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from abc import ABCMeta, abstractmethod

class BaseCommodity(metaclass = ABCMeta):
	def __init__(self, commodity, year, month):
		self.commodity = commodity
		self.year = year
		self.month = month
		self.url = None
		self.baseurl = "https://www.usda.gov/oce/commodity/wasde/wasde"
		self.data = None
		self.data_to_string = None
		self.pass_to_xml = None
		self.getDataFromFolder = False

	@abstractmethod
	def DownloadDataWASDE(self):
		pass

	@abstractmethod
	def DownloadDataCornell(self):
		pass

	@abstractmethod
	def DownloadDataPDF(self):
		pass

	@abstractmethod
	def SplitData(self):
		pass

	def commoditySymbol(self):
		name = {"World and U.S Supply and Use for Grains  1/": "sr08",
		"World and U.S. Supply and Use for Grains, Continued  1/": "sr09",
		"World and U.S. Supply and Use for Oilseeds  1/": "sr10",
		"U.S. Wheat Supply and Use  1/": "sr11",
		"U.S. Feed Grain and Corn Supply and Use  1/": "sr12",
		"U.S. Sorghum, Barley, and Oats Supply and Use  1/": "sr13",
		"U.S. Rice Supply and Use  1/": "sr14",
		"U.S. Soybeans and Products Supply and Use (Domestic Measure)  1/": "sr15",
		"U.S. Sugar Supply and Use  1/": "sr16",
		"U.S. Cotton Supply and Use  1/": "sr17",
		"World Wheat Supply and Use  1/": "sr18",
		"World Wheat Supply and Use  1/  (Cont'd.)": "sr19",
		"World Coarse Grain Supply and Use  1/": "sr20",
		"World Coarse Grain Supply and Use  1/  (Cont'd.)": "sr21",
		"World Corn Supply and Use  1/": "sr22",
		"World Corn Supply and Use  1/  (Cont'd.)": "sr23",
		"World Rice Supply and Use  (Milled Basis)  1/": "sr24",
		"World Rice Supply and Use  (Milled Basis)  1/  (Cont'd.)": "sr25",
		"World Cotton Supply and Use  1/": "sr26",
		"World Cotton Supply and Use  1/": "sr27",
		"World Soybean Supply and Use  1/": "sr28",
		"World Soybean Meal Supply and Use  1/": "sr29",
		"World Soybean Oil Supply and Use  1/": "sr30",
		"U.S. Quarterly Animal Product Production  1/": "sr31",
		"U.S. Meats Supply and Use": "sr32",
		"U.S. Egg Supply and Use": "sr33",
		"U.S. Dairy Prices": "sr34",
		"Reliability of December Projections 1/": "sr35",
		"Reliability of December Projections  (Continued) 1/": "sr36",
		"Reliability of United States December Projections  1/": "sr37"
		}
		return name





class CommodityInizialization(BaseCommodity):
	"""docstring for ClassName"""
	def __init__(self, commodity, year, month):
		super().__init__(commodity, year, month)

	def GetDataFromFolder(self, fileRoot):
		soup = BeautifulSoup(open(fileRoot,"r"))
		return soup

	def GetDataFromFolder1(self, fileRoot):
		#print(soup, "__")
		data = ET.parse(fileRoot)
		root = data.getroot()
		rs = ET.tostring(root, encoding='unicode')
		soup = BeautifulSoup(rs, "xml")
		self.getDataFromFolder = True
		return soup

	def DownloadDataWASDE(self):
		"""
		The WASDE website only allows to download the XML file of the last two month
		"""
		#"https://www.usda.gov/oce/commodity/wasde/wasde0122.xml"
		self.url = self.baseurl + self.month + self.year + ".xml"
		self.data = requests.get(self.url)
		print(self.data, self.url)
		self.data_to_string = self.data.content.decode("utf-8")
		soup = BeautifulSoup(self.data_to_string, "xml")
		self.getDataFromFolder = False
		return soup

	def DownloadDataCornell(self, page):
		"""
		The Cornell Website has XML file from July 2010 to the present.
		Important: from July 2010 there are some months without XML  
		"""
		url = "https://usda.library.cornell.edu/concern/publications/3t945q76s?locale=en&page={0}#release-items".format(page)
		data = requests.get(url)
		##Get the table with the link
		soup = BeautifulSoup(data.content.decode("utf-8"))
		table = soup.find("table")
		thead = table.find("thead")
		tbody = table.find("tbody")
		tbody_tr = tbody.findAll("tr")
		self.getDataFromFolder = False
		pass

	def DownloadDataCornellLink(self):
		"""
		In this part the code is going to download the link in the row's table. Possible links pdf, txt, xls, xml
		"""
		pass

	def DownloadDataPDF(self):
		"""
		tabula-py does not look accurate to parse the pdf document. 
		Research more
		"""


	def SplitData(self):
		pass
		


class USWheat:
	"""
	This class is going to download data from the usda report (fix this. Do not need to download the data), 
	then get the wheat indentifier "sr11" and filter to get the two wheat table.
	Then is going to get the name of the rows, values, dates, etc.
	The idea is to pass this to a tabular structure.

	Fix:
		I need to create a base clase, where I need to put as a entry parameters:
			month
			year
			commodity Name
	"""
	def __init__(self, data, getDataFromFolder, codeNumber):
		self.data = data
		self.matrix1 = None
		self.matrix2 = None
		self.m1_attribute_group = None
		self.getDataFromFolder = getDataFromFolder
		self.codeNumber = codeNumber
		self.dictionary = {}
		self.splitMatrix()

	def splitMatrix(self):
		#split data in matrix1 and matrix2
		self.matrix1 = self.data.find("matrix1")
		self.m1_attribute_group = self.matrix1.findAll("m1_attribute_group")
		self.matrix2 = self.data.find("matrix2")

	def m1_filler1(self):
		"""
		matrix1
			m1_filler
		"""
		#Header = m1_filler1
		head = self.matrix1.find("m1_filler1")
		return head

	def m1_year_group(self): #Name Row Matrix
		"""
		This part is going to be able to get the head of the document.
		UD = Unit Description
		Year Month UD| Year Est Month UD| Year Proj Month UD|Year Proj Month UD
		"""
		head = self.m1_filler1()
		rowHead = head.findAll("m1_year_group")
		for i in rowHead:
			getYear = i.get("market_year1")
			getMonth = i.find("m1_month_group").get("forecast_month1")
			getUnitDescription = i.find("Cell").get("m1_unit_descr1")
			print(getYear, "*", getMonth, "*", getUnitDescription)

	def attribute1_values(self, data, name):
		year = data.get("market_year1")
		if name not in self.dictionary:
			self.dictionary[name] = []

		if self.getDataFromFolder == True:
			    month = data.find("m1_month_group").get("forecast_month1")
			    value = data.find("Cell").get("cell_value1")
			    self.dictionary[name].append([year, month, value]) 
		else:
			for cell in data:
				month = cell.find("m1_month_group").get("forecast_month1")
				value = cell.find("Cell").get("cell_value1")
				print(value, "___")
				self.dictionary[name].append([year, month, value]) 
		

	def attribute1(self):
		maintable = self.m1_attribute_group
		for row in maintable:
			rowAttribute = row.find("attribute1")
			name = rowAttribute.get("attribute1")
			rowCollection = rowAttribute.find("m1_year_group_Collection")
			yearGroup = rowCollection.findAll("m1_year_group")
			#print(yearGroup, "\n")
			print("\n", name)
			for yearGroupValue in yearGroup:
				self.attribute1_values(yearGroupValue, name)
		#print(self.dictionary)	
		self.transformDictToPandas()

	def transformDictToPandas(self):
		firstElement = list(self.dictionary.keys())[0]
		ValuesFirstElement = self.dictionary[firstElement]
		columns = [i[0] for i in ValuesFirstElement]
		result = [[j[2] for j in i] for i in self.dictionary.values()]
		result = pd.DataFrame(result, columns = columns)
		print(result)
		#I need to add the Header of the DataFrame
		

		"""
		for row in maintable:
			rowAttribute = row.find("attribute1")
			name = rowAttribute.get("attribute1")
			fields= rowAttribute.findAll("m1_year_group_Collection")
			for cell in row:
				cell_element = cell.findAll("Cell")
				cell_value = [i.get("cell_value1") for i in cell_element if i.get("cell_value1") != None]
				if len(cell_value) > 0:
					values.append(cell_value)
		"""

	###############################TABLE 2###########################
	def matrix2(self):
		#get second
		pass

	def m2_year_group_corn(self):
		data = self.matrix2.findAll("m2_attribute_group")
		mylist = []
		for index, i in enumerate(data):
			#Header
			yeardata= i.find("m2_filler1")
			subdata_yeardata = yeardata.findAll("m2_year_group")
			for row in subdata_yeardata:
				yearhead = row.get("market_year2")
				rowmonth = row.find("m2_month_group")
				month = rowmonth.get("forecast_month2")
			#Body table
			bodydata = i.find("attribute2")
			name = bodydata.get("attribute2")
			subdata_bodydata = bodydata.findAll("m2_year_group")
			mysublist = [name]
			if index == 0:
				columnsName = ["Name"]
			#2019/20 || 2020/21 Est. || 2021/22 Proj.(Dec) || 2021/22 Proj.(Jan)
			for row in subdata_bodydata:
				yearbody = row.get("market_year2")
				rowmonth = row.find("m2_month_group")
				monthbody = rowmonth.get("forecast_month2")
				valuebody = rowmonth.find("Cell").get("cell_value2")
				mysublist.append(valuebody)
				if index == 0:
					toappend = yearbody
					if monthbody != "": 
						toappend = toappend  + "-" + monthbody
					columnsName.append(toappend)
			mylist.append(mysublist)
		mypandasTable  = pd.DataFrame(mylist, columns = columnsName)
		print(mypandasTable)


	def m2_year_group_wheat(self):
		#Wheat
		"""
		<m2_year_group_Collection>
                    <m2_year_group market_year2="2020/21 (Est.) ">
                        <m2_month_group_Collection>
                            <m2_month_group attribute2="Beginning Stocks">
                                <m2_attribute_group_Collection>
                                    <m2_attribute_group forecast_month2="">
                                        <m2_attribute_order_Collection>
                                            <m2_attribute_order attribute_group2="Hard Red&#xD;&#xA;Winter">
                                                <m2_unit_descr1 m2_unit_descr1="">
                                                    <Cell cell_value2="506" />
                <m2_attribute_group_Collection>
                    <m2_attribute_group>
                        <m2_filler1 m2_filler1="Filler">
                            <m2_year_group_Collection>
                                <m2_year_group market_year2="2019/20">
                                    <m2_month_group_Collection>
                                        <m2_month_group forecast_month2="">
                                            <Cell m2_filler2="Filler" />
        """
		data = self.matrix2.findAll("m2_year_group")
		dictionary = {}
		mylist = []
		for index, i in enumerate(data):
			year = i.get("market_year2")
			subdata = i.find("m2_month_group")
			name = subdata.get("attribute2")
			dictionary[name] = {"year": year}
			sub_subdata = subdata.find("m2_attribute_group_Collection") #The second component using findAll is not relevant
			row_ssdata = sub_subdata.findAll("m2_attribute_order")
			internallist = [year, name]
			if index == 0:
				columnsName = ["Year", "Name"]
			for elements in row_ssdata:
				typecommodity = elements.get("attribute_group2").replace("\n", "").replace("\r", "")
				unit_description = elements.find("m2_unit_descr1").get("m2_unit_descr1")
				value_unit = elements.find("Cell").get("cell_value2")
				print(typecommodity, "*", unit_description, "*", value_unit)
				dictionary[name][typecommodity] = [unit_description, value_unit]
				internallist.append(value_unit)
				if index == 0:
					columnsName.append(typecommodity)
			mylist.append(internallist)

		print(pd.DataFrame(mylist, columns = columnsName))
		#print(dictionary)
		#I am having Only Projected values. Where are the estimated values?
		#Next convert table to pandas
		#PLEASE REMEMBER: Soft Red Winter is measured in  Millions and White is measured in Bushels (Please: Fix)

	def nameRowMatrix1(self):
		#Get the name of the row
		pass

	def valueRowMatrix1(self):
		#Get the value of the row
		pass



class USGrainAndCorn:
	"""
	This class is going to download data from the usda report (fix this. Do not need to download the data), 
	then get the wheat indentifier "sr11" and filter to get the two wheat table.
	Then is going to get the name of the rows, values, dates, etc.
	The idea is to pass this to a tabular structure.

	Fix:
		I need to create a base clase, where I need to put as a entry parameters:
			month
			year
			commodity Name
	"""
	def __init__(self, data, getDataFromFolder):
		self.data = data
		self.matrix1 = None
		self.matrix2 = None
		self.m1_attribute_group = None
		self.getDataFromFolder = getDataFromFolder
		self.dictionary = {}
		self.splitMatrix()

	def splitMatrix(self):
		#split data in matrix1 and matrix2
		self.matrix1 = self.data.find("matrix1")
		self.m1_attribute_group = self.matrix1.findAll("m1_attribute_group")
		self.matrix2 = self.data.find("matrix2")

	def attribute1_values(self, data, name):
		year = data.get("market_year1")
		if name not in self.dictionary:
			self.dictionary[name] = []

		if self.getDataFromFolder == True:
			    month = data.find("m1_month_group").get("forecast_month1")
			    value = data.find("Cell").get("cell_value1")
			    self.dictionary[name].append([year, month, value]) 
		else:
			for cell in data:
				month = cell.find("m1_month_group").get("forecast_month1")
				value = cell.find("Cell").get("cell_value1")
				self.dictionary[name].append([year, month, value]) 

	def attribute1(self):
		maintable = self.m1_attribute_group
		for row in maintable:
			rowAttribute = row.find("attribute1")
			name = rowAttribute.get("attribute1")
			rowCollection = rowAttribute.find("m1_year_group_Collection")
			yearGroup = rowCollection.findAll("m1_year_group")
			#print(yearGroup, "\n")
			#print("\n", name)
			for yearGroupValue in yearGroup:
				self.attribute1_values(yearGroupValue, name)
		#print(self.dictionary)	
		self.transformDictToPandas()

	def transformDictToPandas(self):
		firstElement = list(self.dictionary.keys())[0]
		ValuesFirstElement = self.dictionary[firstElement]
		columns = [i[0] for i in ValuesFirstElement]
		result = [[j[2] for j in i] for i in self.dictionary.values()]
		result = pd.DataFrame(result, columns = columns)
		print(result)
		#I need to add the Header of the DataFrame




start = time.time()
myfile = "../../data/usda/wasde/wasde1221.xml" #"../../data/usda/wasde/wasde0122.xml"
inizialization = CommodityInizialization("Hola", "22", "01")
#wasdedata = inizialization.GetDataFromFolder1(myfile) #Does not work yet Fix this part
wasdedata = inizialization.DownloadDataWASDE()
end = time.time()
print("Time to download data", end - start)

##Split data by commodity identifier

codeNumber = "sr13"
wheat = wasdedata.find(codeNumber)
print(inizialization.getDataFromFolder, "________________")
tw = USWheat(wheat, inizialization.getDataFromFolder, codeNumber)
tw.m2_year_group_corn()
#tw.attribute1()

"""
Next Task:
The tables:
-FEED GRAINS
-CORN
-SORGHUM
-BARLEY
-OATS
-etc

follows the same structure. The main difference, it is the location of the table (matrix1 or matrix2 or matrix3), this makes changes in the tag.
Modify the main class to take in cosideration the previous point and be able to get.
In total there are 15 (less or more) tables with this pattern  
"""
