
import os

#项目common路径
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

#conf入参路径
conf_dir=os.path.join(BASE_DIR,"\\config\\conf.ini")
#入参上级路径
inputParameters_dir = os.path.join(BASE_DIR,"inputParameters")

#login路径
login_dir= os.path.join(inputParameters_dir,"login.ini")

