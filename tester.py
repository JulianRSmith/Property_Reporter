import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, flowables, Table, TableStyle
from reportlab.lib import colors, styles as style, enums

from nearby import nearby_data, googleMapsApi
from web import  web_data

# Global variables
styles = style.getSampleStyleSheet()
styles.add(style.ParagraphStyle(name='Center', alignment=enums.TA_CENTER))
styles.add(style.ParagraphStyle(name='Justify', alignment=enums.TA_JUSTIFY))
story = []

margin = 100
file_name = "test_pdf"
client_name = "Mr John Doe"
client_address = "10 Client Street, London, SW1X 5AH"
client_email = "client@clientproperty.co.uk"
client_phone = "12345678910"
site_name = "221 Example House"
postcode = "HP6 6SW"
# HA4 8NN
site_address = site_name + ", London , " + postcode

# ------------------------------------------------ Date suffix adders --------------------------------------------------
def suffix(d):
    return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')


def custom_date(date_text, current_date):
    return current_date.strftime(date_text).replace('{S}', str(current_date.day) + suffix(current_date.day))
# ----------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------- Create the PDF ----------------------------------------------------
def create():
    doc = SimpleDocTemplate("%s.pdf" % file_name, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)

    create_front_page()
    create_transport_data()
    doc.build(story)
# ----------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------- Create the front page -------------------------------------------------
def create_front_page():
    # Company Title
    title_text = "<font size=25>New Homes Pricing Report</font>"
    story.append(Paragraph(title_text, styles["Center"]))
    story.append(Spacer(1, 50))

    # Client Information
    today_date = custom_date("%A {S} %B %Y", datetime.datetime.now())
    title_client_text("Date:", today_date)
    title_client_text("For:", client_name)
    title_client_text("Address:", client_address)
    title_client_text("E-Mail:", client_email)
    title_client_text("Phone:", client_phone)

    story.append(Spacer(1, 100))

    # Site Address
    site_address_split = site_address.split(", ")
    for item in site_address_split:
        p_text = "<font size=15>{0}</font>".format(item)
        story.append(Paragraph(p_text, styles["Center"]))
        story.append(Spacer(1, 5))

    story.append(Spacer(1, 100))

    story.append(PageBreak())
# ----------------------------------------------------------------------------------------------------------------------


def create_transport_data():
    create_title("Local Transport")

    distance_miles = 3

    # Train Stations ---------------------------------------------------------------------------------------------------
    train_list = nearby_data.transport_train(postcode, distance_miles)
    station_count = len(train_list)
    nearest_station = train_list[0]
    nearest_station_name = nearest_station[0]
    nearest_station_dist = str(nearest_station[1]) + " miles"

    destination_trip = googleMapsApi.directions_calc_train(nearest_station_name, "London")
    destination_line = list(destination_trip)[0]
    destination_length = destination_trip[destination_line]

    wiki_info = web_data.station_information(nearest_station_name)

    # Creates a paragraph with the data in it
    p_text = '<font size=12>Within a {0} mile radius, {1} is situated around {2} train stations, the closest being ' \
             '{3} at {4} away. {5} {3} also provides transport links straight into London, with the journey only ' \
             'taking {6} minutes via {7}.</font>'.format(distance_miles, site_name, station_count, nearest_station_name,
                                                         nearest_station_dist, wiki_info,  destination_length,
                                                         destination_line)
    story.append(Paragraph(p_text, styles["Justify"]))
    story.append(Spacer(1, 12))

    # Generates a table with the data inside it
    data = [['Station Name', 'Distance']]
    for item in train_list:
        data.append([item[0], str(item[1]) + " miles"])
    t = Table(data)
    t.setStyle(TableStyle([('BOX', (0, 0), (1, station_count), 1, colors.black),
                           ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                           ('BACKGROUND', (0, 0), (1, 0), colors.black),
                           ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
                           ('BACKGROUND', (0, 1), (1, 1), colors.lightgrey)]))
    story.append(t)
    story.append(Spacer(1, 12))
    # ------------------------------------------------------------------------------------------------------------------

    # Airports ---------------------------------------------------------------------------------------------------------
    distance_miles_airport = 60
    airport_list = nearby_data.transport_airport(postcode, distance_miles_airport)
    airport_count = len(airport_list)
    nearest_airport = airport_list[0]
    nearest_airport_name = nearest_airport[0]
    nearest_airport_dist = str(nearest_airport[1]) + " miles"

    p_text = "<font size=12>Within a {0} mile radius, {1} is situated around {2} airports, the closest being {3} at " \
             "{4} away.</font>".format(distance_miles_airport, site_name, airport_count, nearest_airport_name,
                                       nearest_airport_dist)
    story.append(Paragraph(p_text, styles["Justify"]))
    story.append(Spacer(1, 12))
    # ------------------------------------------------------------------------------------------------------------------


def create_title(title_text):
    p_text = '<font size=15><b>%s</b></font>' % title_text
    story.append(Paragraph(p_text, styles["Normal"]))
    story.append(Spacer(1, 6))
    d = flowables.HRFlowable(width="100%", thickness=1, lineCap='square', color=colors.black, dash=None)
    story.append(d)
    story.append(Spacer(1, 10))


def title_client_text(name, item):
    p_text = "<font size=12><b>{0}</b> <i>{1}</i></font>".format(name, item)
    story.append(Paragraph(p_text, styles["Normal"]))
    story.append(Spacer(1, 2))


create()
