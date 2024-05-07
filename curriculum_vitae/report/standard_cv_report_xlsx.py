from odoo import models
import base64, io


class StandardCVXlsx(models.AbstractModel):
    _name = "report.curriculum_vitae.standard_cv_report_data"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, lines):
        for line in lines:
            sheet = workbook.add_worksheet(line.name)
            sheet.set_column(0, 4, 20)
            sheet.set_row(0, 110)

            image_data = base64.b64decode(line.image)
            image = io.BytesIO(image_data)
            sheet.insert_image("A1", "image.png", {"image_data": image, "x_scale": 0.3, "y_scale": 0.3})

            header_format = workbook.add_format({"font_size": 16, "bold": True, "valign": "vcenter"})
            header_data = "{} - {} - {}".format(line.name, line.apply_job.name, line.salary)
            sheet.merge_range("B1:E1", header_data, header_format)

            title_format = workbook.add_format({"font_size": 14, "bold": True,
                                                "bg_color": "green", "color": "white"})
            label_format = workbook.add_format({"font_size": 12, "bold": True})
            date_format = workbook.add_format({"align": "left", "num_format": "dd mmm yyyy"})

            sheet.merge_range("A2:E2", "Personal Particulars", title_format)
            sheet.write("A3", "Date of Birth", label_format)
            sheet.merge_range("B3:E3", line.dob, date_format)
            sheet.write("A4", "NRC", label_format)
            sheet.merge_range("B4:E4", line.nrc)
            sheet.write("A5", "Nationality", label_format)
            sheet.merge_range("B5:E5", line.nationality)
            sheet.write("A6", "Phone", label_format)
            sheet.merge_range("B6:E6", line.phone)
            sheet.write("A7", "Email", label_format)
            sheet.merge_range("B7:E7", line.email)
            sheet.write("A8", "Current Address", label_format)
            sheet.merge_range("B8:E8", line.address)
            sheet.write("A9", "Gender", label_format)
            sheet.merge_range("B9:E9", line.gender)
            sheet.write("A10", "Marital Status", label_format)
            sheet.merge_range("B10:E10", line.marital)

            sheet.merge_range("A11:E11", "Career Objectives", title_format)
            sheet.set_row(11, 70)
            sheet.merge_range("A12:E12", line.objective, workbook.add_format({"valign": "top"}))

            eb_row = 13
            eb_column = 0
            sheet.merge_range("A13:E13", "Education Background", title_format)
            sheet.write(eb_row, eb_column, "Certificate", label_format)
            eb_column += 1
            sheet.write(eb_row, eb_column, "Education Center", label_format)

            eb_row += 1
            eb_column = 0
            for certificate in line.certificate_ids:
                sheet.write(eb_row, eb_column, certificate.name)
                eb_column += 1
                sheet.write(eb_row, eb_column, certificate.education_center)

                eb_row += 1
                eb_column = 0

            eh_row = eb_row
            eh_column = 0
            sheet.merge_range(eh_row, eh_column, eh_row, eh_column + 4, "Employment History", title_format)
            eh_row += 1
            sheet.write(eh_row, eh_column, "Job Position", label_format)
            eh_column += 1
            sheet.write(eh_row, eh_column, "Company", label_format)
            eh_column += 1
            sheet.write(eh_row, eh_column, "Responsibility", label_format)
            eh_column += 1
            sheet.write(eh_row, eh_column, "Period From", label_format)
            eh_column += 1
            sheet.write(eh_row, eh_column, "Period To", label_format)

            eh_row += 1
            eh_column = 0
            for employment in line.employment_line_ids:
                sheet.write(eh_row, eh_column, employment.employment_id.name)
                eh_column += 1
                sheet.write(eh_row, eh_column, employment.company)
                eh_column += 1
                sheet.write(eh_row, eh_column, employment.responsibility)
                eh_column += 1
                sheet.write(eh_row, eh_column, employment.period_from, date_format)
                eh_column += 1
                sheet.write(eh_row, eh_column, employment.period_to, date_format)

                eh_row += 1
                eh_column = 0
