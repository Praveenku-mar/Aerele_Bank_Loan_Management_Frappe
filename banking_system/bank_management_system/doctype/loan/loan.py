# Copyright (c) 2026, Praveenkumar Dhanasekar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Loan(Document):
	def before_save(self):
		self.validate_loan()
		self.set_paid_rem_amt()
		self.set_monthly_pay()

	def set_monthly_pay(self):
		if int(self.credit_score) <= 30:
			frappe.msgprint("Sorry, your credit does not meet our requirements.")
			self.cancel()
		loan_type = self.loan_type 
		if loan_type == "Personal":
			interest = 10
		elif loan_type == "Vehicle":
			interest = 9
		elif loan_type == "Business":
			interest = 8
		elif loan_type == "Loan Against Property":
			interest = 7
		elif loan_type == "House Loan":
			interest = 6
		elif loan_type == "Gold Loan":
			interest = 5
		else :
			interest = 4
		
		total_interest = self.remaining_amount * interest / 100 * self.month
		self.monthly_interest = total_interest / (self.month * 12)
		self.monthly_pay = (self.req_amount + total_interest) / (self.month * 12)
 
		

	def set_paid_rem_amt(self):
		self.paid_amount = 0
		self.remaining_amount = self.req_amount

	def validate_loan(self):
		return 

