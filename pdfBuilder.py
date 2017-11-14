import datetime
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

margin = 100
file_name = "test_pdf"
client_name = "Mr John Doe"
site_address = "221 Example House, London , SW1X 5GH"


# ------------------------------------------------ Date suffix adders --------------------------------------------------
def suffix(d):
    return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')


def custom_date(date_text, current_date):
    return current_date.strftime(date_text).replace('{S}', str(current_date.day) + suffix(current_date.day))
# ----------------------------------------------------------------------------------------------------------------------


def create():
    doc = SimpleDocTemplate("%s.pdf" % file_name, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)

    story = []
    create_header(story)
    doc.build(story)


def create_header(story):
    today_date = custom_date("%A {S} %B %Y", datetime.datetime.now())
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    ptext = '<font size=12><b>Date: </b><i>%s</i></font>' % today_date
    story.append(Paragraph(ptext, styles["Normal"]))
    story.append(Spacer(1, 12))
    ptext = '<font size=12><b>For: </b><i>%s</i></font>' % client_name
    story.append(Paragraph(ptext, styles["Normal"]))
    story.append(Spacer(1, 12))

    ptext = '<font size=12><b>Site: </b><i>%s</i></font>' % site_address
    story.append(Paragraph(ptext, styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(PageBreak())