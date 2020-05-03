from flask import Flask
#from forms import PostForm
import io

from flask import render_template, request, redirect, url_for, Response, session, json
from flask_cors import CORS
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from interpolacion import flask
from eca_sir import *
from PIL import Image
import time



eca = None
eca_mexico = None
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
            print("numDatos", numDatos)
            next = request.args.get('next', None)
            fig = flask(numDatos)
            output = io.BytesIO()
            FigureCanvas(fig).print_png(output)
            if next:
            #return redirect(next)
                return Response(output.getvalue(), mimetype='image/png')
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
        global eca
        cell_x = request.form['cell_x']
        cell_y = request.form['cell_y']
        step=0
        epsilon = request.form['epsilon']
        v = request.form['v']
        N = request.form['N']
        m = request.form['m']
        c = request.form['c']
        print("\n****   ", type(epsilon), epsilon)
        eca = ECA (int(cell_x), int(cell_y) ,step,True, float(epsilon), float(v), int(N), float(m),float(c) )

        eca.initializate() 
        return render_template("sir_canvas.html", N=N,step=step,v=v, epsilon=epsilon, m=m, c=c )
 
    return render_template("parametros.html")

@app.route("/sir-mexico/", methods=["GET", "POST"])
def sir_mexico():
    if request.method == 'POST':
        global eca
        epsilon = request.form['epsilon']
        v = request.form['v']
        step = request.form['step']
        m = request.form['m']
        c = request.form['c']

        eca = ECA (cell_x=10,cell_y=10,step=step,flask=True, epsilon=float(epsilon), v=float(v), N=None , m=float(m),c=float(c) )
        eca.iniciar_mexico()
       
        return render_template("sir_canvas_mexico.html",step=step,v=v, epsilon=epsilon, m=m, c=c)
                   
        
    return render_template("parametros_mexico.html")


@app.route("/evolucion-sir/", methods=["GET", "POST"])
def sir_evolucion():
    if request.method == 'GET':
        #result = eca.simulacion_flask()
        #render_template("sir_canvas.html", result=result)
        #step = request.form['step']
        step = 15
        """
        cell_x = request.form['cell_x']
        print(cell_x)
        """
        #return redirect(url_for("sir_evolucion", result=result))
        """
        if eca == None :
            print("evolucion-sir  none")
            return redirect(url_for("sir"))
        """
        return render_template("sir_canvas.html",step=step)
               
    return render_template("sir_canvas.html")


@app.route("/evolucion-sir-mexico/", methods=["GET", "POST"])
def sir_evolucion_mexico():
    if request.method == 'GET':
        #result = eca.simulacion_flask()
        #render_template("sir_canvas.html", result=result)
        #step = request.form['step']
        step = 15
        """
        cell_x = request.form['cell_x']
        print(cell_x)
        """
        #return redirect(url_for("sir_evolucion", result=result))
        """
        if eca == None :
            print("evolucion-sir  none")
            return redirect(url_for("sir"))
        """
        return render_template("sir_canvas.html",step=step)

    return render_template("sir_canvas.html")




@app.route("/evolucion-sir-ajax/", methods=["GET"])
def sir_evolucion_ajax():
   
   
    """
    if eca == None :
        print("ajax none")
        return redirect(url_for("sir"))
    """
    


    """
        cell_x = request.form['cell_x']
        print(cell_x)
    """
        #return redirect(url_for("sir_evolucion", result=result))
    return render_template("sir_canvas_ajax.html")         

@app.route('/plot/<imgdata>')
def plot(imgdata):
    result = eca.simulacion_flask()

    output = io.BytesIO()

    result.save(output, 'PNG')
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/plot_mexico/<imgdata>')
def plot_mexico(imgdata):
    print("")
    result = eca.simulacion_flask()

    output = io.BytesIO()

    result.save(output, 'PNG')
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/plot_mexico_grafica/<imgdata>')
def plot_mexico_grafica(imgdata):
    
    fig = eca.graficas_flask()    
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)


