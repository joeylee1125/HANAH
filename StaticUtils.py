# -*- 'coding',: 'UTF',-'8', -*-
import re


court_trans = {'zhongji':'中级',
              'chengdu':'成都',
              'zigong':'自贡',
              'panzhihua':'攀枝花',
              'luzhou':'泸州',
              'deyang':'德阳',
              'mianyang':'绵阳',
              'guangyuan':'广元',
              'shuining':'遂宁',
              'neijiang':'内江',
              'leshan':'乐山',
              'nanchong':'南充',
              'meishan':'眉山',
              'yibing':'宜宾',
              'guangan':'广安',
              'dazhou':'达州',
              'yaan':'雅安',
              'bazhong':'巴中',
              'ziyang':'资阳',
              'wenchuan':'汶川',
              'kangding':'康定',
              'xichang':'西昌',
              'tielu':'铁路'}

court_set = {#'zhongji':'',
              'chengdu':'',
              'zigong':'',
              'panzhihua':'',
              'luzhou':'',
              'deyang':'',
              'mianyang':'',
              'guangyuan':'',
              'shuining':'',
              'neijiang':'',
              'leshan':'',
              'nanchong':'',
              'meishan':'',
              'yibing':'',
              'guangan':'',
              'dazhou':'',
              'yaan':'',
              'bazhong':'',
              'ziyang':'',
              'wenchuan':'',
              'kangding':'',
              'xichang':'',
              'tielu':''}
              

court_set['zhongji'] = {'四川省成都市中级人民法院',
'四川省自贡市中级人法院',
'四川省攀枝花市中级人民法院',
'四川省泸州市中级人民法院',
'四川省德阳市中级人民法院',
'四川省绵阳市中级人民法院',
'四川省广元市中级人民法院',
'四川省遂宁市中级人民法院',
'四川省内江市中级人民法院',
'四川省乐山市中级人民法院',
'四川省南充市中级人民法院',
'四川省眉山市中级人民法院',
'四川省宜宾市中级人民法院',
'四川省广安市中级人民法院',
'四川省达州市中级人民法院',
'四川省雅安市中级人民法院',
'四川省巴中市中级人民法院',
'四川省资阳市中级人民法院',
'四川省阿坝藏族羌族自治州中级人民法院',
'四川省甘孜藏族自治州中级人民法院',
'四川省凉山彝族自治州中级人民法院',
'成都铁路运输中级法院'}


court_set['chengdu'] = {'成都市中级人民法院',
'成都市锦江区人民法院',
'成都市青羊区人民法院',
'成都市金牛区人民法院',
'成都市武侯区人民法院',
'成都市成华区人民法院',
'成都市龙泉驿区人民法院',
'成都市青白江区人民法院',
'成都市温江区人民法院',
'金堂县人民法院',
'双流区人民法院',
'双流县人民法院',
'郫县人民法院',
'大邑县人民法院',
'蒲江县人民法院',
'新津县人民法院',
'都江堰市人民法院',
'彭州市人民法院',
'邛崃市人民法院',
'崇州市人民法院',
'成都高新技术产业开发区人民法院'}

court_set['zigong'] = {'自贡市中级人民法院',
'自贡市自流井区人民法院',
'自贡市贡井区人民法院',
'自贡市大安区人民法院',
'自贡市沿滩区人民法院',
'荣县人民法院',
'富顺县人民法院'}

court_set['panzhihua'] = {'攀枝花市中级人民法院',
'攀枝花市东区人民法院',
'攀枝花市西区人民法院',
'攀枝花市仁和区人民法院',
'米易县人民法院',
'盐边县人民法院'}

court_set['luzhou'] = {'泸州市中级人民法院',
'泸州市江阳区人民法院',
'泸州市纳溪区人民法院',
'泸州市龙马潭区人民法院',
'泸县人民法院',
'合江县人民法院',
'叙永县人民法院',
'古蔺县人民法院'}

court_set['deyang'] = {'德阳市中级人民法院',
'德阳市旌阳区人民法院',
'中江县人民法院',
'罗江县人民法院',
'广汉市人民法院',
'什邡市人民法院',
'绵竹市人民法院'}

court_set['mianyang'] = {'绵阳市中级人民法院',
'绵阳市涪城区人民法院',
'绵阳市游仙区人民法院',
'三台县人民法院',
'盐亭县人民法院',
'绵阳市安州区人民法院',
'安县人民法院',
'梓潼县人民法院',
'北川羌族自治县人民法院',
'平武县人民法院',
'江油市人民法院',
'四川省科学城人民法院',
'绵阳高新技术产业开发区人民法院'}

court_set['guangyuan'] = {'广元市中级人民法院',
'广元市利州区人民法院',
'广元市昭化区人民法院',
'广元市朝天区人民法院',
'旺苍县人民法院',
'青川县人民法院',
'剑阁县人民法院',
'苍溪县人民法院'}

court_set['shuining'] = {'遂宁市中级人民法院',
'遂宁市船山区人民法院',
'船山区人民法院',
'遂宁市安居区人民法院',
'蓬溪县人民法院',
'射洪县人民法院',
'大英县人民法院'}

court_set['neijiang'] = {'内江市中级人民法院',
'内江市市中区人民法院',
'内江市东兴区人民法院',
'威远县人民法院',
'资中县人民法院',
'隆昌县人民法院'}

court_set['leshan'] = {'乐山市中级人民法院',
'乐山市市中区人民法院',
'乐山市沙湾区人民法院',
'乐山市五通桥区人民法院',
'乐山市金口河区人民法院',
'犍为县人民法院',
'井研县人民法院',
'夹江县人民法院',
'沐川县人民法院',
'峨边彝族自治县人民法院',
'马边彝族自治县人民法院',
'峨眉山市人民法院'}


court_set['nanchong'] = {'南充市中级人民法院',
'南充市顺庆区人民法院',
'南充市高坪区人民法院',
'南充市嘉陵区人民法院',
'南部县人民法院',
'营山县人民法院',
'蓬安县人民法院',
'仪陇县人民法院',
'西充县人民法院',
'阆中市人民法院'}


court_set['meishan'] = {'眉山市中级人民法院',
'眉山市东坡区人民法院',
'眉山市彭山区人民法院',
'仁寿县人民法院',
'彭山县人民法院',
'洪雅县人民法院',
'丹棱县人民法院',
'青神县人民法院'}

