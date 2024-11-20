from concurrent import futures
import grpc
import logging
import numpy as np
import pickle
import signData_pb2_grpc
import signData_pb2

model_dict = pickle.load(open('models/model.p', 'rb'))
model = model_dict['model']

labels_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: '0'}

class SignDataServer(signData_pb2_grpc.StreamDataServiceServicer):
    def biDirectionalStream(self, request, context):
        try:
            prediction = model.predict([np.asarray(request.data)])
            predicted_character = labels_dict[int(prediction[0])]
            if isinstance(predicted_character, str):
                return signData_pb2.ResponseMessage(reply=f"{predicted_character}")
        except Exception as e:
            print(f"Error: {e}")

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