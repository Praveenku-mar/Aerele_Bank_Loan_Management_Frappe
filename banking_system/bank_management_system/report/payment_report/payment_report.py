# Copyright (c) 2026, Praveenkumar Dhanasekar and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	beneficer = filters.get("beneficer")
	date = filters.get("date")
	loan_id = filters.get("loan_id")

	if date and loan_id:
		return get_loan_date_cols(), get_loan_date_data(date,loan_id)

	if beneficer and date:
		return get_beneficer_date_cols(), get_beneficer_date_data(beneficer,date)

	if beneficer:
		return get_beneficer_cols(), get_beneficer_data(beneficer)

	if date:
		return get_date_cols(), get_date_data(date)

	if loan_id:
		return get_loan_cols(), get_loan_data(loan_id)

	return get_all_cols(),get_all_data()

def get_all_cols():
	return[
		{
			'fieldname':'type',
			'fieldtype':'Data',
			'label':'Type',
			'width':150
		},
		{
			'fieldname':'beneficer',
			'fieldtype':'Data',
			'label':'Benificer',
			'width':200
		},
		{
			'fieldname':'customer',
			'fieldtype':'Data',
			'label':'Customer',
			'width':300
		},
		{
			'fieldname':'amount',
			'fieldtype':'Currency',
			'label':'Amount',
			'width':200
		},
		{
			'fieldname':'date',
			'fieldtype':'Date',
			'label':'Date',
			'width':200
		}
	]


def get_all_data():
	data = frappe.get_all("Payment",fields=[
			"type",
            "beneficer",
            "customer",
            "amount",
            "date"])

	return data
	
def get_loan_date_cols():
	return[
		{
			'fieldname':'amount',
			'fieldtype':'Currency',
			'label':'Amount',
			'width':200
		}
	]

def get_loan_date_data(date,loan_id):
	data  =frappe.get_all("Payment",
		filters={
			'customer':loan_id,
			'date':date
		},
		fields={'amount'}
	)
	return data

def get_beneficer_date_cols():
	return[
		{
			'fieldname':'customer',
			'fieldtype':'Data',
			'label':'Customer',
			'width':300
		},
		{
			'fieldname':'amount',
			'fieldtype':'Currency',
			'label':'Amount',
			'width':200
		}
	]

def get_beneficer_date_data(beneficer,date):
	data = frappe.get_all("Payment",
		filters={
			'beneficer':beneficer,
			'date':date
		},
		fields={
			'customer',
			'amount'
		}
	)

	return data


def get_beneficer_cols():
	return[
		{
			'fieldname':'type',
			'fieldtype':'Data',
			'label':'Type',
			'width':150
		},
		{
			'fieldname':'customer',
			'fieldtype':'Data',
			'label':'Customer',
			'width':300
		},
		{
			'fieldname':'amount',
			'fieldtype':'Currency',
			'label':'Amount',
			'width':200
		},
		{
			'fieldname':'date',
			'fieldtype':'Date',
			'label':'Date',
			'width':200
		}
	]

def get_beneficer_data(beneficer):
	data = frappe.get_all("Payment",
		filters={
			'beneficer':beneficer
		},
		fields={
			'type',
			'customer',
			'amount',
			'date'
		}
	)

	return data
def get_date_cols():
	return[
		{
			'fieldname':'type',
			'fieldtype':'Data',
			'label':'Type',
			'width':150
		},
		{
			'fieldname':'beneficer',
			'fieldtype':'Data',
			'label':'Benificer',
			'width':200
		},
		{
			'fieldname':'customer',
			'fieldtype':'Data',
			'label':'Customer',
			'width':300
		},
		{
			'fieldname':'amount',
			'fieldtype':'Currency',
			'label':'Amount',
			'width':200
		}
	]

def get_date_data(date):
	data = frappe.get_all("Payment",
		filters={
			'date':date
		},
		fields={
			"type",
			"beneficer",
			"customer",
			"amount",
		})

	return data

def get_loan_cols():
	return[
		{
			'fieldname':'type',
			'fieldtype':'Data',
			'label':'Type',
			'width':150
		},
		{
			'fieldname':'beneficer',
			'fieldtype':'Data',
			'label':'Benificer',
			'width':200
		},
		{
			'fieldname':'customer',
			'fieldtype':'Data',
			'label':'Customer',
			'width':200
		},
		{
			'fieldname':'amount',
			'fieldtype':'Currency',
			'label':'Amount',
			'width':200
		},
		{
			'fieldname':'date',
			'fieldtype':'Date',
			'label':'Date',
			'width':200
		}
	]

def get_loan_data(loan_id):
	frappe.log_error('2222')
	data = frappe.get_all("Payment",
		filters={
			'customer':loan_id
		},
		fields=[
            "type",
            "beneficer",
            "customer",
            "amount",
            "date"
        ]
	)
	frappe.log_error("111111",data)
	return data