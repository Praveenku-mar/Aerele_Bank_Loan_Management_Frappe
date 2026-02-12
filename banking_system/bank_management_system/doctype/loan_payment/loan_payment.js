// Copyright (c) 2026, Praveenkumar Dhanasekar and contributors
// For license information, please see license.txt

frappe.ui.form.on("Loan Payment", {
    setup(frm) {

        frappe.call({
            method: "banking_system.bank_management_system.doctype.loan_payment.loan_payment.get_approve_loan",
            callback: (r) => {

                let loan_approve = r.message || [];
                console.log(loan_approve)

                frm.set_query("loan_id", function() {
                    return {
                        filters: {
                            name: ["in", loan_approve]
                        }
                    };
                });

            }
        });

    },
});

