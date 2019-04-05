from troposphere import Base64, FindInMap, GetAtt, Join, Output
from troposphere import Parameter, Ref, Tags, Template
from troposphere.autoscaling import Metadata
from troposphere.ec2 import PortRange, NetworkAcl, Route, \
    VPCGatewayAttachment, SubnetRouteTableAssociation, Subnet, RouteTable, \
    VPC, NetworkInterfaceProperty, NetworkAclEntry, \
    SubnetNetworkAclAssociation, EIP, Instance, InternetGateway, \
    SecurityGroupRule, SecurityGroup
from troposphere.policies import CreationPolicy, ResourceSignal
from troposphere.cloudformation import Init, InitFile, InitFiles, \
    InitConfig, InitService, InitServices

template = Template()

template.add_description("Service VPC")
template.add_metadata({
    "DependsOn": [],
    "Environment": "Development",
    "StackName": "Development-VPC",
})

ref_stack_id = Ref('AWS::StackId')

internetgateway = template.add_resource(InternetGateway(
    "InternetGateway",
    Tags=Tags(
        Environment="Development", Name="Development-InternetGateway")
))

VPC = template.add_resource(
    VPC(
        'VPC',
        CidrBlock='10.0.0.0/16',
        EnableDnsHostnames="true",
        EnableDnsSupport="true",
        InstanceTenancy="default",
        Tags=Tags(
            Environment="Development", Name="Development-ServiceVPC")))

gatewayattachment = template.add_resource(VPCGatewayAttachment(
    "GatewayAttachment",
    VpcId=Ref("VPC"),
    InternetGatewayId=Ref("InternetGateway"),
))

networkAcl = template.add_resource(
    NetworkAcl(
        'NetworkAcl',
        VpcId=Ref(VPC),
        Tags=Tags(
            Environment="Development", Name="Development-NetworkAcl"),
    ))

VpcNetworkAclInboundRule = template.add_resource(
    NetworkAclEntry(
        'VpcNetworkAclInboundRule',
        NetworkAclId=Ref(networkAcl),
        RuleNumber='100',
        Protocol='6',
        PortRange=PortRange(To='443', From='443'),
        Egress='false',
        RuleAction='allow',
        CidrBlock='0.0.0.0/0',
    ))

VpcNetworkAclOutboundRule = template.add_resource(
    NetworkAclEntry(
        'VpcNetworkAclOutboundRule',
        NetworkAclId=Ref(networkAcl),
        RuleNumber='200',
        Protocol='6',
        Egress='true',
        RuleAction='allow',
        CidrBlock='0.0.0.0/0',
    ))

print(template.to_json())
