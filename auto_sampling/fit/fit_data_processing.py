import csv
import os
import re

def is_zero(func_data):
    for key in func_data:
        if func_data[key]==0:
            return True
    return False

os.system('mv ./fit_data ./fit_data_old')

modules = ["cpl","atm","lnd","ice","ocn","glc","wrf","gea","cplatm","cpllnd","cplice","cplocn","cplglc","cplwrf","cplgea","none"]

if not os.path.exists("./fit_data"):
    os.mkdir("./fit_data")
else:
    os.system('rm -r ./fit_data')
    os.mkdir("./fit_data")


for module in modules:
    fit_file = "./fit_data_old/fit_data_module_" + module + ".csv"
    
    orginal_data = csv.reader(open(fit_file, 'r'))
    
    fit_data = {}


    head = next(orginal_data)
    
    #16,30,64,128,192,256,384,448,512
    x = [str(str_i) for str_i in head] #获取采样进程
    num_procs = len(x)

    #id,func_name,self_time1,self_time2,self_time3,self_time4,self_time5,self_time6,self_time7,self_time8,self_time9
    title = next(orginal_data)

    merge_datas = {}
    for line in orginal_data:
        funcname = line[1]
        
        #y:[time1,time2...]
        y = [int(line[i]) for i in range(2,num_procs + 2)]
        
        #{'16':xx}
        func_data = {}
        for i in range(num_procs):
            func_data[x[i]] = y[i]
        
        # funcname:{'16':xxx}
        fit_data[funcname] = func_data
        

        #筛选不在所有采样进程上运行的函数
        if re.match(r'mpi_',funcname,re.IGNORECASE) == None:
            merge_func = {}
            for  i in range(num_procs):
                merge_func[x[i]] = y[i]
            merge_datas[funcname] = merge_func
    # print(module)

    cd={}
    fa={}
    calldata_filenames = os.popen("find ./result_diff_module -name " + module + "_*")
    calldata_filenames = str(calldata_filenames.read()).split('\n')[:-1]
    for fl in calldata_filenames:
        nproc = re.findall(r"\d+", fl)[-1]

        fa_son_relation = csv.reader(open(fl, 'r'))
        for line in fa_son_relation:
            if line[3]=='0' and line[4]=='0':
                continue
            
            if re.match(r'mpi_',line[1],re.IGNORECASE) != None or re.match(r'mpi_',line[2],re.IGNORECASE)!=None:
                continue

            if line[2] not in cd:
                cd[line[2]]=1
            else:
                cd[line[2]]=cd[line[2]]+1 #非叶子节点

            if line[1] not in fa:
                fa[line[1]]=[]
            fa[line[1]].append([line[2],line[4],nproc])
            
    
    
    q=[]
    
    for func_data in merge_datas:
        if func_data not in cd or cd[func_data]<=0:
            q.append(func_data)
    
    
    while len(q)>0:
        tp=q[0]
        q=q[1:]
        
        if tp not in merge_datas:
            continue
        if is_zero(merge_datas[tp])==False and tp in fa:
            for f in fa[tp]:
                cd[f[0]]=cd[f[0]]-1
                if cd[f[0]]==0:
                    q.append(f[0])
            continue
        
        ldata=merge_datas[tp]
        
        #根结点
        if tp not in fa:
            continue

        for np in ldata:
            sum=0
            # 本进程的父子关系
            for f in fa[tp]:
                if f[2]!=np:
                    continue
                sum+=int(f[1])
                cd[f[0]]=cd[f[0]]-1
                if cd[f[0]]==0:
                    q.append(f[0])
            
            if sum==0:
                continue

            for f in fa[tp]:
                if f[2]!=np or f[0] not in merge_datas:
                    continue

                radio=int(f[1])/sum
                merge_datas[f[0]][np]+=merge_datas[tp][np]*radio
            merge_datas[tp][np]=0


  

    #write to file
    wf =  open("./fit_data/fit_data_module_" + module + ".csv", 'a', newline='')
    csv_write = csv.writer(wf)
    csv_write.writerow(head)
    csv_write.writerow(title)
    id = 0
    for key in merge_datas:
        if is_zero(merge_datas[key])==True:
            continue
        tmp_list = []
        tmp_list.append(id)
        tmp_list.append(key)
        id += 1
        for i in range(num_procs):
            tmp_list.append(int(merge_datas[key][x[i]]))
        csv_write.writerow(tmp_list)
       

    for key in fit_data:
        if key not in merge_datas:
            tmp_list=[]
            tmp_list.append(id)
            tmp_list.append(key)
            id+=1
            for i in range(num_procs):
                tmp_list.append(int(fit_data[key][x[i]]))
            csv_write.writerow(tmp_list)

    wf.close()
