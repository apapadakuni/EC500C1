from flask import Flask
from agonzagaAPIEXERCISETESTER import module


#Running on http://127.0.0.1:5000/


app = Flask(__name__)

@app.route('/')
def hello_world():
    return """
    <!DOCTYPE html>
    <head>
    	<title> API Exercise pt. 2 </title>
    </head>
    <body>
    	<p> Andre's Code is being tested with the twitter handle 'Cristiano' and a number of 10 tweets </p>  
      <p> To view the labels returned by the Google Cloud Vision API, type '/labels' after the current URL </p>
    	<p> OUTPUT VIDEO as a .mp4 file: </p>
    	<video controls>
  			<source src="/output.mp4" type="video/mp4">
  		</video>
  	</body>

"""
#only way i could think of printing a result from a module
@app.route("/labels")
def labels():
  text = module('Cristiano',10)
  return str(text)



if __name__ == '__main__':
    text = module('Cristiano',10)
    app.run(debug = True, use_reloader = True)