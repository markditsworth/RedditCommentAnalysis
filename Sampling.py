
import zen
import numpy as np
import random

def getSamples(G,smpl_size):
    deg=np.zeros(G.num_nodes,dtype=int)
    for i in range(G.num_nodes):
        	deg[i] = G.degree_(i)
	
    Nmax = float(max(deg))

    sample_nodes = np.zeros(smpl_size,dtype=int)

    nodes = G.nodes_()
    np.random.shuffle(nodes)   # randomize the order of nodes
    i = 0
    sample_idx=0
    loop = 1
    while loop:
        if i == G.num_nodes:
            i = 0
        if nodes[i] not in sample_nodes:
            prob = G.degree_(nodes[i])/Nmax
            if random.random() < prob:      # sample node with probability proportional to its degree
                sample_nodes[sample_idx] = int(nodes[i])
                sample_idx += 1
        if sample_idx == smpl_size:
            loop = 0
        i += 1
    return sample_nodes

def sampleGraph(G,samples):
    H = zen.DiGraph()
    for i in samples:
        for j in samples:
            if G.has_edge_(i,j):        # if G has edge between i and j
                idx = H.add_edge(G.node_object(i),G.node_object(j))  # add edge to H
                H.set_weight_(idx,H.weight_(H.edge_idx(G.node_object(i),G.node_object(j)))) # copy weight
    
    return H

            
def main(argv):
    networkFile = ''
    outputFile = ''
    
    while argv:
        if argv[0] == '-s':
            networkFile = argv[1]
        elif argv[0] == '-d':
            outputFile = argv[1]
        argv = argv[1:]
    
    if networkFile == '':
        print 'Error. No network gml file. Use -s <file>'
    elif outputFile == '':
        print 'Error. No output gml file. Use -d <file>'
    else:
        G = zen.io.gml.read(networkFile,weight_fxn=lambda x:x['weight'])
        
        samples = getSamples(G,15000)
        G_ = sampleGraph(G,samples)
        
        zen.io.gml.write(G_,outputFile)
        print 'done.'

if __name__ == '__main__':
    from sys import argv
    main(argv)
    