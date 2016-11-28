#coding: utf-8
import psycopg2

class CDB:
	def __init__(self, dbName, un, pw, host = '127.0.0.1', port = '5432'):
		self.__dbName = dbName
		self.__un = un
		self.__pw = pw
		self.__host = host
		self.__port = port

		try:
			self.__connect = psycopg2.connect(database = self.__dbName, user = self.__un, password = self.__pw, host = self.__host, port = self.__port)
		except:
			print 'DB Connection ERROR!!!'
		else:
			CDB.Connect = self.__connect
			self.__cursor = self.__connect.cursor()
			CDB.Cursor = self.__connect

	def Commit(self):
		self.__connect.commit()

	def Close(self):
		self.__cursor.close()
		self.__connect.close()

	def Exec(self, sql):
		self.__cursor.execute(sql)
	
class CCompress:
	def __init__(self, value):
		self.__value = value

	def Decode(self):
		try:
			return self.__value.decode('base64').decode('bz2').decode('utf-8').encode('gbk')
		except Exception:
			return self.__value

	def Encode(self):
		try:
			return self.__value.decode('gbk').encode('utf-8').encode('bz2').encode('base64')
		except Exception:
			return self.__value
