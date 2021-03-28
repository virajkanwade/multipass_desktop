import configparser
import grpc
import json

from . import multipass_pb2
from . import multipass_pb2_grpc


INSTANCE_STATUS = {k: v.name for k, v in multipass_pb2._INSTANCESTATUS_STATUS.values_by_number.items()}


class MutlipassGRpcClient():
    def __init__(self, ini_path):
        config = configparser.ConfigParser()
        config.read(ini_path)

        grpc_server = config['multipass']['grpc_server']
        grpc_cert = config['multipass']['grpc_cert']
        self.instances_info_fname = config['multipass']['instances_info']

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
        _instance_info = {'name': instance_name}

        static_info = {}
        with open(self.instances_info_fname) as fp:
            static_info = json.load(fp).get(instance_name)

        _instance_info['deleted'] = static_info['deleted']
        _instance_info['cpu'] = static_info['num_cores']
        _instance_info['mac_addr'] = static_info['mac_addr']
        _instance_info['memory'] = static_info['mem_size']
        _instance_info['disk'] = static_info['disk_space']

        info_req = multipass_pb2.InfoRequest(
            instance_names=multipass_pb2.InstanceNames(
                instance_name=[instance_name, ]
            )
        )
        resp = self.stub.info(info_req)

        for r in resp:
            for i in r.info:
                print('current_release', i.current_release)
                print('disk_total', i.disk_total)
                print('disk_usage', i.disk_usage)
                print('memory_total', i.memory_total)
                print('memory_usage', i.memory_usage)
                print('mount_info', i.mount_info)
                _instance_info['release'] = i.image_release
                _instance_info['status'] = INSTANCE_STATUS[i.instance_status.status]
                _instance_info['ipv4'] = i.ipv4
                _instance_info['ipv6'] = i.ipv6
                _instance_info['load'] = i.load

        return _instance_info

    def start_instance(self, instance_name):
        print('Starting', instance_name)
        start_req = multipass_pb2.StartRequest(
            instance_names=multipass_pb2.InstanceNames(
                instance_name=[instance_name, ]
            )
        )

        resp = self.stub.start(start_req)

        for r in resp:
            print(r)

    def stop_instance(self, instance_name):
        print('Stopping', instance_name)
        stop_req = multipass_pb2.StopRequest(
            instance_names=multipass_pb2.InstanceNames(
                instance_name=[instance_name, ]
            )
        )

        resp = self.stub.stop(stop_req)

        for r in resp:
            print(r)
