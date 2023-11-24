#include <llvm/Pass.h>
#include <llvm/IR/Function.h>
#include <llvm/Support/raw_ostream.h>
#include <llvm/IR/InstIterator.h>
#include <llvm/IR/Instruction.h>
#include <llvm/IR/Instructions.h>
#include <llvm/IR/Module.h>
#include <llvm/IR/Metadata.h>
#include <llvm/IR/DebugInfo.h>
#include <llvm/IR/DebugLoc.h>
#include <llvm/IR/IntrinsicInst.h>
#include <llvm/Analysis/AliasAnalysis.h>
#include "llvm/IR/GlobalValue.h"
#include "llvm/IR/DerivedTypes.h"
#include "llvm/IR/Type.h"
#include "llvm/Support/FileSystem.h"

#include <string>
#include <iostream>
#include <unistd.h>
#include <string.h>
#include <fstream>


#define MAX_PATH 300

using namespace llvm;

namespace {
	class GetUsrDF : public ModulePass {
	public:
		static char ID;
		GetUsrDF() :ModulePass(ID) { }
		virtual bool runOnModule(Module &M) {
			
			
			char fpass[MAX_PATH];
			
			getcwd(fpass, MAX_PATH);
			
			std::error_code EC;
			std::string name;
			enum sys::fs::OpenFlags OpenFlag;
			OpenFlag = sys::fs::OF_Append;
			StringRef fileName1("${CASEPATH}/sampling/usrDF.csv");
			raw_fd_ostream file1(fileName1,  EC,  OpenFlag);

			StringRef fileName2("${CASEPATH}/sampling/no_insert_function.csv");
			raw_fd_ostream file2(fileName2,  EC,  OpenFlag);
			
			

			
			StringRef modulename(M.getName()); 
			sprintf(fpass, "%s/%s", fpass, modulename.data());

			for(Module::iterator F = M.begin(), E = M.end(); F != E; ++F){
				if( ! F -> isDeclaration()){
					file1 << F -> getName() << ","  << fpass << ","<< *( F -> getFunctionType()) ;
					for(Function :: arg_iterator ai = F ->arg_begin(), ae = F -> arg_end(); ai != ae; ++ai){
						Type* t = ai -> getType();
						file1 << ","<<  ai->getName().str() << "," << *t ;
					}
					file1 << "\n";
					name= F->getName();
					if(name =="MAIN_"|| name == "main"||name.find("mpi")!=name.npos||name.find("MPI")!=name.npos)
						continue;
					unsigned int instCount = 0;
					for (BasicBlock& bb : *F)
					{
					  instCount += std::distance(bb.begin(), bb.end());
					}
					if(instCount<20)
					{
						file2<<F -> getName()<<"\n";
					}
				}
				
			}
			
			file1.close();
			file2.close();
			return false;
		}
	};
	
}

char GetUsrDF :: ID = 0;
static RegisterPass<GetUsrDF> X("GetUsrDF", "find user define function",false, false);
