#include <string>
#include <system_error>
#include <iostream>
#include <set>
#include <fstream>
#include <string.h>

#include "llvm/Support/raw_ostream.h"
#include "llvm/Pass.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/Transforms/IPO/PassManagerBuilder.h"

using namespace llvm;

struct Ins_TimeFunc : public ModulePass
{
	static char ID;
	Ins_TimeFunc() : ModulePass(ID){}
    
	bool runOnModule(Module &M) override
	{
		std::string s;
		std::ifstream infile2; 
		
		infile2.open("${CASEPATH}/sampling/no_insert_function.csv"); 
		std::set<std::string> no_insert_func;
		while(std::getline(infile2,s))
		{
			no_insert_func.insert(s);
		}
		infile2.close();
		
		LLVMContext &llvmContext = M.getContext(); 
		for(Module::iterator F = M.begin(); F != M.end(); ++F)
		{  
			if (Function* G = dyn_cast<Function>(F))
			{
				std::string father= F->getName();
				LLVMContext &context = G->getContext();
				
				if(no_insert_func.find(father)!=no_insert_func.end())
					continue;
				
				if(F->getBasicBlockList().begin() != F->getBasicBlockList().end())
				{
					BasicBlock &bb = G->getEntryBlock();
					Instruction *beginInst = dyn_cast<Instruction>(bb.begin());
					
					if(father=="main"||father=="MAIN_")
					{
						FunctionType *type = FunctionType::get(Type::getVoidTy(context), {}, false);
						Constant *beginFun = G->getParent()->getOrInsertFunction("__profile__initialize_table", type);
						CallInst *inst = CallInst::Create(beginFun);
						inst->insertBefore(beginInst);
					}
					
					FunctionType *type = FunctionType::get(Type::getInt64Ty(context), {}, false);
					Constant *beginFun = F->getParent()->getOrInsertFunction("__profile__record_time_begin", type);
					Value *beginTime = nullptr;					
					
					if (Function *fun = dyn_cast<Function>(beginFun))
					{
					  
					  CallInst *inst = CallInst::Create(beginFun);
					  inst->insertBefore(beginInst);
					  beginTime = inst;
					}
					
					
					for (Function::iterator I = F->begin(), E = F->end(); I != E; ++I)
					{
					  BasicBlock &BB = *I;
					  for (BasicBlock::iterator I = BB.begin(), E = BB.end(); I != E; ++I)
					  {

						ReturnInst *IST = dyn_cast<ReturnInst>(I);
						if (IST)
						{
						  FunctionType *type = FunctionType::get(Type::getVoidTy(context), {Type::getInt8PtrTy(context),Type::getInt64Ty(context)}, false);
						  Constant *s = BB.getModule()->getOrInsertFunction("__profile__record_time_end", type);
						  if (Function *fun = dyn_cast<Function>(s))
						  {
							IRBuilder<> builder(&BB);
							CallInst *inst = CallInst::Create(fun, {builder.CreateGlobalStringPtr(BB.getParent()->getName()), beginTime});
							inst->insertBefore(IST);
							if(father=="main"||father=="MAIN_")
							{
								FunctionType *type = FunctionType::get(Type::getVoidTy(context), {}, false);
								Constant *beginFun = G->getParent()->getOrInsertFunction("__profile__input_csv", type);
								CallInst *inst = CallInst::Create(beginFun);
								inst->insertBefore(IST);
							}
						  }
						}
					  }
					}
				}
			}
		}	
		return false;
	}
};

char Ins_TimeFunc::ID = 0;

static RegisterPass<Ins_TimeFunc> X("Ins_TimeFunc", "Ins_TimeFunc", false, false);