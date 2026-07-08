import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from predict import predict_image

app = Flask(__name__)
app.secret_key = 'super_secret_key_tea_leaf'

# Config
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Pastikan folder uploads ada
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Inisialisasi Database SQLite
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            filename TEXT,
            disease TEXT,
            confidence REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Data Penyakit
DISEASE_INFO = {
    'Algal Spot': {
        'deskripsi': 'Bercak alga adalah penyakit yang disebabkan oleh alga parasit Cephaleuros virescens. Terlihat sebagai bercak cokelat kemerahan atau oranye pada daun.',
        'penyebab': 'Kelembapan tinggi, sirkulasi udara buruk, dan kurangnya sinar matahari.',
        'saran': 'Tingkatkan sirkulasi udara, kurangi kelembapan dengan pemangkasan yang tepat, dan gunakan fungisida berbasis tembaga jika infeksi parah.'
    },
    'Brown Blight': {
        'deskripsi': 'Penyakit hawar cokelat disebabkan oleh jamur Colletotrichum camelliae. Biasanya muncul sebagai bercak cokelat besar yang menyebar dari tepi daun.',
        'penyebab': 'Cuaca hangat dan lembap, serta luka pada daun akibat pemetikan.',
        'saran': 'Buang daun yang terinfeksi, hindari pemetikan saat daun basah, dan semprotkan fungisida yang direkomendasikan secara berkala.'
    },
    'Gray Blight': {
        'deskripsi': 'Hawar abu-abu disebabkan oleh jamur Pestalotiopsis theae. Ciri utamanya adalah bercak abu-abu berbentuk tidak beraturan dengan tepi cokelat gelap.',
        'penyebab': 'Kondisi lingkungan yang lembap dan kurang nutrisi pada tanaman.',
        'saran': 'Jaga kebersihan kebun teh, perbaiki drainase, dan berikan pupuk yang seimbang (terutama Kalium).'
    },
    'Healthy': {
        'deskripsi': 'Daun teh sehat tanpa tanda-tanda infeksi penyakit atau serangan hama.',
        'penyebab': 'Perawatan yang baik dan lingkungan yang mendukung.',
        'saran': 'Lanjutkan rutinitas perawatan, pemupukan, dan penyiraman secara optimal.'
    },
    'Helopeltis': {
        'deskripsi': 'Helopeltis (Kepik pengisap daun) adalah hama yang menusuk dan mengisap cairan daun muda, menyebabkan bercak-bercak hitam atau tembus pandang.',
        'penyebab': 'Serangan serangga Helopeltis sp.',
        'saran': 'Gunakan insektisida yang sesuai, lakukan pemangkasan rutin untuk memutus siklus hidup hama, dan perhatikan sanitasi kebun.'
    },
    'Red Spot': {
        'deskripsi': 'Bercak merah sering kali dikaitkan dengan infeksi jamur tertentu atau defisiensi nutrisi yang menyebabkan bintik-bintik merah kecil di permukaan daun.',
        'penyebab': 'Infeksi jamur sekunder atau kondisi cuaca yang fluktuatif.',
        'saran': 'Gunakan fungisida pelindung, perbaiki kondisi tanah, dan pastikan tanaman mendapatkan asupan nutrisi yang cukup.'
    }
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/disease')
def disease():
    return render_template('disease.html', diseases=DISEASE_INFO)

@app.route('/upload', methods=['GET'])
def upload_form():
    return render_template('upload.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        flash('Tidak ada file bagian')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('Tidak ada gambar yang dipilih')
        return redirect(url_for('upload_form'))
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Prediksi menggunakan model
        disease_name, confidence = predict_image(file_path)
        
        if disease_name:
            # Simpan ke Database
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute("INSERT INTO history (date, filename, disease, confidence) VALUES (?, ?, ?, ?)",
                      (date_now, filename, disease_name, confidence))
            conn.commit()
            conn.close()
            
            info = DISEASE_INFO.get(disease_name, {})
            
            return render_template('result.html', 
                                   filename=filename, 
                                   disease=disease_name, 
                                   confidence=round(confidence, 2),
                                   info=info)
        else:
            flash(f'Terjadi kesalahan saat memproses gambar: {confidence}')
            return redirect(url_for('upload_form'))
            
    else:
        flash('Ekstensi file tidak diizinkan. Gunakan png, jpg, atau jpeg.')
        return redirect(url_for('upload_form'))

@app.route('/history')
def history():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM history ORDER BY id DESC")
    records = c.fetchall()
    conn.close()
    return render_template('history.html', records=records)

# Endpoint untuk mengambil gambar dari folder uploads (agar bisa ditampilkan di result)
from flask import send_from_directory
@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

if __name__ == '__main__':
    app.run(debug=True)
