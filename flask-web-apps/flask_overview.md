# What the Flask?

Flask is a popular python package that simplifies the process of building web apps. In the main Flask lecture, we went over how to build a Flask app from scratch, but in practice many Flask apps are modified from existing apps. For instance, you might want to fork an existing cancer prediction app (`additional_resources/cancer_app/cancer-predictor-app.py`) and use it to predict another disease.

The best way to learn Flask is to look at a working app, so let's quickly look at it.

# cancer-predictor-app.py code structure, with comments

```
import flask
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd
```

To set up the app, all Python libraries need to be imported. Typically, this include Flask, SKLearn, numpy, pandas, etc. 

```
#---------- MODEL IN MEMORY ----------------#

# Read the scientific data on breast cancer survival,
# Build a LogisticRegression predictor on it
patients = pd.read_csv("haberman.data", header=None)
patients.columns = ['age', 'year', 'nodes', 'survived']
# The value 2 means death in 5 years, update to more common 0
patients = patients.replace(2, 0)

X = patients[['age', 'year', 'nodes']]
Y = patients['survived']
PREDICTOR = LogisticRegression().fit(X, Y)
```

The app needs a machine learning model to run. Smaller models can be trained directly in the app itself. For larger models, consider saving and loading a Pickle file instead; see `train_save_model.ipynb` for an example.

```
#---------- URLS AND WEB PAGES -------------#

# Initialize the app
app = flask.Flask(__name__)
```

Make a Flask object, `app`, and change it to create a webapp.

```
# Homepage
@app.route("/")
def viz_page():
    """
    Homepage: serve our visualization page, awesome.html
    """
    with open("awesome.html", 'r') as viz_file:
        return viz_file.read()
```

`@app.route('/')` is a decorator that tells the app to run the following function whenever anyone navigates to that page (i.e. the homepage). The function returns the page we want to load, in this case `awesome.html` which is located in the same directory as the predictor-app.py file.

```
# Get an example and return it's score from the predictor model
@app.route("/score", methods=["POST"])
def score():
    """
    When A POST request with json data is made to this uri,
    Read the example from the json, predict probability and
    send it with a response
    """
    # Get decision score for our example that came with the request
    data = flask.request.json
    x = np.matrix(data["example"])
    score = PREDICTOR.predict_proba(x)
    # Put the result in a nice dict so we can send it as json
    results = {"score": score[0, 1]}
    return flask.jsonify(results)
```

Score (prediction) page. Typically, the prediction results are generated using a combination of HTML structures (forms, lists, etc.) in HTML template files, CSS, JSON, D3 (which uses JSON), etc. You should decide what's appropriate for your project.

```
#--------- RUN WEB APP SERVER ------------#

# Start the app server on port 80
# (The default website port)
app.run(host='0.0.0.0')
app.run(debug=True)
```

The last two lines allow us to activate the web app whenever we run the file. You may want to hardcode a port number, in case your local machine is running another service (e.g. Jupyter notebook, other web servers including Flask, etc.) on the default port. To do so, use `app.run(port=x)`, where `x` is the desired port number.

## Run cancer-predictor-app locally

Call the command `python3 cancer-prediction-app.py` and the following output (or similar) should appear in terminal.

```
* Serving Flask app "app" (lazy loading)
* Environment: production
  WARNING: Do not use the development server in a production environment.
  Use a production WSGI server instead.
* Debug mode: off
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
And then you can load up http://127.0.0.1:5000/ in your browser.
```

When you're finished, be sure to close out the app with CTRL-C.

# Exercise - Build an Iris Predictor App

## Step 0: Save a model

Check out the notebook where we store a model that predicts the species of flower based on attributes [here](train_save_model.ipynb). Run this notebook to generate a logistic regression pickle (`lr.pkl`) in your directory.

## Step 1: Build an app that loads the model

Copy the existing `app.py` into a new file named `predictor_app.py` in the `solutions` subdirectory. We'll be working in this subdirectory for the remainder of this exercise, which contains the needed html and templates subdirectories to support our Flask app.

Make the following changes to `predictor_app.py`:

### Add new routes
Add a `template_engine` route:
```
@app.route("/template_engine")
def template_engine():
    return flask.render_template('template_engine.html')
```

This function is run for the URL http://127.0.0.1:5000/template_engine, which will be used to demonstrate how Flask template engines work in Steps 1.5 + 1.9.

Add a `predict` route:
```
@app.route("/predict")
def predict():
    return "predict page placeholder"
```

This function is run for the URL http://127.0.0.1:5000/predict. The functionality to play around with your model will be stored in this page, which we'll see in Step 3.

### Add code above the routing function that loads the pickled model. 

Note that you may have to adjust the path to the Logistic Regression pickle file.

```
with open("../lr.pkl", "rb") as f:
    lr_model = pickle.load(f)

feature_names = lr_model.feature_names
```

