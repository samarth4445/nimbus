import boto3
from nimbus.services.enums import ServiceEnum
from nimbus.services import constants as Constants
from nimbus.services.ecs import TaskDefinition, NetworkConfiguration
from nimbus.utils import Logger

class ElasticContainerService:
    def __init__(self, cluster_name: str, launch_type: str) -> None:
        self.cluster_name = cluster_name
        self.client = boto3.client(ServiceEnum.ECS.value, region_name=Constants.REGION_NAME)
        self.launch_type = launch_type
        self.logger = Logger().get_logger()

    def create_cluster(self):
        self.logger.info(f"Creating cluster {self.cluster_name}")
        response = self.client.create_cluster(clusterName=self.cluster_name)
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            self.logger.error(f"Failed to create cluster of name {self.cluster_name}")
            raise Exception(f"Failed to create cluster of name {self.cluster_name}")
        return response

    def delete_cluster(self):
        self.logger.info(f"Deleting cluster {self.cluster_name}")
        response = self.client.delete_cluster(cluster=self.cluster_name)
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            self.logger.error(f"Failed to delete cluster of name {self.cluster_name}")
            raise Exception(f"Failed to delete cluster of name {self.cluster_name}")
        return response
    
    def task_register(self, task_definition: TaskDefinition):
        task_definition.requiresCompatibilities = [self.launch_type]
        self.logger.info(f"Registering task definition {task_definition.family}")
        response =  self.client.register_task_definition(**task_definition.to_dict())
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            self.logger.error(f"Failed to register task definitionc of family {task_definition.family}")
            raise Exception(f"Failed to register task definition of family {task_definition.family}")
        return response

    def task_deregister(self, task_arn):
        self.logger.info(f"Deregistering task definition of ARN {task_arn}")
        response = self.client.deregister_task_definition(taskDefinition=task_arn)
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            self.logger.error(f"Failed to deregister task definition of ARN {task_arn}")
            raise Exception(f"Failed to deregister task definition of ARN {task_arn}")
        return response

    def task_run(self, task_arn, network_configuration: NetworkConfiguration):
        self.logger.info(f"Running task of ARN {task_arn}")
        response = self.client.run_task(cluster=self.cluster_name, 
                                    taskDefinition=task_arn,
                                    launchType=self.launch_type,
                                    count=Constants.COUNT,
                                    networkConfiguration={
                                        'awsvpcConfiguration': network_configuration.to_dict()
                                    })
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            self.logger.error(f"Failed to run task of ARN {task_arn}")
            raise Exception(f"Failed to run task of ARN {task_arn}")
        return response
    
    def task_stop(self, task_arn):
        self.logger.info(f"Stopping task of ARN {task_arn}")
        response = self.client.stop_task(cluster=self.cluster_name, task=task_arn)
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            self.logger.error(f"Failed to stop task of ARN {task_arn}")
            raise Exception(f"Failed to stop task of ARN {task_arn}")
        return response

    def describe_tasks(self):
        task_arns = self.client.list_tasks(cluster=self.cluster_name).get('taskArns', [])
        response = self.client.describe_tasks(cluster=self.cluster_name, tasks=task_arns)
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            self.logger.error(f"Failed to get description tasks of cluster {self.cluster_name}")
            raise Exception(f"Failed to get description tasks of cluster {self.cluster_name}")
        return response