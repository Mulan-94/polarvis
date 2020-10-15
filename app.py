from flask import Flask, render_template

app = Flask("cygserver")


@app.route("/", methods=['GET', 'POST', 'PUT'])
def run_js9():
    return render_template("js9.html")


app.run(debug=True)
