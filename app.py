
from flask import Flask, request,render_template
variable="dummy"
app = Flask(__name__)

import pygame
import random
import time 
import csv_bs

@app.route('/',methods=['GET', 'POST'])
def login():
    if (request.method == 'GET'):
         return render_template("frontend.html")
    else:
        import main_logic
        return render_template("sample.html")

if(__name__ == "__main__"): 
    app.run(debug=True)  