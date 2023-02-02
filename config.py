import json
import os
import time

class Config():
    def __init__(self, json_config_file="config.json"):

        self.json_config_file = json_config_file

        if not os.path.exists(self.json_config_file):
            
            print(f"Do not exist {self.json_config_file}. Create file ...")

            current_data = {"created_time":  str(time.time())}

            self.data = current_data

            with open(json_config_file, "w") as f:
                json.dump(self.data, f, indent=4)

        else:
            try:
                with open(self.json_config_file) as f:
                    self.data = json.load(f)
            except json.decoder.JSONDecodeError:
                current_data = {"created_time":  str(time.time())}

                self.data = current_data

                with open(json_config_file, "w") as f:
                    json.dump(self.data, f, indent=4)


    def commit(self):
        with open(self.json_config_file, "w") as f:
            json.dump(self.data, f, indent= 4)

    def update(self, column):
        self.data.update(column)
        
        self.commit()

    def delete(self, keys):
        for key in keys:
            if key in self.data.keys():
                del self.data[key]
        
        self.commit()
    
    def __call__(self, key):
        return self.data[key]
        