court_set['yibing'] = {'宜宾市中级人民法院',
'宜宾市翠屏区人民法院',
'宜宾市南溪区人民法院',
'宜宾县人民法院',
'江安县人民法院',
'长宁县人民法院',
'高县人民法院',
'珙县人民法院',
'筠连县人民法院',
'兴文县人民法院',
'屏山县人民法院'}

court_set['guangan'] = {'广安市中级人民法院',
'广安市广安区人民法院',
'广安市前锋区人民法院',
'岳池县人民法院',
'武胜县人民法院',
'邻水县人民法院',
'华蓥市人民法院'}

court_set['dazhou'] = {'达州市中级人民法院',
'达州市通川区人民法院',
'达州市达川区人民法院',
'宣汉县人民法院',
'开江县人民法院',
'大竹县人民法院',
'渠县人民法院',
'万源市人民法院'}

court_set['yaan'] = {'雅安市中级人民法院',
'雅安市雨城区人民法院',
'雅安市名山区人民法院',
'荥经县人民法院',
'汉源县人民法院',
'石棉县人民法院',
'天全县人民法院',
'芦山县人民法院',
'宝兴县人民法院'}

court_set['bazhong'] = {'巴中市中级人民法院',
'巴中市巴州区人民法院',
'巴中市恩阳区人民法院',
'通江县人民法院',
'南江县人民法院',
'平昌县人民法院'}

court_set['ziyang'] = {'资阳市中级人民法院',
'资阳市雁江区人民法院',
'安岳县人民法院',
'乐至县人民法院',
'简阳市人民法院'}

court_set['wenchuan'] = {'阿坝藏族羌族自治州中级人民法院',
'汶川县人民法院',
'理县人民法院',
'茂县人民法院',
'松潘县人民法院',
'九寨沟县人民法院',
'金川县人民法院',
'小金县人民法院',
'黑水县人民法院',
'马尔康市人民法院',
'马尔康县人民法院',
'壤塘县人民法院',
'阿坝县人民法院',
'若尔盖县人民法院',
'红原县人民法院'}

court_set['kangding'] = {'甘孜藏族自治州中级人民法院',
'康定市人民法院',
'康定县人民法院',
'泸定县人民法院',
'丹巴县人民法院',
'九龙县人民法院',
'雅江县人民法院',
'道孚县人民法院',
'炉霍县人民法院',
'甘孜县人民法院',
'新龙县人民法院',
'德格县人民法院',
'白玉县人民法院',
'石渠县人民法院',
'色达县人民法院',
'理塘县人民法院',
'巴塘县人民法院',
'乡城县人民法院',
'稻城县人民法院',
'得荣县人民法院'}

court_set['xichang'] = {'凉山彝族自治州中级人民法院',
'西昌市人民法院',
'木里藏族自治县人民法院',
'盐源县人民法院',
'德昌县人民法院',
'会理县人民法院',
'会东县人民法院',
'宁南县人民法院',
'普格县人民法院',
'布拖县人民法院',
'金阳县人民法院',
'昭觉县人民法院',
'喜德县人民法院',
'冕宁县人民法院',
'越西县人民法院',
'甘洛县人民法院',
'美姑县人民法院',
'雷波县人民法院'}

court_set['tielu'] = {'成都铁路运输中级法院',
'成都铁路运输法院',
'西昌铁路运输法院'}

report_col_names = ['file_name', 'verdict', 'id', 'court', 'region', 'court_level', 'prosecutor',
              'procedure', 'year', 'd_name', 'd_age', 'd_sex', 'd_nation', 'd_education',
              'd_job', 'd_lawyer', 'd_lawyer_n', 'd_s_lawyer', 'd_s_lawyer_n', 'd_has_lawyer',
              'd_charge', 'd_charge_c', 'd_prison', 'd_prison_l', 'd_probation', 'd_probation_l',
              'd_fine', 'd_bail', 'd_pre_charge','d_sue_date', 'd_judge_date', 'd_days_in_court']



