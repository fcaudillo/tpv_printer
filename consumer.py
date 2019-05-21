from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin
import json
import os


queue_name_impresion = 'msgreload_' +  os.environ['CLIENTE_ID']

class Worker(ConsumerMixin):
    exchange = Exchange(queue_name_impresion, type='direct')
    q = Queue(exchange=exchange, routing_key=queue_name_impresion, exclusive=True)
    print ("Cola de iimpresion : " + queue_name_impresion)
    def __init__(self, connection):
        self.connection = connection

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=[self.q], callbacks=[self.on_task])]

    def on_task(self, body, message):
        print (body)
        jsonObject = json.loads(body)
        print (jsonObject.get('cliente_giro'))
        print (jsonObject.get('ticket_pie'))
        message.ack()


if __name__ == '__main__':
    #str = '{"ticket_pie": "Gracias por su compra", "xmlDevData": null, "rcode_description": "Transaccion Aprobada", "cliente_giro": "Tlapaleria y Papeleria", "op_authorization": "502735", "cliente_nombre": "Fantasy S.A. de C.V.", "op_account": "5560217782", "template_tae": "print_recibo_tae", "rcode": 0, "transaction_id": 12357}'

    #jsonObject = json.loads(str)
    #print (jsonObject.get('cliente_giro'))
    #print (jsonObject.get('ticket_pie'))

    #broker_url = 'amqp://%s:%s@elverde.mx:5672//' % (os.environ['USUARIO_MQ'],os.environ['PASSWORD_MQ'])
    broker_url = 'amqp://%s:%s@localhost:5672//' % (os.environ['USUARIO_MQ'],os.environ['PASSWORD_MQ'])
    print (broker_url)
    with Connection(broker_url) as conn:
        worker = Worker(conn)
        print ('arrancando...')
        worker.run()
		
