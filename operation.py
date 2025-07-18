import datetime
from write import WriteFile

class Operation:
  def __init__(self):
    global write_to_file
    write_to_file = WriteFile()

  #Displayes the intro text
  def display_intro(self, counter):
    if counter > 0:
        print("\nPlease choose one of the operations below:")
    else:
     print("\nWelcome to TechnoPropertyNepal Land Management System")
    print("-----------------------------------------------------")
    print("1. Display Available Lands")
    print("2. Rent Land")
    print("3. Return Land")
    print("4. Exit")
  
  #Helper method to add month in Datetime
  def add_months(self, original_date, months):
    # Calculate new month and year
    new_month = original_date.month + months
    new_year = original_date.year + (new_month - 1) // 12
    new_month = new_month % 12 or 12  # Correct the month to wrap properly

    # Handle December case
    if new_month == 12:
        new_year -= 1
    
    # Calculate day
    new_day = original_date.day
    # Create the initial new date (might be adjusted if days don't fit in the month)
    while True:
        try:
            return datetime.datetime(new_year, new_month, new_day)
        except ValueError:
            # This happens if new_day is not in the new month, reduce day by one and retry
            new_day -= 1
  #created a custom strip that trims the input
  def custom_strip(self, string_to_strip):
    start = None
    end = None
    
    # Find the first non-space character from the start
    for i in range(len(string_to_strip)):
        if string_to_strip[i] != ' ':
            start = i
            break
    
    # Find the first non-space character from the end
    for j in range(len(string_to_strip) - 1, -1, -1):
        if string_to_strip[j] != ' ':
            end = j
            break
    
    # If no non-space character found, return an empty string
    if start is None or end is None:
        return ""
    
    # Manually construct the new string without leading and trailing spaces
    stripped_string = ''
    for k in range(start, end + 1):
        stripped_string += string_to_strip[k]
    
    return stripped_string
 
 #Display the land
  def display_lands(self,lands):
    print("\nList of Lands:")
    counter = 0
    for land in lands:
        if land['status'] == 'Available':
            counter = counter + 1
            print(f"Kitta: {land['kitta']}, Location: {land['city']} {land['direction']}, {land['anna']} anna, Price: Rs.{land['price']}/month, Status: {land['status']}")
    if counter == 0:
      print("Sorry no land is available")
 #Find the land
  def find_land(self,lands, kitta):
    for land in lands:
        if land['kitta'] == kitta:
            return land
    return None
  #Rent the land
  def rent_land(self,lands, kittas, customer_name, months):
        total_amount = 0
        expiry_date = self.add_months(datetime.datetime.now().date(),months)
        rented_lands = []
        
        for kitta in kittas:
            land = self.find_land(lands, kitta)
            if land:
                if land['status'] == 'Available':
                    land['status'] = 'Not Available'
                    land['rented_till'] = expiry_date.strftime("%Y-%m-%d")
                    land['month'] = months
                    rent_amount = months * land['price']
                    total_amount += rent_amount
                    rented_lands.append(land)
                else:
                    print(f"Land with kitta {kitta} is currently not available for rent.")
            else:
                print(f"No land found with kitta number {kitta}.")

        if rented_lands:
            self.generate_invoice("rent", rented_lands, customer_name, months, total_amount)
            write_to_file.save_lands("lands.txt", lands)
        return total_amount


  # Return the land
  def return_land(self, lands, kittas, customer_name):
    today = datetime.datetime.now().date()
    total_amount = 0
    returned_lands = []
    late_fees = 0
    late_months = 0
    for kitta in kittas:
        land = self.find_land(lands, kitta)
        if land:
            if land['status'] == 'Not Available':
                rented_till = datetime.datetime.strptime(land['rented_till'], "%Y-%m-%d").date()
                duration = land["month"]          
                late_fee = 0
                late_month = 0
                if today > rented_till:
                    late_month = ((today - rented_till).days // 30) + 1
                    late_fee = late_month * land['price'] * 0.1  # Assume 10% monthly rate
                total_amount += duration * land['price']
                late_months += late_month
                late_fees += late_fee
                returned_lands.append(land)
                land['status'] = 'Available'
                land['month']= 0
                land['rented_till'] = ""
            else:
                print(f"Land with kitta {kitta} is currently not rented out.")
        else:
            print(f"No land found with kitta number {kitta}.")

    if returned_lands:
        self.generate_invoice("return", returned_lands, customer_name, duration, total_amount, late_fees, late_months)
        write_to_file.save_lands("lands.txt", lands)


#Get the user input
  def get_user_input(self,prompt, input_type=int):
    while True:
        try:
            return input_type(input(prompt))
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")

        print("Land is already available or does not exist.")

#Generate the invoice for transaction
  def generate_invoice(self,transaction_type, lands, customer_name, duration, total_amount, late_fee=0, late_month =0):
    timestamp = datetime.datetime.now()
    file_name = f"{transaction_type}_{timestamp.strftime('%Y%m%d_%H%M%S')}.txt"
    with open(file_name, "w") as file:
        file.write(f"TechnoPropertyNepal - {transaction_type.capitalize()} Invoice\n")
        file.write("-------------------------------------------------\n")
        file.write(f"Date: {timestamp.strftime('%Y-%m-%d')}\n")
        file.write(f"Time: {timestamp.strftime('%H:%M:%S')}\n")
        file.write(f"Customer Name: {customer_name}\n")  
        for land in lands:
            file.write(f"\nKitta Number: {land['kitta']}\nLocation: {land['city']}\nDirection: {land['direction']}\nArea: {land['anna']} anna\nDuration: {duration} months\nPrice: Rs. {land['price']}/ month\n\n")
        if late_fee > 0:
            file.write(f"Late Duration: {late_month}\n")
            file.write(f"Total Late Fee: Rs. {late_fee}\n")
            file.write(f"Late Duration is fined 10% per month\n")
        file.write("-------------------------------------------------\n")
        file.write(f"Total Amount: Rs. {total_amount + late_fee}\n")
        file.write("\nThank you for using TechnoPropertyNepal!\n")
    print(f"Invoice generated: {file_name}")
