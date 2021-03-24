Check /Library/Logs/Multipass/multipassd.log for gRPC information.
In my case it was unix:/var/run/multipass_socket

Update config.ini with appropriate paths for gRpc server and localhost certificate.


Note:
gRpc protocol definition:

curl -O https://raw.githubusercontent.com/canonical/multipass/4ebba1f7029aa5b80443d56f37a0060e9719a5f0/src/rpc/multipass.proto
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. multipass.proto

in multipass_pb2_grpc.py replace
import multipass_pb2 as multipass__pb2
with
from . import multipass_pb2 as multipass__pb2