court_list_all = ['成都市锦江区人民法院',
'成都市青羊区人民法院',
'成都市金牛区人民法院',
'成都市武侯区人民法院',
'成都市成华区人民法院',
'成都市龙泉驿区人民法院',
'成都市青白江区人民法院',
'成都市新都区人民法院',
'成都市温江区人民法院',
'金堂县人民法院',
'成都市双流区人民法院',
'郫都区人民法院',
'大邑县人民法院',
'蒲江县人民法院',
'新津县人民法院',
'都江堰市人民法院',
'彭州市人民法院',
'邛崃市人民法院',
'崇州市人民法院',
'成都高新技术产业开发区人民法院',
'自贡市自流井区人民法院',
'自贡市贡井区人民法院',
'自贡市大安区人民法院',
'自贡市沿滩区人民法院',
'荣县人民法院',
'富顺县人民法院',
'攀枝花市东区人民法院',
'攀枝花市西区人民法院',
'攀枝花市仁和区人民法院',
'米易县人民法院',
'盐边县人民法院',
'泸州市江阳区人民法院',
'泸州市纳溪区人民法院',
'泸州市龙马潭区人民法院',
'泸县人民法院',
'合江县人民法院',
'叙永县人民法院',
'古蔺县人民法院',
'德阳市旌阳区人民法院',
'中江县人民法院',
'罗江县人民法院',
'广汉市人民法院',
'什邡市人民法院',
'绵竹市人民法院',
'绵阳市涪城区人民法院',
'绵阳市游仙区人民法院',
'三台县人民法院',
'盐亭县人民法院',
'绵阳市安州区人民法院',
'梓潼县人民法院',
'北川羌族自治县人民法院',
'平武县人民法院',
'江油市人民法院',
'四川省科学城人民法院',
'绵阳高新技术产业开发区人民法院',
'广元市利州区人民法院',
'广元市昭化区人民法院',
'广元市朝天区人民法院',
'旺苍县人民法院',
'青川县人民法院',
'剑阁县人民法院',
'苍溪县人民法院',
'遂宁市船山区人民法院',
'遂宁市安居区人民法院',
'蓬溪县人民法院',
'射洪县人民法院',
'大英县人民法院',
'内江市市中区人民法院',
'内江市东兴区人民法院',
'威远县人民法院',
'资中县人民法院',
'隆昌县人民法院',
'乐山市市中区人民法院',
'乐山市沙湾区人民法院',
'乐山市五通桥区人民法院',
'乐山市金口河区人民法院',
'犍为县人民法院',
'井研县人民法院',
'夹江县人民法院',
'沐川县人民法院',
'峨边彝族自治县人民法院',
'马边彝族自治县人民法院',
'峨眉山市人民法院',
'南充市顺庆区人民法院',
'南充市高坪区人民法院',
'南充市嘉陵区人民法院',
'南部县人民法院',
'营山县人民法院',
'蓬安县人民法院',
'仪陇县人民法院',
'西充县人民法院',
'阆中市人民法院',
'眉山市东坡区人民法院',
'眉山市彭山区人民法院',
'仁寿县人民法院',
'洪雅县人民法院',
'丹棱县人民法院',
'青神县人民法院',
'宜宾市翠屏区人民法院',
'宜宾市南溪区人民法院',
'宜宾县人民法院',
'江安县人民法院',
'长宁县人民法院',
'高县人民法院',
'珙县人民法院',
'筠连县人民法院',
'兴文县人民法院',
'屏山县人民法院',
'广安市广安区人民法院',
'广安市前锋区人民法院',
'岳池县人民法院',
'武胜县人民法院',
'邻水县人民法院',
'华蓥市人民法院',
'达州市通川区人民法院',
'达州市达川区人民法院',
'宣汉县人民法院',
'开江县人民法院',
'大竹县人民法院',
'渠县人民法院',
'万源市人民法院',
'雅安市雨城区人民法院',
'雅安市名山区人民法院',
'荥经县人民法院',
'汉源县人民法院',
'石棉县人民法院',
'天全县人民法院',
'芦山县人民法院',
'宝兴县人民法院',
'巴中市巴州区人民法院',
'巴中市恩阳区人民法院',
'通江县人民法院',
'南江县人民法院',
'平昌县人民法院',
'资阳市雁江区人民法院',
'安岳县人民法院',
'乐至县人民法院',
'简阳市人民法院',
'汶川县人民法院',
'理县人民法院',
'茂县人民法院',
'松潘县人民法院',
'九寨沟县人民法院',
'金川县人民法院',
'小金县人民法院',
'黑水县人民法院',
'马尔康市人民法院',
'壤塘县人民法院',
'阿坝县人民法院',
'若尔盖县人民法院',
'红原县人民法院',
'康定市人民法院',
'泸定县人民法院',
'丹巴县人民法院',
'九龙县人民法院',
'雅江县人民法院',
'道孚县人民法院',
'炉霍县人民法院',
'甘孜县人民法院',
'新龙县人民法院',
'德格县人民法院',
'白玉县人民法院',
'石渠县人民法院',
'色达县人民法院',
'理塘县人民法院',
'巴塘县人民法院',
'乡城县人民法院',
'稻城县人民法院',
'得荣县人民法院',
'西昌市人民法院',
'木里藏族自治县人民法院',
'盐源县人民法院',
'德昌县人民法院',
'会理县人民法院',
'会东县人民法院',
'宁南县人民法院',
'普格县人民法院',
'布拖县人民法院',
'金阳县人民法院',
'昭觉县人民法院',
'喜德县人民法院',
'冕宁县人民法院',
'越西县人民法院',
'甘洛县人民法院',
'美姑县人民法院',
'雷波县人民法院',
'成都铁路运输法院',
'西昌铁路运输法院']

zm_group_list = ['sq_list', 'jtzs_wxjs_list', 'jysxzmdqt_list', 'twhl_list', 
                 'scxswlsp_list', 'dpfz_list', 'dq_list', 'qjie_list', 'qjian_list', 'qduo_list',
                 'gysr_list', 'gysh_list', 'ffjj_list', 'ksdc_list', 'cx_list',
                 'jzdo_xxzs_list', 'dflm_list', 'zp_list', 'fx_list','zzjsmy_list',
                 'qt_list'] 






zm_group_name = {'sq_list':'涉枪犯罪',
                 'jtzs_wxjs_list':'交通肇事和危险驾驶', 
                 'jysxzmdqt_list':'具有死刑罪名的其他', 
                 'twhl_list':'贪污贿赂', 
                 'scxswlsp_list':'生产销售伪劣商品', 
                 'dpfz_list':'毒品犯罪',
                 'dq_list':'盗窃',
                 'qjie_list':'抢劫',
                 'qduo_list':'抢夺',
                 'qjian_list':'强奸',
                 'gysr_list':'故意杀人',
                 'gysh_list':'故意伤害',
                 'ffjj_list':'非法拘禁',
                 'ksdc_list':'开设赌场',
                 'cx_list':'传销',
                 'jzdo_xxzs_list':'聚众斗殴和寻衅滋事',
                 'dflm_list':'盗伐林木',
                 'zp_list':'诈骗',
                 'fx_list':'非法吸收公众存款',
                 'zzjsmy_list':'组织介绍卖淫',
                 'qt_list':'其他'}
                 
                 

zm_group = {}


zm_group['fx_list'] = ['非法吸收公共存款', '非法吸收公众存款']
zm_group['dq_list'] = ['盗窃']
zm_group['qjie_list'] = ['抢劫']
zm_group['qduo_list'] = ['抢夺']
zm_group['qjian_list'] = ['强奸']
zm_group['gysh_list'] = ['故意伤.', '故意伤害', '伤害']
zm_group['gysr_list'] = ['故意杀人']
zm_group['ffjj_list'] = ['非法拘禁']
zm_group['ksdc_list'] = ['开设赌场', '开赌场']
zm_group['cx_list'] = ['传销', '组织、领导传销活动']

