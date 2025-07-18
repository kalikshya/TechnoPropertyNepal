from operation import Operation
from read import ReadFile
from write import WriteFile


def main():
    try:
      #creating objects     
      read_from_file = ReadFile()
      operate = Operation()
      counter = 0
      while True:
          operate.display_intro(counter)
          counter = counter + 1
          choice = input("Enter your choice: ")
          operate.custom_strip(choice)
          if choice == '1':
              lands = read_from_file.load_lands("lands.txt")
              operate.display_lands(lands)
          elif choice == '2':
              lands = read_from_file.load_lands("lands.txt")
              kittas = list(map(int, input("Enter the kitta numbers of the lands to rent (separate by commas): ").split(',')))
              customer_name = input("Enter customer name: ")
              months = int(input("Enter the number of months to rent: "))
              total_rented = operate.rent_land(lands, kittas, customer_name, months)
              if total_rented > 0:
                  print(f"Total rental amount for all lands: Rs. {total_rented}")
              else:
                  print("No lands were rented.")
          elif choice == '3':
              kittas = list(map(int, input("Enter the kitta numbers of the lands to return (separate by commas): ").split(',')))
              customer_name = input("Enter customer name: ")
              lands = read_from_file.load_lands("lands.txt")
              operate.return_land(lands, kittas, customer_name)
          elif choice == '4':
              print("Thank you for using our program.")
              print("Exiting the program.")
              break
          else:
              print("Invalid choice. Please try again.")                              
    except Exception as e:
        print(f"An unexpected error occured: {e}") 

if __name__ == "__main__":
    main()