from flask import Flask
#from forms import PostForm
import io

from flask import render_template, request, redirect, url_for, Response, session
from flask_cors import CORS
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from interpolacion import flask
from eca_sir import *
eca = None
app = Flask(__name__ , template_folder='templates')
app.secret_key = 'app secret key'
CORS(app)
app.debug = True

@app.route("/")
def hello():
    return "Covid 19 alirob"
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
        return Response(output.getvalue(), mimetype='image/png')

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
        eca = ECA (50,50,100,flask=True)
        #session['eca'] = eca
        if next:

        #return redirect(next)
            return redirect(url_for('sir_evolucion'))
            #return Response(output.getvalue(), mimetype='image/png')
        #return redirect(url_for('index'))
        #return 'recurso no encontrado'
        
        #return redirect("/evolucion-sir", messages={"main":"Condition failed on page baz"})
                # return Response(output.getvalue(), mimetype='image/png')
    return render_template("parametros.html")

@app.route("/evolucion-sir/", methods=["GET", "POST"])
def sir_evolucion():
    if request.method == 'GET':
        #result = eca.simulacion_flask()
        #render_template("sir_canvas.html", result=result)
        
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
        return render_template("sir_canvas.html")
               
    return render_template("sir_canvas.html")

@app.route("/evolucion-sir-ajax/", methods=["GET"])
def sir_evolucion_ajax():
    """
    if eca == None :
        print("ajax none")
        return redirect(url_for("sir"))
    """
    result = eca.simulacion_flask()
    """
        cell_x = request.form['cell_x']
        print(cell_x)
    """
        #return redirect(url_for("sir_evolucion", result=result))
    return render_template("sir_canvas_ajax.html", result=result)           
    
if __name__ == "__main__":
    app.run()