# 其他
zm_group['qt_list'] = ['走私珍贵动物制品',
                       '走私普通货物、物品',
                       '走私普通物品',
                      '出售非法制造的发票',
                      '虚假广告',
                      '挪用特定款物',
                      '重大劳动安全事故',
                      '扰乱法庭秩序',
                      '聚众扰乱(社会|公共场所|交通)?秩序',
                      #'聚众扰乱社会秩序',
                      #'聚众扰乱交通秩序',
                      #'聚众扰乱秩序',
                      '虚开用于抵扣税款发票',
                      '私分国有资产',
                      '利用封建迷信致人死亡',
                      '徇私舞弊暂予监外执行',
                      '盗掘古文化遗址',
                      '非法获取公民个人信息',
                      '出售、非法提供公民个人信息',
                      '非法处置冻结的财产',
                      '持有伪造的发票',
                      '拒不执行(人民)?(法院)?判决',
                      '帮助毁灭伪造证据',
                      '过失致人重',
                      '帮助(伪造|毁灭)证据',
                      '偷越国境',
                      #'非法毁坏国家重点保护植物',
                      '非法(毁坏|采伐|运输)国家重点保护植物',
                      '非法收购、运输、出售国家重点保护植物',
                      #'非法采伐国家重点保护植物',
                      '非法收购、运输国家重点保护植物',
                      '非法(出售|收购)国家重点保护植物',
                      #'非法收购国家重点保护植物',
                      '违法发放贷款',
                      '非法提供信用卡信息',
                      '倒卖文物',
                      '伪造金融票证',
                      '聚众哄抢',
                      #'非法(收购|猎捕)珍贵、濒危野生动物',
                      #'非法收购、出售珍贵、濒危野生动物',
                      '侵占',
                      '环境污染',
                      '持有、使用假币',
                      '聚众淫乱',
                      '侮辱',
                      '抽逃出资',
                      '巨额财产来源不明',
                      '收买、非法提供信用卡信息',
                      '提供侵入、非法控制计算机信息系统程序、工具',
                      '虚开抵扣税款发票',
                      #'',
                      '虚开发票',
                      '脱逃',
                      '伪造、变造国家机关公文',
                      '(伪造|买卖)(国家机关|武装部队)(印章|证件|公文)',
                      '伪造国家机关证件、印章',
                      '非法侵入他人住宅',
                      '倒卖车票',
                      '敲诈勒索',
                      #'伪造武装部队印章',
                      '(毁|损)坏(公私)?财物',
                      '职务侵占',
                      '非法侵入住宅',
                      '买卖身份证件',
                      '替考',
                      '妨害公务',
                      '妨碍公务',
                      '行贿',
                      '隐瞒(犯罪)?所得',
                      '过失致人(死亡|重伤)',
                      '污染环境',
                      '赌博',
                      '重大责任事故',
                      '.造.*(印章|证件)',
                      '伪造居民身份证',
                      '伪造货币',
                      '(购买|持有)假币',
                      '失火',
                      '拒不支付劳动报酬',
                      '猥亵',
                      '非法获取国家秘密',
                      '玩忽职守',
                      '滥用职权',
                      '重婚',
                      '假冒注册商标',
                      '破坏电力设备',
                      '挪用公款',
                      '非法经营',
                      '串通投标',
                      '(出售|购买|运输)假币',
                      '挪用资金',
                      '非法行医',
                      '招摇撞骗',
                      '冒充军人招摇撞骗',
                      '强迫交易',
                      '传播淫秽物品牟利',
                      '..尸体',
                      '销售非法制造的注册商标标识',
                      '拒不(执|履)行判决',
                      '窝藏',
                      '非法占(有|用)农用地',
                      '非法占用农用地',
                      '破坏公用电信设施',
                      '妨害信用卡管理',
                      #'(非法)?(收购.)?(运输.)?(出售.)?(珍贵.)?(濒危)?野生动物制品',
                      #'非法猎捕、杀害珍贵、濒危野生动物',
                      #'非法收购、运输国家珍贵、濒危野生动物',
                      #'非法收购、运输国家重点保护的珍贵野生动物',
                      '野生动物',
                      '非法采伐、毁坏国家重点保护植物',
                      '破坏军婚',
                      '破坏计算机信息系统',
                      '犯?非法获取计算机信息系统数据',
                      '非法狩猎',
                      '非法采矿',
                      '非法入侵(他人)?住宅',
                      '爆炸',
                      '非法制造、买卖、储存爆炸物',
                      '骗取贷款',
                      '扰乱无线电通讯管理秩序',
                      '虚开增值税专用发票',
                      '伪证',
                      '盗掘古墓葬',
                      '侵犯公民个人信息',
                      '徇私枉法',
                      '掩饰、隐瞒犯',
                      '组织考试作弊',
                      '伪造(事业单位|公司)印章',
                      '信用卡诈骗',
                      '代替考试',
                      '组织未成年人进行违反治安管理活动',
                      '贩卖淫秽物品牟利',
                      '非国家工作人员(行|受)贿',
                      '包庇',
                      '单位行贿',
                      '掩饰隐瞒犯',
                      '逃税',
                      '防火',
                      '非法获取计算机信息系统数据',
                      '编造虚假恐怖信息',
                      '利用邪教组织破坏法律实施',
                      '诬告陷害',
                      '非法储存炸物',
                      '破坏生产经营',
                      '失职致使在押人员脱逃',
                      '虐待',
                      '使用虚假身份证件',
                      '非法处置查封的财产',
                      '购买伪造的增值税专用发票',
                      '破坏监管秩序',
                      '非法处置查封的财产',
                      '虚开抵扣发票',
                      '偷越国（边）境',
                      '妨害作证',
                      '传播淫秽物品',
                      '非法捕捞水产品',
                      '虚假诉讼',
                      '洗钱',
                      '遗弃',
                      '高利转贷',
                      '聚众冲击国家机关',
                      '国有公司人员失职',
                      '提供侵入计算机信息系统程序',
                      '提供非法控制计算机信息系统程序',
                      '国有事业单位人员失职',
                      '非法收购珍贵野生动物',
                      '非法收购、运输珍贵、濒危野生动物',
                      '危害驾驶',
                      '侵犯著作权',
                      '贩卖淫秽物品',
                      '虚报注册资本',
                      '破坏广播电视设施',
                      '过失损坏公用电信设施',
                      '非法处置查封、扣押、冻结的财产',
                      '非法处置扣押的财产',
                      '非法处置查封、扣押的财产',
                      '非法生产警用装备',
                      #'非法杀害珍贵、濒危野生动物',
                      '内幕交易',
                        '走私国家禁止进出口的货物',
                        '贩卖、制造品',
                      '非法采伐、出售国家重点保护植物']


                      
# 组织介绍卖淫
zm_group['zzjsmy_list'] = ['组织淫秽表演', '介绍、容留卖淫', '容留、介绍卖淫', '容留卖淫', '协助组织卖淫', '介绍卖淫', '组织卖淫', '\w\w卖淫']                     
#组织淫秽表演


