#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter, namedtuple
import gzip, json, os, time

from shapely.geometry import Point, shape
from shapely.strtree import STRtree


District = namedtuple('District', 'code, province, city, county, name, valid, attr')

def __bycode(code):
    return __index.get(code)

def __byname(name, **kwargs):
    return __bycode(__match_name(name, **kwargs))

def __byloc(lon, lat, **kwargs):
    return __bycode(__match_loc(lon, lat, **kwargs))

def __tier(self):
    if 'tier' in self.attr:
        return self.attr['tier']
    if self.code % 10000 == 0:
        return 'NA'
    city = __bycode(self.code // 100)
    return city.attr.get('tier', 'T4-') if city else 'T4-'

def __region(self):
    if 'region' in self.attr:
        return self.attr['region']
    province = __bycode(self.code // 10000)
    return province.attr.get('region', 'NA') if province else 'NA'

def __cur_city(self):
    if 'curCity' in self.attr:
        return District.bycode(self.attr['curCity'])
    if self.valid and self.code % 10000 > 9000:
        return self
    city = __bycode(self.code // 100)
    if city and city.valid:
        return city
    return District.bycode(city.attr.get('curCity')) if city else None


District.bycode = __bycode
District.byname = __byname
District.byloc = __byloc
District.tier = __tier
District.region = __region
District.curcity = __cur_city


regions = ['东北', '华东', '华中', '华北', '华南', '西北', '西南']
city_tiers = ['T1', 'T2a', 'T2b', 'T3', 'T4-']

__autonomous_terms = set([
    '东乡族', '仡佬族', '仫佬族', '侗族', '保安族', '傈僳族', '傣族', '哈尼族',
    '哈萨克族', '回族', '土家族', '土族', '塔吉克族', '壮族', '布依族', '彝族',
    '撒拉族', '景颇族', '朝鲜族', '柯尔克孜族', '毛南族', '水族', '满族',
    '瑶族', '畲族', '白族', '维吾尔族', '羌族', '苗族', '蒙古族', '藏族',
    '锡伯族', '黎族',
])

def __rstrip_autonomous_terms(x):
    while True:
        done = True
        for i in range(len(x) - 2, 1, -1):
            if x[-i:] in __autonomous_terms or x[-i:] + '族' in __autonomous_terms:
                x = x[:-i]
                done = False
                break
        if done: break
    return x

def __gen_province_alias(province):
    if not isinstance(province, str) or not province:
        return None
    if province.endswith('自治区'):
        return (__rstrip_autonomous_terms(province[:-3]), province)
    elif province.endswith('特别行政区'):
        return (province[:-5], province)
    elif province.endswith('省') or province.endswith('市'):
        return (province[:-1], province)
    return (province,)

def __gen_city_alias(city):
    if not isinstance(city, str) or not city:
        return None
    if city == '市辖区' or city == '县' or '直辖县' in city:
        return None
    if city.endswith('自治州'):
        a = __rstrip_autonomous_terms(city[:-3])
        return (a + '州', a, city)
    elif city.endswith('地区'):
        return (city[:-2], city)
    elif city.endswith('盟'):
        return (city, city[:-1])
    elif len(city) > 2 and (city.endswith('市') or city.endswith('县')):
        return (city[:-1], city)
    return (city,)

def __gen_county_alias(county):
    if not isinstance(county, str) or not county or county == '市辖区':
        return None
    if len(county) > 3 and county[-2:] in ('新区', '矿区', '林区'):
        return (county, county[:-2])
    elif county.endswith('自治县'):
        c = __rstrip_autonomous_terms(county[:-3])
        return (c, c + '县', county)
    elif len(county) > 2 and county[-1] in ('区', '市', '县'):
        return (county[:-1], county)
    return (county,)

def __add_term(index, term, src_term, info):
    if term not in index:
        index[term] = (src_term, [info])
    else:
        cur_src_term, info_list = index[term]
        if cur_src_term is not None and cur_src_term != src_term:
            index[term] = (None, info_list)
        if info not in info_list:
            info_list.append(info)

def __load_data():
    index, inv_index = {}, {}
    filepath = os.path.join(os.path.dirname(__file__), 'district-info.tsv')
    for line in open(filepath, 'r'):
        code_s, flag, name, attr = line.split('\t')
        code = int(code_s)
        province, city, county = name.split(',')
        attr = json.loads(attr)
        province_alias = attr['province_alias'] = __gen_province_alias(province)
        city_alias = attr['city_alias'] = __gen_city_alias(city)
        county_alias = attr['county_alias'] = __gen_county_alias(county)
        province = province_alias[0] if province_alias else ''
        city = province if province_alias[-1][-1:] == '市' else \
               city_alias[0] if city_alias else ''
        county = county_alias[0] if county_alias else ''

        name = province + ('' if province_alias[-1][-1:] == '市' else city) + county
        d = District(code, province, city, county, name, 'A' in flag, attr)
        if code not in index or not index[code].valid:
            index[code] = index[code_s] = d
            if code_s[-2:] == '00':
                index[code//100] = index[code_s[:-2]] = d
            if code_s[-4:] == '0000':
                index[code//10000] = index[code_s[:-4]] = d

        if province_alias:
            leaf = city_alias is None and county_alias is None
            for a in province_alias:
                __add_term(inv_index, a, province, (d, 1, leaf))
        if city_alias:
            leaf = county_alias is None
            for a in city_alias:
                __add_term(inv_index, a, city, (d, 2, leaf))
        if county_alias:
            for a in county_alias:
                __add_term(inv_index, a, county, (d, 3, True))

    return index, inv_index

__timer = time.time()
__index, __inv_index = __load_data()
__inv_index_len = max(len(t) for t in __inv_index.keys())
# logging.info('District info loaded in %.2f seconds' % (time.time() - __timer, ))
# print(json.dumps(__index, ensure_ascii=False, indent=2))

def __match_name(name, valid=False):
    if not isinstance(name, str) or not name:
        return None

    name = name.strip()
    counter = Counter()
    while True:
        done = True
        for i in range(min(len(name), __inv_index_len), 1, -1):
            term = name[:i]
            if term in __inv_index:
                code_set, match = set(), False
                src_term, info_list = __inv_index[term]
                for d, level, leaf in info_list:
                    if (valid and not d.valid) or d.code in code_set:
                        continue
                    code_set.add(d.code)
                    counter[d.code] += 4 - 0.5 * level + leaf + d.valid + 0.1 * len(name)
                    match = True
                if match:
                    name = name[i:].lstrip(' |,.')
                    done = False
                    break
        if done: break

    if counter:
        # print(counter.most_common(3))
        return counter.most_common(1)[0][0]



def _load_boundary():

    province_boundary, city_boundary, county_boundary = [], [], []

    filepath = os.path.join(os.path.dirname(__file__), 'district-boundary.tsv.gz')
    for line in gzip.open(filepath, 'rt'):
        if not line or line[0] == '#':
            continue
        code, name, geodata = line.split('\t')
        polygon = shape(json.loads(geodata))
        polygon.dcode = int(code)
        if code[:2] not in ('11', '12', '31', '50') and code[2:] == '0000':
            province_boundary.append(polygon)
        elif code[2:4] == '90' or code[4:] == '00':
            city_boundary.append(polygon)
        else:
            county_boundary.append(polygon)

    return STRtree(province_boundary), STRtree(city_boundary), STRtree(county_boundary)

_timer = time.time()
_province_rtree, _city_rtree, _county_rtree = _load_boundary()
print('District boundaries loaded in %.2f secs' % (time.time() - _timer, ))

def __match_loc(lon, lat, match_county=False):
    pt = Point(lon, lat)
    if match_county:
        for c in _county_rtree.query(pt):
            if c.contains(pt):
                return c.dcode
    for c in _city_rtree.query(pt):
        if c.contains(pt):
            return c.dcode
    for p in _province_rtree.query(pt):
        if p.contains(pt):
            return p.dcode
    return None
