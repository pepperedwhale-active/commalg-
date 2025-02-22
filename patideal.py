def patideal(graph, n):
    def dfs(node, path):
        # If the path has exactly n vertices, add to results
        if len(path) == n:
            result.append(path[:])
            return
        # Explore neighbors
        for neighbor in graph.get(node, []):
            if neighbor not in path:  # Avoid revisiting nodes
                dfs(neighbor, path + [neighbor])

    result = []
    for start_node in graph:  # Try all nodes as starting points
        dfs(start_node, [start_node])
    return result



def ideal_to_M2_input(result):
    duplicates = []
    generatorlist = []
    for generator in result:
        if (''.join(sorted(generator))) in duplicates:
            pass
        else:
            generatorlist.append('*'.join(generator))
            duplicates.append(''.join(sorted(generator)))
    
    finalstring = f"betti res ideal({','.join(generatorlist)})"
    print(finalstring)
    return finalstring

# testgraph = {
#     'a' : ['b'],
#     'b' : ['a','c','d'],
#     'c' : ['b'] 
# }

# if __name__ == '__main__':
#     paths = patideal(graph, 3)
#     print(paths)
