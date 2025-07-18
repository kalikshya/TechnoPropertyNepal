import os
from operation import Operation
class ReadFile:
  def __init__(self):
    None 
  #loads the land details from the file
  def load_lands(self, filename):
    operate = Operation()
    #The below statement takes absolute file to work on any OS
    try:
      filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename) 
      lands = []
      with open(filename, 'r') as file:
          for line in file:
              if line == "\n" :
                continue
              try:
                parts = operate.custom_strip(line)
                parts = parts.split(',')
                lands.append({
                    "kitta": int(parts[0]),
                    "city": operate.custom_strip(parts[1]),
                    "direction": operate.custom_strip(parts[2]),
                    "anna": int(parts[3]),
                    "price": int(parts[4]),
                    "status": operate.custom_strip(parts[5]),
                    "month": int(parts[6]),
                    "rented_till": operate.custom_strip(parts[7]) if len(parts) > 7 else ""
                })
              except ValueError as e:
                        print(f"Error converting data types in the line: {line}. Error: {e}")
              except IndexError as e:
                        print(f"Missing data in the line: {line}. Error: {e}") 
    except FileNotFoundError:
            print(f"The file {filename} does not exist.")
            return []
    except PermissionError:
            print(f"Permission denied: Unable to access {filename}")
            return []
    except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []
    return lands