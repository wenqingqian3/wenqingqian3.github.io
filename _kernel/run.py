import os
import shutil
import subprocess

import argparse




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--command', type=str, help='command', required=False, default='update')
    parser.add_argument('-bit', '--blog_index_toc', type=str, help='blog_index_toc', required=False, default='on')
    
    args = parser.parse_args()

    # Define paths
    BLOG_MD = "../user/blog/"
    BLOG_CPP = "./src/_blog/"
    BLOG_WEB = "../webroot/blog/"

    if (args.command == "clean" or args.command == "all"):
        build_src = "./build"
        if os.path.exists(build_src):
            shutil.rmtree(build_src)
        if os.path.exists(BLOG_WEB):
            shutil.rmtree(BLOG_WEB)
        os.makedirs(BLOG_WEB)
    
    if (args.command == "update" or args.command == "all"):
        # Delete and create a new BLOG_CPP directory
        if os.path.exists(BLOG_CPP):
            shutil.rmtree(BLOG_CPP)
        os.makedirs(BLOG_CPP)

        # Generate CMakeLists.txt
        cmake_src = "./src/CMakeLists.txt"
        if os.path.exists(cmake_src):
            os.remove(cmake_src)
        open(cmake_src, 'w').close()

        # Traverse folders in the BLOG_MD directory
        multi_cate_once_gen = set()
        for blog_cate in os.listdir(BLOG_MD):
            blog_cate_path = os.path.join(BLOG_MD, blog_cate)
            
            if os.path.isdir(blog_cate_path):
                blog_cate_only = os.path.basename(blog_cate_path)

                # Create the corresponding BLOG_WEB directory
                blog_web_cate_path = os.path.join(BLOG_WEB, blog_cate_only)
                if not os.path.exists(blog_web_cate_path):
                    os.makedirs(blog_web_cate_path)

                # Create BLOG_CPP directory and CMakeLists.txt
                blog_cpp_cate_path = os.path.join(BLOG_CPP, blog_cate_only)
                os.makedirs(blog_cpp_cate_path)
                with open(os.path.join(blog_cpp_cate_path, "CMakeLists.txt"), "w") as cmake_file:
                    cmake_file.write(f'file(GLOB blogfile "*.cpp")\n')
                    cmake_file.write(f'add_library(blog_{blog_cate_only} STATIC ${{blogfile}})\n')

                # Update the main CMakeLists.txt
                with open(cmake_src, "a") as cmake_file:
                    cmake_file.write(f'add_subdirectory(./_blog/{blog_cate_only})\n')

                # Traverse .md files
                for file in os.listdir(blog_cate_path):
                    if file.endswith(".md"):
                        filepath = os.path.join(blog_cate_path, file)
                        filename = os.path.splitext(file)[0]
                        struct_name = ''.join([c if c.isalnum() else '_' for c in filename])

                        # Parse YAML front matter
                        with open(filepath, "r") as md_file:
                            lines = md_file.readlines()
                            yaml_content = [line.strip() for line in lines if "---" not in line]
                        
                        def get_field(field):
                            return next((line.split(":")[1].strip() for line in yaml_content if line.startswith(field)), "")

                        title = get_field("title")
                        date = get_field("date")
                        description = get_field("description")
                        category = get_field("category")
                        categorys = []
                        if category : categorys = category.split()
                        
                        author = get_field("author")
                        type_ = get_field("type")
                        language = get_field("language")
                        ps = get_field("ps")
                        redirect = get_field("redirect")

                        if category and blog_cate_only not in categorys:
                            print(f"Warning: blog {file} category in file ({category}) \
                                  doesn't match its directory name ({blog_cate_only}).")
                        
                        if len(categorys) > 1:
                            if not multi_cate_once_gen.__contains__(f"{struct_name}{category}{title}"):
                                multi_cate_once_gen.add(f"{struct_name}{category}{title}")
                            else:
                                print(f"error: file {blog_cate_only}/{filename}.md exist in other cate in {category}") 
                                continue

                        # Generate .cpp file
                        cpp_file = os.path.join(blog_cpp_cate_path, f"{filename}.cpp")
                        with open(cpp_file, "w") as cpp:
                            cpp.write('#include "blog.h"\n\n')
                            cpp.write(f"struct blog blog_{blog_cate_only}_{struct_name} = {{\n")
                            cpp.write(f'    target_file_name: "{filename}",\n')
                            cpp.write(f'    title: "{title}",\n')
                            cpp.write(f'    date: "{date}",\n')
                            cpp.write(f'    description: "{description}",\n')
                            cpp.write(f'    category: "{category}",\n')
                            cpp.write(f'    pri_category: "{blog_cate_only}",\n')
                            cpp.write(f'    author: "{author}",\n')
                            cpp.write(f'    type: "{type_}",\n')
                            cpp.write(f'    language: "{language}",\n')
                            cpp.write(f'    ps: "{ps}",\n')
                            cpp.write(f'    redirect: "{redirect}",\n')
                            cpp.write("};\n")

                        print(f"Created {cpp_file}")

        # Append to the CMakeLists.txt
        with open(cmake_src, "a") as cmake_file:
            cmake_file.write('file(GLOB file "*.cpp")\n')
            cmake_file.write('add_executable(generator ${file})\n')

        # Traverse the generator's target_link_libraries
        for blog_cate in os.listdir(BLOG_MD):
            blog_cate_path = os.path.join(BLOG_MD, blog_cate)
            if os.path.isdir(blog_cate_path):
                blog_cate_only = os.path.basename(blog_cate_path)
                with open(cmake_src, "a") as cmake_file:
                    cmake_file.write(f'target_link_libraries(generator blog_{blog_cate_only})\n')

        # Automatically update generator.cpp
        input_file = "./src/generator.cpp"
        directory = BLOG_CPP
        names = []

        # Extract struct blog names
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".cpp"):
                    filepath = os.path.join(root, file)
                    with open(filepath, "r") as cpp_file:
                        for line in cpp_file:
                            if "struct blog" in line:
                                name = line.split()[2].replace("=", "").strip()
                                names.append(name)

        # Modify generator.cpp
        inside_block = False
        new_content = ""

        with open(input_file, "r") as f:
            lines = f.readlines()

        for line in lines:
            if "// blog_generator_beg" in line:
                inside_block = True
                new_content += line
                for name in names:
                    new_content += f"extern blog {name};\n"
                new_content += "\nvoid blog_generate(){\n\tvector<blog> blogvec {\n"
                for name in names:
                    new_content += f"\t\t{name},\n"
                new_content += "\t};\n\textern void generate_blog_index(vector<blog>&, bool);\n"
                new_content += "\tgenerate_blog_index(blogvec, IF_GEN_BLOG_INDEX_TOC);\n}\n"
            elif "// blog_generator_end" in line:
                inside_block = False
                new_content += line
            elif inside_block:
                continue
            else:
                new_content += line

        with open(input_file, "w") as f:
            f.write(new_content)

        # Blog Archiving
        if not os.path.exists("../user/_blog_history"):
            os.makedirs("../user/_blog_history")
        shutil.copytree(BLOG_WEB, "../user/_blog_history", dirs_exist_ok=True)

        # Run CMake and make
        if not os.path.exists("build"):
            os.makedirs("build")

        subprocess.run(["cmake", ".."], cwd="build")
        subprocess.run(["make", "-j8"], cwd="build")

        # Run generator
        # subprocess.run(["./generator", args.blog_index_toc])

    if (args.command == "run" or args.command == "all"):
        subprocess.run(["./generator", args.blog_index_toc])