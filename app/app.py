from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import yaml
import PyPDF2
import sys
import re
import s3_handler


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure MySQL
db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] =  os.getenv('MYSQL_USER') #sys.argv[1] #db['mysql_user']
app.config['MYSQL_PASSWORD'] =  os.getenv('MYSQL_PASSWORD') #sys.argv[2] #db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)
ssql="SELECT concat(left(filename,5),'..',right(filename,4)) as filename, upload_time, filedesc, filename as fn, filetext, id FROM files WHERE username = %s"

# File upload configuration
UPLOAD_FOLDER = 'uploads/' #define uploads folder
DOWNLOAD_FOLDER = 'downloads/' #define donloads folder
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#homepage
@app.route('/')
def home():
    return render_template('login.html')

#return from login page. if user found - redirect to users file list page. if user not found return to login page
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
   
    #check user credentials in db
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
    if result > 0:
        user = cur.fetchone()
        if check_password_hash(user[2], password):
            #user found -> keep username in session object and proceed to users file list
            session['username'] = username
            return redirect(url_for('files'))
        else:
            flash("Invalid credentials. Please try again.", "danger")
    else:
        flash("Invalid credentials. Please try again.", "danger")
    cur.close()
    #user not found -> return to login page
    return redirect(url_for('home'))

#signup page
@app.route('/signup')
def signup():
    return render_template('signup.html')

#after succeful signup. save user to db and return to login page
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    hashed_password = generate_password_hash(password, method='sha256')

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    mysql.connection.commit()
    cur.close()

    flash("You have successfully signed up!", "success")
    return redirect(url_for('home'))

#upload page
@app.route('/upload', methods=['GET','POST'])
def upload_file():
    pdftext = ''
    if 'username' not in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        filedesc = request.form['File_desc']
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            fullpathfn = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(fullpathfn)
            s3_handler.upload_file_to_s3(fullpathfn, filename)
            # Insert file info into database
            cur = mysql.connection.cursor()
            pdftext = pdf_to_text(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            cur.execute("INSERT INTO files (username, filename, filedesc, filetext) VALUES (%s, %s, %s, %s)", (session['username'], filename, filedesc, pdftext))
            mysql.connection.commit()
            cur.close()

            flash('File successfully uploaded', 'success')
            return redirect(url_for('files'))

    cur = mysql.connection.cursor()
    cur.execute(ssql, [session['username']])
    files = cur.fetchall()
    cur.close()
    
    #if upload succefully completed -> go to users file list
    return render_template('upload.html', pdftext=pdftext)
    #return render_template('files.html', files=files, uname=session['username'])

@app.route('/files')
def files():
    if 'username' not in session:
        return redirect(url_for('home'))

    cur = mysql.connection.cursor()
    cur.execute(ssql, [session['username']])
    files = cur.fetchall()
    cur.close()
    return render_template('files.html', files=files, uname=session['username'], myre=re)

@app.route('/<filename>')
def uploaded_file(filename):
    if 'username' not in session:
        return redirect(url_for('home'))
    #return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    # Generate S3 file URL
    fullpathdfn = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
    s3_handler.download_file_from_s3(fullpathdfn, filename)
    #file_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{filename}"
    #return redirect(file_url)
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)

#render pdf to pext
def pdf_to_text(pdf_path):
    # Open the PDF file in read-binary mode
    with open(pdf_path, 'rb') as pdf_file:
        # Create a PdfReader object instead of PdfFileReader
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Initialize an empty string to store the text
        text = ''

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        #delete the file after rendering
        os.remove(pdf_path)
        return text    

@app.route('/delete/<fileid>', methods=['POST'])
def delete_file(fileid):
    # Get the current user
    if 'username' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))

    username = session['username']

    # Step 1: Delete file from the S3 bucket
    try:
        cur = mysql.connection.cursor()
        cur.execute("select filename FROM files WHERE id=%s AND username=%s", (fileid, username))        
        filename = cur.fetchone()
        cur.close()
        if filename:
          s3_handler.delete_file_from_s3(filename[0])

    except Exception as e:
        flash(f"Error deleting file from S3: {str(e)}")
        return redirect(url_for('files'))

    # Step 2: Delete file from MySQL database
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM files WHERE id=%s AND username=%s", (fileid, username))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        flash(f"Error deleting file from the database: {str(e)}")
        return redirect(url_for('files'))

    flash(f"File '{filename}' deleted successfully.")
    return redirect(url_for('files'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)