
graphString = """
ID      1
LABEL   First item
TITLE   This is popup text
        this can be multiple lines
        but don't go crazy
LINKTO  2 3

ID      2
URL     testsource.html
LABEL   Second Item
TITLE   This is popup text
URL     testsource.html
LINKTO  3

ID      3
LABEL   Another Second-level Item
TITLE   This is popup text
URL     testsource.html
"""
options = { "physics"  :{"enabled":True},
            "configure":{"enabled":True},
            "autoResize": True,
            "layout":{"improvedLayout": True, "hierarchical":{
                                          "shakeTowards": 'roots',
                                          "enabled": True,
                                          "direction": 'LR',
                                          "sortMethod": "directed",
                                          "nodeSpacing":1,
                                          "treeSpacing":1}},
                "edges":{"smooth": True,
                         "arrows":{"to":True},
                         "shadow" : True
                         },
                 "nodes":{"shape":"box",
                          "font" :"14px",
                          "shadow": True
                         }
             };



keywords = """"id label url title linkto color shape
font nodes edges x y layout physics hierarchical border
borderWidth background opacity hidden""".split()

def getChunks(graphString):  ##OLD
    #break each chunk at keyword to create records
    goodLines = []
    graphString = graphString.replace(chr(11),'\n')
    for line in graphString.split('\n'):
        line=line.strip()
        if line.strip():             #keep non-blank lines
            goodLines.append(line)
        else:                        #throw out the other
            goodLines.append('BREAK\n')
    goodLines = '\n'.join(goodLines).split('BREAK\n')                    #make a string
    chunks = [line.strip() for line in goodLines if line.strip()]        #split it at the BREAKs to make a chunk that will become a record
    print('Chunks', chunks)
    return chunks

def getChunks(graphString):
    if graphString.startswith('id '):
        graphString = graphString[3:]
    chunks = graphString.split('\nid')
    chunks = ['id '+chunk for chunk in chunks]
    print('chunks', chunks)
    return chunks

def getRecords(graphString):
    chunks = getChunks(graphString)
    records = []
    for chunk in chunks:
        for keyword in keywords: #we are now assuming indents
            chunk=chunk.replace('\n\t'+ keyword,'BREAK'+ keyword) #keywords must be at beginning
        lines=chunk.split('BREAK')
        records.append([line.strip() for line in lines if line.strip()])
    return records #used by getOptions and getNodes



def parseOptions(graphString=graphString):
    records = getRecords(graphString)
    newOpts = [record for record in records if record[0] in 'NODES EDGES LAYOUT PHYSICS'.lower().split()]
    if newOpts:
        print('NO',newOpts)
    options={}
    for newOpt in newOpts:
        nodesOrEdges = newOpt[0].lower()
        options[nodesOrEdges]= {}
        for opt in newOpt[1:]:
            if len(opt.split())>1:
                k,vs = opt.split()[0], opt.split()[1:]

                if len(vs)==1:
                    v=vs[0]
                    options[nodesOrEdges][k] = v

                if len(vs)==2:
                    k2, v = vs
                    if k not in options[nodesOrEdges]: #make sure we have the dict created
                        options[nodesOrEdges][k]=dict()

                    options[nodesOrEdges][k][k2] = v

                if len(vs)==3: #will fail beyond this
                    k2, k3, v = vs
                    if k not in options[nodesOrEdges]:
                        options[nodesOrEdges][k]=dict()

                    if k2 not in options[nodesOrEdges][k]:
                        options[nodesOrEdges][k][k2] = dict()

                    options[nodesOrEdges][k][k2][k3] = v


    return options

def getNodes(graphString=graphString):
    records=getRecords(graphString)
    # convert records into nodes
    nodes = []
    for record in records:
        node = dict(url='') #seems to fix a bug where I get double events on click
        for line in record:
            key = line.split()[0].lower()
            value = ' '.join(line.split(' ')[1:]).strip()
            node[key] = value
        nodes.append(node)
    #[print(node) for node in nodes]

    return(nodes)

def getEdges(nodes):
        edges = []#[{'from':'1', 'to':'2'}]
        for node in nodes:
            if 'linkto' in node.keys():
                links = node['linkto'].split()
                for link in links:
                    edges.append({'from':node['id'],
                                   'to': link})
        return edges

test= """NODES
COLOR red


ID 0
LABEL
LINKTO 1 8

ID 1
LABEL HOW
THIS
WORKS
COLOR lime
SHAPE circle
FONT 22
LINKTO 1b 2 3
"""
def dataAndOptions(graphString= test):
    nodesWithOptions = getNodes(graphString)
    optionWords = set('nodes edges physics layout'.split())

    nodes=[]; newOptions = []
    for i, node in enumerate(nodesWithOptions):
        optionWord = set(node.keys()).intersection(optionWords)
        if optionWord: #don't create a node if its an optionWord (like NODES, EDGES etc.)
            optionKey=optionWord.pop()
            newOptions.append(node)
        else:
            nodes.append(node)

    edges=getEdges(nodes)
    data={'nodes':nodes, 'edges': edges}
    return data, options
