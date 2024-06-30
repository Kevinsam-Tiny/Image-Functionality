from flask import Flask, request, send_file,render_template
from rembg import remove
import zipfile
from PIL import Image, ImageEnhance
import io

app = Flask(__name__)
@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/remove_background', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return "No file part"
    file = request.files['image']
    if file.filename == '':
        return "No selected file"
    if file:
        # Read the image file
        input_image = Image.open(file.stream)
        
        # Remove the background
        output_image = remove(input_image)

        # Save the processed image to a BytesIO object
        img_byte_arr = io.BytesIO()
        output_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        return send_file(img_byte_arr, mimetype='image/png', as_attachment=True, download_name='output.png')
    

@app.route('/enhance', methods=['POST'])
def enhance_image():
    if 'image' not in request.files:
        return "No file part"
    file = request.files['image']
    if file.filename == '':
        return "No selected file"
    if file:
        # Read the image file
        input_image = Image.open(file.stream)

        # Enhance the image (example: adjust contrast, sharpness, and brightness)
        enhancer = ImageEnhance.Contrast(input_image)
        image_enhanced = enhancer.enhance(1.5)  # Increase contrast

        enhancer = ImageEnhance.Sharpness(image_enhanced)
        image_enhanced = enhancer.enhance(2.0)  # Increase sharpness

        enhancer = ImageEnhance.Brightness(image_enhanced)
        image_enhanced = enhancer.enhance(1.2)  # Increase brightness

        # Save the processed image to a BytesIO object
        img_byte_arr = io.BytesIO()
        image_enhanced.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        return send_file(img_byte_arr, mimetype='image/png', as_attachment=True, download_name='enhanced.png')

@app.route('/compress', methods=['POST'])
def compress_image():
    if 'image' not in request.files:
        return "No file part"
    file = request.files['image']
    if file.filename == '':
        return "No selected file"
    if file:
        input_image = Image.open(file.stream)
        output_image = io.BytesIO()
        input_image.save(output_image, format='JPEG', quality=20, optimize=True)
        output_image.seek(0)
        return send_file(output_image, mimetype='image/jpeg', as_attachment=True, download_name='compressed.jpg')





@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return "No file part"
    file = request.files['image']
    if file.filename == '':
        return "No selected file"
    if file:
        # Read the image file
        input_image = Image.open(file.stream)

        # Remove the background
        image_no_bg = remove(input_image)

        # Enhance the image (example: adjust contrast, sharpness, and brightness)
        enhancer = ImageEnhance.Contrast(input_image)
        image_enhanced = enhancer.enhance(1.5)  # Increase contrast

        enhancer = ImageEnhance.Sharpness(image_enhanced)
        image_enhanced = enhancer.enhance(2.0)  # Increase sharpness

        enhancer = ImageEnhance.Brightness(image_enhanced)
        image_enhanced = enhancer.enhance(1.2)  # Increase brightness

        # Compress the image by reducing its quality
        img_byte_arr_no_bg = io.BytesIO()
        img_byte_arr_enhanced = io.BytesIO()
        img_byte_arr_compressed = io.BytesIO()

        image_no_bg.save(img_byte_arr_no_bg, format='PNG')
        img_byte_arr_no_bg.seek(0)

        image_enhanced.save(img_byte_arr_enhanced, format='PNG')
        img_byte_arr_enhanced.seek(0)

        input_image.save(img_byte_arr_compressed, format='JPEG', quality=25)
        img_byte_arr_compressed.seek(0)

        # Create a zip file containing all three images
        zip_byte_arr = io.BytesIO()
        with zipfile.ZipFile(zip_byte_arr, 'w') as zf:
            zf.writestr('image_no_bg.png', img_byte_arr_no_bg.getvalue())
            zf.writestr('image_enhanced.png', img_byte_arr_enhanced.getvalue())
            zf.writestr('image_compressed.jpg', img_byte_arr_compressed.getvalue())
        zip_byte_arr.seek(0)

        return send_file(zip_byte_arr, mimetype='application/zip', as_attachment=True, download_name='processed_images.zip')



if __name__ == "__main__":
    app.run(debug=True)
