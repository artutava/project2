document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
     
    // get username
    

    

    // When connected, configure buttons
    socket.on('connect', () => {

        // send message
        document.querySelector('#message_form').onsubmit = () => {
            msg= document.querySelector('#message_field').value;
            socket.emit('incoming msg', {'msg': msg});
            return false;
            
            
        }


        // button for creating room
        document.querySelector('#room_form').onsubmit = () => {
            room_name= document.querySelector('#cr_room_name').value;
            socket.emit('create room', {'room_name': room_name});
            return false;
            
            
        }
        // click to join room
        document.querySelectorAll('.room_click').forEach(button => {
            button.onclick = () => {
                const room_selection = button.dataset.channel;
                socket.emit('join room', {'room_selection': room_selection});
            };
        });
    });

    // When display messages come in
    socket.on('display_message', data => {
        const li = document.createElement('li');
        li.innerHTML = `<span class="usermark"> ${data.username} </span> <span class="time"> ${data.hour} </span> </br> <span class="usermessage"> ${data.msg} </span> `;
        document.querySelector('#chatbox').append(li);
        document.querySelector('#message_field').value = '';
        const smsg = document.querySelector('#chat_scroll');
        smsg.scrollTop = smsg.scrollHeight;
        
    });

    //automatic scroll, when loaded page
    const smsg = document.querySelector('#chat_scroll');
    const sbox = document.querySelector('#chatbox');
    if (sbox > smsg) {
        smsg.scrollTop = smsg.scrollHeight;

    }
    

    // When room info come
    socket.on('insert_room', data => {
        new_room_name=data.new_room;
        const li = document.createElement('li');
        li.className = 'room_click';
        li.innerHTML = new_room_name;
        li.dataset.channel = new_room_name;
        document.querySelector('#roomsbox').append(li);
        document.querySelector('#cr_room_name').value = '';
        window.location.reload();
        
        
    });

    // When room info come
    socket.on('change room', data => {
        window.location.reload();
        
    });


    

    
});