document.addEventListener("DOMContentLoaded", (event) => {
const protocol=window.location.protocol=== 'https:'? 'wss:' : 'ws:';
const form=document.getElementById('user_query_form');
const chatResponse=document.getElementById("chat-response")
    function websocketconnection(parameters) {
        return new WebSocket(protocol + '//'+'localhost:8000/' + parameters);
    }
    const websocketUser=websocketconnection('ws/chat/user/')
    const websocketGuest=websocketconnection('ws/chat/guest/')

    form.addEventListener('submit', (e)=>{
        e.preventDefault();
        const message= document.getElementById('user-query-text').value;
        const id=document.getElementById('who').value.trim();
        console.log(message);
        console.log(id);
        document.getElementById("user-query-text").value="";
        document.getElementById("user-query-text").focus();
        const queryTextContainer= document.createElement('div');
        queryTextContainer.classList.add('flex', 'justify-end');
        chatResponse.appendChild(queryTextContainer);
        const queryText=document.createElement('div');
        queryText.id='user-query';
        queryText.classList.add('bg-opacity-30','mt-4', 'bg-gray-800', 'text-white', 'mb-2', 'font-sans1', 'rounded-xl', 'break-words',	'py-2', 'px-4','max-w-sm','outline', 'outline-offset-2' ,'outline-blue-500');
        queryText.textContent=message;
        queryTextContainer.appendChild(queryText);
        if (id === 'guest') {
            websocketGuest.send(JSON.stringify({id, message}));

        }else{
            websocketUser.send(JSON.stringify({id, message}));

        }
    })
    websocketGuest.addEventListener('message', (e)=>{
        console.log("Recieved response from the server:", e.data)
        const messagefromserver=JSON.parse(e.data);
        const chatResponse=document.getElementById("chat-response");
        const conv_id = messagefromserver['conv_id'];
        let llm_container = document.getElementById(`llm-response_${conv_id}`);
        if (!messagefromserver.done) {
            if (!llm_container) {
                const llmresponseContainer = document.createElement('div');
                llmresponseContainer.classList.add('flex', 'justify-start');
                llm_container = document.createElement('div');
                llm_container.id = `llm-response_${conv_id}`;
                llm_container.classList.add('bg-opacity-30', 'mt-2', 'mb-2', 'bg-gray-800', 'text-white', 'break-words','font-sans1', 'rounded-lg', 'py-2', 'px-4', 'max-w-sm', 'outline', 'outline-offset-2', 'outline-cyan-500');
                llm_container.textContent = messagefromserver.message;
                llmresponseContainer.appendChild(llm_container);
                chatResponse.appendChild(llmresponseContainer);
            } else {
                llm_container.textContent += ' ' + messagefromserver.message;
            }
        }
    })
    websocketUser.addEventListener('message', (e) => {
        console.log("Received response from the server:", e.data);
        const messagefromserver = JSON.parse(e.data);
        const chatResponse = document.getElementById("chat-response");
        const conv_id = messagefromserver['conv_id'];
        let llm_container = document.getElementById(`llm-response_${conv_id}`);
        if (!messagefromserver.done) {
            if (!llm_container) {
                const llmresponseContainer = document.createElement('div');
                llmresponseContainer.classList.add('flex', 'justify-start');
                llm_container = document.createElement('div');
                llm_container.id = `llm-response_${conv_id}`;
                llm_container.classList.add('bg-opacity-30', 'mt-2', 'mb-2', 'bg-gray-800', 'text-white', 'font-sans1', 'rounded-lg', 'py-2', 'px-4', 'max-w-sm', 'break-words', 'overflow-y-auto', 'outline', 'outline-offset-2', 'outline-cyan-500');
                llm_container.textContent = messagefromserver.message;
                llmresponseContainer.appendChild(llm_container);
                chatResponse.appendChild(llmresponseContainer);
            } else {
                llm_container.textContent += ' ' + messagefromserver.message;
            }
        }
    });
});
