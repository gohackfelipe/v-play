from troposphere import Output, Ref, Tags, Template
from troposphere.ec2 import PortRange, NetworkAcl, Route, VPCGatewayAttachment, \
    VPC, NetworkAclEntry, InternetGateway

template = Template()

template.add_description("Service VPC")

template.add_metadata({
    "DependsOn": [],
    "Environment": "Development",
    "StackName": "Development-VPC",
})

internet_gateway = template.add_resource(InternetGateway(
    "InternetGateway",
    Tags=Tags(
        Environment="Development", Name="Development-InternetGateway")
))

vpc = template.add_resource(
    VPC(
        'VPC',
        CidrBlock='10.0.0.0/16',
        EnableDnsHostnames="true",
        EnableDnsSupport="true",
        InstanceTenancy="default",
        Tags=Tags(
            Environment="Development", Name="Development-ServiceVPC")))

gateway_attachment = template.add_resource(VPCGatewayAttachment(
    "VpcGatewayAttachment",
    VpcId=Ref("VPC"),
    InternetGatewayId=Ref("InternetGateway"),
))

network_acl = template.add_resource(
    NetworkAcl(
        'VpcNetworkAcl',
        VpcId=Ref(vpc),
        Tags=Tags(
            Environment="Development", Name="Development-NetworkAcl"),
    ))

VpcNetworkAclInboundRule = template.add_resource(
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

network_acl_outbound_rule = template.add_resource(
    NetworkAclEntry(
        'VpcNetworkAclOutboundRule',
        NetworkAclId=Ref(network_acl),
        RuleNumber=200,
        Protocol='6',
        Egress='true',
        RuleAction='allow',
        CidrBlock='0.0.0.0/0',
    ))

# Outputs
template.add_output([
    Output('InternetGateway', Value=Ref(internet_gateway)),
    Output('VPCID', Value=Ref(vpc))
])

print(template.to_json())
