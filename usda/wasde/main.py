import requests
from bs4 import BeautifulSoup
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
		wheat = soup.find("sr11")
		return wheat

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
		https://arxiv.org/ftp/arxiv/papers/2004/2004.12629.pdf
		"""


	def SplitData(self):
		pass
		
inizialization = CommodityInizialization("Hola", "22", "01")
print(inizialization.DownloadDataWASDE())
#print(inizialization.baseurl)

class USWheat(BaseCommodity):
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
	def __init__(self, commodity, year, month):
		self.url = None
		self.data = None
		self.data_to_string = None
		self.pass_to_xml = None

	def splitMatrix(self):
		#split data in matrix1 and matrix2
		pass

	def matrix1(self):
		#Get first Matrix
		pass

	def matrix2(slef):
		#get second
		pass

	def nameRowMatrix1(self):
		#Get the name of the row
		pass

	def valueRowMatrix1(self):
		#Get the value of the row
		pass

"""
url = "https://www.usda.gov/oce/commodity/wasde/wasde0122.xml"
data = requests.get(url = url)
data_to_string = data.content.decode('utf-8')
soup = BeautifulSoup(data_to_string,'xml')
#print(soup)

##Wheat sr11
wheat = soup.find("sr11")
#First Table
matrix1 = wheat.find("matrix1")
"""
"""
m1_attribute_group_Collection
	m1_attribute_group
		-Area Planted
		-Area Harvested
		...
		-Avg.FarmPrice ($/bu)  2/  
m1_attribute_group
	m1_filler1
	attribute1 (Area Planted)
	m1_filler2
	m1_filler3
"""
"""
#Header = m1_filler1
head = matrix1.find("m1_filler1")
maintable = matrix1.findAll("m1_attribute_group")
values = []
for row in maintable:
	rowAttribute = row.find("attribute1")
	name = rowAttribute.get("attribute1")
	fields= rowAttribute.findAll("m1_year_group_Collection")
	for cell in row:
		cell_element = cell.findAll("Cell")
		cell_value = [i.get("cell_value1") for i in cell_element if i.get("cell_value1") != None]
		if len(cell_value) > 0:
			values.append(cell_value)


	print(name, "\n")
print(values, len(values))


#Second Table
matrix2 = wheat.find("matrix2")

"""
