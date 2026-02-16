# Copyright (c) 2026, Praveenkumar Dhanasekar and contributors
# For license information, please see license.txt

import frappe
import math
from frappe.model.document import Document
from frappe.utils.pdf import get_pdf


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


@frappe.whitelist()
def history_email(name):
	doc = frappe.get_doc("Loan", name)
	message = """
		<html>
		<body style="margin:0; padding:0; font-family: Arial, sans-serif; background-color:#f4f6f9;">

			<div style="max-width:800px; margin:30px auto; background:#ffffff; border-radius:10px; box-shadow:0 4px 12px rgba(0,0,0,0.1); overflow:hidden;">

				<!-- Header -->
				<div style="background:linear-gradient(90deg,#1e3c72,#2a5298); color:white; padding:20px;">
					<h2 style="margin:0;">Loan Repayment History</h2>
				</div>

				<!-- Loan Details -->
				<div style="padding:20px;">
					<p style="margin:5px 0;"><strong>Loan ID:</strong> {{ doc.name }}</p>
					<p style="margin:5px 0;"><strong>Account Holder:</strong> {{ doc.applicant_name }}</p>
					<p style="margin:5px 0;"><strong>Email:</strong> {{ doc.email }}</p>
				</div>

				<!-- Table -->
				<div style="padding:20px;">
					<table width="100%" cellpadding="10" cellspacing="0" style="border-collapse:collapse;">
						<thead>
							<tr style="background-color:#2a5298; color:white; text-align:left;">
								<th>Serial No</th>
								<th>Payment ID</th>
								<th>Date</th>
								<th>Amount Paid</th>
								<th>Balance</th>
								<th>Interest</th>
								<th>Penalty</th>
							</tr>
						</thead>
						<tbody>
							{% for row in doc.payment_tab %}
							<tr style="border-bottom:1px solid #ddd;">
								<td>{{ loop.index }}</td>
								<td>{{ row.payment_link }}</td>
								<td>{{ row.payment_data }}</td>
								<td style="color:green; font-weight:bold;">₹ {{ row.amount_paid }}</td>
								<td style="color:#d9534f;">₹ {{ row.remaining_amount | round(2)}}</td>
								<td>₹ {{ row.interest | round(2)}}</td>
								<td style="color:#ff9800;">₹ {{ row.penalty }}</td>
							</tr>
							{% endfor %}
						</tbody>
					</table>
				</div>
					<p style="font-size:14px; color:#555; "margin:5px 0;">
                            Need help? Contact us:<br>
                            📧 praveensekar223@gmail.com<br>
                            📞 9092837965
                        </p>
        
                        <p style="margin-bottom:0; "margin:5px 0;">
                            Regards,<br>
                            <strong>PK Bank of India, Tharamanagalam</strong>
                        </p>

				<!-- Footer -->
				<div style="background:#f1f1f1; padding:15px; text-align:center; font-size:12px; color:#777;">
					This is an automated loan repayment report. Please do not reply to this email.
				</div>

			</div>

		</body>
		</html>
		"""

	rendered_message = frappe.render_template(message, {"doc": doc})
	pdf = get_pdf(rendered_message)

	frappe.sendmail(
		recipients=[doc.email],
		subject=f"Loan repayment history {doc.name}",
		message=f"{rendered_message} \n Please find the attached loan repayment history.",
		attachments=[{
            "fname": "Loan Invoice.pdf",
            "fcontent": pdf
        }],
		now=True
	)





