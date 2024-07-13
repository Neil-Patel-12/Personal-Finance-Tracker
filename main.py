import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_amount, get_category, get_description

class CSV:
	CSV_FILE = "finance_data.csv"
	COLUMNS = ["date", "amount", "category", "description"]
	FORMAT = "%d-%m-%Y"

	@classmethod
	def initialize_csv(cls):
		try:
			pd.read_csv(cls.CSV_FILE)
		except FileNotFoundError:
			# the data frame will access different rows and columns from a csv file
			df = pd.DataFrame(columns=cls.COLUMNS)
			# export the created data frame to a csv file
			df.to_csv(cls.CSV_FILE, index=False)

	@classmethod
	def add_csv_entry(cls, date, amount, category, description):
		new_entry = {
			"date": date,
			"amount": amount,
			"category": category,
			"description": description
		}
		with open (cls.CSV_FILE, "a", newline="") as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
			writer.writerow(new_entry)
		print("Entery added successfully")



def add():
	CSV.initialize_csv()

	text = "Enter the date of the transaction (dd-mm-yyyy) or Enter for today: "
	date = get_date(text, allow_default=True)

	amount = get_amount()
	category = get_category()
	description = get_description()

	CSV.add_csv_entry(date, amount, category, description)


add()
