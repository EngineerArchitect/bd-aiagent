from functions.get_files_info import get_files_info

def get_files_info_tests():
    test_cases = [
        ("calculator", "."),
        ("calculator", "pkg"),
        ("calculator", "/bin"),
        ("calculator", "../")
    ]
    
    for i, (working_dir, directory) in enumerate(test_cases, 1):
        print(f"\nTest case {i}: get_files_info('{working_dir}', '{directory}')")
        print("-" * 60)
        result = get_files_info(working_dir, directory)
        print(result)
        print("-" * 60)

if __name__ == "__main__":
    get_files_info_tests()