from flask import Flask
#from forms import PostForm
import io

from flask import render_template, request, redirect, url_for, Response
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from interpolacion import flask
app = Flask(__name__ , template_folder='templates')
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

if __name__ == "__main__":
    app.run()


