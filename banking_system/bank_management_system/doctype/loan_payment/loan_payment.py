	# Copyright (c) 2026, Praveenkumar Dhanasekar and contributors
	# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class LoanPayment(Document):
	def before_save(self):
		self.validate_loan()

	def validate(self):
		self.check_penalty()

	def on_submit(self):
		self.set_rem_paid_amt()

	def before_cancel(self):
		self.roll_back_loan()

	

	def check_penalty(self):
		end_date = frappe.db.get_single_value("Bank Setting", "loan_payment_end_date")
		fine = frappe.db.get_single_value("Bank Setting", "fine_per_day")

		end_date = getdate(end_date)
		payment_date = getdate(self.date_of_payment)

		if payment_date > end_date:
			day_diff = (payment_date - end_date).days
			late_day_interest = round(self.remaining_amount * (self.rate_of_interest / 365) * (day_diff / 365))
			self.penalty_amount = late_day_interest
			frappe.msgprint(
				title="Penalty Alert",
				msg=f"Penalty of ₹{self.penalty_amount} has been deducted from your payment.",
				indicator="red"
			)
		else:
			self.penalty_amount = 0

			
		
	def roll_back_loan(self):
		loan = frappe.get_doc("Loan",self.loan_id)
		amount = self.amount
		mon_interest = loan.monthly_interest
		aft_interest = amount - mon_interest
		paid = loan.paid_amount - amount
		rem = loan.remaining_amount + aft_interest
		for row in loan.payment_tab:
			if row.payment_link == self.name:
				frappe.log_error("1111111",rem)
				payment = frappe.get_doc("Payment",row.payment)
				payment.cancel().delete()
				loan.remove(row)
		frappe.db.set_value("Account",loan.applicant_acc_no,{
			"paid_loan_amount":paid,
			"remaining_loan_amount":rem
		})
		#calculate monthly interest after loan repayment
		#loan.next_interest_amount += loan.next_interest_amount * (loan.monthly_interest * 12)
		loan.paid_amount = paid
		loan.remaining_amount = rem
		loan.save(ignore_permissions=True)
		# frappe.db.set_value("Loan",self.loan_id,
		# {
		# 	"paid_amount" : paid,
		# 	"remaining_amount":rem
		# }
		# )
				


	def set_rem_paid_amt(self):
		if self.penalty_amount == 0:
			aft_interest = self.amount - self.monthly_interest 
		else:
			aft_interest = self.amount - self.monthly_interest - self.penalty_amount
		if aft_interest <= 0:
			frappe.throw("Payment amount is not sufficient to cover interest.")

		if aft_interest > self.remaining_amount:
			frappe.throw("Payment exceeds remaining loan amount.")

		rem_amt = self.remaining_amount - aft_interest
		
		loan = frappe.get_doc("Loan",self.loan_id)

		paid_amt = self.paid_amount + self.amount 
		
		frappe.log_error("2222222",paid_amt)
		frappe.log_error("11111111",rem_amt)
		loan.next_interest_amount = self.calculate_next_month_interest(rem_amt,loan.monthly_interest)
		loan.paid_amount=paid_amt
		loan.remaining_amount=rem_amt

		payment = frappe.get_doc({
			'doctype':"Payment",
			'type':'Loan Repayment',
			'beneficer':'Customer',
			'customer':self.loan_id,
			'amount':self.amount,
			'date':self.date_of_payment	
		})
		# payment.type = "Loan Repayment"
		# payment.beneficer = "Customer"
		# payment.customer = self.loan_id
		# payment.amount = self.amount
		# payment.date = self.date_of_payment
		payment.insert()
		payment.submit()

		loan.append("payment_tab", {
			"payment_link":self.name,
			"amount_paid": self.amount,
			"total_paid_amount":paid_amt,
			"remaining_amount": rem_amt,
			"payment_data":self.date_of_payment,
			"payment":payment.name,
			'penalty':self.penalty_amount,
			'interest':self.monthly_interest
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

	@staticmethod
	def calculate_next_month_interest(rem_amt,interest):
		month_ins = interest / 12
		month_ins_amt = rem_amt * (month_ins / 100)

		return month_ins_amt


	def validate_loan(self):
		if self.remaining_amount < self.amount:
			frappe.throw("Amount should be less than the Remaining loan amount")
		
		if self.remaining_amount == self.amount:
			frappe.throw("Loan completed")


@frappe.whitelist()
def get_approve_loan():
	loan_approve = frappe.get_all("Loan",
	filters={
		'loan_status':'Approved'
	},pluck='name'
	)

	return loan_approve


