"""The Python implementation of the melo rpc client."""

from __future__ import print_function

import grpc

import melo_rpc_pb2
import melo_rpc_pb2_grpc


def rpc_pause():
    channel = grpc.insecure_channel('localhost:14167')
    stub = melo_rpc_pb2_grpc.MeloRpcStub(channel)
    try:
        response = stub.Pause(melo_rpc_pb2.PauseRequest(message=''))
        print("Response from melo rpc server for pause: " + ("success" if response.result else "failed"))
    except:
        print("Cannot connected to melo server for pause request")

        
def rpc_resume():
    channel = grpc.insecure_channel('localhost:14167')
    stub = melo_rpc_pb2_grpc.MeloRpcStub(channel)
    try:
        response = stub.Resume(melo_rpc_pb2.ResumeRequest(message=''))
        print("Response from melo rpc server for resume: " + ("success" if response.result else "failed"))
    except:
        print("Cannot connected to melo server for resume request")

# if __name__ == '__main__':
    # for i in range(5):
        # test1()
        # test2()
