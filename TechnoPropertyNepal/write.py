import os
class WriteFile:
  def __init__(self):
      None  
  #Goes to the file and writes to it
  def save_lands(self,filename, lands):
    filename =os.path.join(os.path.dirname(os.path.abspath(__file__)), filename) 
    try:
        with open(filename, 'w') as file:
            for land in lands:
                try:
                    file.write(f'{land["kitta"]}, {land["city"]}, {land["direction"]}, {land["anna"]}, {land["price"]}, {land["status"]}, {land["month"]}, {self.remove_nextline(land["rented_till"])},\n')
                except KeyError as e:
                        print(f"Missing key in land data: {e}")
                except TypeError as e:
                        print(f"Type error with the data of land: {e}")
    except FileNotFoundError:
            print(f"The file path {filename} could not be found.")
    except PermissionError:
            print(f"Permission denied: Unable to write to {filename}.")
    except OSError as e:
            print(f"OS error occurred: {e}")
    except Exception as e:
            print(f"An unexpected error occurred while writing to the file: {e}")
            
  #Removes next line character
  def remove_nextline(self, string_to_remove):
     new_text = ''  # Initialize an empty string to store the result
     for char in string_to_remove:
        if char != '\n':  # Check if the character is not a newline
            new_text += char  # Add it to the new string if it's not a newline
     return new_text