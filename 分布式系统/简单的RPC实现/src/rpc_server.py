from concurrent import futures
import logging
import grpc
import hw3_pb2
import hw3_pb2_grpc

import numpy as np
from sklearn.cluster import KMeans


class HW3(hw3_pb2_grpc.HW3Servicer):

    def SayHello(self, request,context):
        return hw3_pb2.HelloReply(message='Hello, %s! This is 17341189_YSJ\'s servicer.' % request.name)

    def RpcMultiplication(self, request, context):
        a = request.num1
        b = request.num2
        result = a * b
        print('Compute multiplication finished.')
        return hw3_pb2.Multiplication_output(res=result)

    def RpcSquare(self, request, context):
        a = request.data
        result = a * a
        print('Compute square finished.')
        return hw3_pb2.Square_data(data=result)

    def RpcKmeans(self, request, context):
        x = request.x_coor
        y = request.y_coor
        n = request.n_cluster
        coordinate = []
        for i in range(len(x)):
            coordinate.append([x[i], y[i]])

        colors_predict = KMeans(n_clusters=n).fit_predict(coordinate)
        print('Kmeans finished.')
        return hw3_pb2.Color(colors=colors_predict)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))    # 线程池,支持多客户端同时使用
    hw3_pb2_grpc.add_HW3Servicer_to_server(HW3(), server)               # 服务器与端口绑定
    server.add_insecure_port('[::]:50051')                              # 分配提供服务的端口
    server.start()
    print('The server is running...')
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
