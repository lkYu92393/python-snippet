import requests

def save_response_content(target_url, destination):
    session = requests.Session()
    response = session.get(target_url, stream=True)

    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                
    save_response_content(response, destination)

