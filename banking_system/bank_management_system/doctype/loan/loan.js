// Copyright (c) 2026, Praveenkumar Dhanasekar and contributors
// For license information, please see license.txt

frappe.ui.form.on("Loan", {
    refresh(frm) {

        if (!frm.doc.email || frm.doc.loan_status == "Rejected") {
            return; // no email → no button
        }



        frm.add_custom_button("Send History Email", () => {

            frappe.confirm(
                "Are you sure you want to send the repayment history email?",
                () => {

                    frappe.call({
                        method: "banking_system.bank_management_system.doctype.loan.loan.history_email",
                        args: {
                            name: frm.doc.name
                        },
                        freeze: true,
                        freeze_message: "Sending email...",
                        callback: function (r) {
                            if (!r.exc) {
                                frappe.msgprint({
                                    title: "Success",
                                    message: "Loan repayment history email sent successfully.",
                                    indicator: "green"
                                });
                            }
                        }
                    });

                }
            );

        }, "Actions");
    }
});

