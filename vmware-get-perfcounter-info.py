#!/usr/bin/env python3
from pyVim.connect import SmartConnect, Disconnect
from getpass import getpass
from collections import OrderedDict
import ssl
import atexit
import argparse
import json

class login:
    """
    ログイン処理を抽象化したクラス
    """
    def __init__(self):
        self.username = ''
        self.password = ''
        self.host = ''

    def get_service_instance(self):
        """
        ServiceInstanceを取得するメソッド

        :rtype: class
        :return: pyVmomi.VmomiSupport.vim.ServiceInstance
        """
        # SSL証明書対策
        context = None
        if hasattr(ssl, '_create_unverified_context'):
            context = ssl._create_unverified_context()

        # ServiceInstanceを取得
        si = SmartConnect(host = self.host,
                          user = self.username,
                          pwd = self.password,
                          sslContext = context)

        # 処理完了時にvCenterから切断
        atexit.register(Disconnect, si)

        return si

def options():
    """
    コマンドラインオプション設定

    :rtype: class
    :return: argparse.Namespace
    """
    parser = argparse.ArgumentParser(prog='',
                                     add_help=True,
                                     description='')
    parser.add_argument('--host', '-vc',
                        type=str, required=True,
                        help='vCenterのIP又はホスト名')
    parser.add_argument('--username', '-u',
                        type=str, default='administrator@vsphere.local',
                        help='vCenterのログインユーザー名(default:administrator@vsphere.local)')
    parser.add_argument('--password', '-p',
                        type=str,
                        help='vCenterのログインユーザーパスワード')
    args = parser.parse_args()

    if(not(args.password)):
        args.password = getpass()

    return args

if __name__ == '__main__':
    # オプションを取得
    args = options()

    # ログイン情報を設定
    login = login()
    login.username = args.username
    login.password = args.password
    login.host = args.host

    # ServiceContentを取得
    content = login.get_service_instance().content

    # Performance Counterを取得
    perfCounters = content.perfManager.perfCounter

    # Performance Counterを整理
    r = {}
    for p in perfCounters:
        group = p.groupInfo.key
        counter = p.nameInfo.key
        rollup = p.rollupType
        unit = p.unitInfo.label
        if(p.groupInfo.label in r):
            r[p.groupInfo.label].append({
                'group': group,
                'counter': counter,
                'rollup': rollup,
                'unit': unit
            })
        else:
            r[p.groupInfo.label] = []
            r[p.groupInfo.label] = [{
                'group': group,
                'counter': counter,
                'rollup': rollup,
                'unit': unit
            }]

    # 結果をソートしてJSONで表示
    print(json.dumps(OrderedDict(sorted(r.items(), key=lambda x:x[0])), indent=2))
