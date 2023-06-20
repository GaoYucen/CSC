# import generate as gen
import matplotlib.pyplot as plt
import numpy as np
import math
import random
#from mpl_toolkits.mplot3d import Axes3D
import TSP_LKH
import TSP_GD
import kruskal_clustering_balance as ks
import time

#%%
dimen = 3

def euclidean_distance(pos1, pos2):
    distances = math.sqrt(np.power(pos1 - pos2, 2).sum())
    return distances

def projection(point): # embedding函数
    return sphere((point[0],point[1],-1))

def sphere(point): # 球面函数
    point_s = np.zeros(dimen)
    sum = 0
    for i in range(dimen):
        sum += point[i]**2
    scale = math.sqrt(sum)
    for i in range(dimen):
        point_s[i] = point[i]/scale

    return point_s

# time start
start = time.perf_counter()

#%% read data
points = np.loadtxt('points.csv')
p_num = len(points)
M = int(5) #小车数量

#%% 初始化embedding，假设是映射到另一个三维球面上
# 保持原x，y，三维点是0，摸长为1
points_p = np.zeros(p_num*dimen).reshape(p_num, dimen)
for i in range(0, p_num):
    points_p[i] = projection(points[i])

#%% set initial tsp
stopping_criteria = 0.001 #停止检查
stopping_itera = 5
Iteration = 100
best_tsp_value_route = np.zeros(M) #M维度的数组 greedy算法计算best route
lr = 100 #学习率

for route_num in range (1, M+1):
    former_tsp_value = 10000
    max_iter = 0
    #进入迭代
    for _ in range(Iteration):
        #%% 高维空间聚类+划分簇
        index, mst_value, edge_list = ks.clustering(points_p, route_num)

        #%% 输出tsp value
        tsp_value = np.zeros(route_num)
        tsp_car = np.zeros(route_num) #每个环分配的车的数量
        for i in range(route_num):
            tsp_car[i] = 1
        cluster = list(range(route_num))
        for i in range(0,route_num):
            if (len(index[i]) >= 2):
                tsp_value[i], cluster[i] = TSP_GD.tsp(np.array(points[index[i]]), index[i])
            else:
                cluster[i] = index[i]
        # print(tsp_value)
        for i in range(0,M-route_num):
            tsp_car[np.argmax(tsp_value)] += 1
            mst_value[np.argmax(tsp_value)] = mst_value[np.argmax(tsp_value)]*(tsp_car[np.argmax(tsp_value)]-1)/tsp_car[np.argmax(tsp_value)]
            tsp_value[np.argmax(tsp_value)] = tsp_value[np.argmax(tsp_value)]*(tsp_car[np.argmax(tsp_value)]-1)/tsp_car[np.argmax(tsp_value)]

        # if (former_tsp_value-max(tsp_value)<stopping_criteria) and (former_tsp_value-max(tsp_value)>0): #有优化，但是优化幅度过小，无需保留此次优化结果
        #     max_iter = _
        #     break
        if (former_tsp_value-max(tsp_value)>0): #只要有优化
            max_iter = _
            tsp_value_temp = tsp_value #保存目前最好的结果
            mst_value_temp = mst_value
            cluster_temp = cluster

            former_tsp_value = max(tsp_value) #更新最优解

            factor_calc = mst_value_temp / tsp_value_temp
            for i in range(len(factor_calc)):
                if np.isnan(factor_calc[i]):
                    factor_calc[i] = 0

            for index_tmp in range(route_num):
                len_c = len(index[index_tmp]) # 最大的环中包含的点的数量
                #更新点的操作
                factor = 2/route_num*(factor_calc[index_tmp]-1/route_num*sum(factor_calc))
                for i in range(len_c):
                    factor2 = [0,0,0]
                    for edge in edge_list:
                        if (edge[0] == index[index_tmp][i]):
                            factor2 += (points_p[edge[1]]-points_p[edge[0]])/euclidean_distance(points_p[edge[1]],points_p[edge[0]])
                            # print(points_p[edge[1]], points_p[edge[0]])
                        elif (edge[1] == index[index_tmp][i]):
                            factor2 += (points_p[edge[0]]-points_p[edge[1]])/euclidean_distance(points_p[edge[0]],points_p[edge[1]])
                            # print(points_p[edge[1]], points_p[edge[0]])
                    step = [lr * factor * factor2[i] for i in range(dimen)]
                    points_p[index[index_tmp][i]] = sphere(points_p[index[index_tmp][i]]+step) #更新点的位置
        else: #没有优化
            if (_ - max_iter >= stopping_itera): #连续5次没有优化
                break

            tsp_value_temp = tsp_value #保存目前最好的结果
            mst_value_temp = mst_value
            cluster_temp = cluster

            factor_calc = mst_value_temp / tsp_value_temp
            for i in range(len(factor_calc)):
                if np.isnan(factor_calc[i]):
                    factor_calc[i] = 0

            for index_tmp in range(route_num):
                len_c = len(index[index_tmp])  # 最大的环中包含的点的数量
                # 更新点的操作
                factor = 2/route_num*(factor_calc[index_tmp]-1/route_num*sum(factor_calc))
                for i in range(len_c):
                    factor2 = [0,0,0]
                    for edge in edge_list:
                        if (edge[0] == index[index_tmp][i]):
                            factor2 += (points_p[edge[1]] - points_p[edge[0]]) / euclidean_distance(points_p[edge[1]],
                                                                                                    points_p[edge[0]])
                        elif (edge[1] == index[index_tmp][i]):
                            factor2 += (points_p[edge[0]] - points_p[edge[1]]) / euclidean_distance(points_p[edge[0]],
                                                                                                    points_p[edge[1]])
                    step = [lr * factor * factor2[i] for i in range(dimen)]
                    points_p[index[index_tmp][i]] = sphere(points_p[index[index_tmp][i]] + step)  # 更新点的位置

        print(tsp_value_temp)
        # print(tsp_car)
        print(cluster_temp)

    best_tsp_value_route[route_num-1] = former_tsp_value #对于当前环数量的最好的结果

print(best_tsp_value_route)
print(min(best_tsp_value_route))

# time stop
end = time.perf_counter()
print("程序的运行时间是：%s" % (end - start))

