from flask import Flask, render_template, request
import os
from PIL import Image, ExifTags
import pikepdf

app = Flask(__name__)

video_extensions = ['.mp4', '.mov', '.avi', '.wmv', '.flv', '.mkv', '.webm']
allowed_extensions = ['.jpg', '.jpeg', '.png', '.pdf']

def extract_metadata(file_path):
    metadata = {}
    
    # Extract metadata from an image
    if file_path.endswith(('.jpg', '.jpeg', '.png')):
        try:
            img = Image.open(file_path)
            for tag, value in img._getexif().items():
                if tag in ExifTags.TAGS:
                    metadata[ExifTags.TAGS[tag]] = value
        except:
            return render_template('upload.html', error="No metadata found")

    
    # Extract metadata from a PDF
    elif file_path.endswith('.pdf'):
        try:
            pdf = pikepdf.Pdf.open(file_path)
            info = pdf.docinfo
            for key, value in info.items():
                metadata[key] = value
        except:
            return render_template('upload.html', error="No metadata found")
    
    return metadata


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['photo']
        file_path = os.path.join('uploads', f.filename)
        try:
            f.save(file_path)
        except:
            return render_template('upload.html', error="Failed to upload file")

        if not any(file_path.endswith(ext) for ext in allowed_extensions):
            return render_template('upload.html', error="Invalid file type")

        metadata = extract_metadata(file_path)
        
        if metadata is None:
            return render_template('upload.html', error="Failed to extract metadata")
        print(metadata)
        try:
            return render_template('upload.html', metadata=metadata)
        except:
            return render_template('upload.html', error="Failed to extract metadata")


if __name__ == '__main__':
    app.run(debug=True)
