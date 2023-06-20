#Uses python3
import sys
import math
import random
import numpy as np

# The “clusters” are the connected components that Kruskal’s 
# algorithm has created after a certain point.

class Node:
    def __init__(self, pos, p):
        self.pos = pos
        self.parent = p
        self.rank = 0 #rank大表示排序高
        self.index = p

class Edge:
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.weight = w

# #二维distance
# def euclidean_distance(x1, y1, x2, y2):
#   return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

def euclidean_distance(pos1, pos2):
    distances = math.sqrt(np.power(pos1 - pos2, 2).sum())
    return distances

def Find(i, nodes): #find root %%缺少迭代更新的过程
  if (i != nodes[i].parent) :
        nodes[i].parent = Find(nodes[i].parent, nodes)
  return nodes[i].parent

def Union(u, v, nodes):
    r1 = Find(u, nodes)
    r2 = Find(v, nodes)
    if (r1 != r2):
        if (nodes[r1].rank > nodes[r2].rank):
            nodes[r2].parent = r1
        else:
            nodes[r1].parent = r2
            if (nodes[r1].rank == nodes[r2].rank):
                nodes[r2].rank += 1

def clustering(points, k):
    #initialization
    n = points.shape[0]
    pos = []
    for i in range(n):
        pos.append(points[i])
    edges = []
    nodes = []
    
    #initialize nodes with xy-coordinates and index
    for i in range(n):
       nodes.append(Node(pos[i], i))
    
    #initialize edges with the Euclidean distance between coordinates
    for i in range(n):
        for j in range(i+1, n):
            edges.append(Edge(i, j, euclidean_distance(pos[i], pos[j])))
    
    edges = sorted(edges, key=lambda edge: edge.weight) # 按边权排序

    index = [[] for i in range(k)] # 簇包括的点
    index_all = [] # 所有簇包括的点
    mst = [0 for i in range(k)] # 簇对应的MST总长度
    edge_added_list = [] # 已经添加的边
    
    # 初始化簇
    for i in range(0, k):
        for edge in edges:
            # 如果edge.u和edge.v不属于index_all
            if (edge.u not in index_all) and (edge.v not in index_all):
                index[i].append(edge.u)
                index[i].append(edge.v)
                mst[i] += edge.weight
                print(mst, end='\n')
                index_all.append(edge.u)
                index_all.append(edge.v)
                # 向已添加列表中添加edge
                edge_added_list.append([edge.u, edge.v])
                # 从edges中删除edge
                edges.remove(edge)
                break

    # 添加剩余的n-2k条边
    for i in range(k, n-2*k):
        # 挑选mst最小的簇
        min_mst_index = mst.index(min(mst))
        for edge in edges:
            # 如果一个点属于index[i]，另一个点不属于index_all
            if ((edge.u in index[min_mst_index]) and (edge.v not in index_all)) or ((edge.u not in index_all) and (edge.v in index[min_mst_index])):
                index[min_mst_index].append(edge.u)
                index[min_mst_index].append(edge.v)
                mst[min_mst_index] += edge.weight
                print(mst, end='\n')
                index_all.append(edge.u)
                index_all.append(edge.v)
                # 向已添加列表中添加edge
                edge_added_list.append([edge.u, edge.v])
                # 从edges中删除edge
                edges.remove(edge)
                break

    return index, mst, edge_added_list


if __name__ == '__main__':
    p_num = 100
    points = np.loadtxt('points.csv')
    k = 5
    print(clustering(points[0:p_num], k))