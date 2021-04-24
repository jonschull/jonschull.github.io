
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
options = { "physics":{"enabled":True
                      },
            "autoResize": True,
            "layout":{  "improvedLayout": True, "hierarchical":{
                                          "enabled": True,
                                          "direction": 'LR',
                                          "sortMethod": "directed",
                                          "nodeSpacing":5,
                                          "treeSpacing":5}},
                "edges":{"smooth": True,
                         "arrows":{"to":True}
                         },
                 "nodes":{"shape":"box",
                          "font" :"14px"
                         }
             };

def getNodes(graphString=graphString):
    keywords = 'ID LABEL URL TITLE LINKTO COLOR SHAPE FONT NODES EDGES'.split()

    goodLines = []
    for line in graphString.split('\n'):
        line=line.strip()
        if line.strip():             #keep non-blank lines
            goodLines.append(line)
        else:                        #throw out the other
            goodLines.append('BREAK\n')
    goodLines = '\n'.join(goodLines).split('BREAK\n')                    #make a string
    chunks = [line.strip() for line in goodLines if line.strip()]        #split it at the BREAKs to make a chunk that will become a record

    #break each chunk at keyword to create records
    records = []
    for chunk in chunks:
        for keyword in keywords:
            chunk=chunk.replace('\n'+ keyword,'BREAK'+ keyword)
        lines=chunk.split('BREAK')
        records.append([line.strip() for line in lines if line.strip()])


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
