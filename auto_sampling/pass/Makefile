all:
	clang -shared  -fPIC  `llvm-config --cxxflags`  `llvm-config --ldflags` GetUsrDF.cpp -o GetUsrDF.so
	clang -shared  -fPIC    `llvm-config --cxxflags`  `llvm-config --ldflags`  insert_tableline.cpp -o insert_tableline.so
	clang -shared  -fPIC    `llvm-config --cxxflags`  `llvm-config --ldflags`  instrument_time_function.cpp -o instrument_time_function.so
