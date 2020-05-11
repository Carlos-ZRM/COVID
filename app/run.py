from flask import Flask
#from forms import PostForm
import io

from flask import render_template, request, redirect, url_for, Response, session, jsonify
from flask_cors import CORS
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from interpolacion import flask
from interpolacion import datos
from eca_sir import *
from PIL import Image
import time


global_key = 0
eca_dic = {}
csv = False

app = Flask(__name__ , template_folder='templates')
app.secret_key = 'app secret key'
CORS(app)
app.debug = True

@app.route("/")
def hello():
    return render_template("index.html")
@app.route("/interpolacion/", methods=["GET", "POST"])
def interpolacion_form():
    if request.method == 'POST':
            numDatos = request.form['numDatos']
            numInicio = request.form['numInicio']
            next = request.args.get('next', None)
            #fig = flask(numDatos)
            #output = io.BytesIO()
            #FigureCanvas(fig).print_png(output)
            if next:
            #return redirect(next)
                #return Response(output.getvalue(), mimetype='image/png')
                return render_template("interpolacion_canvas.html")
        #return redirect(url_for('index'))
        #return 'recurso no encontrado'

    return render_template("parametrosLineal.html")

    """
    form = interpolacion_form()
    if form.validate_on_submit():
        numDatos= form.numDatos.dta
    """
@app.route("/sir/", methods=["GET", "POST"])
def sir():
    if request.method == 'POST':
        global global_key
        global eca_dic
        cell_x = request.form['cell_x']
        cell_y = request.form['cell_y']
        step = 0
        epsilon = request.form['epsilon']
        v = request.form['v']
        N = request.form['N']
        m = request.form['m']
        c = request.form['c']
        
        # Se crea el objeto, se guarda en el diccionario y se suma uno
        eca = ECA (int(cell_x), int(cell_y) ,step,True, float(epsilon), float(v), int(N), float(m),float(c) )
        eca.initializate() 
        
        eca_dic[str(global_key)] = eca
        print(eca_dic.keys())
        poblacion= int(cell_x)*int(cell_y)*int(N)
        global_key +=1
        return render_template("sir_canvas.html", cell_x=cell_x, cell_y = cell_y , N=N,poblacion=poblacion,v=v, epsilon=epsilon, m=m, c=c, key = global_key-1 )
 
    return render_template("parametros.html")

@app.route("/sir-mexico/", methods=["GET", "POST"])
def sir_mexico():
    if request.method == 'POST':
        global eca
        epsilon = request.form['epsilon']
        v = request.form['v']
        #sstep = request.form['step']
        step = 10
        m = request.form['m']
        c = request.form['c']

        eca = ECA (cell_x=10,cell_y=10,step=step,flask=True, epsilon=float(epsilon), v=float(v), N=None , m=float(m),c=float(c) )
        eca.iniciar_mexico()
       
        return render_template("sir_canvas_mexico.html",step=step,v=v, epsilon=epsilon, m=m, c=c)
                   
        
    return render_template("parametros_mexico.html")




@app.route('/plot/<imgdata>')
def plot(imgdata):
    k = imgdata.index('-')
    key = imgdata[:k]
    eca = eca_dic[key]

    result = eca.simulacion_flask()

    output = io.BytesIO()

    result.save(output, 'PNG')
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/plot_mexico/<imgdata>')
def plot_mexico(imgdata):
    k = imgdata.index('-')
    
    key = imgdata[:k]
    eca = eca_dic[key]    

    result = eca.simulacion_flask()

    output = io.BytesIO()

    result.save(output, 'PNG')
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/plot_mexico_grafica/<imgdata>')
def plot_mexico_grafica(imgdata):
    
    k = imgdata.index('-')
    key = imgdata[:k]
    eca = eca_dic[key]

    fig = eca.graficas_flask()    
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/plot_mexico_grafica_ac/<imgdata>')
def plot_mexico_grafica_ac(imgdata):
    k = imgdata.index('-')
    key = imgdata[:k]
    eca = eca_dic[key]

    fig = eca.graficas_flask(opc=2)    
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/plot_csv/<imgdata>')
def plot_mexico_grafica_csv(imgdata):
    global csv
    if csv == False:
        csv = datos()
    
    k = imgdata.index('-')
    opc = int(imgdata[:k])
    dias = int(imgdata[k+1:])

    fig = csv.graficas_datos(opc, dias)   
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/plot_interpolacion/<imgdata>')
def plot_interpolacion(imgdata):
    fig = flask(imgdata)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/get_datos/<imgdata>')
def get_datos(imgdata):
    global csv
    if csv == False:
        csv = datos()
        
    
    
    k = imgdata.index('-')
    key = imgdata[:k]
    dias = int (imgdata[k+1:])
    eca = eca_dic[key]
    
    nc_csv, nca_csv, defu_csv = csv.get_datos( dias=dias)
    s,  i , r, ac, nc = eca.get_datos()


    return jsonify(s=s,i=i,r=r,ac = ac, nc = nc, nc_csv= nc_csv , nca_csv=nca_csv, defu_csv = defu_csv)

@app.route('/get_datos_csv/<imgdata>')
def get_datos_csv(imgdata):
    global csv
    if csv == False:
        csv = datos()
        
    dias = int(imgdata)
    
    nc, nca, defu = csv.get_datos( dias=dias)

    return jsonify(nc=nc, nca=nca, defu=defu)

@app.route('/clear/<key>')
def clear(key):
    global eca_dic
    if key in eca_dic :
        del eca_dic[key]
    return jsonify(res="clear")



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("80"), debug=True)


