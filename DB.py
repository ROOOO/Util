#coding: utf-8
import psycopg2
import sqlite3

class CDB:
	def __init__(self, dbName, un, pw, host = '127.0.0.1', port = '5432'):
		self.__dbName = dbName
		self.__un = un
		self.__pw = pw
		self.__host = host
		self.__port = port

		try:
			self.connect = psycopg2.connect(database = self.__dbName, user = self.__un, password = self.__pw, host = self.__host, port = self.__port)
		except:
			print 'DB Connection ERROR!!!'
		else:
			self.cursor = self.connect.cursor()

	def Commit(self):
		self.connect.commit()

	def Close(self):
		self.cursor.close()
		self.connect.close()

class CDBSqlite(CDB):
	def __init__(self, path):
		try:
			self.connect = sqlite3.connect(path)
		except:
			print 'DB Connection ERROR!!!'
		else:
			self.cursor = self.connect.cursor()
	
class CCompress:
	def __init__(self):
		pass

	def Decode(self, value):
		try:
			return value.decode('base64').decode('bz2').decode('utf-8').encode('gbk')
		except Exception:
			return value

	def Encode(self, value):
		try:
			return value.decode('gbk').encode('utf-8').encode('bz2').encode('base64')
		except Exception:
			return value
