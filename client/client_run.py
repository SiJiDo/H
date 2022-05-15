import os
import configparser
from time import time

cfg = configparser.ConfigParser()
cfg.read('config.ini')
FILEPATH = os.path.split(os.path.realpath(__file__))[0]

def run():
    #启动subfinder的celery
    if(cfg.get("WORKER_CONFIG", "subdomain_subfinder") == 'True'):
        os.chdir("{}/subdomain_scan/subfinder".format(FILEPATH))
        os.system("nohup celery -A subfinder worker -l info -Q subfinder -n subfinder_{} -c 1 &".format(time()))
    #启动amass的celery
    if(cfg.get("WORKER_CONFIG", "subdomain_amass") == 'True'):
        os.chdir("{}/subdomain_scan/amass".format(FILEPATH))
        os.system("nohup celery -A amass worker -l info -Q amass -n amass_{} -c 1 &".format(time()))
    #启动shuffledns的celery
    if(cfg.get("WORKER_CONFIG", "subdomain_shuffledns") == 'True'):
        os.chdir("{}/subdomain_scan/shuffledns".format(FILEPATH))
        os.system("nohup celery -A shuffledns worker -l info -Q shuffledns -n shuffledns_{} -c {} &".format(time(),cfg.get("WORKER_CONFIG", "subdomain_shufflends_count")))
    #启动domaininfo的celery
    if(cfg.get("WORKER_CONFIG", "subdomain_domaininfo") == 'True'):
        os.chdir("{}/subdomain_scan/domaininfo".format(FILEPATH))
        os.system("nohup celery -A domaininfo worker -l info -Q domaininfo -n domaininfo_{} -c 1 &".format(time()))
    #启动naabu的celery
    if(cfg.get("WORKER_CONFIG", "port_naabu") == 'True'):
        os.chdir("{}/port_scan/naabu".format(FILEPATH))
        os.system("nohup celery -A naabu worker -l info -Q naabu -n naabu_{} -c {} &".format(time(),cfg.get("WORKER_CONFIG", "port_naabu_count") ))
    #启动httpx的celery
    if(cfg.get("WORKER_CONFIG", "http_httpx") == 'True'):
        os.chdir("{}/http_scan/httpx".format(FILEPATH))
        os.system("nohup celery -A httpx worker -l info -Q httpx -n httpx_{} -c 1 &".format(time()))
    #启动screenshot的celery
    if(cfg.get("WORKER_CONFIG", "http_screenshot") == 'True'):
        os.chdir("{}/http_scan/screenshot".format(FILEPATH))
        os.system("nohup celery -A screenshot worker -l info -Q screenshot -n screenshot_{} -c 1 &".format(time()))
    #启动ehole的celery
    if(cfg.get("WORKER_CONFIG", "http_ehole") == 'True'):
        os.chdir("{}/http_scan/ehole".format(FILEPATH))
        os.system("nohup celery -A ehole worker -l info -Q ehole -n ehole_{} -c 1 &".format(time()))
    #启动JSFinder的celery
    if(cfg.get("WORKER_CONFIG", "dir_jsfinder") == 'True'):
        os.chdir("{}/dir_scan/jsfinder".format(FILEPATH))
        os.system("nohup celery -A jsfinder worker -l info -Q jsfinder -n jsfinder_{} -c {} &".format(time(),cfg.get("WORKER_CONFIG", "dir_jsfinder_count")))
    #启动fileleak的celery
    if(cfg.get("WORKER_CONFIG", "dir_fileleak") == 'True'):
        os.chdir("{}/dir_scan/fileleak".format(FILEPATH))
        os.system("nohup celery -A fileleak worker -l info -Q fileleak -n fileleak_{} -c {} &".format(time(),cfg.get("WORKER_CONFIG", "dir_fileleak_count")))
    #启动nuclei的celery
    if(cfg.get("WORKER_CONFIG", "vuln_nuclei") == 'True'):
        os.chdir("{}/vuln_scan/nuclei".format(FILEPATH))
        os.system("nohup celery -A nuclei worker -l info -Q nuclei -n nuclei_{} -c {} &".format(time(),cfg.get("WORKER_CONFIG", "vuln_nuclei_count")))
    #启动xray的celery
    if(cfg.get("WORKER_CONFIG", "vuln_xray") == 'True'):
        os.chdir("{}/vuln_scan/xray_scan".format(FILEPATH))
        os.system("nohup celery -A xray worker -l info -Q xray -n xray_{} -c 1 &".format(time()))
        os.system("nohup tools/xray/xray webscan --listen 0.0.0.0:7777 --webhook-output http://{}/webhook  &".format(cfg.get("WORKER_CONFIG", "vuln_xray_webhook")))
    #启动icp备案的celery
    if(cfg.get("WORKER_CONFIG", "plugin_icpget") == 'True'):
        os.chdir("{}/icp_scan".format(FILEPATH))
        os.system("nohup celery -A icpget worker -l info -Q icpget -n icpget_{} &".format(time()))
    #启动fscan备案的celery
    if(cfg.get("WORKER_CONFIG", "vuln_fscan") == 'True'):
        os.chdir("{}/vuln_scan/fscan".format(FILEPATH))
        os.system("nohup celery -A fscan worker -l info -Q fscan -n fscan_{} -c {} &".format(time(),cfg.get("WORKER_CONFIG", "vuln_fscan_count")))

if __name__ == '__main__':
    run()