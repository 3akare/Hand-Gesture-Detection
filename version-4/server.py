from concurrent import futures
import logging
import  signData_pb2_grpc
import  signData_pb2
import grpc

class SignDataServer(signData_pb2_grpc.StreamDataServiceServicer):
    def biDirectionalStream(self, request, context):
        print(request.data)
        return signData_pb2.ResponseMessage(reply="received")

def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    signData_pb2_grpc.add_StreamDataServiceServicer_to_server(SignDataServer(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()