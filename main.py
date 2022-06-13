import os
import sys
import argparse
import GitOperations
import warnings
import re


def create_remote_token(input_args):
    git_operator = GitOperations.GitOperator()
    remote_stat = git_operator.get_remote_url(input_args.remote_old)
    string_match = re.search('((?<=//).+)', remote_stat)
    url = string_match.group(0)
    url = "https://" + input_args.u + ":" + input_args.t + "@" + url
    git_operator.add_remote(input_args.remote_new, url)


def generate_remote_token(input_args):
    # don't change to active directory unless specified
    if args.dir is None:
        create_remote_token(args)
        return

    execution_dir = os.getcwd()

    for directory in args.dir:
        git_dir = os.path.abspath(directory)
        if not os.path.exists(git_dir):
            warnings.warn("Path " + git_dir + "doesn't exist, trying next path...", Warning, 2)
            continue
        os.chdir(git_dir)
        print("Creating remote token for git folder: " + git_dir)
        create_remote_token(input_args)
        os.chdir(execution_dir)


def tag_branch(input_args):
    git_operator = GitOperations.GitOperator()
    if input_args.r is not None:
        git_operator.set_remote(input_args.r)

    print(git_operator.checkout(input_args.s))

    print(git_operator.pull(input_args.s))
    print(git_operator.pull(input_args.d))

    print(git_operator.push(input_args.s, input_args.d))
    if input_args.m is not None:
        print(git_operator.tag(input_args.t, input_args.m))
    else:
        print(git_operator.tag(input_args.t))
    print(git_operator.push_tags())
    return


def tag_repositories(input_args):
    # don't change to active directory if specified
    if args.dir is None:
        tag_branch(args)
        return
    execution_dir = os.getcwd()

    for directory in args.dir:
        git_dir = os.path.abspath(directory)
        if not os.path.exists(git_dir):
            warnings.warn("Path " + git_dir + "doesn't exist, trying next path...", Warning, 2)
            continue
        os.chdir(git_dir)
        print("Tagging git folder: " + git_dir)
        tag_branch(args)
        os.chdir(execution_dir)


argParser = argparse.ArgumentParser("Tag Generator")
subParsers = argParser.add_subparsers(help='Tag Generator', dest="subcommand")

tagParser = subParsers.add_parser('tag')
tagParser.add_argument('-d', type=str, help='Destination branch')
tagParser.add_argument('-s', type=str, help='Source branch')
tagParser.add_argument('-m', type=str, help='Tag message')
tagParser.add_argument('-t', type=str, help='tag version')
tagParser.add_argument('-r', type=str, help='the remote in the .git to use')
tagParser.add_argument('-dir', type=str, nargs='*', help='directory or list of git directories to tag')


tokenParser = subParsers.add_parser('generate-tokens')
tokenParser.add_argument('-t', type=str, help="Token to use for the remote")
tokenParser.add_argument('-u', type=str, help="The username from which the token was generated")
tokenParser.add_argument('--remote-old', type=str, help="The existing remote from which the link will be generated",
                         required=True)
tokenParser.add_argument('--remote-new', type=str, help="The name of the new remote for which the link will be "
                                                        "generated")
tokenParser.add_argument('-dir', type=str, nargs='*', help='directory or list of git directories to tag')

args = argParser.parse_args()
if args.subcommand == 'tag':
    tag_repositories(args)
else:
    generate_remote_token(args)
exit(0)
