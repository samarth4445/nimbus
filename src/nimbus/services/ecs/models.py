from nimbus.utils import ClassUtility
from nimbus.services import constants as Constants

class ContainerDefinition:
    def __init__(self, image, name=None) -> None:
        self.name = name
        self.image = image
        self.cpu = 0
        self.portMappings = []
        self.essential = True
        self.environment = []
        self.mountPoints = []
        self.volumesFrom = []
    
    def to_dict(self):
        return ClassUtility.to_dict(self)
    
    def __str__(self):
        return self.to_dict()
    
class TaskDefinition:
    def __init__(self, **kwargs):
        self.containerDefinitions = [ContainerDefinition(**kwargs.get('containerDefinitions'))]
        self.cpu = kwargs.get('cpu')
        self.memory = kwargs.get('memory')
        self.family = kwargs.get('family') # PROJECTNAME_USER_ID
        self.requiresCompatibilities = None
        self.executionRoleArn = kwargs.get('executionRoleArn')
        self.networkMode = kwargs.get('networkMode')

    def to_dict(self):
        return ClassUtility.to_dict(self)

    def __str__(self):
        return self.to_dict()

class NetworkConfiguration:
    def __init__(self, subnets, assign_public_ip, security_groups) -> None:
        self.subnets = subnets
        self.assignPublicIp = assign_public_ip
        self.securityGroups = security_groups

    def to_dict(self):
        return ClassUtility.to_dict(self)

    def __str__(self):
        return self.to_dict()