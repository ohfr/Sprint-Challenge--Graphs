from room import Room
from player import Player
from world import World

import random
from os import path
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "projects/adventure/maps/test_line.txt"
# map_file = "projects/adventure/maps/test_cross.txt"
# map_file = "projects/adventure/maps/test_loop.txt"
# map_file = "projects/adventure/maps/test_loop_fork.txt"
map_file = "projects/adventure/maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(path.abspath(map_file), "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

def bfs(room, graph):
    q = []
    q.append([room.id])

    visited = set()

    while len(q) > 0:
        curPath = q.pop()

        cur = curPath[-1]

        if cur not in visited:
            visited.add(cur)
            if graph[cur]:
                for exits in graph[cur]:
                    if graph[cur][exits] == '?':
                        return curPath
                    else:
                        if graph[cur][exits] not in visited:
                            tempPath = list.copy(curPath)
                            tempPath.append(graph[cur][exits])
                            q.append(tempPath)
    return None
        
traversal_path = []

def backtrack(start_room,path, graph):
    # print('startroom', start_room)
    # print('path', path)
    path.pop(0)
    room = start_room
    while len(path) > 0:
        cur = path.pop(0)
        for tup in graph[room].items():
            if cur == tup[1]:
                traversal_path.append(tup[0])
                player.travel(tup[0])
        room = cur
    # print('current',player.current_room.id)
        


# Fill this out with directions to walk
# traversal_path = ['n', 'n']

dftStack = []

dftStack.append(player.current_room)
visited = {}
loop = True
while len(dftStack) > 0 and loop:
    cur = dftStack.pop()

    exits = cur.get_exits()

    print('current room', cur.id)

    if exits:
        if cur.id not in visited:
            visited[cur.id] = {}
            for path in exits:
                visited[cur.id][path] = '?'

            traversal_path.append(exits[-1])
            player.travel(exits[-1])
            dftStack.append(player.current_room)
            visited[cur.id][exits[-1]] = player.current_room.id

            visited[player.current_room.id] = {}
            for paths in player.current_room.get_exits():
                  visited[player.current_room.id][paths] = '?'

            if exits[-1] == 'n':
                visited[player.current_room.id]['s'] = cur.id
            elif exits[-1] == 'e':
                visited[player.current_room.id]['w'] = cur.id
            elif exits[-1] == 'w':
                visited[player.current_room.id]['e'] = cur.id
            elif exits[-1] == 's':
                visited[player.current_room.id]['n'] = cur.id
                
        else:
            print("hit else", cur.id)
            i = -1
            randomChoice = exits[i]
            while visited[cur.id][randomChoice] != '?':
                if i == len(exits)-1:
                    break
                randomChoice = exits[i]
                i+=1

            if visited[cur.id][randomChoice] == '?':
                traversal_path.append(randomChoice)
                player.travel(randomChoice)
                dftStack.append(player.current_room)
                visited[cur.id][randomChoice] = player.current_room.id
                
                if player.current_room.id not in visited:
                    visited[player.current_room.id] = {}
                    for paths in player.current_room.get_exits():
                        visited[player.current_room.id][paths] = '?'

                if randomChoice == 'n':
                    visited[player.current_room.id]['s'] = cur.id
                elif randomChoice == 'e':
                    visited[player.current_room.id]['w'] = cur.id
                elif randomChoice == 'w':
                    visited[player.current_room.id]['e'] = cur.id
                elif randomChoice == 's':
                    visited[player.current_room.id]['n'] = cur.id                    
            else:
                # print("currently couldnt get the path", cur.id)
                path = bfs(cur, visited)

                print(path, cur.id, 'path')

                if path:
                    backtrack(player.current_room.id, path, visited)
                    dftStack.append(player.current_room)
                else:
                    loop = False
                    break
    else:
        path = bfs(cur, visited)

        if path:
            print("backtracked else")
            dftStack.append(player.current_room)
        else:
            print('no backtrack else')
            loop = False
            break



print('traversal path', traversal_path)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
