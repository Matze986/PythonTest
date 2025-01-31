import json
import sys


http_mode = "PUT"
package_service_base_url = ""
minio_base_url = ""
s3_bucket_name = ""

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
            curl_command += f'  --form "file=@{file_path}" \\\n'

        # Remove trailing backslash and newline
        curl_command = curl_command.rstrip(" \\\n")
        print("Building form data object completed.\n")
        
    except Exception:
        print(f"Something went wrong on building formData object: {Exception}")

    return curl_command

def download_package_file(PackageContentS3Key):
    is_package_downloaded = False
    try:
        print("Downloading ...\n")
        is_package_downloaded = True
        print("Downloading finished successfully.\n")
    except Exception:        
        print(f"Download failed: {Exception} ")

    return is_package_downloaded


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

    if PackageContentS3Key:
        is_file_downloaded = download_package_file(PackageContentS3Key)

    curl_command = build_form_data(parsed_data, package_service_base_url, http_mode)    

    print(f"{curl_command}")




if __name__ == "__main__":
    PackageMetadata = sys.argv[1]
    PackageContentS3Key = sys.argv[2]
    Email = sys.argv[3]
    BaseUrl = sys.argv[4]
    
    #json_string = json.dumps(parsed_data)
    main(PackageMetadata, PackageContentS3Key, Email, BaseUrl)

