rooms={'main':{'users':['artur','jam'],'messages':[{'user':'artur', 'msg':'hello'},{'user':'julia', 'msg':'bye'}]}}
#
#if 'user' in rooms:
 #   print('user in rooms')
#if 'main' in rooms:
 #   print('main in rooms')

room_users=rooms['main']['users']
print(room_users)

current_room_msg= rooms['main']['messages']
print(current_room_msg)

for each in current_room_msg:
    print(each.get('user'),'said:', each.get('msg'))