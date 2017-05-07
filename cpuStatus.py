import re
import xlwt
workbook = xlwt.Workbook()
sheet=workbook.add_sheet("cpu",cell_overwrite_ok=True)
arr=["usr","sys","nic","idle","io","irq","sirq"]
for i,p in enumerate(arr):
	sheet.write(0,i,p)
def logfile(loc):
	with open(loc, 'r',encoding="utf-8") as f:
		log=f.read()
		return log

def writeData(file):
	if "CPU:" in file:
		result=re.findall(r".*CPU:.*", file)
		print(result[0].split(","))
	else:
		result=re.findall(r".*Cpu\(s\).*", file)
		wxls(result)

def wxls(result):
	for i,p in enumerate(result):
		data=result[i].split("):")[1].split(",")
		for index,j in enumerate(data):
			if index>6:
				break
			sheet.write(i+1,index,float(re.findall(r"\d+",j)[0]))

file=logfile("d:/top.log")
writeData(file)
workbook.save("f:/cpu.xls")