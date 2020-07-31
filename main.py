# =====================================================================

from app.database import Database      # Database class
from app.editor import Editor          # Table Editor class
from terminaltables import SingleTable # Using to create beautiful tables in console
import sys                             # Using to exit a program

# =====================================================================


database_path = input("Write a database path => ")

db = Database(database_path)

db.connect()

run = True

# Main loop
while run:
	print("\n\n=============== THERE IS A LIST OF ALL TABLES FROM THIS DATABASE ===============\n")

	all_tables = []



	# ========================= Analyzing tables from database using Database class ===========================
	for table in db.analyze():
		all_tables.append([table[0]])

	tables_table = SingleTable(all_tables, "All tables from " + database_path)
	tables_table.inner_heading_row_border = False

	print(tables_table.table)

	# ========================= Analyzing tables from database using Database class ===========================



	print('''


	ACTIONS:

	[1] => Create new table (BETA)

	[2] => Table editor mode

	[3] => Remove this database

	[4] => Exit


		''')

	# Wainting for user will write a number of action
	action = input("Choose action => ")


	# ===================== Handling creating new table (beta) =====================
	if action == "1":
		table_name = input("Write a name of table [STRING] (.0 to exit) => ")

		if table_name == ".0":
			continue

		cols_num = input("How many columns will be in your table? [INT] => ")

		columns = []

		for col in range(int(cols_num)):
			column = []
			colname = input("Name of " + str(col+1) + " column [STRING] => ")
			column.append(colname)
			coltype = input("Type of " + str(col+1) + " column [SQL_COLTYPE] => ")
			column.append(coltype)
			columns.append(column)

		query = "CREATE TABLE {name} (".format(name=table_name)

		for item in columns:
			query +=  item[0] + " " + item[1]

			if item != columns[-1]:
				query += " default NULL, "
			else:
				query += " default NULL)"

		print("There is your generated query => " + query)

		db.execute(query)

		print("Table created!")

		continue
	# =====================// Handling creating new table (beta) \\=====================





	# ===================== Handling editor mode (using class Editor) =====================
	elif action == "2":
		editor_running = True
		table_name = input("\n\nWrite table name => ")
		editor = Editor(db, table_name)
		print("\n\nEDITOR > You entered editor mode")
		while editor_running:
			print("\n\n=============== THERE IS ALL DATA FROM THIS TABLE ===============\n")
			editor.list()
			print('''


			EDITOR > ACTIONS:

			[1] => Insert row into table

			[2] => Remove row from table 

			[3] => Edit row from table

			[4] => Clear table

			[5] => Remove table

			[6] => Leave editor mode


				''')
			editor_action = input("EDITOR > Choose action => ")

			if editor_action == "1":
				cols_array = editor.list(return_data_array_only=True)

				row_values = []

				for i in range(len(cols_array)):
					row_values.append(input("Write a value for the `{key}` => ".format(key=cols_array[i])))

				editor.insert(row_values)

			elif editor_action == "2":

				delete_array = []

				key = input("Write a key for deleting a row => ")
				value = input("Write a value for {_key} => ".format(_key=key))

				delete_array.append(key)
				delete_array.append(value)

				editor.remove(delete_array)

			elif editor_action == "3":

				where = []
				values = []

				where_key = input("Write a key for finding a row => ")
				where_value = input("Write a value for finding a row => ")

				where.append(where_key)
				where.append(where_value)

				set_key = input("Write a key for set a value => ")
				set_value = input("Write a value for `{k}` => ".format(k=set_key))

				values.append(set_key)
				values.append(set_value)

				editor.update(where, values)

			elif editor_action == "4":
				confirm = input("Do you really want to clear table {tablename} ? (y/n) => ".format(tablename=table_name))

				if confirm.lower() == "y":
					editor.clear()


			elif editor_action == "5":
				confirm = input("Do you really want to DELETE table {tablename} ? (y/n) => ".format(tablename=table_name))

				if confirm.lower() == "y":
					editor.drop()

					break

			elif editor_action == "6":
				break
	# =====================// Handling editor mode (using class Editor) \\=====================





	# ===================== Handling removing database =====================
	elif action == "3":
		confirm = input("Do you REALLY want to REMOVE DATABASE {dbname}?? (y/n) => ".format(dbname=database_path));
		if confirm.lower() == "y":
			print("Closing connection...")
			db.disconnect()
			print("Removing database file...")
			db.remove()
			print("Removed.")
			input("Press enter to exit program => ")
			sys.exit()
	# =====================// Handling removing database \\=====================





	# ===================== Handling exiting program =====================
	elif action == "4":
		print("Closing connection...")
		db.disconnect()
		print("Bye!")
		sys.exit()
	# =====================// Handling exiting program \\=====================