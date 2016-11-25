import os
from flask import Flask, request, render_template, send_file


FLAG = 'QCTF_Encryption_After_Compression_May_Be_Vulnerable'
CORRECT_DNA_CODE = 'TTGAGCGATCTATCCA'

app = Flask(__name__,
            static_folder='dna_checker/static',
            static_url_path='/dna_checker/static')


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        dna_code = request.form.get('dnaCode', '')
        if dna_code == CORRECT_DNA_CODE:
            return render_template('flag.html', flag=FLAG)
        return render_template('index.html', err_msg='Неверный код!')
