import boto3
from nimbus.services.enums import ServiceEnum
from nimbus.services import constants as Constants
from nimbus.services.ecs import TaskDefinition, NetworkConfiguration

class ElasticContainerService:
    def __init__(self, cluster_name: str, launch_type: str) -> None:
        self.cluster_name = cluster_name
        self.client = boto3.client(ServiceEnum.ECS.value, region_name=Constants.AWS_REGION)
        self.launch_type = launch_type

    def create_cluster(self):
        return self.client.create_cluster(clusterName=self.cluster_name)

    def delete_cluster(self):
        return self.client.delete_cluster(cluster=self.cluster_name)
    
    def task_register(self, task_definition: TaskDefinition):
        task_definition.requiresCompatibilities = [self.launch_type]
        response =  self.client.register_task_definition(**task_definition.to_dict())
        return response

    def task_deregister(self, task_arn):
        return self.client.deregister_task_definition(taskDefinition=task_arn)

    def task_run(self, task_arn, network_configuration: NetworkConfiguration):
        return self.client.run_task(cluster=self.cluster_name, 
                                    taskDefinition=task_arn,
                                    launchType=self.launch_type,
                                    count=Constants.COUNT,
                                    networkConfiguration={
                                        'awsvpcConfiguration': network_configuration.to_dict()
                                    })
    
    def task_stop(self, task_arn):
        return self.client.stop_task(cluster=self.cluster_name, task=task_arn)
