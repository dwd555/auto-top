#################################################################################################
#author：Joshua                                                                                 #
#目前只能对正常的top日志进行分析，如果日志错综复杂无规律会影响测试结果，所以建议不要在串口下top #
#如有差不多同名的进程，很容易读取到错误数据，请自行修改列表中的进程                             #
#################################################################################################
import re
import xlwt
import json
with open("./setting.txt","r") as fi:
	setting=json.loads(fi.read())
workbook = xlwt.Workbook()
def logfile(loc):
	with open(loc, 'r',encoding="utf-8") as f:
		log=f.read()
		return log

def writeXls(process,log,index):#1、进程名，2、日志信息，3、下标
	result=re.findall('.*'+process+'$.*', log)
	res=[]
	for i,j in enumerate(result):
		result[i]=re.split(r'\s+', result[i])
		try:
			if "m" in result[i][index]:#查看获取的数据有没有带单位，有的话去掉再添加，没有的除以1000使单位相同
				res.append(re.findall(r'\d+',result[i][index])[0])
			else:
				num=float(re.findall(r'\d+',result[i][index])[0])
				res.append(num/1000)

		except Exception as e:
			print(e)
			
	return res   #返回进程的列表

def exist(process,log):#判断进程在日志中是否存在，1、进程名，2、日志信息
	return process in log

def getIndex(info,log):#获取RES(自行定义)的下标
	result=re.findall('.*'+info+'.*', log)
	return re.split(r'\s+', result[0]).index(info)


def writeData(process,log,index,full,sheet):#1、写入数据，2、日志，3、需要查看的信息，4、是否全输出
	xlsIndex=0
	for p in enumerate(process):#c是下标，p是进程名
		if exist(p,log):
			res=writeXls(p, log,index)#result为进程的列表
			if full:
				sheet.write(0,xlsIndex,p)
				for i,j in enumerate(res):
					sheet.write(i+1,xlsIndex,float(j))
				xlsIndex=xlsIndex+1
			else:
				if int(res[-1])-int(res[0])>0:#判断最后一个比最前一个大，才写入,去掉注释的话输出全部
					sheet.write(0,xlsIndex,p)
					for i,j in enumerate(res):
						sheet.write(i+1,xlsIndex,float(j))
					xlsIndex=xlsIndex+1

def createXls(sheetName):
	return workbook.add_sheet(sheetName,cell_overwrite_ok=True)

def main(file,port,xls,arg,full):#file:读取的日志文件；port：选择atom还是arm,或者只查看单独一个程序；xls：选择保存的路径；arg：需要查看的top信息;full:是否全部输出
	atom=["T_STBSSMain","t.ngod.core","T.STB.CDS","T.CAS.Nagra","T.STB.SIPSI","bstm_resmgr","T.STB.ES","t.ngod.ss",\
	"T.STB.PS","bstm_SWUPMain","bstm_plugin_wai","wb_s","CASManager","T.STB.MD","PssuMain","LAN.MD","T.STB.Carousel","T.STB.Signal",\
	"ntpd","http_agent.plug","p.sysctrl","eventservice","NonIGD.MD","T.CAS.Main","T.STB.Main","ppu1server","ygserver",\
	"CfgFileMailBox","java"]
	arm=["dim-main","p.sysctrlAgent","lan.md.agent","WAN.eRouter","WAN.eSTB","upnpd","WAN.eMTA",\
	"CMV_Check","snmp_agent_cm","miniupnpd","dmg_provisionin","gw_snmp_agent","dispatcher","docsis_mac_mana","dmg_provisionin","psm"]
	#部分容易引起歧义的已经去除，需要可自己增加
	#"main","mysqld","tvview","tvview.plugin","LAN.MPEG"
	print("计算中,请稍后")
	# print(full)
	Process=[]
	if port=="atom":
		Process=atom
	elif port=="arm":
		Process=arm
	else:
		Process=[port]
	log=logfile(file)
	sheet1=createXls(arg)
	index=getIndex(arg,log)
	writeData(Process, log,index,full,sheet1)
	workbook.save(xls)
	print("保存excel文件成功")


#运行
if __name__ == '__main__':
	try:
		main(setting["filename"],setting["progress"],'./resResult.xls',setting["arg"],bool(setting["full"]))
	except Exception as e:
		print(e)

