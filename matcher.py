#! /usr/bin/python
import networkx as nx,sys
import math
import copy
def conv_to_numbers( minutiaes ) :
	numbers = []
	for m in minutiaes :
		numbers.append( [  int( mi ) for mi in m ] )
		
	return numbers

def sort_2d( minutiaes ) :
	minutiaes.sort( key=lambda x: x[1] )
	return minutiaes

def calculate_angle( minutiaes1,minutiaes2 ) :

	angle = (180.0/math.pi )*math.atan( ( minutiaes1[1]-minutiaes2[1] )/( minutiaes1[0]-minutiaes2[0]+0.000000001 ) )

	if angle < 0 :
		return 180+angle
	return angle
def euclidean_distance( p1,p2 ) :
	return math.sqrt( (p2[0]-p1[0])**2 + ( p2[1]-p1[1] )**2 )

def build_intra_table( minutiaes ) :
	iptable = []
	for i in range( len(minutiaes )-1 ) :
		k = i+1
		for j in range( k,len(minutiaes) ) :
			##print minutiaes[i],minutiaes[k]
			##print '(i,j) : ( %d,%d )'%(i,j)
			distance = euclidean_distance( minutiaes[i][ 0:2 ],minutiaes[j][ 0:2 ] )
			##print 'dist is : ',distance
			if distance > 40 :
				continue
			angle_of_line = calculate_angle( minutiaes[i][ 0:2 ],minutiaes[j][ 0:2 ] )

			
			beta1 = minutiaes[i][2] - angle_of_line
			beta2 = minutiaes[j][2] - angle_of_line

			if beta1 < beta2 :
				iptable.append( ( distance, beta1,beta2,i,j ) )
			else :
				iptable.append( ( distance, beta2,beta1,j,i ) )

	return iptable



def use_entry( index_list,li ) : #return first Not-None value
	""" Returns the first value that is not None """
	for i in index_list :
		if li[i] :
			return i



def build_spanning_tree( ct ) :
	'''Build a spanning tree using the edge information in the spanning tree
		ct is compatibility table
	'''
	G1 = nx.Graph() #graph for the first minutiae set
	G2 = nx.Graph() #graph for the first minutiae set

	for entry in ct :
		G1.add_edge( entry[0],entry[1],weight=entry[4] )
		G2.add_edge( entry[2],entry[3],weight=entry[4] )

	#print 'G1.edges are : ', G1.edges()
	#print 'G2.edges are : ', G2.edges()


	min_span_g1 = nx.minimum_spanning_tree( G1 )
	min_span_g2 = nx.minimum_spanning_tree( G2 )

	return min_span_g1,min_span_g2

def build_graph( e1,e2,ct,i1,i2 ) : 
	""" This builds the graph for the compatibility table 
	Right now the starting edge is fixed and stored in queue
	e1 : edge1 from first intratable
	e2 : edge2 from second intratable
	"""

	G1 = nx.Graph()
	G2 = nx.Graph()
	#print 'queue is :',e1,e2
	c1 = []
	c1.extend( e1 )

	c2 = []
	c2.extend( e2 )

	current_queue = [ [ e1[0],e2[0] ], [ e1[1],e2[1] ] ] #current queue , this is a list of list
	#TODO

	current_edge = [ [ e1[0],e1[1] ], [ e2[0],e2[1] ] ]

	current_pair = current_queue.pop( 0 ) #This is a list

	use_index = True

	while use_index : #True should be a condition where no more compatible edges could be found
		'''Find an edge in second minutiae table which is similar to the current edge
			To find an edge similar to this edge find the entry in the compatibility_table
				which has both the nodes '''
		

		#We have the current pair use these to add edges
		#print 'while use_index'
		G1.add_edge( current_edge[0][0], current_edge[0][1] )
		G2.add_edge( current_edge[1][0], current_edge[1][1] )

		

		try :
			avlbl = set( i1[ current_pair[0] ] ) & set( i2[ current_pair[0] ] )
			#print 'avlbl finding'
		except KeyError :
			#print 'KeyError'
			break


		avlbl = list( avlbl )
		#print 'avlbl is : ',avlbl

		use_index = use_entry( avlbl,ct ) #which edge to proceed

		#We have the index from compatibility_table from where similar edges to use

		if use_index : #something is still left in compatibility table to use
			current_queue +=  [ [ ct[ use_index ][0], ct[ use_index ][2] ], [ ct[ use_index ][1], ct[ use_index ][3] ] ]
			current_edge = [ [ ct[ use_index ][0],ct[ use_index ][1] ], [ ct[ use_index ][2],ct[ use_index ][3] ] ]

			#all used. Now set it to None
			ct[ use_index ] = None

		
	
		current_pair = current_queue.pop( 0 )
		
		#print "G1 currently is :", G1.nodes()
		#print 'use_index is : ',use_index
		#print 'hello'

	return G1,G2


