from utils import INTree

def creatImageNetTree(wordfile_path, papafile_path, valFile_path):
    wordfile = open(wordfile_path,'r')
    thelist = wordfile.read().split('\n')
    thedict = {}
    idDict = {}
    thelist.remove('')
    for idn in thelist:
        try:
            ID, name = idn.split('\t')
        except:
            print(idn)
        thedict[name] = ID
        idDict[ID] = name
    wordfile.close()

    papafile = open(papafile_path,'r')
    papalist = papafile.read().split('\n')
    papalist.remove('')
    papadict = {}
    for idn in papalist:
        papa, son = idn.split(' ')
        papadict[son] = papa
    papafile.close()

    valFile = open(valFile_path, 'r')
    valList = valFile.read().split('\n')
    valList.remove('')
    valNames = []
    for idn in valList:
        valNames += [idn.split(':')[1][2:-2]]
    valFile.close()

    def findpapas(ID, exist_papa):
        try:
            papa_ID = papadict[ID]
            exist_papa += [papa_ID]
            findpapas(papa_ID, exist_papa)
        except:
            return

    exist_papa = []
    for name in valNames:
        ID = thedict[name]
        this_papas = [ID]
        findpapas(ID, this_papas)
        exist_papa += [this_papas]
    exist_papa[151] += ['n00001740']

    root = INTree(ID = exist_papa[0][-1], name = idDict[exist_papa[0][-1]])
    for papas in exist_papa:
        big_papa = root
        nPapa = len(papas)
        for i in range(nPapa - 2,-1,-1):
            this_son = papas[i]
            if big_papa.have_son(ID = this_son):
                big_papa = big_papa.descend(ID = this_son)
            else:
                big_papa.add_son(ID = this_son, name = idDict[this_son])
                big_papa = big_papa.descend(ID = this_son, name = idDict[this_son])

    leaf_List = []
    if root.count_leaves() != len(valNames):
        leaf_List = root.find_leaves()
        leaf_Names = []
        for leaf in leaf_List:
            leaf_Names += [leaf.name]
        for i in valNames:
            if not i in leaf_Names:
                root.find_node(name=i).add_son(name = i)
    return root