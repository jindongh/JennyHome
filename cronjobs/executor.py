import json

from .models import Workflow
from .steps import StepManager

class Executor:
    def __init__(self, workflowId):
        self.workflow = Workflow.objects.get(pk=workflowId)

    def execute(self, params):
        steps = json.loads(self.workflow.data)

