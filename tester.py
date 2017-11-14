import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, flowables, Table, TableStyle
from reportlab.lib import colors, styles as style, enums

from nearby import nearby_data, googleMapsApi

# Global variables
styles = style.getSampleStyleSheet()
story = []

margin = 100
file_name = "test_pdf"
client_name = "Mr John Doe"
site_name = "221 Example House"
site_address = site_name + ", London , SW1X 5GH"
postcode = "HA4 0EJ"


# ------------------------------------------------ Date suffix adders --------------------------------------------------
def suffix(d):
    return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')


def custom_date(date_text, current_date):
    return current_date.strftime(date_text).replace('{S}', str(current_date.day) + suffix(current_date.day))
# ----------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------- Create the PDF ----------------------------------------------------
def create():
    doc = SimpleDocTemplate("%s.pdf" % file_name, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)

    create_header()
    create_transport_data()
    doc.build(story)
# ----------------------------------------------------------------------------------------------------------------------


# ------------------------------------------- Create the document headers ----------------------------------------------
def create_header():
    today_date = custom_date("%A {S} %B %Y", datetime.datetime.now())
    styles = style.getSampleStyleSheet()
    styles.add(style.ParagraphStyle(name='Justify', alignment=enums.TA_JUSTIFY))

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
# ----------------------------------------------------------------------------------------------------------------------


def create_transport_data():
    create_title("Local Transport")

    distance_miles = 3

    # Get Data ---------------------------------------------------------------------------------------------------------
    train_dict = nearby_data.transport_train(postcode, distance_miles)
    station_count = len(train_dict)
    nearest_station = list(train_dict)[0]
    nearest_station_dist = str(train_dict[nearest_station]) + " miles"

    destination_trip = googleMapsApi.directions_calc_train(nearest_station, "London")
    destination_line = list(destination_trip)[0]
    destination_length = destination_trip[destination_line]
    # ------------------------------------------------------------------------------------------------------------------

    # Creates a paragraph with the data in it
    pTitle = '<font size=12>Within a {0} mile radius, {1} is situated around {2} train stations, the closest being ' \
             '{3} at {4} away. {3} provides transport links straight into London, with the journey only taking {5} ' \
             'minutes via {6}.</font>'.format(distance_miles, site_name, station_count, nearest_station,
                                              nearest_station_dist, destination_length, destination_line)
    story.append(Paragraph(pTitle, styles["Normal"]))
    story.append(Spacer(1, 12))

    # Generates a table with the data inside it
    data = [['Station Name', 'Distance']]
    for item in train_dict:
        data.append([item, str(train_dict[item]) + " miles"])
    t = Table(data)
    t.setStyle(TableStyle([('BOX', (0, 0), (1, station_count), 2, colors.black),
                           ('INNERGRID', (0, 0), (-1 , -1), 0.25, colors.black),
                           ('BACKGROUND', (0, 0), (1, 0), colors.black),
                           ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
                           ('BACKGROUND', (0, 1), (1, 1), colors.lightgrey)]))
    story.append(t)


def create_title(title_text):
    styles.add(style.ParagraphStyle(name='Justify', alignment=enums.TA_JUSTIFY))
    pTitle = '<font size=15><b>%s</b></font>' % title_text
    story.append(Paragraph(pTitle, styles["Normal"]))
    story.append(Spacer(1, 6))
    d = flowables.HRFlowable(width="100%", thickness=1, lineCap='square', color=colors.black, dash=None)
    story.append(d)
    story.append(Spacer(1, 10))

create()