#盗伐林木(盗伐，滥伐林木）
zm_group['dflm_list'] = ['滥伐林木', '滥发林木', '盗伐林木','非法收购、运输盗伐、滥伐的林木','非法收购盗伐、滥伐的林木','非法收购盗伐的林木','非法运输盗伐、滥伐的林木', '非法收购滥伐的林木']


#诈骗
zm_group['zp_list'] = ['集资诈骗', '合同诈骗', '诈骗', '(合同)?诈骗']

#聚众斗殴和寻衅滋事
zm_group['jzdo_xxzs_list'] = ['聚众斗殴',
                              '寻衅滋事',
                              '寻.滋事']

 
#涉枪犯罪
zm_group['sq_list'] = ['非法持有枪支',
                       '非法制造枪支',
                       '非法持有弹药',
                       '非法持有枪支、弹药',
                       '非法买卖枪支',
                       '非法持枪',
                       '非法制造、买卖枪支',
                       '非法.*(枪|弹药)',
                       '私藏枪支']
                 
                 
#交通肇事和危险驾驶
zm_group['jtzs_wxjs_list'] = [ '交通肇事', '危险驾驶',
                              '交通肇.', '险驾驶',
                              '(危)?险驾驶',
                              '危险(驾)?(驶)?',
                              '危驾']
                 
                 
#============= 具有死刑罪名的其他==================
zm_group['jysxzmdqt_list'] = ['绑架', '拐卖儿童',
                  '拐卖.?(妇女).?(儿童)?',
                  '拐骗儿童',
                  '放火',
                  '以危险方法危害公共安全'
                 ]

#贪污贿赂
zm_group['twhl_list'] = ['介绍贿赂', '受贿', '贪污']

#生产销售伪劣商品
zm_group['scxswlsp_list'] = ['生产、销售有毒食品', '假药', '有害食品', '销售伪劣产品', '生产、销售不符合安全标准的食品',
                             '生产、销售不符合安全标准食品', '生产、销售不符合食品安全标准的食品',
                             '生产、销售有毒、有害食品', '销售不符合安全标准的食品', '生产不符合安全标准的食品']




#毒品犯罪
zm_group['dpfz_list'] = ['转移毒赃', '制造毒品', '贩卖毒品', '容留他人吸毒', '非法持有毒品', '运输毒品', '非法买卖制毒物品',
                         '窝藏、转移毒品', '非法运输制毒物品', '贩卖、运输毒品', '贩卖、制造毒品',
                         '吸毒', '\w\w毒品', '贩毒', '(运输|非法买卖)制毒物品','非法持毒','贩卖毒','容留他人吸']                 
                 

                 
                 
                 
                 
sws_pattern = '(?:大邑|安县|丹棱|射洪|船山|青神|新疆|翠屏|高|攀枝花|蓬溪|通江|盐源|甘洛|普格|会东|丹巴|康定|黑水|茂县|巴中|天全|雅安|万源|渠县|大竹|达州|华蓥|眉山|仁寿|西充|营山|南部|南充|大英|井研|苍溪|剑阁|旺苍|江油|梓潼|三台|罗江|中江|合江|彭州|郫县|金堂|成都|会理|凉山|乐山|德阳|绵阳|宣汉|开江|珙县|宜宾|叙永|古蔺|泸|资中|贵阳|羌茂|金江|岷源|内江|安徽|彰正|四某|辽宁|绵竹|秦兴|剑州|黑龙江|江西|理塘|遂州|仪陇|山西|万商天勤|平昌|慧聪|筠连|甘肃|乐至|邻水|沱江|遂宁|陕西|浙江|重庆|湖|山东|X|广|云南|上海|国浩|河|北京|四川|泰|自贡|康伦|三目|平武|贵州|福建).*?(?:事务所|法律援助中心)'                 
bhr_pattern = '(宜宾|资中|贵阳|羌茂|金江|岷源|内江|安徽|彰正|四某|辽宁|绵竹|秦兴|剑州|黑龙江|江西|理塘|遂州|仪陇|山西|万商天勤|平昌|慧聪|筠连|甘肃|乐至|邻水|沱江|遂宁|陕西|浙江|重庆|湖|山东|X|广|云南|上海|国浩|河|北京|四川|泰|自贡|康伦|三目|平武|泸州|贵州|福建).*?事务所律师'


