import json
import os

from jinja2 import Template

class AnomalyDetector():
    def __init__(self, samples):
        self.samples = samples

    current_directory = os.path.dirname(os.path.abspath(__file__))
    assets_directory = os.path.join(current_directory, '../../assets')
    file_path = os.path.join(assets_directory, 'triggers.json')

    with open(file_path, 'r') as f:
        triggers = json.load(f)

    def evaluate_triggers(self):
        results = {}
        for trigger in self.triggers['triggers']:
            for condition in trigger['conditions']:
                trigger_name = trigger['name']
                template = Template(condition)
                rendered_condition = template.render(samples=self.samples)
                results[trigger_name] = rendered_condition

        return results