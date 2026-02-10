# Copyright (c) 2026, Praveenkumar Dhanasekar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LoanPayment(Document):
	def before_save(self):
		self.validate_loan()
	
	def on_submit(self):
		self.set_rem_paid_amt()

	def set_rem_paid_amt(self):
		aft_interest = self.amount - self.monthly_interest
		if aft_interest <= 0:
			frappe.throw("Payment amount is not sufficient to cover interest.")

		if aft_interest > self.remaining_amount:
			frappe.throw("Payment exceeds remaining loan amount.")

		rem_amt = self.remaining_amount - aft_interest
		
		loan = frappe.get_doc("Loan",self.loan_id)

		paid_amt = self.paid_amount + self.amount 
		
		frappe.log_error("2222222",paid_amt)
		frappe.log_error("11111111",rem_amt)

		loan.paid_amount=paid_amt
		loan.remaining_amount=rem_amt

		loan.append("payment_tab", {
			"payment_link":self.name,
    		"amount_paid": self.amount,
			"total_paid_amount":paid_amt,
    		"remaining_amount": rem_amt,
			"payment_data":self.date_of_payment
		})

		loan.save(ignore_permissions=True)

		acc_no = frappe.db.get_value(
			"Loan",
			self.loan_id,
			"applicant_acc_no"
		)
		if not acc_no:
			frappe.throw("Linked account not found for this loan.")

		frappe.db.set_value("Account",acc_no,{
			"paid_loan_amount":paid_amt,
			"remaining_loan_amount":rem_amt
		})

	def validate_loan(self):
		if self.remaining_amount < self.amount:
			frappe.throw("Amount should be less than the Remaining loan amount")
		
		if self.remaining_amount == self.amount:
			frappe.throw("Loan completed")
