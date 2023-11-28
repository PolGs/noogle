from flask import Flask, render_template, request, jsonify
import yaml

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
    generate_selected_docker_compose('docker-compose.yml', form_data)
    return "ok", 200

def generate_selected_docker_compose(base_compose_file, service_dict):
    with open(base_compose_file, 'r') as f:
        base_compose_data = yaml.safe_load(f)

    selected_services = set(service for service, enabled in service_dict.items() if enabled == '1')
    filtered_services = {service: config for service, config in base_compose_data.get('services', {}).items() if service in selected_services}

    # Update the base Compose data with filtered services
    base_compose_data['services'] = filtered_services

    # Generate a new Docker Compose file with selected services
    new_compose_file = f"docker-compose-selected.yml"
    with open(new_compose_file, 'w') as f:
        yaml.dump(base_compose_data, f, default_flow_style=False)

    return new_compose_file

@app.route('/help')
def help():
    return render_template('help.html')

if __name__ == '__main__':
    # Run the application on port 8067
    print("Starting installation Script")
    app.run(port=8000, debug=True)

