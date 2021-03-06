# This file is NOT licensed under the GPLv3, which is the license for the rest
# of YouCompleteMe.
#
# Here's the license text for this file:
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org/>

import os
import re
import getpass
import subprocess
import ycm_core

# These are the compilation flags that will be used in case there's no
# compilation database set (by default, one is not set).
# CHANGE THIS LIST OF FLAGS. YES, THIS IS THE DROID YOU HAVE BEEN LOOKING FOR.
flags = [
'-x',
'c++',
'-std=c++11',
'-I/usr/include/c++/4.8',
'-Ibuild_override/usr/include',
'-Ikernel/include',
'-Itpc/boost/include',
'-Itpc/include',
'-Ipsdrv_gpl/include',
'-Itpc/malloc2.13',
'-Itpc/lzopro/include',
'-Itpc/valgrind/include',
'-Itpc/xmlrpc/include',
'-Itpc/xmlrpc/local',
'-I/usr/include/dbus-1.0',
'-I/usr/lib/x86_64-linux-gnu/dbus-1.0/include',
'-Iplatform/include',
'-maes',
'-msse2',
'-msse4.1',
'-march=corei7',
'-fpermissive',
'-Wno-ignored-qualifiers',
'-Wno-unused-parameter',
'-Wno-type-limits',
'-Wno-extra',
'-Wno-delete-non-virtual-dtor',
'-Wno-invalid-offsetof',
'-Wno-unused-variable',
'-Wno-tautological-compare',
'-Wno-sometimes-uninitialized',
'-Wno-uninitialized',
'-Wno-unused-const-variable',
'-Wno-attributes',
'-Wno-overloaded-virtual',
'-Wno-return-stack-address',
'-Wno-missing-braces',
'-Wno-uninitialized',
'-Wno-unused-private-field',
'-Wno-null-conversion',
'-Wno-deprecated-register',
'-Wno-unused-function',
'-Wno-return-type',
'-Wno-redeclared-class-member',
'-Wno-gnu-variable-sized-type-not-at-end',
'-Wno-null-dereference',
'-Wno-deprecated-increment-bool',
'-Wno-dangling-field',
'-DPS_TOOLSET_GCC',
'-DPS_BUILD_DEBUG',
'-DPS_BUILD_ASYNC',
'-DPS_TOOLSET_CLANG',
]

# For some reason, system includes are not always returned by compilation database. Add them
# explicitly. See https://github.com/Valloric/YouCompleteMe/issues/303
def LoadSystemIncludes():
    regex = re.compile(ur'(?:\#include \<...\> search starts here\:)(?P<list>.*?)(?:End of search list)', re.DOTALL);
    process = []
    try:
        process = subprocess.Popen(['clang-3.5', '-v', '-E', '-x', 'c++', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE);
    except:
        process = subprocess.Popen(['clang', '-v', '-E', '-x', 'c++', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE);
    process_out, process_err = process.communicate('');
    output = process_out + process_err;
    includes = [];
    for p in re.search(regex, output).group('list').split('\n'):
        p = p.strip();
        if len(p) > 0 and p.find('(framework directory)') < 0:
            includes.append('-isystem');
            includes.append(p);
    return includes;

systemIncludes = LoadSystemIncludes();
# Set this to the absolute path to the folder (NOT the file!) containing the
# compile_commands.json file to use that instead of 'flags'. See here for
# more details: http://clang.llvm.org/docs/JSONCompilationDatabase.html
#
# See https://wiki.purestorage.com/display/IR/Code+Navigation+in+Linux+for+Iridium+Codebase
current_user = getpass.getuser()
compilation_database_folder = '/home/'+ current_user + '/bld_linux/ir-' + current_user

if os.path.exists( compilation_database_folder ) and os.path.exists(compilation_database_folder +
        '/compile_commands.json'):
  database = ycm_core.CompilationDatabase( compilation_database_folder )
else:
  database = None

SOURCE_EXTENSIONS = [ '.cpp', '.cxx', '.cc', '.c', '.m', '.mm' ]

def DirectoryOfThisScript():
  return os.path.dirname( os.path.abspath( __file__ ) )


def MakeRelativePathsInFlagsAbsolute( flags, working_directory ):
  if not working_directory:
    return list( flags )
  new_flags = []
  make_next_absolute = False
  path_flags = [ '-isystem', '-I', '-iquote', '--sysroot=' ]
  for flag in flags:
    new_flag = flag

    if make_next_absolute:
      make_next_absolute = False
      if not flag.startswith( '/' ):
        new_flag = os.path.join( working_directory, flag )

    for path_flag in path_flags:
      if flag == path_flag:
        make_next_absolute = True
        break

      if flag.startswith( path_flag ):
        path = flag[ len( path_flag ): ]
        new_flag = path_flag + os.path.join( working_directory, path )
        break

    if new_flag:
      new_flags.append( new_flag )
  return new_flags


def IsHeaderFile( filename ):
  extension = os.path.splitext( filename )[ 1 ]
  return extension in [ '.h', '.hxx', '.hpp', '.hh' ]


def GetCompilationInfoForFile( filename ):
  # The compilation_commands.json file generated by CMake does not have entries
  # for header files. So we do our best by asking the db for flags for a
  # corresponding source file, if any. If one exists, the flags for that file
  # should be good enough.
  if IsHeaderFile( filename ):
    basename = os.path.splitext( filename )[ 0 ]
    for extension in SOURCE_EXTENSIONS:
      replacement_file = basename + extension
      if os.path.exists( replacement_file ):
        compilation_info = database.GetCompilationInfoForFile(
          replacement_file )
        if compilation_info.compiler_flags_:
          return compilation_info
    return None
  return database.GetCompilationInfoForFile( filename )


def FlagsForFile( filename, **kwargs ):
  if IsHeaderFile(filename):
    relative_to = DirectoryOfThisScript()
    final_flags = MakeRelativePathsInFlagsAbsolute( flags, relative_to ) + systemIncludes
    return {
      'flags': final_flags,
      'do_cache': True
    }

  if database:
    # Bear in mind that compilation_info.compiler_flags_ does NOT return a
    # python list, but a "list-like" StringVec object
    compilation_info = GetCompilationInfoForFile( filename )
    if not compilation_info:
      return None

    final_flags = MakeRelativePathsInFlagsAbsolute(
      compilation_info.compiler_flags_,
      compilation_info.compiler_working_dir_ ) + systemIncludes

  else:
    relative_to = DirectoryOfThisScript()
    final_flags = MakeRelativePathsInFlagsAbsolute( flags, relative_to )

  return {
    'flags': final_flags,
    'do_cache': True
  }
