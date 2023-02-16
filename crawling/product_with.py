# FEAT: TODO: WITH 추가
WITHPRODUCT = itemInfo['referencesList']
for item in WITHPRODUCT:
    WITHLIST = item['StyleProductCode'].split('_')
    WITHPCID = WITHLIST[0] + '_' + WITHLIST[1]
    print(WITHPCID)