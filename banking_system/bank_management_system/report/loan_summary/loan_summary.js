// Copyright (c) 2026, Praveenkumar Dhanasekar and contributors
// For license information, please see license.txt

frappe.query_reports["Loan Summary"] = {
	"filters": [
		{
			'fieldname':"loan_id",
			'fieldtype':'Link',
			'options':'Loan',
			'label':"Loan Id"
		},
		{
			'fieldname':'type',
			'fieldtype':'Select',
			'lable':'Loan Type',
			'options':[" ","House Loan","Business Loan","Vehicle Loan","Gold Loan","Loan Against Property","Personal Loan","Education Loan"]
		},
		{
			'fieldname':'date',
			'fieldtype':'Date',
			'label':"Date",
		}

	]
};
