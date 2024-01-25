from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Excel.Files import Files
from RPA.PDF import PDF
from RPA.Tables import Tables
from PIL import Image


@task
def order_robots_from_RobotSpareBin():
    """Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images."""
    browser.configure()
    open_robot_order_website()
    give_up_rights()
   # download_robot_orders_file()
    read_into_table()
    get_orders()
    



def open_robot_order_website():
    """Opens the Robot Order Website"""
    browser.goto("https://robotsparebinindustries.com/#/robot-order")

def give_up_rights():
    page = browser.page()
    page.click("button:text('I guess so')")

def download_robot_orders_file():
    """downloads the csv file"""
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/orders.csv", overwrite=True)

def read_into_table():
    csv = Tables()
    orders = csv.read_table_from_csv("orders.csv", columns=["Order number", "Head", "Body", "Legs", "Address"], header=True)
    
    for row in orders:
        get_orders(row)

def get_orders(robot):
    page = browser.page()

    for i in robot["Order number"]:
        page.select_option("#head", str(robot["Head"]))
        page.click("#id-body-"+str(robot["Legs"]))
        page.fill("input[placeholder='Enter the part number for the legs']", robot["Legs"])
        page.fill("#address", robot["Address"])
        page.click("button:text('Preview')")
        page.click("button:text('ORDER')")

        while page.locator("//div[@class='alert alert-danger']").is_visible():
            page.click("#order")

            if not page.locator("//div[@class='alert alert-danger']").is_visible():
                break

        order_receipt = page.locator("#receipt").inner_html()
        pdf = PDF()
        pdf.html_to_pdf(order_receipt, "output/order_number_"+str(robot["Order number"])+"_receipt.pdf")
        page.screenshot(path="output/ordered_robot_number_"+str(robot["Order number"])+".png")
        page.click("button:text('Order another robot')")
        give_up_rights()

