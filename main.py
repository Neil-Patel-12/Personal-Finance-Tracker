import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_amount, get_category, get_description
import matplotlib.pyplot as plt

class CSV:
	# class methods
	CSV_FILE = "finance_data.csv"
	COLUMNS = ["date", "amount", "category", "description"]
	FORMAT = "%d-%m-%Y"

	# this decorator means it will have access to the class itself, but no access to its instance
	# access to class variables and class methods
	@classmethod
	def initialize_csv(cls):
		try:
			pd.read_csv(cls.CSV_FILE)
		except FileNotFoundError:
			# the data frame will access different rows and columns from a csv file
			df = pd.DataFrame(columns=cls.COLUMNS)
			# export the created DataFrame to a newly created csv file
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


	# will load all transation from start and end date
	'''
	         date  amount category description
	0  13-07-2024  125.65   Income      Salary
	1  13-07-2024   63.00  Expense         gas
	2  13-07-2024  100.01  Expense        food
	3  10-07-2024 3000.00   Income      Salary
	4  20-04-2024  600.00   Income     running
	'''
	@classmethod
	def get_transactions(cls, start_date, end_date):
		# df is the multidimentional DataFrame
		df = pd.read_csv(cls.CSV_FILE)
		# Converts the "date" column in the DataFrame to datetime objects
		# using the specified date format (%d-%m-%Y)
		df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)

		# Converts START & END date strings to datetime objects.
		start_date = datetime.strptime(start_date, CSV.FORMAT)
		end_date = datetime.strptime(end_date, CSV.FORMAT)

		mask = (df["date"] >= start_date) & (df["date"] <= end_date)
		# print(mask) this will be a series of True and False values if it falls in the range
		filtered_df = df.loc[mask] # this will return a new FILTERED DATAFRAME, that has rows where MASK was True

		if filtered_df.empty:
			print("No transaction fount in the given date range")
		else:
			print(f"\nTransactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
			# filtered transactions, formatting the "date" column back to the original dd-mm-yyyy format.
			print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}))

			total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
			total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
			print("\n<--------------->")
			print("Summary:")
			print(f"Total Income: ${total_income:.2f}")
			print(f"Total Expense: ${total_expense:.2f}")
			print(f"Net Savings: ${(total_income - total_expense):.2f}")
			print("<--------------->\n")

		return filtered_df


def add():
	# class method can only be called on classes. 
	CSV.initialize_csv()

	date = get_date("Enter the date of the transaction (dd-mm-yyyy) or Enter for today: ", allow_default=True)

	amount = get_amount()
	category = get_category()
	description = get_description()

	CSV.add_csv_entry(date, amount, category, description)

def plot_transactions(df):
	df.set_index("date", inplace=True)

	income_df = (
		df[df["category"] == "Income"]
		.resample("D")
		.sum()
		.reindex(df.index, fill_value=0)
	)

	expense_df = (
		df[df["category"] == "Expense"]
		.resample("D")
		.sum()
		.reindex(df.index, fill_value=0)
	)

	plt.figure(figsize=(10, 5))
	plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
	plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
	plt.xlabel("Date")
	plt.ylabel("Amount")
	plt.title('Income and Expenses Over Time')
	plt.legend()
	plt.grid(True)
	plt.show()

def main():
	while True:
		print("\n1. Add a new transaction")
		print("2. View transactions and summary within a date range")
		print("3. Exit")
		choice = input("Enter your choice (1-3): ")

		if choice == "1":
			add()
		elif choice == "2":
			start_date = get_date("Enter the START date (dd-mm-yyyy): ")
			end_date = get_date("Enter the END date (dd-mm-yyyy): ")
			df = CSV.get_transactions(start_date, end_date)
			if input("Do you want to see a plot? (y/n) ").lower() == "y":
				plot_transactions(df)
		elif choice == "3":
			print("\nThank you, have a nice day.\n")
			break
		else:
			print("Invalid choice. Enter 1, 2, or 3. ")

if __name__ == "__main__":
	main()