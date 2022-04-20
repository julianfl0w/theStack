import sys
import json
infile = sys.argv[1]
with open(infile, 'r') as f:
    indict = json.loads(f.read())

	
def json2bs(name, indict):
	children = []
	for k, v in indict.items():
		if type(v) is dict:
			if len(v.items()):
				newchild = json2bs(k, v)
			else:
				newchild = {"name":k, "size":200}
		children += [newchild]
	
	newdict = {}
	newdict["children"] = children
	newdict["name"] = name
	return newdict
		
print(json.dumps(json2bs(infile, indict), indent = 3))
