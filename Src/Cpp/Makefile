###################################
# SOURCE FILES AND RELEVANT PATHS
###################################

# Name of library
LIB=hsmooth

# Include paths
MYLIB_PATH=.
EIGEN_PATH=${HOME}/MyLibraries/Eigen
IGL_PATH=${HOME}/MyLibraries/libigl/include

# Source files
MYLIB_CPPS=Base.cpp HierarchicalSmooth.cpp Triangulation.cpp VolumeSolver.cpp

######################################
# COMPILER AND FLAGS
######################################

CPPS=$(patsubst %.cpp, $(MYLIB_PATH)/%.cpp, $(MYLIB_CPPS) )\
		$(patsubst %.cpp, $(EIGEN_PATH)/%.cpp, $(EIGEN_CPPS) )\
		$(patsubst %.cpp, $(PROJ_PATH)/%.cpp, $(PROJ_CPPS) )

HEADER_FILES=$(patsubst %.cpp, %.h, $(MYLIB_CPPS) )

OBJS = $(patsubst %.cpp, %.o, $(CPPS))

INCL = -I. -I$(MYLIB_PATH) -I$(EIGEN_PATH) -I$(IGL_PATH)

PRIMARY_FLAGS=-Wno-deprecated-declarations 
OPTIMIZER_FLAGS= -O3 -std=c++11 -fPIC
MY_LIBS=
DEBUG_FLAGS=
CFLAGS= ${PRIMARY_FLAGS} ${DEBUG_FLAGS} ${OPTIMIZER_FLAGS}

CC= /usr/bin/g++
AR= /usr/bin/ar
CTAGS= /usr/bin/ctags

######################################
# MAKE DIRECTIVES
######################################

%.o : %.cpp
	$(CC) -c $(INCL) $(CFLAGS) $< -o $@  $(MY_LIBS)

$(LIB):$(OBJS)
	$(AR) rcs lib${LIB}.a *.o
	$(CC) -shared -o lib${LIB}.so $(OBJS)
	$(CTAGS) $(HEADER_FILES) $(MYLIB_CPPS)

clean:
	rm -f $(OBJS) *~ $(MYLIB_PATH)/*~ $(EIGEN_PATH)/*~ *.a *.so tags


