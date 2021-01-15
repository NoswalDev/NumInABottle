# minimal example from:
# http://flask.pocoo.org/docs/quickstart/

from flask import Flask

app = Flask(__name__)  # create instance of Flask class


@app.route('/')  # the site to route to, index/main in this case
def hello_world() -> str:
    """Let's say Hi to the world.

    Returns:
        str: The HTML we want our browser to render.
    """
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    imayge = "https://www.shapinguptobeamom.com/wp-content/uploads/2014/05/its-gonna-be-may.jpg"
    birb = "https://media1.giphy.com/media/l3q2zVr6cu95nF6O4/giphy.gif?cid=ecf05e477f8ed158f5953475e62af1974c561c804939c445&rid=giphy.gif"
    hats = '''
           <img src= {img} style="width:300px;">
           <img src= {img} style="width:300px;">
           <img src= {img} style="width:300px;">
           
           '''
    outp = hats.format(img = birb)
    return outp

=======
    repeat_count = 9
    return '<img src="https://tinyurl.com/so5mjp3" alt="yoda" width="500">'*repeat_count
>>>>>>> c763981f8131973b89a034c62f1ab4612b4ccc89
=======
    repeat_count = 9
    return '<img src="https://tinyurl.com/so5mjp3" alt="yoda" width="500">'*repeat_count
>>>>>>> c763981f8131973b89a034c62f1ab4612b4ccc89
=======

    return 'Hello World!'

>>>>>>> 4b9e0347602d1984e43df77bcd6852d46c9b8c83

if __name__ == '__main__':
    app.run()
