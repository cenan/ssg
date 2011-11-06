import os

def get(item, default_value=""):
	f = open(os.path.join(os.getcwd(), "ssg.yaml"))
	for s in f.readlines():
		k, v = s.split(":")
		if k == item:
			f.close()
			return v.strip()
	f.close()
	return default_value