Verify that you're loading the pickled model by modifying the predict function to return `feature_names`.

The next two parts (Steps 1.5 + 1.9) explain Flask template engines using lists and forms. To continue directly working on the main Flask app, skip to step 2.

## Step 1.5: List template engines
Flask uses a template engine to allow us to render webpages in response to the data in the app. Refer to the documentation for [Jinja2](http://jinja.pocoo.org/docs/2.10/) when you build your apps.

Say we want to build a list. Normally in HTML, we would do this like so:

```html
<ul>
  <li>Item 1</li>
  <li>Item 2</li>
  <li>Item 3</li>
</ul>
```

In Flask, we can use a template engine to build a list with code:

```html
<ul>
  {% for i in range(1,4) %}
      <li>Item {{ i }}</li>
  {% endfor %}
</ul>
```

Try this by creating the html file `template_engine.html` in the templates folder and inserting this flask template code here. Verify that if you change the range, the list changes too. Now, modify the above to list the feature names (hint: look at the [Flask Docs](http://flask.pocoo.org/docs/1.0/quickstart/#rendering-templates) for more info on passing arguments to a template).

## Step 1.9: List template engines in forms

To do this step, we're going to first look at forms. Here's a form block that comes from w3schools.

```html
<form action="/action_page.php">
  First name:<br>
  <input type="text" name="firstname" value="Mickey">
  <br>
  Last name:<br>
  <input type="text" name="lastname" value="Mouse">
  <br><br>
  <input type="submit" value="Submit">
</form>
```

It has a few parts:
- The `<form action="/action_page.php"></form>` tag is a wrapper around the rest of the form. It includes the action attribute which tells us where to send the results of the form when we're through.
- Within that form are standard html things like text and `<br>`s for linebreaks.
- The `<input type="text" name="lastname" value="Mouse">` tag gives us an empty text field. We'll use this to grab user input. The `value` attribute sets the default value and `name` attribute tells us how to refer to the input block. Make sure that each `<input>` tag as a unique name. Also, note that `<input>`s are self-closing.
- The `<input type="submit" value="Submit">` tag is a special input that renders as a submit button.

Let's convert the form from a fixed number of features (First Name, Last Name) to a dynamic list of features.

Start with the form above and replace the input fields with our feature names. Now change the form action so that it sends us back to the same page. Your code should look something like:

```
<form action="/template_engine">

{% for f in feature_names %}
    <br>
    {{ f }}
    <br>
    <input type="text" name="{{ f }}" value="0">
{% endfor %}
<br>
<input type="submit" value="Submit" method="get">
```

## Step 2: Update predict decorator to send results to prediction page

We would like to send the results of our model to be displayed on the prediction page. Replace your predict function with the following code.

``` python
@app.route("/predict", methods=["POST", "GET"])
def predict():

    x_input = []
    for i in range(len(lr_model.feature_names)):
        f_value = float(
            request.args.get(lr_model.feature_names[i], "0")
            )
        x_input.append(f_value)

    pred_probs = lr_model.predict_proba([x_input]).flat

    return flask.render_template('predictor.html',
    feature_names=lr_model.feature_names,
    x_input=x_input,
    prediction=np.argsort(pred_probs)[::-1]
    )
```

The last line of code sends three variables to `predictor.html`:
- `feature_names`: The feature names of the LR model
- `x_input`: User-selected values for the given features.
- `prediction`: The Iris class probabilities of the model, based on `x_input`.

These features will be populated dynamically into the `predict` page in Step 3.

## Step 3: Create a prediction page template for the Flask app

Let's add dynamic functionality to the `predict` page. Take a look at the pre-written file `predictor.html` in templates subdirectory. It uses the template engines discussed in Steps 1.5 + 1.9 extensively.

```
<!DOCTYPE html>
<html lang="en">

<head>
  <title>My Webpage</title>
</head>

<body>
  <form action="/predict">

    {% for f in feature_names %}
        <br>
        {{ f }}
        <br>
        <input type="text" name="{{ f }}" value="{{x_input[loop.index0]}}">
    {% endfor %}
    <br>
    <input type="submit" value="Submit" method="get">
  </form>
```

The first part of the HTML body is a form with a template engine that produces a list of features to fill out.

```
  <p>
    prediction:
    {% for p in prediction %}
      <br>  {{p['name']}}:{{ 100*p['prob'] | round(1) }}% 
    {% endfor %}
  </p>

</body>

</html>
```

The second part of the HTML body prints out the predicted probabilities for each of the possible Iris classes, again using a list template engine.

Exercise: How do we get the user input? Where's it stored?

## Conclusion
Fire up the app with `python3 predictor_app.py`. Go to the predict page [http://localhost:5000/predict](http://localhost:5000/predict)

Compare your app to the official solution, `predictor_app_solution.py`, which depends on the `predictor_api.py` file. The latter file includes the loading of the model pickle and the feeding of the user inputs into the model itself.
