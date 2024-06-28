// document.addEventListener("DOMContentLoaded", (event) => {
// const protocol=window.location.protocol=== 'https:'? 'wss:' : 'ws:';
// // Testing: protocol+'//'+""
// const ws= new WebSocket('wss://ws.postman-echo.com/raw ');
// const form=document.getElementById('user_query_form');
// const chatResponse=document.getElementById("chat-response")
//
//
//     form.addEventListener('submit', (e)=>{
//         e.preventDefault();
//         const message= document.getElementById('user-query-text').value;
//         const id=document.getElementById('who').value;
//         console.log(message);
//         console.log(id);
//         ws.send(JSON.stringify({id, message}));
//         document.getElementById("user-query-text").value="";
//         document.getElementById("user-query-text").focus();
//         const queryTextContainer= document.createElement('div');
//         queryTextContainer.classList.add('flex', 'justify-end');
//         chatResponse.appendChild(queryTextContainer);
//         const queryText=document.createElement('div');
//         queryText.id='user-query';
//         queryText.classList.add('bg-opacity-30', 'bg-gray-800', 'text-white', 'mb-2', 'font-sans1', 'rounded-xl', 'py-2', 'px-4','max-w-sm' ,'max-h-64', 'overflow-y-auto','outline', 'outline-offset-2' ,'outline-blue-500');
//         queryText.textContent=message;
//         queryTextContainer.appendChild(queryText);
//
//     })
//     ws.addEventListener('message', (e)=>{
//         console.log("Recieved response from the server:", e.data)
//         //we get the data, need to create a div
//         const messagefromserver=JSON.parse(e.data);
//         const chatResponse=document.getElementById("chat-response");
//         const llmresponseContainer=document.createElement('div');
//         llmresponseContainer.classList.add('flex', 'justify-start');
//         chatResponse.appendChild(llmresponseContainer);
//         const llmresponseText=document.createElement('div');
//         llmresponseText.id ='llm-response';
//         llmresponseText.classList.add('bg-opacity-30','mt-2','mb-2','bg-gray-800', 'text-white', 'font-sans1', 'rounded-lg', 'py-2', 'px-4', 'max-w-sm', 'max-h-64', 'overflow-y-auto', 'outline', 'outline-offset-2', 'outline-cyan-500');
//         llmresponseText.textContent=messagefromserver.message;
//         llmresponseContainer.appendChild(llmresponseText);
//         console.log(llmresponseText);
//         console.log(messagefromserver);
//
//     })
//
//
// });
//
//
//
// // TODO: element creation done, need to implement the local backend now