last_name = '(\
A|阿牛|甯|尕|安|艾|昂|庹|阚|岑|敖|雒|阿|\
B|奔|波|白|补|毕|布|卑|班|边|柏|贝|保|鲍|巴|包|八|宾|比|\
C|程|赤|曾|晁|楚|仇|曹|成|常|蔡|陈|采|柴|淳|崔|昌|畅|车|查|此|池|串|操|寸|措|訾|迟|\
D|达|邓|旦|栋|多|丁|窦|党|豆|地|卞|当|杜|但|董|代|登|刁|段|戴|得|东|丹|夺|底|狄|\
E|额|耳|俄|尔|\
F|傅|范|丰|房|扈|奉|俸|附|付|裴|冯|方|符|伏|樊|封|费|扶|凡|番|\
G|盖|贯|更|弓|古|昝|耿|芶|国|关|葛|共|官|瓜|广|谷|勾|郜|龚|干|贵|管|眭|苟|果|顾|桂|高|郭|甘|戈|宫|辜|巩|格|挂|\
H|花|户|洪|瑚|回|惠|缑|衡|何|华|黄|郝|韩|侯|胡|霍|奂|候|贺|赫|黑|海|虎|\
I|\
J|冮|嘉|降|姬|金|敬|蒋|姜|巨|贾|靳|呷|季|焦|景|吉|戢|谯|劼|井|江|晋|甲木|简|鞠|纪|计|淦|甲|加|荆|揭|\
K|柯|克|坤|江|矿|旷|寇|邝|康|孔|匡|亢|卡|\
L|令狐|蔺|廉|兰|缪|路|练|娄|洛|闾|骆|蓝|鲁|勒吾|栾|隆|柳|郎|虞|连|芦|凌|林|楼|黎|罗|陆|赖|龙|卢|李|冷|吕|廖|刘|梁|雷|\
M|麻|苗|马|蒙|门|满|明|庙|牟|梅|米|莫|穆|母|糜|闵|孟|毛|曼|麦|木|卯|\
N|努|倪|聂|尼玛|宁|佀|南|农|尼|牛|\
O|欧|鸥|殴|\
P|皮|彭|潘|普|庞|濮|蒲|泡|卜|平|朴|浦|\
Q|秦|宓|墙|钱|秋|切|祁|权|阙|青|且|齐|戚|卿|漆|瞿|屈|覃|蹇|全|邱|乔|裘|启|强|\
R|冉|任|容|壤|荣|茹|仁|尧|柔|饶|阮|芮|惹|日|\
S|单|苏|寿|宿|山|厍|盛|色|松|粟|舒|石|申|首|双|师|税|佘|史|索|商|尚|孙|桑|施|司|四|赛|沈|邵|沙|宋|帅|什|三|斯|\
T|谭|吐|屠|帖|谈|塔|滕|腾|汤|土|田|唐|童|涂|凃|铁|陶|佟|图|\
W|万|枉|伟|文|汪|卫|乌|闻|魏|巫|危|伍|邬|温|武|韦|王|吴|宛|翁|旺|峗|睢|\
X|宣|项|萧|咸|奚|席|谢|辛|幸|先|旭|解|习|霞|鲜|邢|薛|修|宪|向|肖|夏|徐|许|熊|Ｘ|冼|西|\
Y|伊|院|燕|阴|银|衣|夷|依|言|月|洋|英|医|印|怡|弋|亿|仰|应|姚|禹|尤|云|闫|乐|宇|约|庾|苑|严|阎|羊|尹|亚|夭|游|\
俞|余|叶|邰|胥|袁|雍|阳|易|岳|殷|晏|鄢|颜|喻|杨|扬|越|于|\
Z|足|翟|联|宗|査|志|支|诸|褚|谌|臧|占|种|卓|植|正|资|张|祖|赵|邹|章|仲|甄|詹|竹|祝|庄|左|周|朱|郑|泽|钟|扎|笪|中)'

#曾经，户籍，宣告
ss_last_name = '(日力|曲|曲木|皇甫|乃古|扎西|勒|的日|的的|耍日|洁洁|的莫|木乃|邛莫|耍子|期沙|比布|完颜|次尔|阿迪力|买买提)'
ss_name = '(\
火补色拉|尾则么此扎|麦麦提艾力·艾孜拉|瓦扎阿作|拥中泽郎|萨德|西热艾力.苏勒坦|曲木么里作|沙马木古|头旦夏周|益西曲扎|\
加毛|哈马莫吉杂|萨博|拉衣瓦布|艾孜孜•吐热普|呷绒邓邓|格绒平错|拉马火尔|曲某|拉基作且子|苦里西里莫|水洛小平|吐逊江阿米提|\
结字伍干莫|赤黑某甲|拉马克古|乃保某甲|泥玛仁清|艾克拜尔·麦麦提|西仁次仁|次甲|嘎日东作|瓦加|取比哈体|说各呷呷|阿尔尼支莫|\
赤黑日沙|能子么外子|依力哈某·某某某|伊某某某·某某某某某|阿卜杜力穆太力普·阿吉|拥中江参|壮姆泽仁|朗初扎拉|被告人吐鲁洪麦麦提|\
拉机五加|哈马里呷|麦合木提尼亚孜·库尔班|日嘿日且|马合木提·麦麦提|赤黑扯沙|阿卜杜凯由木·巴斯提拉古丽|阿迪力·阿布都拉|\
吉火么尔阿木|喀迪尔•艾麦提|呷马五各|日火有古么|都光夜|夺尔单|神杂某一|阿力木·麦麦提|日阿木|的地吉哈|比么拉子|\
迪某某.某|恩扎|阿迪力江·牙森|热娜古丽•图尔贡|三郎XXX|比尔加加木|曲木阿木|阿初莫伟作|麦某某某|生龙奇绕|阿依努尔﹒阿尤甫|\
洛某某某|俄的拉根|阿卜力孜•加帕尔|艾某某某|努某某某|库尔班•热合曼|博史呷嘿|三郎石旦真|来来支布|拿黑土黑|\
瓦扎吃古莫|苏呷阿尔|阿布都维力﹒亚库普|黑呷阿木|马查么子扎|降泽|多杰才仁|多吉仁珍|呷然|的石者|拉木小东|\
联保么你作|俄果布则|使掌某甲|珍珠让布|联保么某甲|子尔么木作|基批某某|平西什西木|足窝某某|尔某某|尔某某某|\
跑查莫里洛|凉都么力火|拖觉某某|初布某某|南征某某|麻卡某某|纳黑莫某某|倮古某某某|生吞如洛|杰都某某|尾日子拉\
威色某某|尔布医生|伊斯马伊力·某某某|甫哇甲|次仁降村|摩西罗立|立牛罗西|哈拉扎西某某|水罗彝古|耍惹石叶|\
切吉史者|菜呷日|供某某|贡呷扎西|东周甲木措|艾克拜尔·阿卜都外力|曲别春丽|甲布德珠|更尕泽让|加瓦木及|热连日哈|\
日火莫布洛|夏克尔·艾合麦提|海来阿三|阿卜力米提﹒喀迪尔|阿布都卡地尔·吐儿孙|搏什么次作|保格日方|瓦渣达达子|\
艾沙·吾四曼|瓦尔某某|黑乃拉曲|俄木尔呷|吉差五呷木|马合木提•麦麦提|瓦尔木牛|ＸＸ|依米提斯拉木•吾斯曼|比曲子沙|\
嘿哈么某某|勤别某某|拉日古史|格尔某某|加XXX|尔组伍合|HOANGTHINGHIA|PHAMQUANGDAT|TAXUANNAM|LECONGHOANG|比秋尔色|\
DANGTHANHTUNG|艾亥提·阿布来提|胜扎么某某|博什么某某|都仁某某|巧吉沙尔|结古克的子|咪乃嫫日子|\
以很三哥|惹及拉格|玉苏普•艾合麦提|热依沙·开里木|小木几|召布有日|马某某·如则某某某|热某某某|倮伍姑坡子|玛赫铁红|\
努尔艾力•麦麦提|说日某某|洛古木衣|火布日拉|体哈某某|赤黑么某某|那木么日则|尾什么土各|窝比么扭各|比支发子|\
艾热克尼·某某某某某某|红什某某某|黑吉尔果么|米色沙作|CHUNGJIWOONG|立立曲铁|曲别木铁|枯以格|图尔贡&middot;麦提托合提|\
甲央|吐尔孙·塞买提|LIMZIHAO,MANNTONBENJAMIN|阿的木且|阿依古丽&middot;吐尔迪|尾日子拉|的里尔布|介古格日|介来曲布|\
他巴降泽|伙补子且|介洛某某|尼胡底石|尼杜小兵|俄来木依|吉日蒋平|敌地罗曲|曲木尔合子|艾沙江艾买提|拉尔衣生|麦拥忠泽里|\
阿约约真日|泽真罗尔吾|尼美王修|朋错扎西|尾什么日外|日么沙作|比布哈约|乃乃阿支|社特尔布|维色伍卡|热科么惹作|西绕尼玛|\
瓦渣子鬼|乃保么尔各|勒古么友子|奥杰尔子|能还么色各|拉尔小明|尺都泽仁|让布|努尔艾合麦提·图尔孙|沙马阿西莫|取比比莫|\
艾热克尼托合提克尔办|阿卜杜喀哈尔胡东拜迪|阿布都如苏力买买提|阿比提麦麦提|阿里木土尔滚|抓子央章次尔|尾什么林扎|\
麦麦提尼亚孜托合提|吐尔孙塞买提)'
#|送|本|刀|将|时||把||起未|于
# 基本情况姓名
invalid_name = '(\
把德君|求某|于某|于斌|于佳|于文勇|于光明|于海|于快|于术和|于绍国|于绍斌|于洪波|于仕彪|于长江|于杰|于景会|于洋文|\
于洪伟|于磊|李\*|则周|无名氏|侯映华|高举太|谢某|陈梁|李贵林|龙天旭|都华武|但存彪|\
肉孜尼萨·卡地尔|玛伊努尔·阿卜杜拉|的某某|和某某|起应忠|都建波|买某某|都某某|起朝伟|令某|欠玉泉|\
拉某|开某某|来任重|说泽|来某|某某|从兆存|降错|直巴|未生生|未大彬|未平|马＊|六斤|则惹体|时建文|时某)'
#本|况
#这两个还没有处理

