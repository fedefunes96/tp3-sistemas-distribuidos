import os

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
