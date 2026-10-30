from functions.get_files_info import get_files_info

def run_test(label, directory):
    print(f"Results for {label}:")
    result = get_files_info("calculator", directory)
    prefix = " " if result.startswith("Error:") else " "
    for line in result.split("\n"):
        print(f"{prefix}{line}")
    print()

def main():
    print(get_files_info("calculator", "."))
    print(get_files_info("calculator", "pkg"))
    print(get_files_info("calculator", "/bin"))
    print(get_files_info("calculator", "../"))

if __name__ == "__main__":
    main()
