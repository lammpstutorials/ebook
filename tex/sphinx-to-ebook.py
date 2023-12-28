#!/usr/bin/env python
# coding: utf-8

import sys, os, git

from ReadRST import ReadRST
from WriteTEX import WriteTex
from FixDocument import FixDocument

from tutorialslist import tutorials, non_tutorials

current_path = os.getcwd()
git_repo = git.Repo(current_path, search_parent_directories=True)
git_path = git_repo.git.rev_parse("--show-toplevel")
#sys.path.append(git_path+"/docs/inputs/shared-pyplot-files/")

if os.path.exists(git_path+'/tex/converted_files') is False:
    os.mkdir(git_path+'/tex/converted_files')

for level in tutorials.keys():
    if os.path.exists(git_path+'/tex/converted_files/'+level) is False:
        os.mkdir(git_path+'/tex/converted_files/'+level)
    for tutorial in tutorials[level]:
        print(level, "tutorial", tutorial)
        print("-----------------------------------------")
        rst_file_name = git_path+'/lammpstutorials.github.io/docs/sphinx/source/tutorials/'+level+'/'+tutorial+'.rst'
        tex_file_name = git_path+'/tex/converted_files/'+level+'/'+tutorial+'.tex'        
        RST = ReadRST(rst_file_name)
        RST.convert_file()
        assert len(RST.label_positions) == 1, """Careful, more than one label"""
        if ("vmd" in tutorial) | ("mdanalysis" in tutorial):
            TEX = WriteTex(tex_file_name, RST, git_path, nonumber=True)
        else:
            TEX = WriteTex(tex_file_name, RST, git_path)
        TEX.convert_file()
        FIX = FixDocument(tex_file_name)
        FIX.fix_document()

#non_tutorials = {"solutions": ["solutions"],
#                 "before-you-start": ["before-you-start"]}

if os.path.exists(git_path+'/tex/converted_files/non-tutorials/') is False:
    os.mkdir(git_path+'/tex/converted_files/non-tutorials/')

print("before-you-start")
print("-----------------------------------------")

rst_file_name = git_path+'/lammpstutorials.github.io/docs/sphinx/source/non-tutorials/before-you-start.rst'
tex_file_name = git_path+'/tex/converted_files/non-tutorials/before-you-start.tex'
RST = ReadRST(rst_file_name)
RST.convert_file()
assert len(RST.label_positions) == 1, """Careful, more than one label"""
TEX = WriteTex(tex_file_name, RST, git_path, nonumber=True)
TEX.convert_file()
FIX = FixDocument(tex_file_name)
FIX.fix_document()

print("solutions")
print("-----------------------------------------")

rst_file_name = git_path+'/lammpstutorials.github.io/docs/sphinx/source/non-tutorials/solutions.rst'
tex_file_name = git_path+'/tex/converted_files/non-tutorials/solutions.tex'
RST = ReadRST(rst_file_name)
RST.convert_file()
assert len(RST.label_positions) == 1, """Careful, more than one label"""
TEX = WriteTex(tex_file_name, RST, git_path, nonumber=True)
TEX.convert_file()
FIX = FixDocument(tex_file_name)
FIX.fix_document()
