from odoo import models, fields, api, _


class CustomerPaymentReportWizard(models.TransientModel):
    _name = "customer.payment.pdf.report.wizard"
    _description = "Customer Payment Detailed PDF Report"

    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')

    def action_print_report(self):
        report_from_date = self.from_date.strftime('%d-%b-%Y')
        report_to_date = self.to_date.strftime('%d-%b-%Y')
        print("report_date_to", report_to_date)
        print("report_date_from", report_from_date)

        query = """
                      SELECT
                          move.partner_id,
                          partner.name AS partner_name,
                          MIN(move.create_date) AS first_sales_date,
                          COUNT(move.id) AS total_sale_count,
                          pmt.amount AS total_paid_amount,
                          SUM(move.amount_total) AS total_amount,
                          (SUM(move.amount_total) - pmt.amount) AS balance_amount
                      FROM
                          account_move AS move
                      LEFT JOIN res_partner AS partner ON move.partner_id = partner.id
                      LEFT JOIN (
                          SELECT
                              pmt.partner_id,
                              SUM(pmt.amount) AS amount
                          FROM
                              account_payment AS pmt
                          WHERE
                              pmt.payment_type = 'inbound'
                          GROUP BY
                              pmt.partner_id
                      ) AS pmt ON move.partner_id = pmt.partner_id
                      WHERE
                          move.move_type = 'out_invoice'
                           AND DATE(move.date) BETWEEN '%s' AND '%s'
                      GROUP BY
                          move.partner_id, partner.name, pmt.amount
                  """ % (report_from_date, report_to_date)

        self._cr.execute(query)
        data = self._cr.dictfetchall()
        print(data)

        data = {
            'ids': self.ids,
            'model': self._name,
            'date_from': report_from_date,
            'date_to': report_to_date,
            'vals': data
        }
        print('data', data)
        action = self.env.ref('customer_payment_pdf.customer_payment_pdf_report_print').report_action(self, data=data)

        return action
