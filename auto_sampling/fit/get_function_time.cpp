#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <sstream>
#include <stdlib.h>
#include <memory.h>
#include <sys/stat.h> 
#include <map>
/*
处理时需不需要将各module下相应进程的csv合并处理？
1.合并
1.1 func_a在module 1上运行，在2上没用运行。其时间在2上的记录为0. 在处理module 2时，func_a的父函数不能减去func_a的运行时间。
1.2 若一个函数在两个module下均运行，则合并后其时间被合并
2. 分离

问题：一个函数的子函数属于另一个module，在当前module中的计时为0；即在当前module中统计时，该函数并不会减去其属于另一个module的子函数的时间。
*/
using namespace std;
typedef struct 
{
	string func_name;
	long long sub_func_time=0;
	long long self_time=0;
	long long called_time=0;
}node;

typedef struct
{
	string func_name;
	long long self_time=0;
	long long called_time=0;
} son;

typedef struct 
{
	string func_name;
	long long sub_func_time=0;
} father;

int main(int argc, char *argv[])
{
	string outfilepath;
	outfilepath="./readable_result_diff_module";
	mkdir(outfilepath.c_str(),S_IRWXU|S_IRGRP|S_IXGRP|S_IROTH);
	
	int procnumber,i,j,k,z,p,flag, nums, count;
	char *p1 = argv[1];
	// int procnum[12] = {0,0,0,0,0,0,0,0,0,0,0,0};
	char *p2;
	char *p3;
	string modules[16] = {"cpl","atm","lnd","ice","ocn","glc","wrf","gea","cplatm","cpllnd","cplice","cplocn","cplglc","cplwrf","cplgea","none"};
	nums = 0;
	map<string,string> module_procs;
	
	p2 = strtok(p1, ",");
	procnumber = stoi(p2);
	while(NULL !=p2)
	{
		p2 = strtok(NULL, ",");
		if (p2 != NULL){
			if (nums %2 ==0){
				p3 = p2;
			}
			else{
				module_procs[p3] = p2;
			}
			nums++;
		}
	}
	//创建readable文件
	outfilepath= "./readable_result_diff_module/readable_result_diff_module_" + to_string(procnumber); 
	mkdir(outfilepath.c_str(),S_IRWXU|S_IRGRP|S_IXGRP|S_IROTH);
	
	for (k = 0; k < 16; ++k)
	{
		
		ostringstream inputfile,outputfile;
		inputfile << "./result_diff_module/result_diff_module_" << procnumber<< "/" << modules[k] << '_'  << module_procs.find(modules[k]) ->second<< ".csv";
		outputfile << outfilepath<<  "/single_" << modules[k] << '_'  << module_procs.find(modules[k]) ->second<< ".csv";
		ifstream fr;
		
		fr.open(inputfile.str());//以输入方式打开文件存到缓冲空间fin中
		
		ofstream fw;
		fw.open(outputfile.str());
		string line,inter;
		
		vector<son> vson;
		vector<father> vfather;
		vector<node> vnode;
		
		
		
		while(getline(fr,line))//读取fin中的整行字符存在line中
		{//cout<<line<<endl;
			if(line.length() < 2)	continue;
			vector<string> v;
			
			for (j = 0; j < line.length(); ++j)
			{
				if (line[j] == ',')
				{
					line[j] = ' ';
				}
			}

			stringstream is(line);
			while (is >> inter)
			{
				v.push_back(inter);
			}
			if(v[3]=="0"&&v[4]=="0")
				continue;
			
			if (v[1].find("ccsm_comp_mod_ccsm_")  != v[1].npos && modules[k] != "none"){
				continue;
			}
			son s;
			father f;

			s.func_name=v[1];

			s.self_time=stoll(v[4]);
			s.called_time=stoll(v[3]);
			
			f.func_name=v[2];
			f.sub_func_time+=stoll(v[4]);
			
			
			
			flag=0;//标记是否已经记录过函数
			for(j=0;j<vson.size();j++)
			{
				if(s.func_name==vson[j].func_name)
				{
					vson[j].self_time+=s.self_time;
					vson[j].called_time+=s.called_time;
					flag=1;
					break;
				}
			}
			if(flag==0)
				vson.push_back(s);
			flag=0;
			if(f.func_name=="NULL")
			{
				flag=1;
			}
			else if (f.func_name.find("ccsm_comp_mod_ccsm_")  != f.func_name.npos && modules[k] != "none"){
				flag = 1;
			}
			else{
				for(j=0;j<vfather.size();j++)
					if(f.func_name==vfather[j].func_name)
					{
						vfather[j].sub_func_time+=f.sub_func_time;
						flag=1;
						break;
					}
				}
			
			if(flag==0)
				vfather.push_back(f);
		}
		
		
		fr.close();
		
		
		//cout<<vson.size()<<endl;
		for(j=0;j<vson.size();j++)
		{
			node n;
			n.func_name=vson[j].func_name;
			n.self_time=vson[j].self_time;
			n.called_time=vson[j].called_time;

			for(z=0;z<vfather.size();z++)
			{
				if(vfather[z].func_name==n.func_name)
				{
					n.sub_func_time+=vfather[z].sub_func_time;
				}
			}
			if(n.func_name.find("ccsm_comp_mod_ccsm_") != n.func_name.npos and modules[k] == "none")
			{
				for(i=0; i < 15; i++){
					ostringstream module_file;
					ifstream overtime_process;
					module_file << "./result_diff_module/result_diff_module_" << procnumber << "/" <<modules[i] << '_' << module_procs.find(modules[i]) ->second << ".csv";
					overtime_process.open(module_file.str());
					//cout<<module_file.str()<<endl;
					while(getline(overtime_process,line))
					{
						vector<string> v;
						for (z = 0; z < line.length(); ++z)
						{
							if (line[z] == ',')
							{
								line[z] = ' ';
							}
						}

						stringstream is(line);
						while (is >> inter)
						{
							v.push_back(inter);
						}
						if(v[2] == n.func_name && v[3] != "0"){
							n.sub_func_time+= stoll(v[4]);
						}
					}
					overtime_process.close();
				}
			}
			vnode.push_back(n);
		}

		fw<<"id,func_name,sub_func_time,called_times,run_time,self_time"<<endl;
		count=0;

		for(j=0;j<vnode.size();j++)
		{
			fw<<count<<","<<vnode[j].func_name<<","<<vnode[j].sub_func_time<<","<<vnode[j].called_time<<","<<vnode[j].self_time<<","<<vnode[j].self_time-vnode[j].sub_func_time<<endl;
			count++;
		}
		fw.close();
	
	}

	return 0;
}