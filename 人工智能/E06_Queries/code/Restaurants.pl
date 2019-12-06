restaurant(mixuebingcheng,1998,drinks).
restaurant(muwushaokao,2003,barbecue).
restaurant(diandude,1993,yuecai).
restaurant(ajukejiacai,2007,yuecai).
restaurant(hongmenyan,2015,yuecai).
restaurant(dagangxianmiaoshaoji,2015,yuecai).
restaurant(huangmenjimifan,1935,lucai).
restaurant(shaxianxiaochi,1998,mincai).
restaurant(tongxianghui,2013,xiangcai).
restaurant(yangguofu,2007,dongbeicai).

branch(mixuebingcheng,wushan).
branch(mixuebingcheng,lujiang).
branch(mixuebingcheng,shipaixi).
branch(mixuebingcheng,yiyuannan).
branch(mixuebingcheng,beiting).
branch(mixuebingcheng,xintiandi).
branch(mixuebingcheng,beigang).
branch(mixuebingcheng,chentian).
branch(mixuebingcheng,chisha).
branch(mixuebingcheng,longdong).
branch(mixuebingcheng,zhucun).
branch(mixuebingcheng,shiqiao).

branch(muwushaokao,gangding).
branch(muwushaokao,shayuan).
branch(muwushaokao,heguang).
branch(muwushaokao,tangxia).
branch(muwushaokao,dongpu).
branch(muwushaokao,shengdi).
branch(muwushaokao,xiaogang).
branch(muwushaokao,tonghe).
branch(muwushaokao,diwangguangchang).
branch(muwushaokao,runzhengguangchang).

branch(diandude,huachengdadao).
branch(diandude,zhongshansi).
branch(diandude,huifudong).
branch(diandude,youtuobangshiguang).
branch(diandude,bainaohui).
branch(diandude,panfu).
branch(diandude,yangji).
branch(diandude,tianhebei).
branch(diandude,shiqiao).
branch(diandude,linhe).

branch(ajukejiacai,yongfu).
branch(ajukejiacai,xintiandi).
branch(ajukejiacai,shatainan).

branch(hongmenyan,xintiandi).
branch(hongmenyan,zhilanwan).

branch(dagangxianmiaoshaoji,yuancun).
branch(dagangxianmiaoshaoji,kecun).
branch(dagangxianmiaoshaoji,beishan).
branch(dagangxianmiaoshaoji,nanpudadao).
branch(dagangxianmiaoshaoji,xinshi).
branch(dagangxianmiaoshaoji,dongpu).
branch(dagangxianmiaoshaoji,huadong).
branch(dagangxianmiaoshaoji,fangcun).
branch(dagangxianmiaoshaoji,cencun).
branch(dagangxianmiaoshaoji,changxing).
branch(dagangxianmiaoshaoji,gaosheng).

branch(huangmenjimifan,siyoubei).
branch(huangmenjimifan,yuancun).
branch(huangmenjimifan,dongxiaonan).
branch(huangmenjimifan,dongxiaonan).
branch(huangmenjimifan,dongqu).
branch(huangmenjimifan,dalingang).
branch(huangmenjimifan,pazhou).
branch(huangmenjimifan,beigang).

branch(shaxianxiaochi,kangwangnan).
branch(shaxianxiaochi,beigang).
branch(shaxianxiaochi,luolang).

branch(yangguofu,xintiandi).
branch(yangguofu,dayuan).
branch(yangguofu,shishangtianhe).
branch(yangguofu,chebei).

branch(tongxianghui,bainaohui).
branch(tongxianghui,tianhebei).
branch(tongxianghui,yongfu).
branch(tongxianghui,shimaocheng).
branch(tongxianghui,hanting).
branch(tongxianghui,yuanyangmingyuan).
branch(tongxianghui,zhongshanyilu).
branch(tongxianghui,huizhoudasha).
branch(tongxianghui,kaifadadao).
branch(tongxianghui,maoshengdasha).

district(wushan,tianhe).
district(shipaixi,tianhe).
district(longdong,tianhe).
district(gangding,tianhe).
district(heguang,tianhe).
district(tangxia,tianhe).
district(dongpu,tianhe).
district(huachengdadao,tianhe).
district(youtuobangshiguang,tianhe).
district(bainaohui,tianhe).
district(tianhebei,tianhe).
district(linhe,tianhe).
district(yuancun,tianhe).
district(cencun,tianhe).
district(changxing,tianhe).
district(dalingang,tianhe).
district(shishangtianhe,tianhe).
district(chebei,tianhe).
district(bainaohui,tianhe).
district(hanting,tianhe).
district(yuanyangmingyuan,tianhe).


district(lujiang,haizhu).
district(yiyuannan,haizhu).
district(chisha,haizhu).
district(shayuan,haizhu).
district(xiaogang,haizhu).
district(runzhengguangchang,haizhu).
district(kecun,haizhu).
district(beishan,haizhu).
district(dongxiaonan,haizhu).
district(pazhou,haizhu).
district(huizhoudasha,haizhu).

district(beiting,panyu).
district(beigang,panyu).
district(xintiandi,panyu).
district(shiqiao,panyu).
district(zhilanwan,panyu).
district(nanpudadao,panyu).
district(maoshengdasha,panyu).

district(chentian,baiyun).
district(shengdi,baiyun).
district(tonghe,baiyun).
district(shatainan,baiyun).
district(xinshi,baiyun).
district(dayuan,baiyun).

district(zhucun,huadu).
district(huadong,huadu).

district(diwangguangchang,yuexiu).
district(zhongshansi,yuexiu).
district(huifudong,yuexiu).
district(panfu,yuexiu).
district(yangji,yuexiu).
district(yongfu,yuexiu).
district(siyoubei,yuexiu).
district(zhongshanyilu,yuexiu).

district(fangcun,liwan).
district(gaosheng,liwan).
district(kangwangnan,liwan).
district(shimaocheng,liwan).

district(dongqu,huangpu).
district(luolang,huangpu).
district(kaifadadao,huangpu).

% 2 区Dis 有种类为Type的菜
has_type(Dis,Type):-restaurant(R,_,Type),branch(R,Area),district(Area,Dis).

% 3 饭店R 有N个分支
num_branches(R,N):-setof(B,(restaurant(R,_,_),branch(R,B)),Branches), length(Branches,N).

% 4 地区A 有两个或更多饭店
more_than_2R(A):-setof(R,branch(R,A),L),length(L,Len),Len>=2.

% 6 饭店R有10个分支
more_than_10B(R):-setof(B,branch(R,B),L),length(L,Len),Len>=10.

% 7 饭店R1，R2，在同一个区都有分支
sameDistrict(R1, R2):-branch(R1, A1), branch(R2, A2), district(A1, D), district(A2, D), R1\=R2.



