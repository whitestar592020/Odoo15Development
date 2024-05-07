{
    "name": "CV Form",
    "website": "https//www.facebook.com/odooerpdevelopment",
    "category": "Productivity",
    "summary": "Custom module for the CV form creation!",
    "author": "White Star Myanmar education center",
    "application": True,
    "depends": ["base", "report_xlsx", "mail"],
    "data": [
        "security/cv_security.xml",
        "security/ir.model.access.csv",
        "views/standard_cv_views.xml",

        "views/job_type_views.xml",
        "views/certificate_views.xml",
        "views/employment_views.xml",
        "views/employment_line_views.xml",

        "views/standard_cv_views_form.xml",
        "views/standard_cv_views_tree.xml",

        "report/standard_cv_report_pdf.xml",
        "report/standard_cv_report_template.xml",
        "report/standard_cv_report_xlsx.xml",

        "views/standard_cv_views_kanban.xml",
        "views/standard_cv_views_search.xml",
        "views/standard_cv_views_reporting.xml",
        "views/standard_cv_views_graph.xml",
        "views/standard_cv_views_pivot.xml",
        "views/standard_cv_views_calendar.xml",
    ],
    "demo": [
        "data/job_type_demo.xml",
    ]
}
