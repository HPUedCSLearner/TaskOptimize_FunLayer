#include <string>
#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <set>
#include <map>
using namespace std;
int main()
{
	set<string> deletemulti;

	ifstream fr;
	fr.open("./usrDF.csv");
	ofstream fw;
	fw.open("./new_usrDF.csv");
	string line,inter;
	int usrdfflag=0;
	while(getline(fr,line))//读取fin中的整行字符存在line中
	{
		vector<string> v;
		for (int i = 0; i < line.length(); ++i)
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
		
		//将module func放在usfdf函数的前n个，这样不用再timer里再搜索
		if(deletemulti.find(v[0])==deletemulti.end())
		{
			deletemulti.insert(v[0]);
			fw<<usrdfflag;
			fw<<" "<<v[0];
			fw<<endl;
			usrdfflag++;
		}
		
	}
		
	return 0;
}