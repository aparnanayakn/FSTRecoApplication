from flask import Flask, render_template, request, redirect, url_for, flash
import os
from supportingPythonFiles  import extractmf
from SPARQLWrapper import SPARQLWrapper, JSON
from supportingPythonFiles  import binGenerator

app = Flask(__name__)
port_number = 5555


filePath = None

app.config["DEBUG"] = True
app.debug = True

UPLOAD_FOLDER = 'static/files' # Upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/visualise', methods=['GET'])
def temp():
    global filePath
    data = extractmf.extractMetaFeature(filePath)
    dataset,graph_path, predicted_label =  binGenerator.binGenerator(data)
    return render_template('visualisation.html', graph_path=graph_path, predicted_label=predicted_label,  data=dataset)


# Get the uploaded files
@app.route("/", methods=['POST'])
def uploadFiles():
    global filePath
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('temp'))
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # set the file path
        uploaded_file.save(file_path)
        filePath = file_path
    return redirect(url_for('temp'))

if __name__ == "__main__":
    app.run(debug=True, port=port_number)

