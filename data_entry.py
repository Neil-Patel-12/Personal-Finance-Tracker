from datetime import datetime

CATEGORIES = {"I": "Income", "E": "Expense"}

def get_date(prompt, allow_default=False):
	date_str = input(prompt)
	if allow_default and not date_str:
		# this will return todays date.
		# datetime.today() will print "2024-07-14 09:03:37.899155"
		# datetime.today().strftime("%d-%m-%Y") will format to "14-07-2024"
		return datetime.today().strftime("%d-%m-%Y")

	try:
		# ensures the date is in the correct dd-mm-yyyy format.
		valid_date = datetime.strptime(date_str, "%d-%m-%Y")
		print(f"{valid_date} is a valid date")
		return valid_date.strftime("%d-%m-%Y")
	except ValueError:
		print("Invalid date frmat. Please enter the date in dd-mm-yyyy format")
		return get_date(prompt, allow_default)



def get_amount():
	try:
		amount = float(input("Enter the amount: "))
		if amount <= 0:
			raise ValueError("Amount must be a non-negative non-zero value.")
		return amount
	except ValueError as e:
		print(e)
		return get_amount()


def get_category():
	category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper()
	if category in CATEGORIES:
		return CATEGORIES[category]

	print("Invalid category. Please enter 'I' for Income or 'E' for Expense.")
	return get_category


def get_description():
	return input("Enter a description (optional): ")