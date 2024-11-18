const grpc = require("@grpc/grpc-js")
const protoLoader = require("@grpc/proto-loader")
const packageDef = protoLoader.loadSync("todo.proto", {});
const grpcObject = grpc.loadPackageDefinition(packageDef);
const todoPackage = grpcObject.todoPackage;


const server = new grpc.Server();
server.bindAsync("localhost:8080", grpc.ServerCredentials.createInsecure(), ()=>{
    console.log("server started")
    server.start();
})

server.addService(todoPackage.Todo.service,
    {
        "createTodo": createTodo,
        "readTodos": readTodos,
        "readTodosStream": readTodosStream,
    })

const todos = [ { id: 1, text: 'Find the dog' },
    { id: 2, text: 'Find the dog' },
    { id: 3, text: 'Find the dog' },
    { id: 4, text: 'Find the dog' },
    { id: 5, text: 'Find the dog' },
    { id: 6, text: 'Find the dog' },
    { id: 7, text: 'Find the dog' },
    { id: 8, text: 'Find the dog' },
    { id: 9, text: 'Find the dog' },
    { id: 10, text: 'Find the dog' },
    { id: 11, text: 'Find the dog' },
    { id: 12, text: 'Find the dog' },
    { id: 13, text: 'Find the dog' },
    { id: 14, text: 'Find the dog' },
]

function createTodo (call, callback) {
    const todoItem = {
        "id": todos.length + 1,
        "text": call['request']['text'],
    }
    todos.push(todoItem);
    callback(null, todoItem); // response
}

function readTodos (call, callback) {
    callback(null, {"items": todos})
}

function readTodosStream (call, callback) {
    todos.forEach(t => call.write(t));
    return call.end();
}
