from flask import render_template
from flask.globals import request
import os
from time import time
from subprocess import Popen
import urllib.parse

FILEPATH = os.path.split(os.path.realpath(__file__))[0]

def apkget():
    content = {}
    work_dir = FILEPATH + '/tools'
    if( request.method == "POST"):
        f = request.files['apkfile']
        file_name = '{}.apk'.format(str(time()))
        output_file = '{}.txt'.format(str(time()))
        upload_path = os.path.join(work_dir, file_name)  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)

        command = "java -jar apktool.jar d {}".format(file_name)
        cmd = Popen(command, cwd=work_dir ,shell=True)
        while 1:
            ret = Popen.poll(cmd)
            if ret == 0:
                break
        command2 ='grep -E "https?://[a-zA-Z0-9\.\/_&=@$%?~#-]*" -r {} > {}'.format(file_name.split(".apk")[0], output_file)
        cmd = Popen(command2, cwd=work_dir ,shell=True)
        while 1:
            ret = Popen.poll(cmd)
            if ret == 0:
                break
        f = open(work_dir + "/" + output_file, 'r')
        urlresults = set()
        domainresult = set()
        for line in f.readlines():
            line = line.strip()
            if('http://' in line or 'https://' in line):
                if('http://' in line):
                    result = "http://" + line.split('http://')[1]
                else:
                    result = "https://" + line.split('https://')[1]
                if('"' in result):
                    result = result.split('"')[0]
                if(' ' in result):
                    result = result.split(' ')[0]
                if('<' in result):
                    result = result.split(' ')[0]
                urlresults.add(result)
            else:
                pass
            
        for i in urlresults:
            domainresult.add(urllib.parse.urlparse(i).netloc)

        content = {'urlresults': urlresults, 'domainresult': domainresult}

        try:
            os.system("rm -rf {}".format(work_dir + "/" + file_name))
            os.system("rm -rf {}".format(work_dir + "/" + output_file))
            os.system("rm -rf {}".format(work_dir + "/" + file_name.split(".apk")[0]))
        except:
            pass

    return render_template('apkget.html', form=content, segment='apkget')