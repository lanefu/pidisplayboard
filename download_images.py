import boto3
import schedule
import time
import logging
bucketLocation = 'home-displayboard'
fileLocation = '/tmp/'



def job():
    logging.info("[JOB] Running AWS Pi Image Download Job...")
    s3 = boto3.client('s3')
    list = s3.list_objects(Bucket=bucketLocation)['Contents']

    for s3_key in list:
        s3_object = s3_key['Key']
        if not s3_object.endswith("/"):
            s3.download_file(bucketLocation, s3_object, fileLocation+s3_object)
        else:
            import os
            if not os.path_exists(s3_object):
                os.makedirs(s3_object)

def heartbeat():
    logging.info("[HEARTBEAT] Heartbeat Log entry.")


schedule.every(5).minutes.do(job)
schedule.every(1).minutes.do(heartbeat)
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)



while 1:
    schedule.run_pending()
    time.sleep(1)







