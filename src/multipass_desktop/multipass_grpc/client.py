import configparser
import grpc

from . import multipass_pb2
from . import multipass_pb2_grpc


INSTANCE_STATUS = {k: v.name for k, v in multipass_pb2._INSTANCESTATUS_STATUS.values_by_number.items()}


class MutlipassGRpcClient():
    def __init__(self, ini_path):
        config = configparser.ConfigParser()
        config.read(ini_path)

        grpc_server = config['multipass']['grpc_server']
        grpc_cert = config['multipass']['grpc_cert']

        with open(grpc_cert, 'rb') as fp:
            creds = grpc.ssl_channel_credentials(fp.read())

        self.channel = grpc.secure_channel(grpc_server, creds)
        self.stub = multipass_pb2_grpc.RpcStub(self.channel)

    def instances_list(self):
        list_req = multipass_pb2.ListRequest()
        list_req.request_ipv4 = False
        resp = self.stub.list(list_req)

        _instances = []

        for list_reply in resp:
            # _instances.extend(list_reply.instances)
            for instance in list_reply.instances:
                _instances.append({
                    'name': instance.name,
                    'release': instance.current_release,
                    'status': INSTANCE_STATUS[instance.instance_status.status]
                })

        return _instances

    def instance_info(self, instance_name):
        info_req = multipass_pb2.InfoRequest(
            instance_names=multipass_pb2.InstanceNames(
                instance_name=[instance_name, ]
            )
        )
        resp = self.stub.info(info_req)

        for r in resp:
            print(r)
