from concurrent import futures
import logging
import  todo_pb2_grpc
import  todo_pb2
import grpc

class Greeter(todo_pb2_grpc.TodoServicer):
    todos = []
    def createTodo(self, request, context):
        print("create todo")
        return todo_pb2.TodoItem(text=f"{request.text}", id=len(self.todos))
    def readTodos(self, request, context):
        print("read todos")
        return todo_pb2.TodoItems(items=[
    todo_pb2.TodoItem(text="Task 1", id=1),
    todo_pb2.TodoItem(text="Task 2", id=2),
])

def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    todo_pb2_grpc.add_TodoServicer_to_server(Greeter(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()