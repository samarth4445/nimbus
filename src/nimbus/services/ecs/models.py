from nimbus.utils import ClassUtility
from nimbus.services import constants as Constants

class ContainerDefinition:
    def __init__(self, image, container_name=None) -> None:
        self.name = container_name
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
        self.containerDefinitions = [kwargs.get('container_definition')]
        self.cpu = kwargs.get('cpu')
        self.memory = kwargs.get('memory')
        self.family = kwargs.get('family_name')
        self.requiresCompatibilities = None
        self.exectionRoleArn = kwargs.get('execution_role_arn')
        self.networkMode = kwargs.get('network_mode')

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