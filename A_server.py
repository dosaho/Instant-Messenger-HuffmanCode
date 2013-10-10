#! /usr/bin/env python2
import pika
import yaml
import thread


rabbitmq_host = 'localhost'


class DataMaster:
    def __init__(self):
        self.masterkey = ['A']
        self.conn_param = pika.ConnectionParameters(host=rabbitmq_host)
        self.connection = pika.SelectConnection(self.conn_param, self.on_connected)

    def serving_loop(self):
        self.connection.ioloop.start()
        print "endofloop??"

    def on_connected(self, connection):
        print "Connected to RabbitMQ!!!"
        connection.channel(self.on_channel_open)

    def on_channel_open(self, channel):
        print "Open channel in RabbitMQ!!!"
        self.channel = channel
        channel.exchange_declare(exchange='server', type='direct')

        for key in self.masterkey:
            print key
            channel.queue_declare(queue='server')
            channel.queue_bind(exchange='server', queue='server', routing_key=key)

        channel.basic_consume(self.trans_message, queue='server', no_ack=True)

    def trans_message(self, channel, method, header, body):
        all_data = yaml.load(body)
        print all_data
        print all_data['to_user']
        channel.basic_publish(exchange=all_data['to_user'], routing_key=all_data['to_user'], body=body)
       

Database_master = DataMaster()
Database_master.serving_loop()
