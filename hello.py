import json
import sys

# Global variables (script-wide)
http_mode = "PUT"
package_service_base_url = ""
minio_base_url = ""
pipeline_state_success = False

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
        return ["http://host.docker.internal:5006/", "http://host.docker.internal:9000/"]
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
    has_curl_succeeded = False

    try:
        print("ASDF")
        has_curl_succeeded = True
    except Exception:
        print(f"Sending curl command failed: {Exception}")
    
    return has_curl_succeeded


def download_package_file(minio_base_url, PackageContentS3Key):
    try:
        print(f"Downloading {PackageContentS3Key}...\n")
        print("Downloading finished successfully.\n")
    except Exception:        
        print(f"Download failed: {Exception} ")
        sys.exit(1)


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

    match PackageContentS3Key:
        case str() if PackageContentS3Key:
            # Checks if it's a non-empty string, download file and append to curl command form data object
            download_package_file(minio_base_url, PackageContentS3Key)
            curl_command = build_form_data(parsed_data, package_service_base_url, http_mode, PackageContentS3Key)
        case _:
            # Default case (None or empty string)
            curl_command = build_form_data(parsed_data, package_service_base_url, http_mode)     

    print(f"Finalized curl command: {curl_command}\n")
    print("Sending curl command ...")
    response = sending_curl_command(curl_command)
    print(response)

    if response:
        print("Script completed successfully")
        sys.exit(0)  # Exit with success

    sys.exit(1)  # Exit with success
    

if __name__ == "__main__":
    PackageMetadata = sys.argv[1]
    PackageContentS3Key = sys.argv[2]
    Email = sys.argv[3]
    BaseUrl = sys.argv[4]
    
    #json_string = json.dumps(parsed_data)
    main(PackageMetadata, PackageContentS3Key, Email, BaseUrl)

