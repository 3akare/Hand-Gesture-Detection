const grpc = require("@grpc/grpc-js")
const protoLoader = require("@grpc/proto-loader")
const packageDef = protoLoader.loadSync("todo.proto", {});
const grpcObject = grpc.loadPackageDefinition(packageDef);
const todoPackage = grpcObject.todoPackage;

const client = new todoPackage.Todo("localhost:8080", grpc.credentials.createInsecure())

// Unary
client.createTodo({
    "id": -1,
    "text": "Find the dog"
}, (err, response)=>{
    console.log(response);
})

client.readTodos({}, (err, response)=>{
    console.log(response);
})

// Server Streaming
const call = client.readTodosStream();
call.on("data", item => {
    console.log(item)
})
call.on("end", e => console.log("Ended"));