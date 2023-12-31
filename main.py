from flask import Flask, render_template, request, send_file
import jinja2
import io
import tarfile

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
    jinja_env = jinja2.Environment()
    with open('templates/docker-compose.yml.jinja', 'r') as file:
        template = file.read()
        compose = jinja_env.from_string(template).render(
            form_data=form_data
        )
        # print (compose)
    with open('templates/Caddyfile.jinja', 'r') as file:
        template = file.read()
        caddyfile = jinja_env.from_string(template).render(
            form_data=form_data
        )
        # print (caddyfile)
    with open('templates/dashyconf.yml.jinja', 'r') as file:
        template = file.read()
        dashyconf = jinja_env.from_string(template).render(
            form_data=form_data
        )
        # print (dashyconf)
    with open('static/script.sh', 'r') as file:
        script = file.read()
        # print (script)
    file1_tarinfo = tarfile.TarInfo('docker-compose.yml')
    file1_tarinfo.size = len(compose)
    file2_tarinfo = tarfile.TarInfo('Caddyfile')
    file2_tarinfo.size = len(caddyfile)
    file3_tarinfo = tarfile.TarInfo('dashyconf.yml')
    file3_tarinfo.size = len(dashyconf)
    file4_tarinfo = tarfile.TarInfo('script.sh')
    file4_tarinfo.size = len(script)
    with tarfile.open('noogle_generated.tar.gz', 'w:gz') as tar:
        tar.addfile(file1_tarinfo, io.BytesIO(compose.encode()))
        tar.addfile(file2_tarinfo, io.BytesIO(caddyfile.encode()))
        tar.addfile(file3_tarinfo, io.BytesIO(dashyconf.encode()))
        tar.addfile(file4_tarinfo, io.BytesIO(script.encode()))
    return render_template('download.html')

@app.route('/download')
def download_file():
    return send_file('noogle_generated.tar.gz', as_attachment=True)

@app.route('/help')
def help():
    return render_template('help.html')

if __name__ == '__main__':
    # Run the application on port 8067
    print("Starting installation Script")
    # app.run(port=8000, debug=True)
    app.run(host='0.0.0.0', port=8000)
