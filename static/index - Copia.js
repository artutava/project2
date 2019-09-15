document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
     
    // get username
    

    room="main";

    // When connected, configure buttons
    socket.on('connect', () => {

        // Each button should emit a "submit vote" event
        document.querySelector('#send_button').onclick = () => {
            msg= document.querySelector('#message_field').value;
            socket.emit('incoming msg', {'msg': msg,'room': room});
            
            
            
        }
    });

    // When display messages come in
    socket.on('display_message', data => {
        const li = document.createElement('li');
        li.innerHTML = `Message: ${data.room} ${data.username} said: ${data.msg}`;
        document.querySelector('#chatbox').append(li);
        document.querySelector('#message_field').value = '';
        
    });

    
});