#!/usr/bin/env python
# coding: utf-8

# With this approach
# --keywords would not need to be upper case
# --they would get put in to LEFT, not ShortHands
# 
# Shorthands will be an editor also so options can be collapsed
# -- and nodes can be collapsed to so they stay into alignment with keywords

# In[1]:


graphString="""id alts
	linkto  refreshGraph one two three
	borderWidth 12
	font size 23
	label alts
id refreshGraph
	linkto  dataAndOptions window.vis.DataSet parseOptions
	color lime
	label alts
id dataAndOptions
	linkto  getNodes getEdges
	label alts
id getNodes
	linkto
	label getNodes
id getEdges
	linkto
	label getEdges
id window.vis.DataSet
	linkto
	label window.vis.DataSet
id parseOptions
	linkto  getRecords
	label parseOptions
id getRecords
	linkto  getChunks
	label getRecords
id getChunks
	linkto
	label getChunks
nodes
	color orange
	borderWidth 15
	font size 23
    
edges
	color red
	font size 23"""


# In[2]:


def getChunks(graphString=graphString):
    """each chunk is a string that needs to be converted into a record"""
    lines = graphString.split('\n')
    withBreaks = []
    for line in lines:
        if not line.startswith('\t'):
            withBreaks.append('@@' + line)
        else:
            withBreaks.append(line)
    rejoined = '\n'.join(withBreaks)
    ret=[ _ for _  in rejoined.split('@@') if _.strip()]
    return ret
getChunks()


# In[3]:


keywords = """"id label url title linkto color shape
font nodes edges x y layout physics hierarchical border
borderWidth background opacity hidden""".split()

def getRecords(graphString):
    """each record is a list of phrases taht will become a key value pair
    complexity comes from fact that labels can be multi-line"""
    chunks = getChunks(graphString)
    records = []
    for chunk in chunks:
        for keyword in keywords: #we are now assuming indents
            chunk=chunk.replace('\n\t'+ keyword,'BREAK'+ keyword) #keywords must be at beginning
        lines=chunk.split('BREAK')
        records.append([line.strip() for line in lines if line.strip()])
    return records #used by getOptions and getNodes

getRecords(graphString)


# In[5]:


def parseOptions(graphString=graphString):
    """Create nested dictionaries as required by visJS.  
    At end, optionProcessing is complete, but nodes and edges need more massaging.
    """
    def fixV(s):
        """deal with non-string values"""
        if s in ['True', 'true']: return True
        if s in ['False', 'false']: return False
        try: # to convert to a number
            return(int(s))
        except:
            return s #then just return as is
    

    records = getRecords(graphString)
    newOpts = records#. SEE WHAT FAILS [record for record in records if record[0] in 'nodes edges layout physics'.split()]
    options={}
    for newOpt in newOpts:
        kind = newOpt[0]
        options[kind]= {}
        for opt in newOpt[1:]:
            if len(opt.split())>1:
                k,vs = opt.split()[0], opt.split()[1:]
                if k=='linkto':  #don't turn into dictionaries
                    options[kind][k]=' '.join(vs) #leave linktos as space delimited 'ONE TWO THREE'
                    break

                if len(vs)==1:
                    v=vs[0]
                    options[kind][k] = fixV(v)

                if len(vs)==2:
                    k2, v = vs
                    if k not in options[kind]: #make sure we have the dict created
                        options[kind][k]=dict()

                    options[kind][k][k2] = fixV(v)

                if len(vs)==3: #will fail beyond this
                    k2, k3, v = vs
                    if k not in options[kind]:
                        options[kind][k]=dict()

                    if k2 not in options[kind][k]:
                        options[kind][k][k2] = dict()

                    options[kind][k][k2][k3] = fixV(v)


    return options
parseOptions()


# In[6]:


def nodesEdgesOptions(graphString=graphString):
    """create a dictionary that has nodes, edges and options formatted as required by visjs
    """
    entries=[]
    PO = parseOptions(graphString)
    entries= dict(nodes=[], edges=[], options={})
    for k,v in PO.items():
        if k.startswith('id'): #create a node entry
            id = k.split('id')[1].strip()
            node = {'id': id}
            for k2,v2 in v.items():
                node[k2]=v2
            entries['nodes'].append(node)
        else:
            entries['options'][k]=v  #create an option entry (we're expecting nodes, layout, physics, edges...maybe interaction )

    for node in entries['nodes']: #create edges entries
        if 'linkto' in node.keys():
            for linkto in node['linkto'].split(' '):
                entries['edges'].append( {'from':node['id'], 'to':linkto} )

    return entries

nodesEdgesOptions()


# In[6]:


try:
    get_ipython().system('jupyter nbconvert --to python parseShorts.ipynb')
except:
    


# In[3]:


get_ipython().system('ls')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




