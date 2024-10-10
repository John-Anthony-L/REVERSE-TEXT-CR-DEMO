from flask import Flask, request, jsonify
from google.cloud import storage

app = Flask(__name__)

# Replace with your bucket names
UPLOAD_BUCKET_NAME = "upload-text-bucket"
REVERSED_BUCKET_NAME = "reversed-text-sourcbucket"

# Initialize Cloud Storage client
storage_client = storage.Client()

@app.route('/upload', methods=['POST'])
def upload_and_reverse():
    file = request.files['file']
    file_name = file.filename

    # Upload to upload-bucket
    bucket = storage_client.bucket(UPLOAD_BUCKET_NAME)
    blob = bucket.blob(file_name)
    blob.upload_from_string(file.read())

    # Reverse text
    with blob.open('r') as f:
        text = f.read()
    reversed_text = text[::-1]

    # Upload to reversed-bucket
    reversed_blob = bucket.blob(f"reversed_{file_name}")
    reversed_blob.upload_from_string(reversed_text)

    # Generate pre-signed URL
    download_url = reversed_blob.generate_signed_url(
        version='v4',
        expiration=3600,  # URL valid for 1 hour
        method='GET'
    )

    return jsonify({'download_url': download_url})

if __name__ == '__main__':
    app.run(debug=True)
