import csv
import os
import uuid

class LibraryLostFoundSystem:
    def __init__(self, items_file="lost_items.csv", scores_file="user_scores.csv"):
        self.items_file = items_file
        self.scores_file = scores_file
        self.ensure_file_exists(self.items_file, ["status", "name", "location", "description", "reporter", "finder", "value", "unique_id"])
        self.ensure_file_exists(self.scores_file, ["username", "score"])

    def ensure_file_exists(self, file_name, headers):
        if not os.path.exists(file_name):
            with open(file_name, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)

    def read_csv(self, file_name):
        try:
            with open(file_name, mode='r', encoding='utf-8') as file:
                return list(csv.DictReader(file))
        except FileNotFoundError:
            print(f"Error: File {file_name} not found.")
            return []
        except Exception as e:
            print(f"Unknown error occurred while reading the file {file_name}: {e}")
            return []

    def write_csv(self, file_name, data, headers):
        try:
            with open(file_name, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)
        except Exception as e:
            print(f"Error occurred while writing to file {file_name}: {e}")

    def report_item(self, name, location, description, reporter, value):
        item = Item(name, location, description, reporter, value)
        data = self.read_csv(self.items_file)
        data.append(item.__dict__)
        self.write_csv(self.items_file, data, ["status", "name", "location", "description", "reporter", "finder", "value", "unique_id"])

    def find_item(self, unique_id, finder):
        data = self.read_csv(self.items_file)
        for item in data:
            if item["unique_id"] == unique_id and item["status"] == "Lost":
                item["status"] = "Found"
                item["finder"] = finder
                break
        self.write_csv(self.items_file, data, ["status", "name", "location", "description", "reporter", "finder", "value", "unique_id"])

    def remove_item(self, unique_id):
        data = self.read_csv(self.items_file)
        new_data = [item for item in data if item["unique_id"] != unique_id]
        if len(new_data) < len(data):
            self.write_csv(self.items_file, new_data, ["status", "name", "location", "description", "reporter", "finder", "value", "unique_id"])
            print("Item successfully removed.")
        else:
            print("Item not found.")

    def display_items(self):
        data = self.read_csv(self.items_file)
        print("Unreturned Items:")
        for item in data:
            if item["status"] != "Returned":
                print(f"Name: {item['name']}, Location: {item['location']}, Status: {item['status']}")

    def update_user_score(self, username, points):
        scores = self.read_csv(self.scores_file)
        found = False
        for user in scores:
            if user["username"] == username:
                try:
                    user["score"] = str(int(user["score"]) + points)
                except ValueError:
                    user["score"] = str(points)
                found = True
                break
        if not found:
            scores.append({"username": username, "score": str(points)})
        self.write_csv(self.scores_file, scores, ["username", "score"])
        print(f"User '{username}' score updated by {points} points.")

    def scoreboard(self):
        scores = self.read_csv(self.scores_file)
        sorted_scores = sorted(scores, key=lambda x: int(x["score"]), reverse=True)
        print("\nUser Scoreboard:")
        for user in sorted_scores:
            print(f"{user['username']}: {user['score']} points")

class Item:
    def __init__(self, name, location, description, reporter, value):
        self.status = "Lost"
        self.name = name
        self.location = location
        self.description = description
        self.reporter = reporter
        self.finder = ""
        self.value = value
        self.unique_id = str(uuid.uuid4())

def main():
    system = LibraryLostFoundSystem("lost_items.csv", "user_scores.csv")
    while True:
        print("\nWelcome to the CampusLibrary Lost & Found System!")
        print("1. Report a lost item")
        print("2. Report a found item")
        print("3. View unreturned items")
        print("4. View user scoreboard")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")
        if choice == "1":
            try:
                name = input("Enter item name: ")
                location = input("Enter item location: ")
                description = input("Enter item description: ")
                reporter = input("Enter your name: ")
                value = input("Enter estimated value: ")
                system.report_item(name, location, description, reporter, value)
            except Exception as e:
                print(f"Error reporting lost item: {e}")
        elif choice == "2":
            try:
                unique_id = input("Enter item unique ID: ")
                finder = input("Enter your name: ")
                system.find_item(unique_id, finder)
            except Exception as e:
                print(f"Error reporting found item: {e}")
        elif choice == "3":
            try:
                system.display_items()
            except Exception as e:
                print(f"Error displaying items: {e}")
        elif choice == "4":
            try:
                system.scoreboard()
            except Exception as e:
                print(f"Error displaying scoreboard: {e}")
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()

