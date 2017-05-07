import re
import xlwt
workbook = xlwt.Workbook()
sheet1 = workbook.add_sheet('res',cell_overwrite_ok=True)
def logfile(loc):
	with open(loc, 'r',encoding="utf-8") as f:
		log=f.read()
		return log

def writeXls(process,log,index):#1、进程名，2、日志信息，3、下标
	# if exist(process,log):
	result=re.findall('.*'+process+'.*', log)
	# print(result)
		# print(index)
	res=[]
	for i,j in enumerate(result):
		result[i]=re.split(r'\s+', result[i])
		try:
			if "m" in result[i][index]:
				res.append(re.findall(r'\d+',result[i][index])[0])
			else:
				num=float(re.findall(r'\d+',result[i][index])[0])
				res.append(num/1000)

		except Exception as e:
			print(e)
			
	return res   #返回进程的列表

def exist(process,log):#判断进程在日志中是否存在，1、进程名，2、日志信息
	return process in log

def resIndex(info,log):#获取RES的下标
	result=re.findall('.*'+info+'.*', log)
	# print(re.split(r'\s+', result[0]).index(info))
	return re.split(r'\s+', result[0]).index(info)


def writeData(process,log,index,full):#1、写入数据，2、日志，3、需要查看的信息，4、是否全输出
	for c,p in enumerate(process):#c是下标，p是进程名
		if exist(p,log):
			res=writeXls(p, log,index)#result为进程的列表
			if full:
				sheet1.write(0,c,p)
				for i,j in enumerate(res):
					sheet1.write(i+1,c,float(j))
			else:
				if int(res[-1])-int(res[0])>0:#判断最后一个比最前一个大，才写入,去掉注释的话输出全部
					sheet1.write(0,c,p)
					for i,j in enumerate(res):
						sheet1.write(i+1,c,float(j))

def main(file,port,xls):
	atom=["T_STBSSMain","t.ngod.core","T.STB.CDS","T.CAS.Nagra","T.STB.SIPSI","bstm_resmgr","T.STB.ES","mysqld","t.ngod.ss",\
	"T.STB.PS","bstm_SWUPMain","main","bstm_plugin_wai","wb_s","CASManager","T.STB.MD","PssuMain","LAN.MD","T.STB.Carousel","T.STB.Signal",\
	"ntpd","tvview","http_agent.plug","p.sysctrl","eventservice","NonIGD.MD","T.CAS.Main","T.STB.Main","ppu1server","ygserver",\
	"tvview.plugin","CfgFileMailBox"]
	# atom=["T_STBSSMain"]#调试数据
	arm=["dim-main","p.sysctrlAgent","lan.md.agent","WAN.eRouter","WAN.eSTB","upnpd","WAN.eMTA",\
	"CMV_Check","snmp_agent_cm","miniupnpd","dmg_provisionin","gw_snmp_agent","dispatcher","docsis_mac_mana","dmg_provisionin","psm"]
	print("计算中,请稍后")
	Process=[]
	if port=="atom":
		Process=atom
	else:
		Process=arm
	log=logfile(file)
	# index=resIndex('RES',log)
	index=resIndex('VSZ',log)
	writeData(Process, log,index,False)
	workbook.save(xls)
	print("保存excel文件成功")
#运行
main("d:/192.168.1.202_05-07 00;00;00.log","atom",'d:/atom.xls')