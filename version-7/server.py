from concurrent import futures
from warnings import catch_warnings

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
            response_string = ""
            for gesture in request.data:
                prediction = model.predict([np.asarray(gesture.points)])
                predicted_character = labels_dict[int(prediction[0])]
                print(predicted_character)
                response_string += predicted_character
        except Exception:
            pass
        return signData_pb2.ResponseMessage(reply="""The sun awakens, soft and bright,
            Chasing away the fading night.
            The morning sings with chirping cheer,
            A gentle call, "The day is here."
            
            The breeze it whispers through the trees,
            Dancing lightly with the leaves.
            A song of calm, a sweet refrain,
            A touch of joy, a soft refrain.
            
            The clouds drift by, their shadows play,
            Upon the fields, where children stay.
            Their laughter rings, a happy tune,
            Beneath the warm embrace of noon.
            
            So listen close, the world’s alive,
            Each moment hums, each second thrives.
            A melody for all to hear,
            A voice that whispers, "Life is near.""")


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