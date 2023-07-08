# import generate as gen
import matplotlib.pyplot as plt
import numpy as np
import math
import KMeans as kmeans
import random
#from mpl_toolkits.mplot3d import Axes3D
import TSP_GD
import time
import kruskal_clustering as ks

#%%
dimen = 3

def projection(point): # embedding函数
    point_p = np.zeros(dimen)
    new = np.zeros(dimen-2)
    for i in range(0,dimen-2):
        new[i] = random.random()
    sum = 0
    for i in range(2):
        sum += point[i]**2
    for i in range(0,dimen-2):
        sum += new[i] ** 2
    scale = math.sqrt(sum)
    for i in range(2):
        point_p[i] = point[i]/scale
    for i in range(0,dimen-2):
        point_p[i+2]=new[i]/scale

    return point_p

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
M = int(10) #小车数量

# #%% 二维点可视化
# fig=plt.figure()
# plt.scatter(points[:, 0], points[:, 1])
# plt.show()

# cluster 几种基础的聚类 k-means，dbscan

# TSP min-max的算法
#%% 初始化embedding，假设是映射到另一个三维球面上
# 保持原x，y，三维点是0，摸长为1
points_p = np.zeros(p_num*dimen).reshape(p_num, dimen)
for i in range(0, p_num):
    points_p[i] = projection(points[i])

#%%三维空间点分布画图
# fig = plt.figure()
# # ax = Axes3D(fig)
# ax = plt.axes(projection='3d')
# ax.scatter3D(points_p[:, 0], points_p[:, 1], points_p[:, 2])
# plt.show()

#%% set initial tsp
former_tsp_value = 100
stoppoing_criteria = 0.001
Iteration = 1000
max_iter = 0

best_tsp_value_route = np.zeros(M) #M维度的数组 greedy算法计算best route
clusters = [[] for i in range(M)]

for route_num in range (1,M+1):
    #进入迭代

    # print(_, '\n')
    #%% 三维空间聚类
    # clf = kmeans.Kmeans(k=route_num,max_iterations=1000,varepsilon=0.000001) #如何设置各个迭代终止条件, dimen=3,p_num=100,varepsilon=0.0000005
    # y_pred, centroids_pred = clf.predict(points_p)

    # #%% 聚类后着色画点
    # fig = plt.figure()
    # # ax = Axes3D(fig)
    # ax = plt.axes(projection='3d')
    # for i in range(0,route_num):
    #     ax.scatter(points_p[y_pred == i][:, 0], points_p[y_pred == i][:, 1], points_p[y_pred == i][:, 2])
    # plt.show()



    #%% 根据聚类的index划分簇
    # index = [[] for i in range(route_num)]
    # for i in range(0,p_num):
    #     index[int(y_pred[i])].append(i)

    index = ks.clustering(points, route_num)[0]

    #%% 输出tsp value
    tsp_value = np.zeros(route_num)
    tsp_car = np.zeros(route_num)
    for i in range(route_num):
        tsp_car[i] = 1
    cluster = list(range(route_num))
    for i in range(0,route_num):
        if (len(index[i]) >= 2):
            tsp_value[i], cluster[i] = TSP_GD.tsp(np.array(points[index[i]]), index[i])
        else:
            cluster[i] = index[i]

    for i in range(0,M-route_num):
        tsp_car[np.argmax(tsp_value)] += 1
        tsp_value[np.argmax(tsp_value)] = tsp_value[np.argmax(tsp_value)]*(tsp_car[np.argmax(tsp_value)]-1)/tsp_car[np.argmax(tsp_value)]

    # print(max_iter,'\n')
    # print(max(tsp_value_temp),'\n')
    # print(tsp_value_temp,'\n')
    # print(cluster_temp,'\n')
    # print('Fail, max_iter = ',max_iter+20)
    best_tsp_value_route[route_num-1] = max(tsp_value)
    clusters[route_num - 1] = cluster

print(best_tsp_value_route)
print(min(best_tsp_value_route))
print(clusters[np.argmin(best_tsp_value_route)])
# time stop
end = time.perf_counter()
print("程序的运行时间是：%s" % (end - start))

