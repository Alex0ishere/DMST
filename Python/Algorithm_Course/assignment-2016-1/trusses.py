import sys, copy, os.path, collections;
from itertools import combinations ;

		
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
  l_vertices = set(tuple([vertex for edge in p_graph for vertex in edge ]))
 # for edge in p_graph:
  #  for vertex in edge:
   #   l_vertices.add(vertex)
  return l_vertices

# return a hash of sets of neighbours vertices for each vertex of the given graph
def neighbours(p_graph):
  l_vertices = graph_vertices(p_graph)
  l_neighbours = {}
  for vertex in l_vertices:
    l_neighbours[vertex] = set() 
  for edge in p_graph:
    l_neighbours[edge[0]].add(edge[1])
    l_neighbours[edge[1]].add(edge[0])
  return l_neighbours

# Main algorithm. Returns the trusses 
def trusses(p_graph, p_number_of_trusses,p_mode='Max'):
  l_neighbours = neighbours(p_graph)
  l_bound = p_number_of_trusses - 2
  l_reduced_graph = [x for x in p_graph if not (len(set.intersection(l_neighbours[x[0]], l_neighbours[x[1]]))) < l_bound]
  
	#debugging
  d = {}
  for key, item in neighbours(l_reduced_graph).items():
	  d[int(key)] = item
  od = collections.OrderedDict(sorted(d.items()))
  for key,item in od.items():
    item = sorted([int(i) for i in item])
    #print (key,':', item)
  print ('')
	
	
  l_reduced_vertices = graph_vertices(l_reduced_graph)
  l_adj_list = neighbours(l_reduced_graph)
  l_reduced_neighbours = neighbours(l_reduced_graph)
  l_trusses = []
  l_possible_trusses = []
  if p_mode == 'Max':
   for vertex in l_reduced_vertices:
     l_possible_trusses.append((vertex,))
     excluded = []#
     for adj_vertex in l_adj_list[vertex]:	
       temp = l_possible_trusses[-1] + (adj_vertex,)
       if len(set.intersection(l_reduced_neighbours[vertex],l_reduced_neighbours[adj_vertex]).difference(excluded)) >= l_bound:
         l_possible_trusses[-1] = temp
       #else:
       #  excluded.append(adj_vertex)
       #if check_truss(l_reduced_neighbours, l_possible_trusses[-1], l_bound):
       #  l_trusses.append(l_possible_trusses[-1])
     #print(vertex,':',l_possible_trusses[-1],'without',excluded)
  elif p_mode == 'All':
    l_possible_trusses = sum([ list(combinations(l_reduced_vertices,i)) for i in range(len(l_reduced_vertices)+1) ],[])
		l_trusses = [truss for truss in l_possible_trusses if check_truss(l_reduced_neighbours, truss, l_bound) ]		
  else:
    print(p_mode,'is incorrect. Please try "Max" or "All". Program exits.')
    sys.exits()

  l_possible_trusses = [ (tuple(item) + tuple([key])) for key, item in l_reduced_neighbours.items() ]	

  l_test_trusses = {}
  l_test_possible_trusses = {}
  for test in l_possible_trusses:
    l_test_possible_trusses[test] = sum([ list(combinations(test,i)) for i in range(len(test)+1) ],[])
    l_test_trusses[test] = [truss for truss in l_test_possible_trusses[test]  if check_truss(l_reduced_neighbours, truss, l_bound) ]
    max = 2
    for i in l_test_trusses[test]:
      if len(i) > max:
        max = len(i)
    for i in copy.deepcopy(l_test_trusses[test]):
      if len(i) < max:
        l_test_trusses[test].remove(i)		
  #[print(t,':',i) for t,i in l_test_trusses.items()]
	#for test
  l_test = set()
  for i in l_test_trusses.values():
    l_test.update(i)
  #print('\n',order(l_test) )
	
  	
  #l_trusses = [tuple(truss) for truss in l_reduced_neighbours.values() if check_truss(l_reduced_neighbours, tuple(truss), l_bound) ]			
  #l_trusses = [truss for l_truss in l_possible_trusses for truss in return_truss(l_reduced_neighbours,l_truss,l_bound) ]
  #l_trusses = [truss for truss in l_trusses if check_truss(l_reduced_neighbours, truss, l_bound) ]
 
  return order(l_test)

