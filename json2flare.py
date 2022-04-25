import sys
import json
infile = sys.argv[1]
with open(infile, 'r') as f:
	indict = json.loads(f.read())

def byname(indict):
	return indict["name"]

def json2flare(name, inval):
	children = []

	if type(inval) is dict:
		for k, v in inval.items():
			children += [json2flare(k, v)]
				
	elif type(inval) is list:
		for i, e in enumerate(inval):
			
			identifier = str(i)
			
			# if the child is a dictionary with a name, 
			# use that name instead of a number
			if type(e) is dict:
				for k in e.keys():
					if "name" in k:
						identifier = e[k]
					if "proto" in k:
						identifier = e["proto"]["name"]
						
			children += [json2flare(identifier, e)]

	elif type(inval) is str and inval.endswith(".json"):
		with open(inval, 'r') as f:
			linkedDict = json.loads(f.read())
		formattedName = inval.replace(".json","")
		children += [json2flare(formattedName, linkedDict)]
		
	else:
		newchild = {"name":str(inval), "value":1}
		children += [newchild]
	
	maxlen = 12
	if len(children) < maxlen:
		newdict = {}
		newdict["name"] = name
		newdict["children"] = children
	else: # if there are more than maxlen children, break
		# it up alphabetically
		newdict = {"name" : name, "children": []}
		children.sort(key=byname)
		itemsPerGroup = int(len(children) / maxlen)
		#print(str(len(children)) + " : " + str(itemsPerGroup))
		for i, c in enumerate(children):
			# if this is an alphabet group boundary
			if not i%itemsPerGroup or i == len(children)-1:
				if i:
					thisAlphaGroupDict["name"] += "-"+c["name"]
					newdict["children"] += [thisAlphaGroupDict]
				thisAlphaGroupDict = {"name" : c["name"], "children": []}
				
			thisAlphaGroupDict["children"] += [c]
				
		#print(json.dumps(newdict, indent = 2))
		
	return newdict

outdict = json2flare(infile, indict)
print(json.dumps(outdict, indent = 3))
