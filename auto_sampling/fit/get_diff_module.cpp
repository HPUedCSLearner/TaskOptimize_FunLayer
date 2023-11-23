#include <string>
#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <set>
#include <map>
#include <sys/stat.h>
#include <string.h>
using namespace std;
typedef struct 
{
	string self,father;
	long long times,acctime,wholetime;
}node;

int main(int argc, char * argv[])
{

	ifstream fr2;
	
	fr2.open("./new_usrDF.csv");
	
	map<string,string> m_num_name;
	string line,inter;
	int flag,i,j,id, nums;
	while(getline(fr2,line))
	{
		vector<string> v;
		for (i = 0; i < line.length(); ++i)
		{
			if (line[i] == ',')
			{
				line[i] = ' ';
			}
		}
		stringstream is(line);
		while (is >> inter)
		{
			v.push_back(inter);
		}
		m_num_name.insert(map<string, string>::value_type (v[0], v[1]));	
	}
	fr2.close();
	
	string filepath;
	filepath = "./result_diff_module";
	mkdir(filepath.c_str(),S_IRWXU|S_IRGRP|S_IXGRP|S_IROTH);
	int csvnum;
	
	char *p1 = argv[1];
	// int procnum[12] = {0,0,0,0,0,0,0,0,0,0,0,0};
	char *p2;
	char *p3;
	//string modules[16] = {"cpl","atm","lnd","ice","ocn","glc","wrf","gea"};
	string modules[16] = {"cpl","atm","lnd","ice","ocn","glc","wrf","gea","cplatm","cpllnd","cplice","cplocn","cplglc","cplwrf","cplgea","none"};
	nums = 0;
	map<string,string> module_procs;
	
	p2 = strtok(p1, ",");
	id = stoi(p2);
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
	//创建各module文件夹
	filepath = "./result_diff_module/result_diff_module_" +to_string(id);
	mkdir(filepath.c_str(),S_IRWXU|S_IRGRP|S_IXGRP|S_IROTH);
	//针对各module找相对应的1/2进程
	for(i=0;i<16;i++)
	{
		vector<node> vv;

		csvnum = stoi(module_procs.find(modules[i]) ->second) / 2;
		string filename1="./result_modules/result_module"+ to_string(id)  +"/"+to_string(csvnum)+".csv";

		ifstream fr1;
		fr1.open(filename1);
		while(getline(fr1,line))//读取fin中的整行字符存在line中
		{
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
			int time_location = i*3 + 2;
			//将module func放在usfdf函数的前n个，这样不用再timer里再搜索
			node nn;
			//mrecord.find(sonfatherflag)->second
			nn.self=m_num_name.find(v[0])->second;
			if(v[1]=="-1")
			{
				nn.father="NULL";
			}
			else
			{
				nn.father=m_num_name.find(v[1])->second;
			}
			nn.times=stoll(v[time_location]);
			nn.acctime=stoll(v[time_location+1]);
			nn.wholetime=stoll(v[time_location+2]);
			
			flag = 0;
			for(j = 0; j < vv.size(); j++){
				if(vv[j].self == nn.self && vv[j].father == nn.father){
					vv[j].times += nn.times;
					vv[j].acctime += nn.acctime;
					vv[j].wholetime += nn.wholetime;
					flag = 1;
				}
			}
			if(flag == 0){
				vv.push_back(nn);
			}
		}
		fr1.close();

		ofstream fw;
		string filename2="./result_diff_module/result_diff_module_" +to_string(id) + "/" +modules[i] + '_' + module_procs.find(modules[i]) ->second + ".csv";

		fw.open(filename2);
		int linenum=0;
		for(j=0;j<vv.size();j++)
		{
			
			fw<<linenum<<","<<vv[j].self<<","<<vv[j].father<<","<<vv[j].times<<","<<vv[j].acctime <<","<<vv[j].wholetime <<endl;
			linenum++;
		}
		fw.close();
		
	}

	return 0;
}