def remove_value_from_index( removable,i1,i2 ) :
	''' find key which has removable as value
	and remove them
	'''
	##print '#remove_value_from_index '
	##print 'i1 is : ',i1
	##print 'i2 is : ',i2

	##print 'removable is : ',removable
	for key in i1 :
		if removable in i1[ key ] :
			i1[ key ].remove( removable )
	
	for key in i2 :
		if removable in i2[ key ] :
			i2[ key ].remove( removable )


def build_graph2( index,ct,i1,i2 ) :
	""" This builds the graph for the compatibility table 
	Right now the starting edge is fixed and stored in queue
	e1 : edge1 from first intratable
	e2 : edge2 from second intratable
	"""

	G1 = nx.Graph()
	G2 = nx.Graph()

	current = index #current index for the compatibility_table ct

	queue = [[  ct[ index ][0],ct[ index ][2] ], [ ct[ index ][1],ct[ index ][3] ] ] #this contains the nodes

	##print '#build_graph2()'

	while current is not None :
		#do your stuff

		#add edge and continue
		##print 'current in while is :',current
		##print 'compatibility_table is :' , ct
		G1.add_edge(  ct[ current ][0], ct[ current ][1]  )
		G2.add_edge(  ct[ current ][2], ct[ current ][3]  )

		
		#print 'Going to remove : ', current
		remove_value_from_index( current,i1,i2 )
		##print 'Removed'
		#after adding edge make that entry None
		ct[ current ] = None
		current = None

		#print 'queue is : ',queue



		#find next current
		pop_queue = False
		while queue :
			##print 'while queue is :', queue
			cm = queue.pop( 0 ) #cm : corresponding minutiae

			#print 'i1 is :',i1
			#print 'i2 is :',i2

			intersection = set( i1[ cm[0] ] ) & set( i2[ cm[1] ] )
			intersection = list( intersection )
			##print 'intersection is :',intersection
			if intersection : #this means we found the next corresponding edge
				current = intersection.pop( 0 )
				if ct[ current ] :
					queue +=  [ [ ct[ current ][0],ct[ current ][2] ], [ ct[ current ][1], ct[ current ][3] ] ]
				##print 'current after popping is : ', current
				while not ct[ current ] :
					if intersection :
						current = intersection.pop( 0 )
					else : #if no intersection found try for the next pair in the queue
						pop_queue = True
						break
					if ct[ current ] :
						queue +=  [ [ ct[ current ][0],ct[ current ][2] ], [ ct[ current ][1], ct[ current ][3] ] ]
				if pop_queue :
					continue
				break #we got current index to work with
			else :
				current = None
				continue

			##print 'current is : ',current
		#work with current in the next loop it will work :P


	return G1,G2




#print sys.argv[1]

f1 = open( sys.argv[1],'r' )
lines1 = f1.readlines()
f1.close()

#print lines1
minutiaes1 = [ a.split()[ : 3 ] for a in lines1 ]
##print 'minutiaes are'
##print minutiaes

minutiaes1 = conv_to_numbers( minutiaes1 )
#print 'minutiaes1 after conversion are :',minutiaes1

minutiaes1 = sort_2d( minutiaes1 )

#print 'sorted minutiaes from 1 are :',minutiaes1

iptable1 = build_intra_table( minutiaes1 )

#print 'max distance is :',max( iptable1,key= lambda x : x[0] )

##print 'iptable is :',iptable1
#print 'minutiaes.size is :',len( minutiaes1 )
#print 'iptable.size is :', len( iptable1 )

#print 'iptable1 is :',iptable1



f2 = open( sys.argv[2],'r' )
lines2 = f2.readlines()
f2.close()

#print lines2
minutiaes2 = [ a.split()[ : 3 ] for a in lines2 ]
##print 'minutiaes are'
##print minutiaes

