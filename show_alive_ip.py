import re, os, time, sys, subprocess

lifeline = re.compile(r"ms")
def atIPC(IP):
    os.system(r"net use \\" + ip + r"\ipc$")
    command = 'AT \\\\' + ip + r' 23:02 D:\\softwaretemp\\excelfilter.exe'
    print command
    os.system(command)
    
def shutdown(hostname):
    os.popen("shutdown /m \\\\"+hostname+" /s /t 1")
                 
fh = open("D:\\host.txt", "r")
for hostname in fh.readlines():
    ip = hostname.strip()
    pingaling = os.popen("ping -n 1 -w 2 " + ip)
    while True:
        line = pingaling.readline()
        if not line: break
        igot = re.findall(lifeline, line)
        if igot:
            print "Host %s is alive" % ip
#            shutdown(ip)
#            schtask(ip)
            atIPC(ip)
#            fp.write("%s\n" % ip)
            break
fh.close()
#fp.close()
#print time.ctime()
