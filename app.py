import click, logging, os, errno

from troposphere import Output, Ref, Tags, Template
from troposphere.ec2 import PortRange, NetworkAcl, Route, VPCGatewayAttachment, \
    VPC, NetworkAclEntry, InternetGateway

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')

@click.command()
@click.option("--env", default='development', help="Cloud enviroment name")
@click.option("--output", help="The output directory. If not informed, the content will be show at screen")

def generate(env, output):
    """Cloud Platform, Viaplay \n
       Simple program that generates the cloudformation to cloud environment context. \n
       Written by Felipe Ribeiro <emaildofeliperibeiro@gmail.com>, April 2019 \n
       Github: https://github.com/gohackfelipe/v-play
    """
    
    logging.info('Initial configurations to create the cloudformation file.')

    template = Template()
    template.add_description("Service VPC")

    logging.info('Adding description on template')

    template.add_metadata({
        "DependsOn": [],
        "Environment": env,
        "StackName": '{}-{}'.format(env, 'VPC'),
    })

    logging.info('Adding metadata on template')

    internet_gateway = template.add_resource(InternetGateway(
        "InternetGateway",
        Tags=Tags(
            Environment=env, Name='{}-{}'.format(env, 'InternetGateway'))
    ))

    logging.info('Adding InternetGateway on template')

    vpc = template.add_resource(
        VPC(
            'VPC',
            CidrBlock='10.0.0.0/16',
            EnableDnsHostnames="true",
            EnableDnsSupport="true",
            InstanceTenancy="default",
            Tags=Tags(
                Environment=env, Name='{}-{}'.format(env, 'ServiceVPC'))))

    logging.info('Adding VPC on template')
                
    template.add_resource(VPCGatewayAttachment(
        "VpcGatewayAttachment",
        VpcId=Ref("VPC"),
        InternetGatewayId=Ref("InternetGateway"),
    ))

    logging.info('Adding VpcGatewayAttachment on template')

    network_acl = template.add_resource(
        NetworkAcl(
            'VpcNetworkAcl',
            VpcId=Ref(vpc),
            Tags=Tags(
                Environment=env, Name='{}-{}'.format(env, 'NetworkAcl')),
        ))
    
    logging.info('Creating Network ALC on template')

    template.add_resource(
        NetworkAclEntry(
            'VpcNetworkAclInboundRule',
            NetworkAclId=Ref(network_acl),
            RuleNumber=100,
            Protocol='6',
            PortRange=PortRange(To='443', From='443'),
            Egress='false',
            RuleAction='allow',
            CidrBlock='0.0.0.0/0',
        ))

    logging.info('Adding Network ALC Inbound Rule on template')
        
    template.add_resource(
        NetworkAclEntry(
            'VpcNetworkAclOutboundRule',
            NetworkAclId=Ref(network_acl),
            RuleNumber=200,
            Protocol='6',
            Egress='true',
            RuleAction='allow',
            CidrBlock='0.0.0.0/0',
        ))

    logging.info('Adding Network ALC Outbound Rule on template')

    # Outputs
    template.add_output([
        Output('InternetGateway', Value=Ref(internet_gateway)),
        Output('VPCID', Value=Ref(vpc))
    ])

    logging.info('Adding Output on template')

    if(not output):
        print(template.to_json())
        logging.info('Printing the cloudformation content on screen.')
    else:
        createFile(output, template.to_json())

def createFile(path_file, content):
    if not os.path.exists(os.path.dirname(path_file)):
        try:
            os.makedirs(os.path.dirname(path_file))
        except OSError as exc:
            logging.exception('An exception occurred')
            if exc.errno != errno.EEXIST:
                raise
                
        with open(path_file, "w") as f:
            f.write(content)
            logging.info('The file was created as {}'.format(path_file))
            f.close()

if __name__ == '__main__':
    generate()