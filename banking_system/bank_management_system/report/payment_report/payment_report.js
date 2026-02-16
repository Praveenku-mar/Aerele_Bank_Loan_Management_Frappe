// Copyright (c) 2026, Praveenkumar Dhanasekar and contributors
// For license information, please see license.txt

frappe.query_reports["Payment Report"] = {
	"filters": [
		{
			'fieldname':'beneficer',
			'fieldtype':'Select',
			'label':'Beneficer',
			'options':[' ','Bank','Customer']
		},
		{
			'fieldname':'date',
			'fieldtype':'Date',
			"label":'Date'
		},
		{
			'fieldname':'loan_id',
			'fieldtype':'Link',
			'label':'Loan Id',
			'options':'Loan'
		}

	]
};
