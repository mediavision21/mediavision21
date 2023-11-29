
class Model:
    def __init__(self, country, package_name, price):
        self.id = self.generate_id(country, package_name)
        self.country = ""
        self.package_name = ""
        self.price = ""
        #self.campaign = ""
        #self.information = ""

    def get_val(self):
        return str(self.package_name)+ str(self.price)

    def generate_id(self, package_name, country):
        return str(package_name) + str(country)
