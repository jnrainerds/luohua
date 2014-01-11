#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 落花 / 测试套件 / 数据结构 / 虚文件
#
# Copyright (C) 2013-2014 JNRain
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals, division

import types

from ..utils import Case
from ..shortcuts import *

from luohua.datastructures import vfile


class TestVFile(Case):
    @classmethod
    def setup_class(cls):
        cls.owner_id = 'foobar'
        cls.ctime = 1329493828  # 这个其实是微雨 repo 的初始提交时间
        cls.title = 'Test topic 测试话题 ざわざわ'
        cls.content = '这是测试内容。\n有换行，显得比较真实\n'
        cls.xattr = {
                'a': 1,
                'b': True,
                }

        cls.file_1 = vfile.VFile(
                {
                    '_V': 1,
                    'o': cls.owner_id,
                    'c': cls.ctime,
                    't': cls.title,
                    'n': cls.content,
                    'x': cls.xattr,
                    },
                )

    @classmethod
    def teardown_class(cls):
        pass

    def test_props_v1(self):
        vf = self.file_1

        assert vf['owner'] == self.owner_id
        assert vf['ctime'] == self.ctime
        assert vf['title'] == self.title
        assert vf['content'] == self.content
        assert vf['xattr'] == self.xattr

    def test_db_ops(self):
        vf1 = self.file_1

        assert 'id' not in vf1
        vf1.save()
        assert 'id' in vf1
        assert vf1['id'] is not None
        vfid = vf1['id']

        vf2 = vfile.VFile.get(vfid)
        assert vf2['id'] == vf1['id']
        assert vf2['owner'] == vf1['owner']
        assert vf2['ctime'] == vf1['ctime']
        assert vf2['title'] == vf1['title']
        assert vf2['content'] == vf1['content']
        assert vf2['xattr'] == vf1['xattr']

        assert vfile.VFile.get('this-does-not-exist-does-it') is None

        vfgen = vfile.VFile.get_multiple([vfid, 'this-does-not-exist-too', ])
        assert isinstance(vfgen, types.GeneratorType)

        vfl = list(vfgen)
        assert len(vfl) == 2
        assert isinstance(vfl[0], vfile.VFile)
        assert vfl[1] is None
        assert vfl[0]['id'] == vfid
        del vfl

        vf2.purge()
        assert 'id' not in vf2

        assert vfile.VFile.get(vfid) is None


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
