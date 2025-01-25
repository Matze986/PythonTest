import sys
import json

def main(package_metadata):
    print(f"Received package metadata: {package_metadata}")
    
    # Parse the JSON string into a Python dictionary
    metadata = json.loads(package_metadata)
    print("Parsed metadata:")

    # Iterate through the keys and values in the dictionary
    for key, value in metadata.items():
        print(f"Key: {key}, Value: {value}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        package_metadata = sys.argv[1]
        main(package_metadata)
    else:
        print("No package metadata provided.")
