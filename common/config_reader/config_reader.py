import os
import json

class ConfigReader:
    def parse_vars(self, evars):
        config_params = {}

        try:
            for var in evars:
                config_params[var] = os.environ[var]
        except KeyError as e:
            raise KeyError("Key was not found. Error: {}. Aborting server".format(e))
        except ValueError as e:
            raise ValueError("Key could not be parsed. Error: {}. Aborting server".format(e))
        
        return config_params	        

    def parse_from_file(self, file):
        config_params = {}

        with open(file, 'r') as f:
            config_params = json.load(f)
        
        return config_params
