def search_log_file(file_path, keyword):
    try:
        with open(file_path, 'r') as file:
            matches = (line.strip() for line in file if keyword in line)

            count = 0
            while True:
                page = []
                try:
                    for _ in range(10):
                        page.append(next(matches))
                        count += 1
                except StopIteration:
                    if page:
                        print("\n".join(page))
                        print(f"\nEnd of results. Total matches found: {count}")
                    else:
                        print("No more results.")
                    break

               
                print("\n".join(page))

          
                user_input = input("\nShow next 10 results? (y/n): ").strip().lower()
                if user_input != 'y':
                    print(f"Stopped. Total matches shown: {count}")
                    break

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    log_path = input("Enter the path to the log file: ").strip()
    search_keyword = input("Enter the keyword to search for: ").strip()
    search_log_file(log_path, search_keyword)