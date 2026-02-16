import frappe
from frappe.utils.jinja import render_template
def send_due_reminder_email():
    loan = frappe.get_all("Loan",
    filters={
        "loan_status":"Approved"
    },
    fields=['name','applicant_name','applicant_acc_no','req_amount','loan_type','monthly_pay','email']
    )
    html_template = """ 
            <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Loan EMI Reminder</title>
        </head>
        <body style="margin:0; padding:0; background-color:#f2f4f7; font-family:Arial, Helvetica, sans-serif;">
        
        <table width="100%" cellpadding="0" cellspacing="0">
        <tr>
        <td align="center" style="padding:30px 15px;">
        
            <table width="650" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:10px; box-shadow:0 4px 15px rgba(0,0,0,0.08); overflow:hidden;">
        
                <!-- Header -->
                <tr>
                    <td style="background:linear-gradient(90deg,#1f4e79,#163a5f); padding:25px; text-align:center; color:#ffffff;">
                        <h1 style="margin:0; font-size:22px; letter-spacing:1px;">Loan EMI Payment Reminder</h1>
                        <p style="margin:5px 0 0; font-size:14px; opacity:0.9;">PK Bank of India</p>
                    </td>
                </tr>
        
                <!-- Body -->
                <tr>
                    <td style="padding:30px; color:#333333; font-size:15px; line-height:1.6;">
        
                        <p style="margin-top:0;">Dear <strong>{{ row.applicant_name }}</strong>,</p>
        
                        <p>
                            This is a friendly reminder that your monthly EMI payment is due. 
                            Please review your loan details below and ensure timely payment to avoid penalties.
                        </p>
        
                        <!-- Loan Details Box -->
                        <table width="100%" cellpadding="10" cellspacing="0" 
                               style="margin:20px 0; border:1px solid #e0e6ed; border-radius:6px; background:#f9fbfd;">
                            <tr>
                                <td width="40%" style="color:#555;"><strong>Loan ID</strong></td>
                                <td>{{ row.name }}</td>
                            </tr>
                            <tr>
                                <td style="color:#555;"><strong>Account Number</strong></td>
                                <td>{{ row.applicant_acc_no }}</td>
                            </tr>
                            <tr>
                                <td style="color:#555;"><strong>Loan Type</strong></td>
                                <td>{{ row.loan_type }}</td>
                            </tr>
                            <tr>
                                <td style="color:#555;"><strong>Monthly EMI</strong></td>
                                <td style="font-size:18px; color:#1f4e79;"><strong>₹ {{ row.monthly_pay | round(2)}}</strong></td>
                            </tr>
                        </table>
        
                        <p>
                            Kindly ensure payment is completed on or before the due date 
                            to avoid late charges.
                        </p>
        
                        <p>
                            If you have already made the payment, please disregard this message.
                        </p>
        
                        <hr style="border:none; border-top:1px solid #e0e6ed; margin:25px 0;">
        
                        <p style="font-size:14px; color:#555;">
                            Need help? Contact us:<br>
                            📧 praveensekar223@gmail.com<br>
                            📞 9092837965
                        </p>
        
                        <p style="margin-bottom:0;">
                            Regards,<br>
                            <strong>PK Bank of India, Tharamanagalam</strong>
                        </p>
        
                    </td>
                </tr>
        
                <!-- Footer -->
                <tr>
                    <td style="background:#f2f4f7; padding:15px; text-align:center; font-size:12px; color:#888;">
                        This is an automated notification. Please do not reply to this email.
                    </td>
                </tr>
        
            </table>
        
        </td>
        </tr>
        </table>
        
        </body>
        </html>
        
    """

    for row in loan:
        html = render_template(html_template, {"row": row})

        frappe.sendmail(recipients=[row['email']],subject="Loan Repayment Reminder",message=html,now=True)