minutiaes2 = conv_to_numbers( minutiaes2 )
##print 'minutiaes are :',minutiaes

minutiaes = sort_2d( minutiaes2 )

#print 'sorted minutiaes from 2 are :',minutiaes2

iptable2 = build_intra_table( minutiaes2 )

#print 'max distance is :',max( iptable2,key= lambda x : x[0] )

#print 'minutiaes.size is :',len( minutiaes2 )
#print 'iptable.size is :', len( iptable2 )

#print 'iptable2 is :',iptable2



'''

'''
def get_disjoint_trees_dynamic( tree_list ) :
	'''Now get all the disjoint trees using dynamic programming
	e.g [ [a,b,c],[a,b],[c,d] ] ==> [a,b,c,d] not [ a,b,c ]
	'''
	num_trees = len( tree_list )

	size_list = [] #maximum size that has all the disjoint trees. This list is a list which stores that maximum size for each index
	size_list.append( len( tree_list[0].nodes() ) )

	nodes_list = [] #stores all the nodes that would be present at that index so as to have maximum number of nodes 
	nodes_list.append( tree_list[0].nodes() )

	included_trees = [] #stores index of the trees which are used for thee tree set stored at the index giving maximum size
	included_trees.append( [0] )

	for i in range( 1,num_trees ) :
		max_index = None #has the index which is disjoint from the current tree
		maximum = 0 #has the number of nodes in each index

		#print '#dynamic i is : ',i

		for j in range( 0,i ) :
			#print 'and operation for ( %d,%d ) ' % ( i,j )
			#print 'nodes_list[j] is :',nodes_list[ j ]
			#print 'tree_list[i].nodes() is :',tree_list[ i ].nodes()
			if not ( set( nodes_list[ j ] ) & ( set( tree_list[ i ].nodes() ) ) ) : #The part for dynamic programming
				#print 'Entered'
				if maximum < size_list[ j ] :
					maximum =  size_list[ j ]
					#print 'maximum is : ',maximum
					max_index = j

		##print 'tree_list[ %d ] is : %s',%( i,'hi' )
		if max_index is not None :
			#print 'tree_list[ i ] is :', tree_list[i].nodes()
			#print 'tree_list[ max_index ] is :', ( tree_list[ max_index ].nodes(), max_index )
			#print 'max_index : size[ %d ] is : ',size_list[ max_index ]
			size_list.append( len( tree_list[ i ].nodes() ) + size_list[ max_index ]  ) 
			#print 'size_list is : ',size_list
			nodes_list.append( nodes_list[ max_index ] + tree_list[ i ].nodes() )
			included_trees.append(  included_trees[ max_index ] + [ i ]  )
		else :
			size_list.append( len( tree_list[ i ].nodes() ) )
			#print 'size_list NA is : ',size_list
			#print 'nodes_list is : ',nodes_list
			#print 'current_nodes are : ',tree_list[ i ].nodes()
			nodes_list.append( tree_list[ i ].nodes() )
			included_trees.append( [ i ] )

	return size_list,included_trees



def get_disjoint_trees( tree_list ) :
	'''Now  get all the disjoint trees 
	@param
	tree_list is a list of trees( networkx graphs ) in order of size . decreasing here
	'''

	#TODO : Think of a dynamic programming approach to get the largest number of disjoint trees
	disjoint_trees = [] # a list of trees. each tree is disjoint in term of nodes
	included_nodes = []
	for tree in tree_list :
		if set( tree.nodes() ) & set( included_nodes ) :	
			pass
		else :
			included_nodes += tree.nodes()
			disjoint_trees.append( tree )

	return disjoint_trees





