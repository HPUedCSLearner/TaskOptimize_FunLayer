#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <sstream>
#include <stdlib.h>
#include <memory.h>
#include <sys/stat.h>
#include <string.h>
#include <sys/types.h>
#include <dirent.h>
#include <map>
using namespace std;

void GetFileNames(string path,vector<string>& filenames)
{
    DIR *pDir;
    struct dirent* ptr;
    if(!(pDir = opendir(path.c_str())))
        return;
    while((ptr = readdir(pDir))!=0) {
        if (strcmp(ptr->d_name, ".") != 0 && strcmp(ptr->d_name, "..") != 0)
            filenames.push_back(ptr->d_name);
    }
    closedir(pDir);

}


void Split(const std::string& src, const std::string& separator, std::vector<std::string>& dest) //字符串分割到数组
{
//参数1：要分割的字符串；参数2：作为分隔符的字符；参数3：存放分割后的字符串的vector向量
	string str = src;
	string substring;
	string::size_type start = 0, index;
	dest.clear();
	index = str.find_first_of(separator,start);
	do
	{
		if (index != string::npos)
		{    
			substring = str.substr(start,index-start );
			dest.push_back(substring);
			start =index+separator.size();
			index = str.find(separator,start);
			if (start == string::npos) break;
		}
	}while(index != string::npos);
 
	//the last part
	substring = str.substr(start);
	dest.push_back(substring);
}

typedef struct{
	string func_name;
	long long self_time1 = 0, self_time2 = 0, self_time3=0, self_time4=0,self_time5=0, self_time6=0,self_time7=0,self_time8=0,self_time9  = 0,self_time10  = 0;
} node;

