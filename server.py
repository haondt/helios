from app import Helios
import yaml 

config_file= "/config/helios.yml"

config = {}
with open(config_file) as f:
    s = f.read()
    config = yaml.load(s, Loader=yaml.FullLoader)['helios']

helios = Helios(config)
if __name__ == '__main__':
    helios.run(host='0.0.0.0', debug=True, port=5000)
