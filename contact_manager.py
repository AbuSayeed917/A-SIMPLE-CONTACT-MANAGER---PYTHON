# contact_manager.py

import json   # Module for handling JSON data
import os     # Module for interacting with the operating system
from typing import List, Optional  # For type hinting


# Define the path to the Contact Files
CONTACTS_FILE = 'contacts.json'


class Contact:
    """
    A class to represent a contact.
    """

    def __init__(self, name: str, phone: str, email: str):
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self) -> dict:
        """
        Convert the contact instance to a dictionary.
        """
        return {
            'name': self.name,
            'phone': self.phone,
            'email': self.email
        }

    @staticmethod
    def from_dict(data: dict):
        """
        Create a contact instance from a dictionary.
        """
        return Contact(name=data['name'], phone=data['phone'], email=data['email'])


class ContactManager:
    """
    A class to manage contacts.
    """

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.contacts: List[Contact] = []
        self.load_contacts()

    def load_contacts(self):
        """
        Load contacts from the file.
        """
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r') as file:
                    data = json.load(file)
                    self.contacts = [Contact.from_dict(item) for item in data]

                print(f"Loaded {len(self.contacts)} contacts.")
            except json.JSONDecodeError:
                print("Error: Invalid JSON file.")
        else:
            print("No existing contacts found. Starting fresh.")

    def save_contacts(self):
        """
        Save contacts to the JSON file.
        """
        try:
            with open(self.filepath, 'w') as file:
                json.dump([contact.to_dict() for contact in self.contacts], file, indent=4)
            print("Contacts saved successfully.")
        except IOError as e:
            print(f"Error saving contacts: {e}")

    def add_contact(self, contact: Contact):
        """
        Add a new contact to the list.
        """
        self.contacts.append(contact)
        print(f"Contact '{contact.name}' added.")

    def view_contacts(self):
        """
        Display all contacts.
        """
        if not self.contacts:
            print("No contacts found.")
            return
        print("\nContacts List")
        print("-" * 40)

        for idx, contact in enumerate(self.contacts, start=1):
            print(f"{idx}. Name: {contact.name}, Phone: {contact.phone}, Email: {contact.email}")

        print("-" * 40)

    def search_contact(self, name: str) -> Optional[Contact]:
        """
        Search for a contact by name.
        """
        for contact in self.contacts:
            if contact.name.lower() == name.lower():
                print(f"Contact '{name}' found.")
                return contact

        print(f"Contact '{name}' not found.")
        return None

    def delete_contact(self, name: str) -> bool:
        """
        Delete a contact by name.
        """
        contact = self.search_contact(name)
        if contact:
            self.contacts.remove(contact)
            print(f"Contact '{name}' deleted.")
            return True
        return False


def display_menu():
    """
    Display the main menu.
    """
    print("\nContact Manager")
    print("1. Add Contact")
    print("2. View Contacts")
    print("3. Search Contact")
    print("4. Delete Contact")
    print("5. Exit")


def get_user_choice() -> int:
    """
    Get the user's choice.
    """
    try:
        choice = int(input("Enter your choice (1-5): "))
        if choice in range(1, 6):
            return choice
        else:
            print("Invalid choice. Please choose a number between 1 and 5.")
            return get_user_choice()
    except ValueError:
        print("Invalid input. Please enter a number.")
        return get_user_choice()


def main():
    """
    Main function.
    """
    manager = ContactManager(CONTACTS_FILE)

    while True:
        display_menu()
        choice = get_user_choice()

        if choice == 1:
            name = input("Enter Name: ").strip()
            phone = input("Enter Phone Number: ").strip()
            email = input("Enter Email: ").strip()
            if name and phone and email:
                contact = Contact(name=name, phone=phone, email=email)
                manager.add_contact(contact)
                manager.save_contacts()
            else:
                print("Please enter all the details.")

        elif choice == 2:
            manager.view_contacts()

        elif choice == 3:
            name = input("Enter Name to Search: ").strip()
            if name:
                contact = manager.search_contact(name)
                if contact:
                    print(f"Name: {contact.name}, Phone: {contact.phone}, Email: {contact.email}")
            else:
                print("Please enter a name.")

        elif choice == 4:
            name = input("Enter Name to Delete: ").strip()
            if name:
                if manager.delete_contact(name):
                    manager.save_contacts()
            else:
                print("Name cannot be empty.")

        elif choice == 5:
            print("Exiting Contact Manager. Goodbye!")
            break


if __name__ == "__main__":
    main()
