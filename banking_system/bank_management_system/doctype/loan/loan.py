# Copyright (c) 2026, Praveenkumar Dhanasekar and contributors
# For license information, please see license.txt

import frappe
import math
from frappe.model.document import Document


class Loan(Document):
	def before_save(self):
		self.set_paid_rem_amt()
		self.set_monthly_pay()

	def on_submit(self):
		if(self.loan_status == "Approved"):
			self.add_payment()
	def on_update_after_submit(self):
		self.set_interest()

	def set_interest(self):
		return
	
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
		frappe.log_error("total Interest:",total_interest)
		next_interest_amount = total_interest / (self.month * 12)
		self.next_interest_amount = math.ceil(next_interest_amount)
		frappe.log_error("next month interest amount ",next_interest_amount)
		self.monthly_interest = interest
		monthly_pay = (self.req_amount + total_interest) / (self.month * 12)
		self.monthly_pay = math.ceil(monthly_pay)
		frappe.log_error("monthly pay",math.ceil(monthly_pay))
 
		

	def set_paid_rem_amt(self):
		self.paid_amount = 0
		self.remaining_amount = self.req_amount

	def add_payment(self):
		payment = frappe.new_doc("Payment")
		payment.type = "Loan payment"
		payment.beneficer = "Bank"
		payment.customer = self.applicant_acc_no
		payment.amount = self.req_amount
		payment.date = self.application_date

		payment.submit()

		self.payment_id = payment.name

def send_due_reminder_email():
	loan = frappe.get_all("Loan",
		filters={
			"loan_status":"Approved"
		},
		fields=['name','applicant_name','applicant_acc_no','req_amount','loan_type','monthly_pay','email']
	)
	
	for row in loan:
		html = """ <!DOCTYPE html>

			<html>
			<head>
			    <meta charset="UTF-8">
			    <title>Loan Due Reminder</title>
			</head>
			<body style="font-family: Arial, sans-serif; background-color: #f4f6f8; margin: 0; padding: 20px;">

			```
			<table width="100%" cellpadding="0" cellspacing="0">
			    <tr>
			        <td align="center">
			            <table width="600" cellpadding="20" cellspacing="0" style="background-color: #ffffff; border-radius: 8px;">

			                <tr>
			                    <td align="center" style="background-color: #1f4e79; color: #ffffff; border-radius: 8px 8px 0 0;">
			                        <h2 style="margin: 0;">Loan EMI Reminder</h2>
			                    </td>
			                </tr>

			                <tr>
			                    <td>
			                        <p>Dear <strong>{{loan.applicant_name}}</strong>,</p>

			                        <p>This is a reminder that your loan EMI payment is due.</p>

			                        <hr>

			                        <h3 style="margin-bottom: 10px;">Loan Details</h3>
			                        <p>
			                            <strong>Loan ID:</strong> {{loan.name}}<br>
										<strong>Account No :</strong>{{loan.applicant_acc_no}}
			                            <strong>Loan Type:</strong> {{loan.loan_type}}<br>
			                            <strong>EMI Amount:</strong> ₹{{loan.monthly_pay}}<br>
			                        </p>

			                        <hr>

			                        <p>
			                            Kindly ensure that the payment is made on or before the due date 
			                            to avoid late payment charges or penalties.
			                        </p>

			                        <p>
			                            If you have already made the payment, please ignore this message.
			                        </p>

			                        <p>
			                            For any assistance, contact us at:<br>
			                            <strong>Email:</strong>praveensekar223@gmail.com<br>
			                            <strong>Phone:</strong> 9092837965
			                        </p>

			                        <br>

			                        <p>Regards,<br>
			                        <strong>PK Bank of India, Tharamanagalam</strong></p>
			                    </td>
			                </tr>

			                <tr>
			                    <td align="center" style="background-color: #f0f0f0; font-size: 12px; color: #777; border-radius: 0 0 8px 8px;">
			                        This is an automated message. Please do not reply directly to this email.
			                    </td>
			                </tr>

			            </table>
			        </td>
			    </tr>
			</table>
			```

			</body>
			</html>

		
		"""

		frappe.sendmail(recipients=loan.email,subject="Loan Repayment Reminder",message=html,now=True)







