from __future__ import print_function
import logging
import grpc
import hw3_pb2
import hw3_pb2_grpc

import matplotlib.pyplot as plt
from sklearn.datasets.samples_generator import make_blobs


def kmeans_test(stub):
    # 随机生成一些坐标，然后调用RpcKmeans来分类
    # 参数分别为  样本数，样本特征数， 中心点，每个类别的方差
    coordinate, _ = make_blobs(n_samples=1000, n_features=2, centers=[[-1, 2], [0, 0], [1, 1], [2, 2]],
                               cluster_std=[0.4, 0.2, 0.2, 0.2])
    fig = plt.figure()
    fig.add_subplot(2, 1, 1)
    plt.scatter(coordinate[:, 0], coordinate[:, 1], marker='o')     # 原始数据画图

    # 调用RpcKmeans对坐标聚类, color即聚类后的标签
    color = stub.RpcKmeans(hw3_pb2.Args(x_coor=coordinate[:, 0], y_coor=coordinate[:, 1], n_cluster=4))
    # 用远程调用 K-means聚类的函数的结果画图
    fig.add_subplot(2, 1, 2)
    plt.scatter(coordinate[:, 0], coordinate[:, 1], c=color.colors)
    plt.show()


def run():
    with grpc.insecure_channel('localhost:50051') as channel:  # 与服务器提供服务的端口建立连接
        stub = hw3_pb2_grpc.HW3Stub(channel)

        # 测试1，打招呼
        response = stub.SayHello(hw3_pb2.HelloRequest(name='YSJ'))
        print("Greeter client received: " + response.message)

        # 乘法
        a = 8
        b = 3
        response = stub.RpcMultiplication(hw3_pb2.Multiplication_input(num1=a, num2=b))
        print(f"Call RpcMultiplication to compute {str(a)} * {str(b)} \nThe result is : ", response.res)
        # print(type(response))

        # 平方
        c = 7
        response = stub.RpcSquare(hw3_pb2.Square_data(data=c))
        print(f"Call RpcSquare to compute the square of {c} \nThe result is : ", response.data)

        # 产生数据并调用RpcKmeans来分类，具体函数实现
        kmeans_test(stub)


if __name__ == '__main__':
    logging.basicConfig()
    run()
