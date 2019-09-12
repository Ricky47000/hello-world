from lxml import etree
import re
import numpy as np


def first_lower(s):
	'''
	This function puts tthe first letter of a string in lowercase
	'''
	if len(s) == 0:
		return s
	else:
		return s[0].lower() + s[1:]


def get_test_mapping(deviceNode):
	'''
	This function returns the mapping of the project
	'''
	testList=[]
	for node in deviceNode.getchildren() :
		regexpC = r"c_(.)*" #Pattern
		regexpM = r"m_(.)*" #Pattern
		if re.match(regexpC, first_lower(node.tag)) or re.match(regexpM, first_lower(node.tag)) : 
			testList.append(node.tag) 
	return testList


def get_device_name(tree):
	'''
	This functions returns the device name
	'''
	for node in tree.xpath("/setup/patterns/Pattern_1/subsites/HOME"):
		child = node.getchildren()
		for i in child:
			if i.get('attr') == "device":
				deviceName = i.tag
				correctNode = i

	return deviceName, correctNode


def atoi(text):
	'''
	This function converts a string to an int
	'''
	return int(text) if text.isdigit() else text


def natural_keys(text):
	'''
	This functions works in combination with sort() in order to sort tests names
	'''
	return [ atoi(c) for c in re.split('(\d+)', text) ]


def parse_xml(xmlFile):
	'''
	This function parses the xml file
	'''
	tree = etree.parse(xmlFile)
	return tree


def get_pad_name(deviceNode):
	'''
	This function returns SMUs names
	'''
	padName=[]
	for node in deviceNode.getchildren() :
		if node.tag == "subdevList":
			subdevNode = node.getchildren()
			for i in subdevNode:
				subdevNode1 = i
				for subNode in subdevNode1.getchildren():
					for pad in subNode.getchildren():
						if pad.tag == "padName":
							padName.append(pad.text)
	return padName	


if __name__ == '__main__':
	
	xmlFile = "I:\\Public\\Sudenten\\Studenten CPE1\\Francois BAUMY\\temp\\SJA1105_RS_SGMII_LBGA159\\SJA1105_RS_SGMII_LBGA159.xml"
	#xmlFile = "C:\\ACS_BASIC\\Projects\\UJA1132RevBendQFP80_Francois\\UJA1132RevBendQFP80_Francois.xml"
	#xmlFile = "I:\\TPE\\06. EQUIPMENT\\Curve trace system selection\\SJA1105P_LQFP144\\SJA1105P_LQFP144.xml"
	root = parse_xml(xmlFile)
	deviceName, deviceNode = get_device_name(root) 
	print("DeviceName :", deviceName)
	
	listTest =  get_test_mapping(deviceNode)
	#listTest = ['m_P26_BAT_GND']
	print(len(listTest), listTest)
	#list_append=[]
	for name in listTest:
		regexpM = r"m_(.)*"
		if re.match(regexpM, name):
			print(name)
			#list_append.append(get_append_test(deviceNode, name))
			print("")
	#print("Append List", list_append)
	#print("Size list", np.shape(list_append))
	pad = get_pad_name(deviceNode)
	print(pad)
	'''
	path = ''
	try :
		find_text = etree.XPath("//text()")
		paths = [root.getpath( text.getparent()) for text in find_text(root)]
	except :
		print("ERROR FINDING PATH NODE")
	#print(len(path), path)


	'''				
					