not_a_name_list = ['户籍', '自愿', '当庭',
                        '曾经', '曾因', '文化',
                        '商量', '尚有', '正当',
                        '多次', '供述', '支付',
                        '宣告', '宣读', '挡获',
                        '常住', '采取', '此次',
                        '容留', '共同']

nation_list = '(\
汉|蒙古|回|藏|维吾尔|苗|彝|壮|布依|朝鲜|满|侗|瑶|\
白|土家|哈尼|哈萨克|傣|黎|僳僳|佤|畲|高山|拉祜|水|\
东乡|纳西|景颇|柯尔克孜|土|达斡尔|仫佬|羌|布朗|撒拉|\
毛南|仡佬|锡伯|阿昌|普米|塔吉克|怒|乌孜别克|俄罗斯|\
鄂温克|德昂|保安|裕固|京|塔塔尔|独龙|鄂伦春|赫哲|\
门巴|珞巴|基诺)'


##########FROM HERE ######################
ch_en_symbol_dict = {"（":"(",
                     "）":")",
                     "。":".",
                     "，":",",
                     "：":":",
                     "；":";",
                     "、":",",
                     "·":""}

ch_en_number_dict = {
"一": 1,
"二": 2,
"三": 3,
"四": 4,
"五": 5,
"六": 6,
"七": 7,
"八": 8,
"九": 9,
"十": 10,
"十一": 11,
"十二": 12,
"十三": 13,
"十四": 14,
"十五": 15,
"十六": 16,
"一六": 16,
"十七": 17,
"一七": 17,
"十八": 18,
"十九": 19,
"二十": 20,
"二十一": 21,
"二十二": 22,
"二十三": 23,
"二十四": 24,
"二十五": 25,
"二十六": 26,
"二十七": 27,
"二十八": 28,
"二十九": 29,
"三十":  30,
"三十一": 31,
"二〇一六":2016,
"二〇一七":2017,
"二〇一八":2018}
########## Patterns #######################
pre_charge_pattern = [re.compile("指控被告人.+犯(.*)罪.*提起公诉")]

defendant_section_pattern = [re.compile('被告人?.*?(?:提起公诉)'),
                             re.compile('被告人?.*?(?:指控)'),
                             re.compile('被告人?.*?(?:起诉书)'),
                             re.compile('被告人?.*?(?:审理查明)')]

convict_section_pattern = [re.compile(r"判[决处](如下|结果).*不服本判决"),
                           re.compile(r"判[决处](?!书)(如下|结果)?.*不服本判决"),
                           re.compile(r"判[决处]如下.*审"),
                           re.compile(r"判[决处]如下.*$"),
                           re.compile(r"之规定,.*不服本判决")]

sue_date_pattern = re.compile("于(?P<year>\d{4})年(?P<month>\d{1,2})月(?P<day>\d{1,2})日向本院提起公诉")

judge_date_pattern = re.compile("(?P<year>[一二三四五六七八九十〇]{4})年(?P<month>[一二三四五六七八九十]{1,2})月(?P<day>[一二三四五六七八九十]{1,3})日")

head_section_pattern = [re.compile(r".*?(?=被告人)")]

verdict_pattern = [re.compile(r".*?判决书")]

case_id_pattern = [re.compile(r"\(\d{4}\).*?号"),
                   re.compile(r"\(\d{4}\)[\w\d]+[初]([字第]+)?[\d]+号?")]

court_pattern = [re.compile(r"\w+人民法院")]

prosecutor_pattern = [re.compile(r"(?<=公诉机关).*?人民检察院")]

convict_info_pattern = re.compile(r"被告人.*?(?=被告人|不服本判决|审|$)")

defendant_info_pattern = [re.compile('被告人?.*?(?=被告|提起公诉|指控|起诉书|审理查明)')]

