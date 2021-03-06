# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import melo_rpc_pb2 as melo__rpc__pb2


class MeloRpcStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Pause = channel.unary_unary(
        '/melo.rpc.MeloRpc/Pause',
        request_serializer=melo__rpc__pb2.PauseRequest.SerializeToString,
        response_deserializer=melo__rpc__pb2.PauseResponse.FromString,
        )
    self.Resume = channel.unary_unary(
        '/melo.rpc.MeloRpc/Resume',
        request_serializer=melo__rpc__pb2.ResumeRequest.SerializeToString,
        response_deserializer=melo__rpc__pb2.ResumeResponse.FromString,
        )


class MeloRpcServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def Pause(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Resume(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_MeloRpcServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Pause': grpc.unary_unary_rpc_method_handler(
          servicer.Pause,
          request_deserializer=melo__rpc__pb2.PauseRequest.FromString,
          response_serializer=melo__rpc__pb2.PauseResponse.SerializeToString,
      ),
      'Resume': grpc.unary_unary_rpc_method_handler(
          servicer.Resume,
          request_deserializer=melo__rpc__pb2.ResumeRequest.FromString,
          response_serializer=melo__rpc__pb2.ResumeResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'melo.rpc.MeloRpc', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
