import json
import sys

# Build form data object
def flatten_json(obj, prefix=''):
    """Recursively flattens nested JSON into key-value pairs using dot notation and bracket indices."""
    flattened = {}

    match obj:
        case dict():
            for key, value in obj.items():
                new_prefix = f"{prefix}.{key}" if prefix else key
                flattened.update(flatten_json(value, new_prefix))
        case list():
            for index, value in enumerate(obj):
                new_prefix = f"{prefix}[{index}]"  # Use bracket notation for indices
                flattened.update(flatten_json(value, new_prefix))
        case _:  # Default case (base values like int, str, bool)
            flattened[prefix] = obj

    return flattened

# Check BaseUrl
def get_base_package_service_url(base_url):
    if "localhost" in base_url:
        return ["http://localhost:5006/", "http://host.docker.internal:9000/"]
    return [base_url]

def build_form_data(parsed_data, package_service_base_url):
    print("Building form data object")
    # Flatten JSON
    flattened_data = flatten_json(parsed_data)

    # Generate the curl command using --form
    curl_command = 'curl -X POST "https://example.com/api" \\\n'
    for key, value in flattened_data.items():
        curl_command += f'  --form "{key}={value}" \\\n'

    # Remove trailing backslash and newline
    curl_command = curl_command.rstrip(" \\\n")

    return curl_command

def download_package_file(PackageContentS3Key):
    is_package_downloaded = False
    try:
        print("Downloading ...")
        is_package_downloaded = True
    except Exception:        
        print(f"Download failed: {Exception} ")

    return is_package_downloaded


def main(PackageMetadata, PackageContentS3Key, Email, BaseUrl):
    print(f"Start building ...")
    
    base_urls = get_base_package_service_url(BaseUrl)
    package_service_base_url = base_urls[0]
    minio_base_url = base_urls[1]
    print(base_urls)
    
    # Parse JSON
    try:
        parsed_data = json.loads(PackageMetadata)
    except json.JSONDecodeError:
        print("Invalid JSON input")
        sys.exit(1)

    if PackageContentS3Key:
        is_file_downloaded = download_package_file(PackageContentS3Key)
    
    curl_command = build_form_data(parsed_data, package_service_base_url)    

    print(f"{curl_command}")




if __name__ == "__main__":
    PackageMetadata = sys.argv[1]
    PackageContentS3Key = sys.argv[2]
    Email = sys.argv[3]
    BaseUrl = sys.argv[4]
    
    #json_string = json.dumps(parsed_data)
    main(PackageMetadata, PackageContentS3Key, Email, BaseUrl)

