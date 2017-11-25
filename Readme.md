# vmware-get-perfcounter-info

ZabbixでVMwareのパフォーマンスカウンター監視をする時に必要なVMwareのパフォーマンスカウンター一覧を表示するツール

## 必要条件

* python3
* pyvmomi

## インストール

```
$ git clone https://github.com/sky-joker/vmware-get-perfcounter-info.git
$ cd vmware-get-perfcounter-info
$ pip3 install -r requirements.txt
$ chmod +x vmware-get-perfcounter-info.py
```

## 使い方

### パフォーマンスカウンターを取得

vCenterからパフォーマンスカウンター一覧を取得します。

```
$ ./vmware-get-perfcounter-info.py -vc vcenter01.local
Password:
{
  "CPU": [
    {
      "group": "cpu",
      "rollup": "none",
      "counter": "usage",
      "unit": "%"
    },
    {
      "group": "cpu",
      "rollup": "average",
      "counter": "usage",
      "unit": "%"
    },
(snip)
```

## ライセンス

[MIT](https://github.com/sky-joker/vmware-get-perfcounter-info/blob/master/LICENSE.txt)

## 作者

[sky-joker](https://github.com/sky-joker)
