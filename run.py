import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--command', type=str, help='command', required=False, default='update')
parser.add_argument('-bit', '--blog_index_toc', type=str, help='blog_index_toc', required=False, default='on')
args = parser.parse_args()

print(args)


subprocess.run(["python3","./run.py"], cwd="webroot")
subprocess.run(["python3","./run.py", "-c", f"{args.command}", "-bit", f"{args.blog_index_toc}"], cwd="_kernel")
