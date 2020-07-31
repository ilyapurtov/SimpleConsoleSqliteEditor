from prettytable import PrettyTable


class Editor:

	table = None
	db = None


	def __init__(self, db_obj, table_name):
		self.db = db_obj
		self.table = table_name

		
	def list(self, return_data_array_only=False):
		self.db.execute("SELECT * FROM {table}".format(table=self.table))
		table_data = self.db.fetchAll()
		self.db.execute("PRAGMA table_info('{table}')".format(table=self.table))
		table_cols = self.db.fetchAll()

		data_array = []

		for i in table_cols:
			data_array.append(i[1])

		table_data_table = PrettyTable(data_array)
		# table_data_table.add_row([])

		for item in table_data:
			table_data_table.add_row(item)

		if return_data_array_only == False:

			print(table_data_table)

			if table_data == []:
				print("\n\nEDITOR > This table is empty.\n")
		else:
			return data_array


	def insert(self, values):

		query = "INSERT INTO `{table_name}` (".format(table_name=self.table)

		for i in self.list(return_data_array_only=True):
			if i == self.list(return_data_array_only=True)[-1]:
				query += "`" + i + "`) VALUES("
			else:
				query += "`" + i + "`, "
		
		for i in values:
			if i == values[-1]:
				query += "'" + i + "')"
			else:
				query += "'" + i + "', "

		self.db.execute(query)

		print("\nRow added!")


	def update(self, where, values):
		query = "UPDATE {tablename} SET `{set_key}` = '{set_value}' WHERE `{where_key}` = '{where_value}'".format(
			tablename   = self.table,
			set_key     = values[0],
			set_value   = values[1],
			where_key   = where[0],
			where_value = where[1]
		)

		self.db.execute(query)

		print("\nRow updated.\n")


	def remove(self, array):
		query = "DELETE FROM {tablename} WHERE `{key}` = '{value}'".format(
			tablename=self.table, 
			key=array[0], 
			value=array[1]
		)

		self.db.execute(query)

		print("\nRow has been deleted.")


	def clear(self):
		self.db.execute("DELETE FROM {tablename}".format(tablename=self.table))

		print("\nTable {tablename} has been cleared.".format(tablename=self.table))


	def drop(self):
		self.db.execute("DROP TABLE {tablename}".format(tablename=self.table))

		print("\nTable {tablename} has been removed.".format(tablename=self.table))

		print("\n\nLeaving editor mode...\n\n")