import psutil

flag = 0

for proc in psutil.process_iter():
	try:
		pName = proc.name()
		pID = proc.pid
		pstr = str(pName)+"\n"  #+":::"+str(pID)
		print(pstr)
		#first time write entire file
		if flag == 0:
			file1 = open("SAFE_MODE_processes.txt","w")
			file1.write(pstr)
			file1.close()
			flag = 1
		else:
			file1 = open("SAFE_MODE_processes.txt","a")
			file1.write(pstr)
			file1.close()

	except Exception as e:
		raise
	else:
		pass
	finally:
		pass