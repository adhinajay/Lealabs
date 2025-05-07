import json

# Function to add a new contact
def add_contact(contact_book, name, phone, email):
    contact_book[name] = {'phone': phone, 'email': email}
    print("Contact for",name,"added successfully!")

# Function to display the contact book
def display_contacts(contact_book):
    if not contact_book:
        print("No contacts found.")
        return
    for name, details in contact_book.items():
        print(f"Name: {name}, Phone: {details['phone']}, Email: {details['email']}")

# Function to save the contact book to a file
def save_contacts(contact_book, filename='contacts.json'):
    with open(filename, 'w') as file:
        json.dump(contact_book, file, indent=4)
    print(f"Contacts saved to {filename}")

# Function to load the contact book from a file
def load_contacts(filename='contacts.json'):
    try:
        with open(filename, 'r') as file:
            contact_book = json.load(file)
        print("Contacts loaded successfully!")
        return contact_book
    except FileNotFoundError:
        print("No contact file found, starting with an empty contact book.")
        return {}

# Main program
def main():
    contact_book = load_contacts()  # Load contacts from file if it exists
    while True:
        print("\n1. Add Contact")
        print("2. Display Contacts")
        print("3. Save and Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter contact name: ")
            phone = input("Enter phone number: ")
            email = input("Enter email address: ")
            add_contact(contact_book, name, phone, email)

        elif choice == '2':
            display_contacts(contact_book)

        elif choice == '3':
            save_contacts(contact_book)  # Save contacts to file
            print("Exiting the program.")
            break

        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
