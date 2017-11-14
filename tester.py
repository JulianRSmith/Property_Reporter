import datetime
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import black
from reportlab.platypus.flowables import *

from nearby import nearby_data, googleMapsApi

margin = 100
file_name = "test_pdf"
client_name = "Mr John Doe"
site_name = "221 Example House"
site_address = site_name + ", London , SW1X 5GH"
postcode = "BN1 7JJ"


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
    create_transport_data(story)
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


def create_transport_data(story):
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    pTitle = '<font size=15><b>%s</b></font>' % "Local Transport"
    story.append(Paragraph(pTitle, styles["Normal"]))
    story.append(Spacer(1, 6))
    d = HRFlowable(width="100%", thickness=1, lineCap='square', color=black, dash=None)
    story.append(d)
    story.append(Spacer(1, 10))

    distance_miles = 3

    train_dict = nearby_data.transport_train(postcode, distance_miles)
    station_count = len(train_dict)
    nearest_station = list(train_dict)[0]
    nearest_station_dist = train_dict[nearest_station]

    destination_trip = googleMapsApi.directions_calc_train(nearest_station, "London")
    destination_line = list(destination_trip)[0]
    destination_length = destination_trip[destination_line]

    pTitle = '<font size=12>Within a {0} mile radius, {1} is situated around {2} train stations, the closest being ' \
             '{3} at {4} away. {3} provides transport links straight into London, with the journey only taking {5} ' \
             'minutes via {6}.</font>'.format(distance_miles, site_name, station_count, nearest_station, nearest_station_dist, destination_length, destination_line)
    story.append(Paragraph(pTitle, styles["Normal"]))
    story.append(Spacer(1, 12))



create()