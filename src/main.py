from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import json

class EasyApplyLinkedIn:
    def __init__(self,data):
        
    ## Parameters
        self.email = data['email']
        self.password = data['password']
        self.keyword = data['keywords']
        self.location = data['location']
        edge_options = Options()
        service = Service(executable_path=data['driver_path'])
        self.driver = webdriver.Edge(service=service, options=edge_options)


        self.driver.get("https://www.linkedin.com")
        input("Press Enter to exit...")  
if __name__ == "__main__":
    with open("../config.json") as config_file:
        data = json.load(config_file)
    bot = EasyApplyLinkedIn(data)