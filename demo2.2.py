'''
2.2 写出 特殊字符串+特殊进制字符串 的----27行
    再处理：有‘\’的留下  目前基本是对的
    问题：序列号好像不一样。。。   嘤嘤嘤  不会吧不会吧 T^T
'''

allList2=[]
with open("111triple.csv",'r')as f1:
    reads=f1.readlines()
    for i in reads:
        i=i.strip().split(',')
        allList2.append(i)
# print(allList2)

# 字典 id_seq={'GID',["id","\x2\..."]}
# 大字典 big_dict={'类别',[dic1,dic2,dic3,,,,]}   根据
 
# 1 先找到IfcGloballyUniqueId_ 所在的三元组,得到key    ---与正则相比，哪个快？目前：in比正则快?~
#   将id 所在三元组 存起来~ id_tri_dict={'IfcGloballyUniqueId_',[ [],[],[] ]}
id_tri_dict={}
for ifc_id in allList2:
    for hrt in ifc_id:  #遍历三元组的每一个,若是有
        if('IfcGloballyUniqueId_' in hrt):
            if hrt in id_tri_dict:
                id_tri_dict[hrt].append(ifc_id)
            else:
                id_tri_dict[hrt]=[]
                id_tri_dict[hrt].append(ifc_id)

# 2 存成字典
id_seq={}
gid_class={}
class_group_xxx=[]
for gid in id_tri_dict:
    # 列表顺序为了确保一致，要遍历两遍
    id_seq[gid]=[]       # 字典 id_seq={'GID',["乱码id","\x2\..."] ,'GID',["乱码id","\x2\..."] ,'GID',["乱码id","\x2\..."] }
    for tri1 in id_tri_dict[gid]: 
        if 'hasString' in tri1:
            id_seq[gid].append(tri1[2])
    class_xxx=[]
    for tri2 in id_tri_dict[gid]:
# 3.找到gid对应的类别，建个字典 gid_class={'ifcwin_xx':'gid'}
# 4.建立 类别_xx的列表，class_xxx=['ifcwin_xx','GID','\x2\...']
        if 'globalId_IfcRoot' in tri2:
            class_xxx.append(tri2[0])
            class_xxx.append(gid)
            gid_class[tri2[0]]=gid
    class_group_xxx.append(class_xxx)

 
# 4.开始找 \x2\... 通过ifcwin_xx            二重for太磨人了，用列表暂存一下吧。。。
class_label={}  #class_label={'ifcwin_xx':'label'}
for tri in allList2:
    for ifc_xx in gid_class:
        if ifc_xx in tri:
            if 'name_IfcRoot' in tri:
                class_label[ifc_xx]=tri[2]
# print(class_label)  ---目前没问题
# 5.找到strig
for tri in allList2:
    for ifc_xx in class_label:
        if class_label[ifc_xx] in tri:
            if "hasString" in tri:
                # print(tri[2]) 有点奇怪，，，不规律。。。
                # 存入class_xxx 
                for one in class_group_xxx:
                    if ifc_xx in one:
                        one.append(tri[2])
                # for i in class_group_xxx:
                #     print(i)


#     存入id_seq
for gid in id_seq:
    for one in class_group_xxx:
        if gid in one:
            try:
                id_seq[gid].append(one[2])
            except IndexError:
                pass

# 原始的 big_dict : big_dict={'类别',[dic1,dic2,dic3,,,,]}   
            # 下边的改成： big_dict={'类别',[[id,乱码],[],[],,,,]}
# 6.最终，写个大字典   id_seq={'GID',["乱码id","\x2\..."] ,'GID',["乱码id","\x2\..."] ,'GID',["乱码id","\x2\..."] }
big_dict={}          # big_dict={'类别',[[id,乱码],[],[],,,,]}
for gid in id_seq:
    for one in class_group_xxx:
        if gid in one:
            clas=one[0].split('_')[0]
    if clas in big_dict:
        big_dict[clas].append(id_seq[gid])
    else:
        big_dict[clas]=[]
        big_dict[clas].append(id_seq[gid])
# print(big_dict)

with open("2.2.txt",'w',newline='',encoding='utf-8')as f1:
    f1.write('类别'+'\t'+'特殊字符串'+'----------'+'特殊进制字符串'+'\n')
    for group in big_dict:
        for lis in big_dict[group]:
            try:
                if "\\" in lis[1]: 
                    f1.write(group+'\t'+lis[0]+'----------'+lis[1]+'\n')
            except IndexError:
                pass
