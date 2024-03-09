import boto3 # Import AWS SDK for Python
import datetime # Work with time and dates in Python

# Initialize a session using Amazon EC2
session = boto3.session.Session() # Manage configurations and create service clients
ec2 = session.client('ec2') # Initialize Amazon EC2 interaction
cloudwatch = session.client('cloudwatch') # Client for CloudWatch used to retrieve monitoring data


# Get CPU Utilization
def getCPUUtilization(instance_id, period=300, interval=30):
    endTime = datetime.datetime.utcnow()
    startTime = endTime - datetime.timedelta(minutes=interval)

    metrics = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
        StartTime=startTime,
        EndTime=endTime,
        Period=period,
        Statistics=['Average']
    )

    cpu_utilization = metrics['Datapoints'][0]['Average'] if metrics['Datapoints'] else None
    if cpu_utilization is None:
        print("No data available for the specified time range.")
    else:
        print(f'CPU Utilization for instance {instance_id}: {cpu_utilization}%')


# Example usage
instance_id = 'i-09a1dd3978dc9a1aa'  # Replace with your actual instance ID
cpu_utilization = getCPUUtilization(instance_id)
print(f'CPU Utilization for instance {instance_id}: {cpu_utilization}%')