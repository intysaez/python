#!/usr/bin/python


import sys
import os
import pprint
import click
import remoteSynch
import repos


@click.group()
def syLib():
    pass


@syLib.command()
@click.option('--cfg', default='config.yml', type=click.Path(exists=True), help='Config yml file | default config.yml')
@click.option('--inside/--no-inside', default=False, help='List files recursive or not')
@click.option('--sha1/--md5', default='True', help='Hash function use for key generation')
@click.argument('origin', default='.', required=True, type=click.Path())
@click.argument('remote', required=True, type=click.Path())
def filekey(cfg, inside, sha1, origin, remote):
    '''
        Team # 2: File keys for all files on remote that match with origin
    '''
    fsHandle = remoteSynch.remoteSync(cfg)
    fsRepo = repos.featuresMgt(cfg)

    orList = fsHandle.getList(click.format_filename(origin), inside)
    rmList = fsHandle.getList(click.format_filename(remote), inside)

    if len(rmList) != 0:
        orList, rmlist = sorted(orList), sorted(rmList)

        matches = [item for item in [os.path.basename(file) for file in rmList] if item in [os.path.basename(file) for file in orList]]
        un_matches = [item for item in [os.path.basename(file) for file in rmList] if item not in [os.path.basename(file) for file in orList]]

        click.echo(''.join(['New files:',' ', str(len(un_matches))]))
        if len(un_matches) != 0:
            pprint.pprint(un_matches)

        for file in matches:
            for index in [item for item in range(len(rmList)) if os.path.basename(rmList[item]) == file]:
                click.echo(''.join([file,' @ ', os.path.dirname(rmList[index])]))

                lkey = fsRepo.fileSignature([filename for filename in [item for item in orList]  if os.path.basename(filename) == file ][0])
                rkey = fsHandle.fileSignature(rmList[index], sha1)
                if lkey != rkey:
                    click.echo(click.style('Origin hash', fg='magenta') + click.style(''.join([' <> ', lkey]), fg='red'))
                    click.echo(click.style('Origin hash', fg='magenta') + click.style(''.join([' <> ', rkey]), fg='blue'))
                else:
                    click.echo(click.style('Origin hash', fg='magenta') + click.style(''.join([' <> ', lkey]), fg='blue'))
                    click.echo(click.style('Origin hash', fg='magenta') + click.style(''.join([' <> ', rkey]), fg='blue'))


# click.echo(''.join([rmList[index],' ',fsHandle.fileSignature(rmList[index], sha1)]))
    else:
        click.echo('Remote does not have files')

@syLib.command()
@click.option('--cfg', default='config.yml', type=click.Path(exists=True), help='Config yml file | default config.yml')
@click.option('--inside/--no-inside', default=False, help='List files recursive or not')
@click.argument('target', default='.', required=True, type=click.Path())

def listFiles(cfg, inside, target):
    '''Team # 1: List all files in target directory
    If inside option is set True, will list files inside all sub-directory in target directory'''
    fsHandle = remoteSynch.remoteSync(cfg)
    pprint.pprint(fsHandle.getList(click.format_filename(target), inside))