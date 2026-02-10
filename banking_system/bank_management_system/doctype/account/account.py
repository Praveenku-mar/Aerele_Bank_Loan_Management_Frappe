# Copyright (c) 2026, Praveenkumar Dhanasekar
# For license information, please see license.txt

import frappe
from frappe.model.document import Document 


# ---------------- Verhoeff Tables (CONSTANTS) ---------------- #

D_TABLE = [
    [0,1,2,3,4,5,6,7,8,9],
    [1,2,3,4,0,6,7,8,9,5],
    [2,3,4,0,1,7,8,9,5,6],
    [3,4,0,1,2,8,9,5,6,7],
    [4,0,1,2,3,9,5,6,7,8],
    [5,9,8,7,6,0,4,3,2,1],
    [6,5,9,8,7,1,0,4,3,2],
    [7,6,5,9,8,2,1,0,4,3],
    [8,7,6,5,9,3,2,1,0,4],
    [9,8,7,6,5,4,3,2,1,0]
]

P_TABLE = [
    [0,1,2,3,4,5,6,7,8,9],
    [1,5,7,6,2,8,3,0,9,4],
    [5,8,0,3,7,9,6,1,4,2],
    [8,9,1,6,0,4,3,5,2,7],
    [9,4,5,3,1,2,6,8,7,0],
    [4,2,8,6,5,7,3,9,0,1],
    [2,7,9,3,8,0,6,4,1,5],
    [7,0,4,6,9,1,3,2,5,8]
]

INV_TABLE = [0,4,3,2,1,5,6,7,8,9]


class Account(Document):

	def before_save(self):
		self.set_full_name()
		self.validate_aadhaar_number()
		self.calculate_credit_score()
	
	def calculate_credit_score(self):
		monthly_income = self.monthly_income
		employee_type = self.salary_type
		income_stability = self.work_stabilityin_years

		if monthly_income <= 0:
			return 0

		if monthly_income >= 100000:
			income_score = 25
		elif monthly_income >= 50000:
			income_score = 18
		elif monthly_income >= 25000:
			income_score = 10
		else:
			income_score = 5

		if employee_type == "Fixed":
			employee_score = 15
		elif employee_type == "Commission Based":
			employee_score = 12
		elif employee_type == "Performance Based":
			employee_score = 11
		else :
			employee_score = 10

		if income_stability >= 5:
			stability_score = 20
		elif income_stability >= 2:
			stability_score = 10
		else:
			stability_score = 5
		
		self.credit_score = (income_score + employee_score + stability_score)


	def set_full_name(self):
		if self.ben_name and self.father_name:
			self.full_name = f"{self.ben_name} {self.father_name}"
		else:
			self.full_name = self.ben_name or ""

	def validate_aadhaar_number(self):
		if not self.is_valid_aadhaar(self.aadhaar_number):
			frappe.throw("Invalid Aadhaar Number.")

	@staticmethod
	def is_valid_aadhaar(aadhaar: str) -> bool:
		if not aadhaar.isdigit() or len(aadhaar) != 12:
			return False

		c = 0
		for i, digit in enumerate(reversed(aadhaar)):
			c = D_TABLE[c][P_TABLE[i % 8][int(digit)]]

		return c == 0
