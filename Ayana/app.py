from flask import Flask, render_template, request
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    original_size = None
    optimized_size = None
    percent = None

    if request.method == 'POST':
        file = request.files['image']

        if file:
            input_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(input_path)

            
            original_size = os.path.getsize(input_path) / 1024

            img = Image.open(input_path)

            
            if img.width > 1200:
                ratio = 1200 / img.width
                img = img.resize((1200, int(img.height * ratio)))

      
            output_path = os.path.join(
                UPLOAD_FOLDER,
                file.filename.split('.')[0] + '.webp'
            )
            img.save(output_path, 'WEBP', quality=78)

            optimized_size = os.path.getsize(output_path) / 1024
            percent = ((original_size - optimized_size) / original_size) * 100

    return render_template(
        'index.html',
        original_size=original_size,
        optimized_size=optimized_size,
        percent=percent
    )

if __name__ == '__main__':
    app.run(debug=True)