def build_ct_and_indexes( iptable1,iptable2 ) :

	compatibility_table = []
	
	index1 = {}
	index2 = {}
	threshold_dist = 3
	threshold_beta1 = 10
	threshold_beta2 = 10
	for i in range( len( iptable1 ) ) :
		for j in range( len( iptable2 ) ) :
			if abs( iptable1[ i ][ 0 ]-iptable2[j][0] ) <= threshold_dist and abs( iptable1[i][1] - iptable2[j][1] ) <= threshold_beta1 and abs( iptable1[i][2] - iptable2[j][2] ) <= threshold_beta2 :
				compatibility_table.append( ( iptable1[i][3],iptable1[i][4],iptable2[j][3],iptable2[j][4],iptable1[i][0] ) )
				#print 'compatibility_table is : ',compatibility_table
				if index1.get( iptable1[i][3] ) :
					index1[ iptable1[i][3] ].append( len( compatibility_table ) - 1 )
				else :
					index1[ iptable1[i][3] ] =  [ len( compatibility_table ) - 1 ] 
	
	
				if index1.get( iptable1[i][4] ) :
					index1[ iptable1[i][4] ].append( len( compatibility_table ) - 1 )
				else :
					index1[ iptable1[i][4] ] =  [ len( compatibility_table ) - 1 ] 
	
	
				if index2.get( iptable2[j][3] ) :
					index2[ iptable2[j][3] ].append( len( compatibility_table ) - 1 )
				else :
					index2[ iptable2[j][3] ] =  [ len( compatibility_table ) - 1 ] 
	
	
				if index2.get( iptable2[j][4] ) :
					index2[ iptable2[j][4] ].append( len( compatibility_table ) - 1 )
				else :
					index2[ iptable2[j][4] ] =  [ len( compatibility_table ) - 1 ] 

	return compatibility_table,index1,index2

compatibility_table,index1,index2 = build_ct_and_indexes( iptable1,iptable2 )

#print 'compatibility table is :'
#print compatibility_table

#print 'index1 is :',index1

#print '\n\n\n\n\n'

#print 'index2 is :',index2


read_only_index1 = dict( index1 )
read_only_index2 = dict( index2 )



maximum = 0
common_nodes = []

tree_list = [] #a list of trees as in networkx

'''
for entry in compatibility_table :
	e1 = [ entry[0],entry[1] ]	
	e2 = [ entry[2],entry[3] ]	
	ct = []
	ct.extend( compatibility_table )

	G1,G2 = build_graph( e1,e2,ct,index1,index2 )

	tree_list.append( G1 )

	#print 'G1.nodes are :',G1.nodes()
	#print 'G2.nodes are :',G2.nodes()

	common_nodes.append( len( G1.nodes() ) )

	if maximum < len( G1.nodes() ) :
		maximum = len( G1.nodes() )

'''

for i in range( len( compatibility_table ) ) :
	#print 'for i in ',i
	ct = []
	ct.extend( compatibility_table )

	i1 = copy.deepcopy( read_only_index1 )
	i2 = copy.deepcopy( read_only_index2 )

	#print 'ct for %d is : %s'%( i,ct )
	#print 'i1 and i2 for %d is : %s\n\n%s'%( i,i1,i2 )
	G1,G2 = build_graph2( i,ct,i1,i2 )

	#print 'after building graph index1 is :',read_only_index1

	tree_list.append( G1 )

	#print 'G1.nodes are :',G1.nodes()
	#print 'G2.nodes are :',G2.nodes()

	#print 'G1.edges are :',G1.edges()
	#print 'G2.edges are :',G2.edges()

	common_nodes.append( len( G1.nodes() ) )

	if maximum < len( G1.nodes() ) :
		maximum = len( G1.nodes() )


#print 'maximum is :',maximum
#print 'common nodes :',common_nodes



tree_list.sort( key = lambda x : len( x.nodes() ),reverse=True )

#print 'The trees are as follows :'
for tree in tree_list :
	#print tree.nodes()
	pass

disjoint_trees = get_disjoint_trees( tree_list )

#print '\n\n\n\n\n\n\n\n\n\n\n\n\nThe disjoint tree list is :'
for tree in disjoint_trees :
	#print tree.nodes()
	pass



#print 'The trees are as follows for dynamic programming :'
for tree in tree_list :
	#print tree.nodes()
	pass

disjoint_list,included_trees = get_disjoint_trees_dynamic( tree_list )

#print 'The tree list in sorted order is :'
#print [ tree.nodes() for tree in tree_list ]

#print 'size(tree_list is :',len(tree_list)

#print 'disjoint_list is :'
#print disjoint_list

#print '\n\n\n\n\n\nThe included tree list : '
#print included_trees

print 'score is : ', ( max( disjoint_list )**2 /( len( minutiaes1 )*len( minutiaes2 )*1.0 ) )


#Also build a spanning tree thingie
Spanning_forest_1,Spanning_forest_2 = build_spanning_tree( compatibility_table )


#print 'Spanning forest 1 is : ', Spanning_forest_1.edges()
#print 'Spanning forest 2 is : ', Spanning_forest_2.edges()
