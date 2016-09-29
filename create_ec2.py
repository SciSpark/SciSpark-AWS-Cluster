import boto3
import time

ec2 = boto3.resource('ec2')

IMAGE_ID = 'ami-8278baef'

def get_instances_ips():
    return [instance.public_ip_address for instance in ec2.instances.filter()]

 
def create_master(image_id):
    userdata = '''#cloud-config
    runcmd:
    - [ sh, -c, "systemctl enable docker.service" ]
    - [ sh, -c, "systemctl start docker-storage-setup.service --ignore-dependencies" ]
    - [ sh, -c, "systemctl start docker.service --ignore-dependencies" ]
    - [ sh, -c, "docker pull mboustani/scispark_cluster_master" ]
    - [ sh, -c, "docker run -d --name scispark_master  -it -p 5050:5050 mboustani/scispark_cluster_master" ]
    '''
    ec2.create_instances(ImageId=image_id, \
                        MinCount=1, \
                        MaxCount=1, \
                        InstanceType='t2.large', \
                        SecurityGroups=['Spark_Cluster_Mesos'], \
                        KeyName='esip_workshop', \
                        UserData=userdata)


def create_slave(image_id, master_ip):
    userdata = '''#cloud-config
    runcmd:
    - [ sh, -c, "systemctl enable docker.service" ]
    - [ sh, -c, "systemctl start docker-storage-setup.service --ignore-dependencies" ]
    - [ sh, -c, "systemctl start docker.service --ignore-dependencies" ]
    - [ sh, -c, "docker pull mboustani/scispark_cluster_slave" ]
    - [ sh, -c, "docker run -d --name scispark_slave -it --privileged -e master_ip={0}:5050 mboustani/scispark_cluster_slave" ]
    '''.format(master_ip)

    ec2.create_instances(ImageId=image_id, \
                        MinCount=2, \
                        MaxCount=2, \
                        InstanceType='t2.large', \
                        SecurityGroups=['Spark_Cluster_Mesos'], \
                        KeyName='esip_workshop', \
                        UserData=userdata)

old_instances =  get_instances_ips()

create_master(IMAGE_ID)

time.sleep(2)

new_instances =  get_instances_ips()

while new_instances == old_instances:
    time.sleep(1)
    new_instances =  get_instances_ips()

master_ip = list(set(new_instances) - set(old_instances))[0]
print master_ip

create_slave(IMAGE_ID, master_ip)
    