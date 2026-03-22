from typing import List, Dict, Optional, Any

# Graph looks like adjacency list except it also has values.
# a = {'a': (35, ['b']), 'b': (83, [])}
def bfs(start:Any, key:Any, grph: Dict) -> Optional[Any]:
    q = [start]
    visited = {}
    while len(q) > 0:
        first = q.pop(0)
        visited[first] = True
        if first == key:
            return grph[first][0]
        for neighbor in grph[first][1]:
            if neighbor not in visited:
                q.append(neighbor)
    return None
        
# TODO: Test this
    