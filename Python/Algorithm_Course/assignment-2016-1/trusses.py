import sys, copy, os.path, collections;

def tuple_without(original_tuple, element_to_remove):
    new_tuple = []
    for s in list(original_tuple):
        if not s == element_to_remove:
            new_tuple.append(s)
    return tuple(new_tuple)
		
		
		
#method to read file and create a list of edges representing the graph
def read_graph(p_filename):
    l_graph = []
    with open(p_filename) as graph_file:
        for line in graph_file:
            parts = line.rstrip().split(' ')
            l_graph.append(parts)
    return l_graph

# return a set of vertices for the graph
def graph_vertices(p_graph):
  l_vertices = set()
  for edge in p_graph:
    for vertex in edge:
      l_vertices.add(vertex)
  return l_vertices

# return a hash of sets of neighbours vertices for each vertex of the given graph
def neighbours(p_graph):
  l_neighbours = {}
  l_vertices = graph_vertices(p_graph)
  for main_vertex in l_vertices:
    l_neighbours[main_vertex] = set()
    for vertex in l_vertices:
      l_edge = set([vertex,main_vertex])
      for edge in p_graph:
        if l_edge == set(edge):
          l_neighbours[main_vertex].add(vertex)
          break
  return l_neighbours

# Main algorithm. Returns the trusses 
def reduce_graph(p_graph,p_number_of_trusses):
  l_graph = copy.deepcopy(p_graph)
  l_neighbours = neighbours(p_graph)
  l_int = p_number_of_trusses - 2
  #for edge in l_graph:
    #print('For',edge,'we have the following neighbours')
    #print(l_neighbours[edge[0]])
    #print(l_neighbours[edge[1]])
    #print(l_neighbours[edge[0]].intersection(l_neighbours[edge[1]]))
    #if (len(set.intersection(l_neighbours[edge[0]],l_neighbours[edge[1]]))) < l_int:
      #print('Removing edge', edge)
     # l_graph.remove(edge)
  l_graph[:] = [x for x in l_graph if not (len(set.intersection(l_neighbours[x[0]],l_neighbours[x[1]]))) < l_int]
  #debugging
  d = {}
  for key, item in adjacency_list(l_graph).items():
	  d[int(key)] = item
  od = collections.OrderedDict(sorted(d.items()))
  for key,item in od.items():
    print (key,':', sorted([int(i) for i in item]))
  print ('')
	
	
  l_reduced_vertices = graph_vertices(l_graph)
  l_adj_list = adjacency_list(l_graph)
  l_reduced_neighbours = neighbours(l_graph)
  l_trusses = []
  for vertex in l_reduced_vertices:
    l_trusses.append((vertex,))
    for adj_vertex in l_adj_list[vertex]:	
      #print('vertex:',vertex,'adj vertex',adj_vertex,l_reduced_neighbours[vertex],l_reduced_neighbours[adj_vertex])
      if (len(l_reduced_neighbours[vertex].intersection(l_reduced_neighbours[adj_vertex])) >= p_number_of_trusses -2):
        l_trusses[-1] = l_trusses[-1] + (adj_vertex,)
	
  tr = copy.deepcopy(l_trusses)
  for truss in tr:
    temp_tr = copy.deepcopy(truss)
    if len(truss) == 1:
      l_trusses.remove(truss)
    for vertex in temp_tr:
      temp_tr = tuple_without(temp_tr,vertex)
      for v in temp_tr:
        #print ('-----------------------')
        #print('Truss:',set(truss),'v1:',vertex,'v2:',v,'N',vertex,':',l_reduced_neighbours[str(vertex)],'N',v,':',l_reduced_neighbours[str(v)])
        #print('N',vertex,'+','v:',l_reduced_neighbours[str(vertex)].intersection(l_reduced_neighbours[str(v)]),set.intersection(l_reduced_neighbours[str(vertex)],l_reduced_neighbours[str(v)],set(truss)))
        if len(set.intersection(l_reduced_neighbours[str(vertex)],l_reduced_neighbours[str(v)],set(truss))) < l_int:
          try:
            l_trusses.remove(truss)	
          except:
            continue				
					
  return order(l_trusses)
	  
# Ordering the result	
def order(p_trusses):
  result = set()
  for truss in p_trusses:
    temp = []
    for i in truss:
      temp.append(int(i))
    result.add(tuple(sorted(temp)))
  return sorted(list(result))
  
def adjacency_list(p_graph):
  l_edges = {}
  for vertex in graph_vertices(p_graph):
    ######int_vertex = int(vertex)
    l_edges[vertex] = []
    for edge in p_graph:
      if edge[0] == vertex:
        l_edges[vertex].append(edge[1])
      elif edge[1] == vertex:	
        l_edges[vertex].append(edge[0])
    # 	l_edges[vertex].sort()		
    #od = collections.OrderedDict(sorted(l_edges.items()))
  return l_edges
	
#main execution starts
#check that the parameters are valid
if len(sys.argv) != 3: 
	print('There are missing arguments. Program exits')
	sys.exit()
else:
  input_file_name = sys.argv[1]
  try:
    input_number_of_trusses = int(sys.argv[2])
  except ValueError:
    print('The number of trusses is not integer. Program exits')
    sys.exit()
		
if not os.path.isfile(input_file_name):
	print('The file',input_file_name,'does not exit. Program exits')
	sys.exit()
elif (input_number_of_trusses == 1 or input_number_of_trusses == 0):
	print('Invalid number of trusses:',input_number_of_trusses)
	sys.exit()
else:
	print ('The program begins to find the ' + str(input_number_of_trusses) + '-trusses in', input_file_name )
	
g_graph = read_graph(input_file_name)
#print(g_graph)
g_vertices = graph_vertices(g_graph)
#print (g_vertices)
g_neighbours = neighbours(g_graph)
#for vertex in g_vertices:
 # print(vertex, ':',g_neighbours[vertex])
for tuple in reduce_graph(g_graph,input_number_of_trusses):
  print (tuple)