# 被告人基本情况姓名丁骆君曾用名无
# 被告人的基本情况:周建,男
# 被告人身份情况姓名秦朋出生日期
# 被告人的基本情况:被告人杜文富,男   此处以被告人为分段标志会切断这一信息，且第一段中无被告人信息。
# 被告人身份情况姓名徐文波性别男
# 被告人基本情况姓名叶琴丽娜曾用名
# 被告人基本情况:姓名:代帅性别
# 被告人罗亮成都市成华区人民检察院
defendant_pattern = [[re.compile('(?<=被告人)' + last_name + '\w{1,2}(?=[.,:(]|$)'),
                      re.compile('(?<=被告人)' + ss_last_name + '\w{1,3}(?=[.,:(]|$)')],
                     [re.compile('(?<=被告人)的?(基本|身份)情况:?(姓名)?:?' + last_name + '\w{1,3}(?=[.,(]|曾用名|出生日期|性别|绰号|成都市|公诉机关)'),
                      re.compile('(?<=被告人)的?(基本|身份)情况:?(姓名)?:?' + ss_last_name + '\w{1,6}(?=[.,(]|曾用名|出生日期|性别|绰号|成都市|公诉机关)')],
                     [re.compile('(?<=被告人姓名)' + last_name + '\w{0,4}出生日期'),
                      re.compile('(?<=被告)人?:?' + last_name + '\w{0,4}(?=[.,(]|201)'),
                      re.compile('(?<=被告人)' + last_name + '\w\w' + last_name + '[某甲]+'),
                      re.compile('(?<=被告人)[,;]?' + last_name + '\w{1,3}([.,(]|户籍)')],
                     [re.compile(ss_name),
                      re.compile(invalid_name)],
                     [re.compile('(?<=被告人)' + last_name + '\w{1,3}(?=成都|公诉机关)'),
                      re.compile('(?<=被告人)' + last_name + '\w{1,3}(?=成都|公诉机关)')],
                     [re.compile('(?<=被告人)(?!不可能|不具有|无社会)\w+(?=[,.(])')]
                     ]
                     #re.compile('(?<=被告人..情况姓名)' + last_name + '\w{0,4}[,(|出生日期|性别]'),
                     #re.compile('(?<=被告人)' + CourtList.last_name + '\w{0,4}(?=成都市)'))


clean_defendant_pattern = [re.compile(r"被告人(的|及辩护人)?基本情况:?$"),
                           re.compile(r"被告人(基本|情况|身份|信息|姓名)+$"),
                           re.compile(r"被告人:?$"),
                           re.compile(r"被告单位"),
                           re.compile(r"被告人(现羁押|取保候审)"),
                           re.compile(r"被告人犯.*?罪"),
                           re.compile(r"被告四川成康矿业开发有限公司"),
                           re.compile(r"被告人及其他诉讼参与人情况公诉机关四川省宜宾市翠屏区人民检察院")]


born_date_pattern = [re.compile('(\d\d\d\d)年(\d{1,2})月(\d{1,2})日出?生'),
                     re.compile('生于(\d\d\d\d)年(\d{1,2})月(\d{1,2})日')]

defendant_lawyer_pattern = [re.compile('(?<!指定|指派)辩护人.*?(?:事务所|法律援助中心|分所)(?:律师|实习律师)'),
                            re.compile('(?<!指定|指派)辩护人\w{3}')]

defendant_s_lawyer_pattern = [re.compile('(?<=指定|指派)辩护人.*?(?:事务所|法律援助中心|分所)律师'),
                              re.compile('(?<=指定|指派)辩护人\w{3}')]

defendant_sex_pattern = re.compile('(?<=,)[男女](?=[,.])')

defendant_nation_pattern = re.compile('(?<=,)' + nation_list + '族(?=[,.])')

defendant_education_pattern = re.compile(r"(大学|大专|中专|专科|高中|初中|小学|文盲|不识字)")

defendant_job_pattern = re.compile(r"(无业|经商|农民|职工|务农|个体|修理工|驾驶员|粮农|工作人员|农村居民|无职业|原系|务工人员|教师)")
# 原支部书记,原村民委员会

defendant_bail_pattern = re.compile(r"取保候审")


defendant_prison_pattern = [re.compile('有期徒刑.{1,6}月'),
                            re.compile('有期徒刑.{1,3}年'),
                            re.compile('拘役.{1,5}月'),
                            re.compile('拘役.年'),
                            re.compile('管制.{1,5}月'),
                            re.compile('管制.年'),
                            re.compile('免[予于]刑事处罚'),
                            re.compile('无期徒刑.*?(?=[.,;(])'),
                            re.compile('死刑.*?(?=[.,;(])'),
                            re.compile('无罪'),
                            re.compile('(?<=判)(!决).*?(?=[.,;(])')]


defendant_probation_pattern = [re.compile('缓刑.{1,5}月'),
                               re.compile('缓刑.年'),
                               re.compile('缓期.*?执行')]

defendant_fine_pattern = [re.compile('(?<=罚金).*?(?=元)')]

#self.defendent_pattern.append(re.compile('(?<=被告人).+?[，,（(。]'))
# self.defendent_pattern.append(re.compile('(?<=被告人)' + CourtList.last_name + '\w{1,3}(?=[。，,（(]|201|犯)'))
#defendent_pattern.append(re.compile('(?<=被告人)' + CourtList.ss_last_name + '\w{1,3}(?=[。，,（(]|201)'))
#defendent_pattern.append(re.compile('(?<=被告人)' + CourtList.ss_name))
#defendent_pattern.append(re.compile('(?<=被告人..情况姓名)' + CourtList.last_name + '\w{0,4}[，（|出生日期|性别]'))
#defendent_pattern.append(re.compile('(?<=被告人)' + CourtList.last_name + '\w{0,4}(?=成都市)'))
#defendent_pattern.append(re.compile('(?<=被告人姓名)' + CourtList.last_name + '\w{0,4}出生日期'))
#defendent_pattern.append(re.compile('(?<=被告)人?[：:]?' + CourtList.last_name + '\w{0,4}(?=[。，,（(]|201)'))
#defendent_pattern.append(re.compile('(?<=被告人)' + CourtList.last_name + '\w\w' + CourtList.last_name + '[某甲]+'))
#defendent_pattern.append(re.compile('(?<=被告人)' + CourtList.last_name + '\w{1,2}'))
##defendent_pattern.append(re.compile(CourtList.invalid_name))



#self.case_id_pattern.append()
#self.case_id_pattern.append(re.compile('\d{4}[\w\d]+[初]([字第]+)?[\d]+号'))
