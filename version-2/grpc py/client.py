import  todo_pb2_grpc
import  todo_pb2
import grpc
import logging

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = todo_pb2_grpc.TodoStub(channel)
        response = stub.createTodo(todo_pb2.TodoItem(id=-1, text="Clean the Dishes"))
        response2 = stub.readTodos(todo_pb2.voidNoParam())
    print(response2)


if __name__ == "__main__":
    logging.basicConfig()
    run()