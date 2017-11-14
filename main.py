from appJar import gui

import pdfBuilder
from nearby import nearby_data
from web import web_visit

app = gui("Property Reporter", "500x400")
app.setBg("white")

app.addLabel("title", "Welcome to Property Reporter")

client_name = "Client   : "
property_name = "Property : "
postcode_name = "Postcode : "

app.addLabelEntry(client_name)
app.addLabelEntry(property_name)
app.addLabelEntry(postcode_name)


def press(button):
    if button == "Submit":
        report_client = app.getEntry(client_name)
        property_address = app.getEntry(property_name)
        post_code = app.getEntry(postcode_name)

        print(client_name, report_client, property_name, property_address, postcode_name, post_code)
        school_locations = nearby_data.schools(post_code)
        transport_locations = nearby_data.transport(post_code)
        shop_locations = nearby_data.shops(post_code)
        # web_visit.soup_setup()


app.addButtons(["Submit"], press)
app.setFocus(postcode_name)


pdfBuilder.create()

app.go()