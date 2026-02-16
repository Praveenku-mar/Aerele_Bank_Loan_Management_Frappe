# Copyright (c) 2026, Praveenkumar Dhanasekar and contributors
# For license information, please see license.txt
import frappe


def execute(filters=None):

	loan_id = filters.get("loan_id")
	loan_type = filters.get("type")
	date = filters.get("date")

	if loan_id:
		return get_loan_id_cols(), get_loan_id_data(loan_id)
	
	if loan_type:
		return get_loan_type_cols(), get_loan_type_data(loan_type)

	if date:
		return get_date_cols(), get_date_data(date)
	
	return get_all_cols(),get_all_data()

#Loan Id alone

def get_loan_id_cols():
	return[
		{
			'fieldname':"applicant_acc_no",
			'fieldtype':'Data',
			'label':'Account No',
			'width':150
		},
		{
			'fieldname':'applicant_name',
			'fieldtype':'Data',
			'label':"Account Holder Name",
			'width':200
		},
		{
			'fieldname':'loan_type',
			'fieldtype':'Data',
			'label':"Loan Type",
			'width':150
		},
		{
			'fieldname':'req_amount',
			'fieldtype':"Currency",
			'label':"Loan Amount",
			'Width':150
		},
		{
			'fieldname':'remaining_amount',
			'fieldtype':"Currency",
			'label':"Remaining Amount",
			'width':150
		},
		{
			'fieldname':'application_date',
			'fieldtype':'Date',
			'label':'Date',
			'width':150
		},
		{
			'fieldname':'loan_status',
			'fieldtype':'Data',
			'label':"Status",
			'width':150
		}
	]

def get_loan_id_data(loan_id):
	data = frappe.get_all("Loan",
		filters={
			"name":loan_id
		},
		fields=['applicant_acc_no','applicant_name','loan_type','req_amount','remaining_amount','application_date','loan_status']
	)

	return data


# Loan type alone
def get_loan_type_cols():
	return[
		{
			'fieldname':"applicant_acc_no",
			'fieldtype':'Data',
			'label':'Account No',
			'width':200
		},
		{
			'fieldname':'applicant_name',
			'fieldtype':'Data',
			'label':"Account Holder Name",
			'width':200
		},
		{
			'fieldname':'req_amount',
			'fieldtype':"Currency",
			'label':"Loan Amount",
			'Width':200
		},
		{
			'fieldname':'remaining_amount',
			'fieldtype':"Currency",
			'label':"Remaining Amount",
			'width':200
		},
		{
			'fieldname':'application_date',
			'fieldtype':'Date',
			'label':'Date',
			'width':200
		},
		{
			'fieldname':'loan_status',
			'fieldtype':'Data',
			'label':"Status",
			'width':200
		}
	]

def get_loan_type_data(loan_id):
	data = frappe.get_all("Loan",
		filters={
			'loan_type':loan_id
		},
		fields=['applicant_acc_no','applicant_name','req_amount','remaining_amount','application_date','loan_status']
	)

	return data

# Date alone
def get_date_cols():
	return[
		{
			'fieldname':"applicant_acc_no",
			'fieldtype':'Data',
			'label':'Account No',
			'width':200
		},
		{
			'fieldname':'applicant_name',
			'fieldtype':'Data',
			'label':"Account Holder Name",
			'width':200
		},
		{
			'fieldname':'req_amount',
			'fieldtype':"Currency",
			'label':"Loan Amount",
			'Width':200
		},
		{
			'fieldname':'remaining_amount',
			'fieldtype':"Currency",
			'label':"Remaining Amount",
			'width':200
		},
		{
			'fieldname':'loan_type',
			'fieldtype':'Data',
			'label':"Loan Type",
			'width':150
		},
		{
			'fieldname':'loan_status',
			'fieldtype':'Data',
			'label':"Status",
			'width':200
		}
	]

def get_date_data(date):
	data = frappe.get_all("Loan",
		filters={
			'application_date':date
		},
		fields=['applicant_acc_no','applicant_name','req_amount','remaining_amount','loan_type','loan_status']
	)

	return data


# Loan id and Date 
def get_all_cols():
	return[
		{
			'fieldname':"applicant_acc_no",
			'fieldtype':'Data',
			'label':'Account No',
			'width':200
		},
		{
			'fieldname':'applicant_name',
			'fieldtype':'Data',
			'label':"Account Holder Name",
			'width':200
		},
		{
			'fieldname':'req_amount',
			'fieldtype':"Currency",
			'label':"Loan Amount",
			'Width':200
		},
		{
			'fieldname':'remaining_amount',
			'fieldtype':"Currency",
			'label':"Remaining Amount",
			'width':200
		},
		{
			'fieldname':'loan_type',
			'fieldtype':'Data',
			'label':"Loan Type",
			'width':150
		},
		{
			'fieldname':'loan_status',
			'fieldtype':'Data',
			'label':"Status",
			'width':200
		},
		{
			'fieldname':'application_date',
			'fieldtype':'Date',
			'label':'Date',
			'width':150
		},
	]

def get_all_data():
	data = frappe.get_all("Loan",
		fields=['applicant_acc_no','applicant_name','req_amount','remaining_amount','loan_type','loan_status',"application_date"]
	)

	return data
