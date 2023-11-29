from flask import Flask, render_template, request, jsonify
import yaml
import jinja2

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/prepare', methods=['GET', 'POST'])
def prepare_services():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        form_data = request.form
        return render_template('prepare.html', form_data=form_data)


@app.route('/generate', methods=['POST'])
def generate_compose():
    form_data = request.form
    print(form_data)
    jinja_env = jinja2.Environment()
    with open('templates/docker-compose.yml.jinja', 'r') as file:
        template = file.read()
        compose = jinja_env.from_string(template).render(
            form_data=form_data
        )
        print (compose)

    with open('templates/Caddyfile.jinja', 'r') as file:
        template = file.read()
        caddyfile = jinja_env.from_string(template).render(
            form_data=form_data
        )
        print (caddyfile)

    return "ok", 200

@app.route('/help')
def help():
    return render_template('help.html')

if __name__ == '__main__':
    # Run the application on port 8067
    print("Starting installation Script")
    app.run(host='0.0.0.0', port=8000, debug=True)

