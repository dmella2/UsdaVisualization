import requests
from bs4 import BeautifulSoup
from abc import ABCMeta, abstractmethod

class BaseCommodity(metaclass = ABCMeta):
	def __init__(self, commodity, year, month):
		self.commodity = commodity
		self.year = year
		self.month = month

	@abstractmethod
	def DownloadData(self):
		pass



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
	def __init__(self):
		self.url = None
		self.data = None
		self.data_to_string = None
		self.pass_to_xml = None
	def DownloadData(self, baseurl, month, year):
		self.url = baseurl + month + year + ".xml"
		self.data = requests.get(self.url)
		self.data_to_string = self.data.content.decode("utf-8")
		soup = BeautifulSoup(self.data_to_string, "xml")
		wheat = soup.find("sr11")
		return wheat

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


""">
<m1_attribute_group_Collection>
	<m1_attribute_group>
		<m1_filler1>
			<m1_year_group_Collection>
				<m1_year_group market_year1="2019/20">
					<m1_month_group_Collection>
						<m1_month_group forecast_month1="">
							<Cell m1_unit_descr1=""/>
						</m1_month_group>
					</m1_month_group_Collection>
				</m1_year_group>
				<m1_year_group market_year1="2020/21 Est.">
					<m1_month_group_Collection>
						<m1_month_group forecast_month1="">
							<Cell m1_unit_descr1=""/>
						</m1_month_group>
					</m1_month_group_Collection>
				</m1_year_group>
				<m1_year_group market_year1="2021/22 Proj.">
					<m1_month_group_Collection>
						<m1_month_group forecast_month1="Nov">
							<Cell m1_unit_descr1="Million Acres"/>
						</m1_month_group>
					</m1_month_group_Collection>
				</m1_year_group>
				<m1_year_group market_year1="2021/22 Proj.">
					<m1_month_group_Collection>
						<m1_month_group forecast_month1="Dec">
							<Cell m1_unit_descr1=""/>
						</m1_month_group>
					</m1_month_group_Collection>
				</m1_year_group>
			</m1_year_group_Collection>
		</m1_filler1>
		<attribute1 attribute1="Area Planted">
			<m1_year_group_Collection>
				<m1_year_group market_year1="2019/20">
					<m1_month_group_Collection>
						<m1_month_group forecast_month1="">
							<Cell cell_value1="45.5"/>
						</m1_month_group>
					</m1_month_group_Collection>
				</m1_year_group>
				<m1_year_group market_year1="2020/21 Est.">
					<m1_month_group_Collection>
						<m1_month_group forecast_month1="">
							<Cell cell_value1="44.5"/>
						</m1_month_group>
					</m1_month_group_Collection>
				</m1_year_group>
				<m1_year_group market_year1="2021/22 Proj.">
					<m1_month_group_Collection>
						<m1_month_group forecast_month1="Nov">
							<Cell cell_value1="46.7"/>
						</m1_month_group>
					</m1_month_group_Collection>
				</m1_year_group>
				<m1_year_group market_year1="2021/22 Proj.">
					<m1_month_group_Collection>
						<m1_month_group forecast_month1="Dec">
							<Cell cell_value1="46.7"/>
						</m1_month_group>
					</m1_month_group_Collection>
				</m1_year_group>
			</m1_year_group_Collection>
		</attribute1>
	</m1_attribute_group>
</m1_attribute_group_Collection>
"""
