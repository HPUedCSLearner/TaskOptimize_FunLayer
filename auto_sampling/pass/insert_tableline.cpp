#include <string>
#include <system_error>
#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <map>
#include <set>
#include <string.h>

#include "llvm/Support/raw_ostream.h"
#include "llvm/Pass.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/Constants.h"
#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/Type.h"
#include "llvm/Transforms/IPO/PassManagerBuilder.h"
#include "llvm/ADT/STLExtras.h"
#include "llvm/Support/Casting.h"
#include "llvm/IR/ModuleSummaryIndex.h"


using namespace llvm;


struct Insert_Tableline : public ModulePass
{
  static char ID;
  Insert_Tableline() : ModulePass(ID){}
  
  bool runOnModule(Module &M) override
  {
	std::string strSplit,s2;
	std::vector<std::string> records, record_line;
	std::stringstream input;
	std::map<std::string,std::string> mrecord;
	std::ifstream infile( "${CASEPATH}/sampling/new_usrDF.csv", std::ios::in);
	std::istreambuf_iterator<char> beg(infile), end;
	std::string s1(beg,end);
	infile.close();
	s1.erase(s1.find_last_not_of("\n") + 1);
	strSplit = "\n";
	std::vector<std::string>::size_type sPos = 0;
	std::vector<std::string>::size_type ePos = s1.find( strSplit, sPos );
	while( ePos != std::string::npos )
	{
		if( sPos != ePos ) records.push_back( s1.substr( sPos, ePos - sPos ) );
		sPos = ePos + strSplit.size();    
		ePos = s1.find( strSplit, sPos );
	}    
	if( sPos < s1.size() ) records.push_back( s1.substr( sPos, s1.size() - sPos ) );
	
	// delete []buff;
	
	for(std::vector<std::string>::iterator iter = records.begin(); iter != records.end(); iter++){
		input.clear();
		input << *iter;
		while(input >> s2)
			record_line.push_back(s2);
		mrecord.insert(make_pair(record_line[1],record_line[0]));//1是funcname,0是funcnum
		input.str("");
		std::vector<std::string>().swap(record_line);
		
	}


	LLVMContext &llvmContext = M.getContext(); 
	
	GlobalVariable* father = new GlobalVariable(/*Module=*/M, 
	/*Type=*/Type::getInt32Ty(llvmContext),
	/*isConstant=*/false,
	/*Linkage=*/GlobalValue::ExternalLinkage,
	/*Initializer=*/0, // has initializer, specified below
	/*Name=*/"__profile__fatherID");
	father->setDSOLocal(true);
	father->setAlignment(4);//set global variable
	
	GlobalVariable* self = new GlobalVariable(/*Module=*/M, 
	/*Type=*/Type::getInt32Ty(llvmContext),
	/*isConstant=*/false,
	/*Linkage=*/GlobalValue::ExternalLinkage,
	/*Initializer=*/0, // has initializer, specified below
	/*Name=*/"__profile__funcID");
	self->setDSOLocal(true);
	self->setAlignment(4);//set global variable
	
	GlobalVariable* module = new GlobalVariable(/*Module=*/M, 
	/*Type=*/Type::getInt32Ty(llvmContext),
	/*isConstant=*/false,
	/*Linkage=*/GlobalValue::ExternalLinkage,
	/*Initializer=*/0, // has initializer, specified below
	/*Name=*/"__profile__module");
	module->setDSOLocal(true);
	module->setAlignment(4);//set global variable
	for(Module::iterator F = M.begin(); F != M.end(); ++F)
	{
		if (Function* G = dyn_cast<Function>(F))
		{
			LLVMContext &context = G->getContext();
			std::string father="";
			father=G->getName();
			if(mrecord.find(father) == mrecord.end() || mrecord.find(father)->second=="")
				continue;
			if(F->getBasicBlockList().begin() != F->getBasicBlockList().end())
			{
				BasicBlock &bb = G->getEntryBlock();
				Instruction *beginInst = dyn_cast<Instruction>(bb.begin());
				ConstantInt* const_int_15 = ConstantInt::get(context, APInt(32, StringRef(mrecord.find(father)->second), 10));
				StoreInst* store_15=new StoreInst(const_int_15, self , beginInst);
			}
		}
	}
	
	return false;
  }
};

char Insert_Tableline::ID = 0;

static RegisterPass<Insert_Tableline> X("Insert_Tableline", "Insert_Tableline", false, false);
