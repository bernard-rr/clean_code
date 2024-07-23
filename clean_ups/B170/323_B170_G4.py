import json
import os


class SnippetManager:
    def __init__(self, data_file="snippets.json"):
        self.data_file = data_file
        self.load_data()

    def load_data(self):
        try:
            with open(self.data_file, "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {}

    def save_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.data, f, indent=4)

    def add_snippet(self, title, code, category):
        if title not in self.data:
            self.data[title] = {"code": code, "category": category}
            self.save_data()
            print("Snippet added successfully!")
        else:
            print("Snippet with this title already exists.")

    def categorize_snippet(self, title, category):
        if title in self.data:
            self.data[title]["category"] = category
            self.save_data()
            print("Snippet category updated!")
        else:
            print("Snippet not found.")

    def search_snippets(self, query):
        resultCount = 0
        print("Search results:")
        for title, snippet in self.data.items():
            if (
                query.lower() in title.lower()
                or query.lower() in snippet["code"].lower()
            ):
                resultCount += 1
                print(f"Snippet {resultCount}:")
                print(
                    f"- **{title}** ({snippet.get('category', 'Uncategorized')})\n{snippet['code']}\n"
                )
        if resultCount == 0:
            print("No snippets found matching your query.")
        else:
            print(f"Found {resultCount} Results")

    def show_all_snippets(self):
        if self.data:
            for title, snippet in self.data.items():
                print(
                    f"- **{title}** ({snippet.get('category', 'Uncategorized')})\n{snippet['code']}\n"
                )
        else:
            print("No snippets saved yet.")


def main():
    manager = SnippetManager()

    while True:
        print("\nChoose an action:")
        print("1. Add snippet")
        print("2. Categorize snippet")
        print("3. Search snippets")
        print("4. Show all snippets")
        print("5. Exit")

        choice = input("> ")

        if choice == "1":
            title = input("Title: ")

            print("Enter your code snippet. End with triple backticks (```)")
            code_lines = ["```"]
            while True:
                line = input()
                if line.strip() == "```":
                    break
                code_lines.append(line)

            code = "\n".join(code_lines)

            category = input("Category (optional): ")
            manager.add_snippet(title, code, category)
        elif choice == "2":
            title = input("Title of snippet to categorize: ")
            category = input("New category: ")
            manager.categorize_snippet(title, category)
        elif choice == "3":
            query = input("Search query: ")
            manager.search_snippets(query)
        elif choice == "4":
            manager.show_all_snippets()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
