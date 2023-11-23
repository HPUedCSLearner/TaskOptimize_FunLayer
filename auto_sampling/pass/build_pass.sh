CXXFLAGS=`llvm-config --cxxflags`
LDFLAGS=`llvm-config --ldflags`

clang -shared  -fPIC  $CXXFLAGS $LDFLAGS GetUsrDF.cpp -o GetUsrDF.so
clang -shared  -fPIC  $CXXFLAGS $LDFLAGS insert_tableline.cpp -o insert_tableline.so
clang -shared  -fPIC  $CXXFLAGS $LDFLAGS instrument_time_function.cpp -o instrument_time_function.so
