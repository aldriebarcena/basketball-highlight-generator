from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory
import os
import shutil

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Ensure the uploads directory exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clear_upload_folder():
    """
    Deletes all files in the uploads folder.
    """
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Delete the file
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Delete the directory
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part in the request', 'error')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            clear_upload_folder()
            
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Process the video (stub for now)
            processed_filename = process_video(file_path)

            flash(f'File {filename} uploaded and processed successfully!', 'success')
            return render_template('index.html', filename=processed_filename)  # Pass processed filename to the template
        else:
            flash('Invalid file type. Allowed types are: mp4, mov, avi, mkv', 'error')
            return redirect(request.url)
    return render_template('index.html')

def process_video(file_path):
    """
    Stub for processing the video.
    For now, just return the same file as the "processed" output.
    """
    print(f"Processing video: {file_path}")
    # Add your video processing logic here in the future

    # For now, just return the same file as the processed output
    processed_filename = f"processed_{os.path.basename(file_path)}"
    processed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)

    # Copy the uploaded file to the processed file path
    import shutil
    shutil.copy(file_path, processed_file_path)

    print(f"Processed video saved as: {processed_filename}")
    return processed_filename

@app.route('/download/<filename>')
def download_file(filename):
    """
    Route to allow downloading the processed video.
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)