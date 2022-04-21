import sys
import json
infile = sys.argv[1]
with open(infile, 'r') as f:
	indict = json.loads(f.read())

	
def json2flare(name, indict):
	children = []
	for k, v in indict.items():
		if type(v) is dict:
			if k.endswith(".json"):
				with open(k, 'r') as f:
					newchild = json2flare(k.replace(".json",""), json.loads(f.read()))
			elif len(v.items()):
				newchild = json2flare(k, v)
			else:
				newchild = {"name":k, "value":200}
		else:
			newchild = {"name":k, "value":200}
		children += [newchild]
	
	newdict = {}
	newdict["name"] = name
	newdict["children"] = children
	return newdict
		
print(json.dumps(json2flare(infile, indict), indent = 3))
