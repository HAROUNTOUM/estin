import hashlib

def calculate_file_hash(file_obj):
    sha256_hash = hashlib.sha256()
    # Read in 4KB chunks to protect server RAM
    for chunk in file_obj.chunks():
        sha256_hash.update(chunk)
    return sha256_hash.hexdigest()