# check if the input truss is a truss for the given bound and neighbours		
def return_truss(p_neighbours, p_truss, p_bound,p_level=1, p_mode='Maximal'):
  if len(p_truss) <= 1:
    return set(())
  l_trusses = set()
  valid = True
  for vertex1 in p_truss:   
    if len(set.intersection(p_neighbours[str(vertex1)], set(p_truss))) < p_bound:	
      valid = False
      l_truss = return_truss(p_neighbours, tuple_without(p_truss,vertex1),(p_level+1), p_bound)
      l_trusses.update(l_truss)

    #if valid:
    #  l_truss = tuple_without(p_truss,vertex1)
    #  for vertex2 in tuple_without(p_truss,vertex1):
    #    if len(set.intersection(p_neighbours[str(vertex1)], p_neighbours[str(vertex2)], set(p_truss))) < p_bound:
    #      valid = False
    #      l_trusses.update(return_truss(p_neighbours, l_truss, p_bound))
    #      l_trusses.update(return_truss(p_neighbours, tuple_without(p_truss, vertex2), p_bound))
  if p_level ==1:
    print ('DEBUG',p_truss,':',valid,l_trusses)	
  if valid:
    return set(tuple([p_truss])) 
  else:
    
    return l_trusses
  # if p_mode == 'Maximal':
   #   return l_trusses
  # else:
   #   return l_trusses	
  		
	
# check if the input truss is a truss for the given bound and neighbours		
def check_truss(p_neighbours, p_truss, p_bound):
  if len(p_truss) <= 1:
    return False
  for vertex in p_truss:
    l_truss = tuple_without(p_truss,vertex)
    for v in l_truss:
      if len(set.intersection(p_neighbours[str(vertex)], p_neighbours[str(v)], set(p_truss))) < p_bound:	
        #for subset_truss in sum([ list(combinations(p_truss,i)) for i in range(len(p_truss)+1) ],[]):
        #  check_truss(p_neighbours,subset_truss,p_bound)				
        return False	
  return True				
		
# Ordering the result	
def order(p_trusses):
  result = set()
  for truss in p_trusses:
    temp = []
    for i in truss:
      temp.append(int(i))
    result.add(tuple(sorted(temp)))
  return sorted(list(result))
	
# return a new tuple with an element removed
def tuple_without(original_tuple, element_to_remove):
    new_tuple = list(original_tuple)
    new_tuple.remove(element_to_remove)
    return tuple(new_tuple)
		
		
#main execution starts
#check that the parameters are valid
if len(sys.argv) < 3: 
	print('There are missing arguments. Program exits.')
	sys.exit()
else:
  input_file_name = sys.argv[1]
  try:
    input_number_of_trusses = int(sys.argv[2])
  except ValueError:
    print('The number of trusses is not integer. Program exits.')
    sys.exit()
		
if not os.path.isfile(input_file_name):
	print('The file',input_file_name,'does not exit. Program exits.')
	sys.exit()
elif (input_number_of_trusses == 1 or input_number_of_trusses == 0):
	print('Invalid number of trusses:',input_number_of_trusses)
	sys.exit()
else:
  # Messsage is commented to mantain the required output format
	#print ('The program begins to find the ' + str(input_number_of_trusses) + '-trusses in', input_file_name )
  pass	

# Main Execution starts 	
g_trusses = []
try:
  g_trusses = trusses(read_graph(input_file_name),input_number_of_trusses,sys.argv[3])
except IndexError:
  try:
    g_trusses = trusses(read_graph(input_file_name),input_number_of_trusses)
  except MemoryError:
    print ('Memory is limited.\n')
    #raise
except MemoryError:
  print ('Memory is limited.\n')
  #raise
except:	
  print ("Unexpected error:",sys.exc_info())
	
for truss in g_trusses:
  print (truss)