int main(int argc, char *argv[]){
	int i, j,k,flag, size,num_procs;
	char *p1 = argv[1];
	// int item_module_procs[12] = {0,0,0,0,0,0,0,0,0,0,0,0};
	string modules[16] = {"cpl","atm","lnd","ice","ocn","glc","wrf","gea","cplatm","cpllnd","cplice","cplocn","cplglc","cplwrf","cplgea","none"};
	num_procs = stoi(argv[1]);
	map<int, map<string, string>> module_procs;
	for (i = 1; i < num_procs + 1; i++){
		vector<string> filenames;
		string modulespath = "./readable_result_diff_module/readable_result_diff_module_" + to_string(i);
		GetFileNames(modulespath,filenames);
		for (int j = 0;j < filenames.size();j++){
			vector<string> tmp1, tmp2;
			Split(filenames[j], ".", tmp1);
			Split(tmp1[0], "_", tmp2);
			module_procs[i][tmp2[1]] = tmp2[2];
		}
	}

	string outfilepath;
	for ( k = 0; k < 16; ++k){
	vector<node> fit_data;
	vector<string> item_module_procs;
	for (i = 1; i < num_procs + 1; i++){ //if procnum_size=16 ,i = 16
		
		ostringstream inputfile;
		string tmp_procs = module_procs.find(i)->second.find(modules[k]) ->second;
		item_module_procs.push_back(tmp_procs);
		inputfile <<  "./readable_result_diff_module/readable_result_diff_module_"  << i  << "/single_"<<  modules[k] << '_'  << tmp_procs << ".csv";
		ifstream fr;
		fr.open(inputfile.str());
		string line,inter;
		
		getline(fr,line); //first line;
		
		while(getline(fr,line)){
			vector<string> s;
			node v;
			int length = line.length();
			for ( j = 0; j < length; ++j)
			{
				if (line[j] == ',')
				{
					line[j] = ' ';
				}
			}
			stringstream is(line);
			while (is >> inter)
			{
				s.push_back(inter);
			}
			
			v.func_name = s[1];
			
			if(i== 1){
				v.self_time1 = stoll(s[5]);
			}
			else if(i== 2){
				v.self_time2 = stoll(s[5]);
			}
			else if(i== 3){
				v.self_time3 = stoll(s[5]);
			}
			else if(i== 4){
				v.self_time4 = stoll(s[5]);
			}
			else if(i== 5){
				v.self_time5 = stoll(s[5]);
			}
			else if(i== 6){
				v.self_time6 = stoll(s[5]);
			}
			else if(i== 7){
				v.self_time7 = stoll(s[5]);
			}
			else if(i== 8){
				v.self_time8 = stoll(s[5]);
			}
			else if(i== 9){
				v.self_time9 = stoll(s[5]);
			}
			else if(i== 10){
				v.self_time10 = stoll(s[5]);
			}
			size = fit_data.size();
			flag = 0;
			for(j=0;j < size; j++){
				if(v.func_name == fit_data[j].func_name ){
					if(i== 1){
						fit_data[j].self_time1 = v.self_time1;
					}
					else if(i== 2){
						fit_data[j].self_time2 = v.self_time2;
					}
					else if(i== 3){
						fit_data[j].self_time3 = v.self_time3;
					}
					else if(i== 4){
						fit_data[j].self_time4 = v.self_time4;
					}
					else if(i== 5){
						fit_data[j].self_time5 = v.self_time5;
					}
					else if(i== 6){
						fit_data[j].self_time6 = v.self_time6;
					}
					else if(i== 7){
						fit_data[j].self_time7 = v.self_time7;
					}
					else if(i== 8){
						fit_data[j].self_time8 = v.self_time8;
					}
					else if(i== 9){
						fit_data[j].self_time9 = v.self_time9;
					}
					else if(i== 10){
						fit_data[j].self_time10 = v.self_time10;
					}
					flag = 1;
					break;
				}
			}
			
			if(flag == 0){
				fit_data.push_back(v);
			}
		}
		fr.close();
	}
	string filepath;
	filepath="./fit_data";
	mkdir(filepath.c_str(),S_IRWXU|S_IRGRP|S_IXGRP|S_IROTH);
	
	ostringstream outputfile;
	
	outputfile <<  "./fit_data/" << "fit_data_module_" << modules[k] <<".csv";
	mkdir(outfilepath.c_str(),S_IRWXU|S_IRGRP|S_IXGRP|S_IROTH);
	ofstream fw;
	fw.open(outputfile.str());
	
	size = fit_data.size();
	
	if (num_procs == 10){
		fw << item_module_procs[0] << "," <<  item_module_procs[1] << "," <<  item_module_procs[2] << "," <<  item_module_procs[3] << "," <<  item_module_procs[4] << "," <<  item_module_procs[5] << "," <<  item_module_procs[6] << "," <<  item_module_procs[7] << "," <<  item_module_procs[8] <<"," <<  item_module_procs[9] << "\n";
		fw << "id,func_name,self_time1,self_time2,self_time3,self_time4,self_time5,self_time6,self_time7,self_time8,self_time9" << "\n";

		for(j=0; j < size; ++j){
			fw << j << "," << fit_data[j].func_name << "," << fit_data[j].self_time1<< "," << fit_data[j].self_time2<< "," << fit_data[j].self_time3 << "," <<  fit_data[j].self_time4 << "," <<fit_data[j].self_time5<<","<< fit_data[j].self_time6 << "," << fit_data[j].self_time7 << ","<< fit_data[j].self_time8 << ","<<fit_data[j].self_time9<< ","<<fit_data[j].self_time10<<"\n";
		}
		fw.close();
	}
	else if (num_procs == 9){
		fw << item_module_procs[0] << "," <<  item_module_procs[1] << "," <<  item_module_procs[2] << "," <<  item_module_procs[3] << "," <<  item_module_procs[4] << "," <<  item_module_procs[5] << "," <<  item_module_procs[6] << "," <<  item_module_procs[7] << "," <<  item_module_procs[8] << "\n";
		fw << "id,func_name,self_time1,self_time2,self_time3,self_time4,self_time5,self_time6,self_time7,self_time8,self_time9" << "\n";

		for(j=0; j < size; ++j){
			fw << j << "," << fit_data[j].func_name << "," << fit_data[j].self_time1<< "," << fit_data[j].self_time2<< "," << fit_data[j].self_time3 << "," <<  fit_data[j].self_time4 << "," <<fit_data[j].self_time5<<","<< fit_data[j].self_time6 << "," << fit_data[j].self_time7 << ","<< fit_data[j].self_time8 << ","<<fit_data[j].self_time9<< "\n";
		}
		fw.close();
	}
	else if (num_procs == 8){
		fw << item_module_procs[0] << "," <<  item_module_procs[1] << "," <<  item_module_procs[2] << "," <<  item_module_procs[3] << "," <<  item_module_procs[4] << "," <<  item_module_procs[5] << "," <<  item_module_procs[6] << "," <<  item_module_procs[7] << "\n";
		fw << "id,func_name,self_time1,self_time2,self_time3,self_time4,self_time5,self_time6,self_time7,self_time8" << "\n";

		for(j=0; j < size; ++j){
			fw << j << "," << fit_data[j].func_name << "," << fit_data[j].self_time1<< "," << fit_data[j].self_time2<< "," << fit_data[j].self_time3 << "," <<  fit_data[j].self_time4 << "," <<fit_data[j].self_time5<<","<< fit_data[j].self_time6 << "," << fit_data[j].self_time7 << ","<< fit_data[j].self_time8 << "\n";
		}
		fw.close();
	}
	else if (num_procs == 7){
		fw << item_module_procs[0] << "," <<  item_module_procs[1] << "," <<  item_module_procs[2] << "," <<  item_module_procs[3] << "," <<  item_module_procs[4] << "," <<  item_module_procs[5] << "," <<  item_module_procs[6] << "\n";
		fw << "id,func_name,self_time1,self_time2,self_time3,self_time4,self_time5,self_time6,self_time7" << "\n";

		for(j=0; j < size; ++j){
			fw << j << "," << fit_data[j].func_name << "," << fit_data[j].self_time1<< "," << fit_data[j].self_time2<< "," << fit_data[j].self_time3 << "," <<  fit_data[j].self_time4 << "," <<fit_data[j].self_time5<<","<< fit_data[j].self_time6 << ","<< fit_data[j].self_time7 << "\n";
		}
		fw.close();
	}
	else if (num_procs == 6){
		fw << item_module_procs[0] << "," <<  item_module_procs[1] << "," <<  item_module_procs[2] << "," <<  item_module_procs[3] << "," <<  item_module_procs[4] << "," <<  item_module_procs[5] << "\n";
		fw << "id,func_name,self_time1,self_time2,self_time3,self_time4,self_time5,self_time6" << "\n";

		for(j=0; j < size; ++j){
			fw << j << "," << fit_data[j].func_name << "," << fit_data[j].self_time1<< "," << fit_data[j].self_time2<< "," << fit_data[j].self_time3 << "," <<  fit_data[j].self_time4 << "," <<fit_data[j].self_time5<< ","<< fit_data[j].self_time6 << "\n";
		}
		fw.close();
	}
	else if (num_procs == 5){
		fw << item_module_procs[0] << "," <<  item_module_procs[1] << "," <<  item_module_procs[2] << "," <<  item_module_procs[3] << "," <<  item_module_procs[4] << "\n";
		fw << "id,func_name,self_time1,self_time2,self_time3,self_time4,self_time5" << "\n";

		for(j=0; j < size; ++j){
			fw << j << "," << fit_data[j].func_name << "," << fit_data[j].self_time1<< "," << fit_data[j].self_time2<< "," << fit_data[j].self_time3 << "," <<  fit_data[j].self_time4 <<","<< fit_data[j].self_time5<<  "\n";
		}
		fw.close();
	}
	vector<node>().swap(fit_data);
	}
	return 0;
}