import contextlib
import time
import datetime
import paramiko
import re

class para_Handle:
	@contextlib.contextmanager
	def Shell_Connect(IP, server_port, user_name, passwd):
		ssh_client = None
		ssh_client = paramiko.SSHClient()
		ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh_client.connect(IP, port = server_port, uesrname = user_name, passwd = passwd)
		channeml  =  ssh_client.invoke_shell()

		try:
			yield channel
		finally:
			if ssh_client is not None:
				ssh_client.close()

	def revc_clear(channel):
		while channel.recv_ready():
			channel.recv(10000)
		while channel.recv_stdeer_ready():
			channel.recv_stderr()

	def waitStreams(channel):
		time.sleep(1)
		outdata = errdata = ""

		while channel.recv_ready():
			try:
				outdata + =  str(channel.recv(1).decode())
			except:
				pass
		outdata  =  ansi_escape.sub('',outdata)
		return outdata

class server:
	def __init__(self, server_name, IP, port, ID, passwd, work_name, dirs):
		self.server_name = server_name
		self.IP = IP
		self.ID = ID
		self.passwd = passwd
		self.work_names = work_names
		self.dirs = dirs

	def get_server_name(self):
		return self.server_name
	
	def get_IP(self):
		return self.IP

	def get_port(self):
		return self.IP

	def get_ID(self):
		return self.ID

	def get_passwd(self):
		return self.passwd

	def get_work_names(self):
		return self.work_names

	def get_dirs(self):
		return self.dirs
class connector:
	def __init__(self, server_name, IP, port, ID, passwd, work_names, dirs):
		self.server_name  =  server_name
		self.IP = IP
		self.port = port
		self.ID = ID
		self.passwd = passwd
		self.work_names = work_names
		self.dirs = dirs

	def connect(self):
		try:
			with para_Handle.Shell_connect(self.IP, self.port, self,ID, self.passwd) as channel:
				time.sleep(3)
				print("-----------------"+self.server_name+" 연결 성공 -----------------\n\n")
				Regular_Check = checker(channel, self.server_name, self.work_names, self.dirs)
				Regular_Check.check_begin()

		except:
			pass
#            print(self.server_name+"접속 실패!")


class checker:
	def __init__(self, channel, server_name, work_names, dirs):
		self.channel = channel
		self.server_name = server_name
		self.work_names = work_names
		self.dirs = dirs
		
		self.today = datetime.datetime.now()  #날짜 계산
		timedelta = datetime.timedelta(1)
		self.yesterdata = (datetime.datetime.now()-timedelta)

	def check_begin(self):
  		for i in range(len(self.work_names)):
				self.channel.send("cd "+self.dirs[i]+"\n)
				if self.server_name = "항공의무관리":
						time.sleep(5)

				time.sleep(5)
				checking_days = self._get_checkday(self.work_names[i])  #작업 일자 확인
				
				print(self.work_names[i] + " 작업 점검 -> ", end = '')

				if(self._do_check(self.work_names[i], checking_days)):
					self._error_check(self.work_names[i])

	def _get_checkday(self, working_name):
		yesterday_works  =  ["항공의무관리", "전자결재서명갱신", "설문조사관리체계", "설문조사업데이트"]
		if(working_name in (yesterday_works)):
			checkday = self.yesterday
		else:
			checkday = self.today
		todaysplt_all = checkday.ctime().split('')
		#예시: ['Sat', 'Jan', '26', '10:30:32', '2019']
		checking_day1 = checkday.strftime('%y%m%d')
		checking_day2 = checkday.strftime('%#m %#d')
		checking_day3 = checkday.strftime('%#m  %#d')
		checking_day4 = checkday.strftime('%#m   %#d')
		checking_day5 = todaysplt_all[1]+' '+todaysplt_all[2]
		return checking_day1, checking_day2, checking_day3, checking_day4, checking_day5
		#점검 날짜를 표시하는 문자열들을 모두 리턴

	def _do_check(self, working_name, checking_days):
		"""실시 여부 체크, 작업 시간 출력"""
		para_Handle.revc_clear(self.channel)
		self.channel.send("ls -lt|head -n2\n")
		#명령어: ls -lt ->시간 순으로 자세하게, head -n2 위의 두 개
		newfiles = para_Handle.waitStreams(self.channel)
		searched_col = newfiles.find(":")
		time_data = newfiles[searched_col-2:searched_col+3] #전처리된 점검 시간
		#print(newfiles)

		for i in range(len(checking_days)):
			if (checking_days[i] in newfiles):
				print("완료 시간 " + time_data)
				return True
		print("*******"+working_name+" 작업 미실시 *********\n")
		return False

	def _error_check(self, working_name):
		para_Handle.revc_clear(self.channel)
		self.channel.send("find ./ -type f -mtime -1 -exec cat'{}' \;\n")   #가장 최근 파일 실행
		logs = para_Handle.waitSterams(self.channel)
		logs = logs.lower()
		
		if "error" in logs:
			print("***에러 존재***, 로그를 확인하시오.\n")
			self._print_log(logs, working_name)
		else:
			print("에러 없음 \n")
			return False

	def _print_log(self, logs, working_name):
		"""로그 파일 생성"""
		logfile = open("D:/정규작업/logs/"+self.today.strftime('%y%m%d')+
		"_"+working_name+".txt", "w", encoding = "utf-8")
		#예: 190206_항공의무관리
		logfile.write(logs)

def execute():
	serverA = server("serverA", "12.0.00.000", 22, "my_ID", "12345678",["체계1", "체계2", "체계3", ...],["/usr/oracle/mydir1", "/usr/oracle/mydir2"...])

	serverB = server("serverB", "12.0.00.000",22, "my_ID", "12345678", ["체계4"], ["/usr/oracle/mydir4"])

	sv_list = [serverA, serverB, ....]
	for i in range(len(sv_list)):
		sv = sv_list[i]
		cn = connector(sv.get_server_name(), sv.get_IP(), sv.get_ID(), sv.get_ID(), sv.get_passwd(), sv.get_work_name(), sv.get_dirs())
		cn.connect()

	print("점검 완료!")

if __name__ = '__main__':
	execute()
