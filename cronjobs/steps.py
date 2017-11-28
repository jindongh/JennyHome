class Step:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.input = {}
        self.output = {}
        self.params = {}

class HttpStep(Step):
    def __init__(self):
        Step.__init__(self, 'http', 'Http')

class ConditionStep(Step):
    def __init__(self):
        Step.__init__(self, 'condition', 'Condition')

class SMSStep(Step):
    def __init__(self):
        Step.__init__(self, 'sms', 'SMS')

class JSStep(Step):
    def __init__(self):
        Step.__init__(self, 'javaScript', 'JavaScript')

class StepManagerCls:
    def __init__(self):
        self.stepList = [
                HttpStep(),
                ConditionStep(),
                SMSStep()
                ]
    def getSteps(self):
        return self.stepList
    def getStep(self, stepId):
        for step in self.stepList:
            if step.id == stepId:
                return step
        return None

StepManager = StepManagerCls()
