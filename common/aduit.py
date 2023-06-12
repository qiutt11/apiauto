from common import dataBase
import re


def aduit(workflow_id):
    db=dataBase.dataBase()
    if re.findall("workflowId", workflow_id):
        sql="update activiti7.workflow set flow_status=3  where workflow_id='%s'"% workflow_id
    else :
        sql="update oms_hr.recruit_offer set process_status=7  where talent_id='%s'"% workflow_id
    coon=db.cursor()
    try:
         coon.execute(sql)
         db.commit()
    except Exception as e:
         raise e
         coon.rollback()
         print("c")
    coon.close()
    db.close()


