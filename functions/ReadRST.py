import rstparse, os
import numpy as np

from utilities import count_line


class ReadRST:
    """Read RST file."""
    def __init__(self, file_name, rst_path, *args, **kwargs,):
        """Initialize"""
        super().__init__(*args, **kwargs)
        self.file_name = file_name
        self.rst_path = rst_path

    def convert_file(self):
        """Main convert function."""
        self.read_rst()
        self.include_extra()
        self.detect_blocks()
        self.detect_sub_blocks()
        self.detect_title()
        self.detect_label_position()

    def read_rst(self):
        """Convert the rst file into a list of strings"""
        rst = rstparse.Parser()
        with open(self.file_name) as f:
            rst.read(f)
        rst.parse()
        file_content = []
        for line in rst.lines:
            file_content.append(line)
        self.file_content = file_content

    def include_extra(self, verbose = False):
        new_content = []
        for line in self.file_content:
            if ("include::" in line):
                relative_path = line.split("::")[1][1:]
                if verbose:
                    print(self.rst_path + relative_path)
                rst = rstparse.Parser()
                with open(self.rst_path+relative_path) as f:
                    rst.read(f)
                rst.parse()
                for extra_line in rst.lines:
                    new_content.append(extra_line)
            else:
                new_content.append(line)


            """
            if "non-tutorials/accessfile.rst" in line:
                assert os.path.exists("../lammpstutorials.github.io/docs/sphinx/source/non-tutorials/accessfile.rst")
                rst = rstparse.Parser()
                with open("../lammpstutorials.github.io/docs/sphinx/source/non-tutorials/accessfile.rst") as f:
                    rst.read(f)
                rst.parse()
                for extra_line in rst.lines:
                    new_content.append(extra_line)
            else:
                new_content.append(line)
            """
        self.file_content = new_content

    def detect_blocks(self):
        """Detect the blocks in the file"""
        main_block_type, main_block = self.read_block()
        self.main_block_type = main_block_type
        self.main_block = main_block 
     
    def detect_sub_blocks(self):
        """Detect the sub-blocks in the file"""
        sub_block_type, sub_block = self.read_subblock()
        self.sub_block_type = sub_block_type
        self.sub_block = sub_block 
            
    def detect_title(self):
        self.detect_title_position()
        assert np.sum(np.array(self.title_types) == "main") == 1, """More than one main title was found"""

    def detect_label_position(self):
        self.label_positions = []
        self.label_types = []
        for n, line in enumerate(self.file_content):
            if ('_' in line) & ('-label' in line):
                self.label_positions.append(n)
                self.label_types.append("main")

    def detect_title_position(self):
        self.title_positions = []
        self.title_types = []
        for n, line in enumerate(self.file_content):
            if line[:3] == "***":
                self.title_positions.append(n-1)
                self.title_types.append("main")
            elif line[:3] == "===":
                self.title_positions.append(n-1)
                self.title_types.append("subtitle")
            elif line[:3] == "---":
                self.title_positions.append(n-1)
                self.title_types.append("subsubtitle")

    def read_block(self):
        main_block = []
        main_block_type = []
        cpt_main_block = 0
        type = 'start'
        for line in self.file_content:
            new_block = False
            if ('.. ' in line) & (' .. ' not in line) & ('...' not in line) & ('../' not in line):
                # new main block with no indentation
                cpt_main_block += 1
                new_block = True
            elif len(line) > 0:
                if line[0] != ' ':
                    # titles
                    if ('====' not in line) & ('****' not in line) & ('----' not in line):
                        # ignore the underlines in titles
                        cpt_main_block += 1
                        new_block = True
            if new_block:
                if ('container:: justify' in line) | ('container:: abstract' in line):
                    type = 'text'
                elif 'container:: hatnote' in line: 
                    type = 'hatnote'
                elif 'admonition::' in line:
                    type = 'admonition' + line.split('::')[1]
                elif ('code-block' in line) & (('bw' in line) | ('bash' in line) | ('python' in line)):
                    type = 'bw-equation'
                elif ('code-block' in line) & ('lammps' in line):
                    type = 'lammps-equation'
                elif ('figure:: ' in line):
                    type = 'figure::' + line.split('::')[1]
                elif ('figurelegend' in line):
                    type = 'figurelegend'
                elif 'math::' in line:
                    type = 'math'
                elif '../non-tutorials/accessfile.rst' in line:
                    type = 'accessfile'
                else:
                    type = 'unknown'
            main_block_type.append(type)
            main_block.append(cpt_main_block)
        return main_block_type, main_block

    def read_subblock(self):
        sub_block = []
        sub_block_type = []
        cpt_sub_block = 0
        ref_space_number = 0
        type = 'start'
        for line, main_block_id in zip(self.file_content, self.main_block):
            new_block = False
            space_number = count_line(line)
            if (' .. ' in line) & ('...' not in line) & ('../' not in line):
                # new sub block
                cpt_sub_block = np.round(0.01 + cpt_sub_block, 2)
                new_block = True
                ref_space_number = space_number
            elif (space_number <= ref_space_number) & (len(line) > 0):
                # main block with no indentation
                cpt_sub_block = np.round(main_block_id * 1.0, 2)
                cpt_sub_block = np.round(0.01 + cpt_sub_block, 2)
                ref_space_number = space_number
                new_block = True
                type = 'unknown'
            if new_block:
                if len(line) > 0:
                    if line[0] != ' ':
                        type = 'unknown'
                    else:
                        if 'container:: justify' in line:
                            type = 'text'
                        elif 'container:: hatnote' in line: 
                            type = 'hatnote'
                        elif 'admonition::' in line:
                            type = 'admonition'
                        elif ('code-block' in line) & ('bw' in line):
                            type = 'bw-equation'
                        elif ('code-block' in line) & ('lammps' in line):
                            type = 'lammps-equation'
                        elif 'math::' in line:
                            type = 'math'
                        elif ('figure:: ' in line):
                            type = 'figure'
                        #elif ('figurelegend' in line):
                        #    type = 'figurelegend'
                        else:
                            type = 'unknown'
            sub_block_type.append(type)
            sub_block.append(cpt_sub_block)
        return sub_block_type, sub_block