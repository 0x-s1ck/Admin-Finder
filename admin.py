import requests

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

def ensure_http(url):
    if not url.startswith(('http://', 'https://')):
        return 'http://' + url
    return url

url_choice = input("(1 Mass Scan, 2 Single Scan): ")

urls = []

if url_choice == '1':
    url_file = input("Mass URL (Input List) : ")
    try:
        with open(url_file, "r") as file:
            urls = [ensure_http(line.strip()) for line in file if line.strip()]
    except FileNotFoundError:
        print(f"File '{url_file}' tidak ditemukan.")
        exit(1)
elif url_choice == '2':
    single_url = input("Single URL : ")
    single_url = ensure_http(single_url)
    urls.append(single_url)
else:
    print("Pilihan tidak valid. Silakan pilih 1 atau 2.")
    exit(1)

output_file = input("Touch Me In : ")

path_file = input("Path List : ")

try:
    with open(path_file, "r") as file:
        paths = [line.strip() for line in file if line.strip()]
except FileNotFoundError:
    print(f"File '{path_file}' tidak ditemukan.")
    exit(1)

results = []
keywords = ["Login", "Admin", "Username", "Password", "Masuk", "Akun"]

print("Checking URLs...")
for base_url in urls:
    for path in paths:
        full_url = f"{base_url}/{path}".strip()
        try:
            headers = {
                'User -Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            response = requests.get(full_url, headers=headers)
            if response.ok:
                if any(keyword in response.text for keyword in keywords):
                    results.append(full_url)
                    print(f"{GREEN}200 OK{RESET} - {full_url}")
                else:
                    print(f"{RED}INVALID{RESET} - {full_url}")
            else:
                print(f"{RED}INVALID{RESET} - {full_url}")
        except requests.exceptions.RequestException:
            print(f"{RED}INVALID{RESET} - {full_url}")

if results:
    with open(output_file, "w") as file:
        for result in results:
            file.write(result + "\n")
    print("\nResult Saved :", output_file)
else:
    print("Mana ? Ga ada awkoawkoak")
