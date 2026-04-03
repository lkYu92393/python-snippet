import requests

def save_response_content(target_url, destination):
    """
    for example,
    url is "https://raw.githubusercontent.com/lkYu92393/python-snippet/refs/heads/main/file/download_example.py"
    destination will be file path, like "./download_example.py"
    """
    response = requests.get(target_url, stream=True)

    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)

