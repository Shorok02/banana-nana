def background_process_file_upload(data: bytes, filename: str, user_id: str, max_retries: int = 3):
    from services.files import process_file_upload_sync
    import time

    attempt = 0
    last_exception = None

    while attempt < max_retries:
        try:
            process_file_upload_sync(data, filename, user_id)
            return  
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for file '{filename}': {e}")
            attempt += 1
            last_exception = e
            time.sleep(2 ** attempt)

    raise last_exception
