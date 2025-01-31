import json
import sys
import subprocess

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
        case _:  
            flattened[prefix] = obj

    return flattened

# Check BaseUrl
def get_base_urls(base_url):
    if "localhost" in base_url:
        return ["http://host.docker.internal:5006", "http://host.docker.internal:9000"]
    return [base_url]

def build_form_data(parsed_data, url, http_method=None, file_path=None):
    print("Building form data object ...")
    
    # Flatten JSON
    flattened_data = flatten_json(parsed_data)
    try:
        # Generate the curl command using --form
        curl_command = f'curl -X "{http_method}" "{url}" \\\n'
        for key, value in flattened_data.items():
            curl_command += f'  --form "{key}={value}" \\\n'

        if file_path:
            curl_command += f'  --form "file=@/tmp/{file_path}" \\\n'

        # Remove trailing backslash and newline
        curl_command = curl_command.rstrip(" \\\n")
        print("Building curl command completed.\n")
        
    except Exception:
        print(f"Something went wrong on building curl command: {Exception}")
        sys.exit(1)

    return curl_command

def sending_curl_command(curl_command):
    try:
        # Execute the curl command
        result = subprocess.run(
            ["curl", "-X", "GET", "https://api64.ipify.org?format=json"],
            capture_output=True,
            text=True,
            check=True
        )

    except subprocess.CalledProcessError as e:
        print(f"Error executing curl: {e}")
    
    return result



def download_package_file(minio_base_url, PackageContentS3Key):
    try:
        print(f"Downloading {PackageContentS3Key}...\n")
        print("Downloading finished successfully.\n")
    except Exception:        
        print(f"Download failed: {Exception} ")
        sys.exit(1)

def build_package_service_endpoint_url(base_url, id=None):
    if id is None:
        build_destination_url = f"{base_url}/SFU/Package/FromJenkins"

    build_destination_url = f"{base_url}/SFU/Package/{id}/FromJenkins"

    return build_destination_url


def main(PackageMetadata, PackageContentS3Key, Email, BaseUrl):
    print(f"Start building ...")
    
    base_urls = get_base_urls(BaseUrl)
    package_service_base_url = base_urls[0]
    minio_base_url = base_urls[1]
    print(base_urls)
    
    # Parse JSON
    try:
        parsed_data = json.loads(PackageMetadata)
    except json.JSONDecodeError:
        print("Invalid JSON input")
        sys.exit(1)    
    
    # Check http_method POST/PUR
    package_id = parsed_data.get("ID")
    if package_id is None:
        print("Warning: 'ID' is missing or null in the JSON data.\n")
        destination_url = build_package_service_endpoint_url(package_service_base_url)
        http_mode = "POST"
    else:
        print(f"Package ID: {package_id}\n")
        destination_url = build_package_service_endpoint_url(package_service_base_url, package_id)
        http_mode = "PUT"

    match PackageContentS3Key:
        case str() if PackageContentS3Key:
            # Checks if it's a non-empty string, download file and append to curl command form data object
            download_package_file(minio_base_url, PackageContentS3Key)
            curl_command = build_form_data(parsed_data, destination_url, http_mode, PackageContentS3Key)
        case _:
            # Default case (None or empty string)
            curl_command = build_form_data(parsed_data, destination_url, http_mode)     

    print(f"Sending curl command: {curl_command} ...\n")
    response = sending_curl_command(curl_command)

    if response.returncode == 0:  # Check if curl was successful
        print("Script completed successfully\n")
        print(f"Response: {response.stdout}")
        sys.exit(0)  # Exit with success
        
    print("Curl command failed!\n")
    print(f"Error: {response.stderr}")
    sys.exit(1)  # Exit with failure
    

if __name__ == "__main__":
    PackageMetadata = sys.argv[1]
    PackageContentS3Key = sys.argv[2]
    Email = sys.argv[3]
    BaseUrl = sys.argv[4]
    
    #json_string = json.dumps(parsed_data)
    main(PackageMetadata, PackageContentS3Key, Email, BaseUrl)

