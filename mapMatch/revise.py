import sys
sys.path.append('..')
from common import Geometry as G

def vertp2l(P, link):
	vert = list()
	P1 = G.Point()
	P2 = G.Point()

	if link.internumber > 0:
		for i in range(link.internumber-1)	
			P1.x = link.interlist[i][0]
			P1.y = link.interlist[i][1]
			P2.x = link.interlist[i+1][0]
			P2.y = link.interlist[i+1][1]
			if P1.y==P2.y:
               intersection=G.Point()
               intersection.x=P.x
               intersection.y=P1.y
               if checkpointonline(intersection,P1,P2)==1:
                   vert.append(intersection)
            elif P1.x==P2.x:
               intersection=G.Point()
               intersection.x=P1.x
               intersection.y=P.y
               if checkpointonline(intersection,P1,P2)==1:
                   vert.append(intersection)
            elif P1.x!=P2.x and P1.y!=P2.y:
               intersection=G.Point()
               k=(P2.y-P1.y)/(P2.x-P1.x)
               intersection.x=(k**2*P1.x+k*(P.y-P1.y)+P.x)/(k**2+1.0)
               intersection.y=k*(intersection.x-P1.x)+P1.y

               if checkpointonline(intersection,P1,P2)==1:
                   vert.append(intersection)
    elif link.internumber==0:
        intersection=Point()
        intersection.x=nodelist[link.node1].long
        intersection.y=nodelist[link.node1].lat
        vert.append(intersection) 
    return vert

#计算link上任意点P到node1的距离
def distp2node1(P,link):
    d=0
    P1=Point()
    P2=Point()
    if link.internumber>0:
        for i in range(link.internumber-1):
            P1.x=link.interlist[i][0]
            P1.y=link.interlist[i][1]
            P2.x=link.interlist[i+1][0]
            P2.y=link.interlist[i+1][1]
            if checkpointonline(P,P1,P2)==1:
                d=d+geodist(P,P1)
                return d
            else:
                d=d+geodist(P1,P2)
    return d

#计算link外的点P到link的垂直距离
def distp2link(P,link):
    vert=vertp2l(P,link)
    nvert=len(vert)
    if nvert==0:
        d=-1
        return (d,-1,-1,link.linkid)
    elif nvert==1:
        d=geodist(P,vert[0])
        return (d,vert[0].x,vert[0].y,link.linkid)
    else:
        dn=[]
        vn=[]  
        for ver in vert:
            dn.append(geodist(P,ver))
            vn.append((ver.x,ver.y))
        d=min(dn) 
        for idn in range(len(dn)):
            if dn[idn]==d:
                return (d,vn[idn][0],vn[idn][1],link.linkid)

def RevisePathEndpoints(tracklist, tracktime, mmpathnodes):
    #修正起点
    #先排除不需要修正的情况
    strackp=G.Point()
    strackp.x=tracklist[tracktime[0]].long
    strackp.y=tracklist[tracktime[0]].lat
    svert=vertp2l(strackp,linklist[GLinkNode[mmpathnodes[0]][mmpathnodes[1]]])  #求垂足
    if not svert:    #如果垂足为空，则修正起点；否则不修正
        sconnectlinks=[]   #收集起点候选link集中与当前路径起点相连通的link
        sconnectnodes={}   #保存起点候选link集中与当前路径起点相连通的link的起点 
        for s_link in s_links:
            sdrmlink=linklist[s_link]
            snod1=sdrmlink.node1
            snod2=sdrmlink.node2
            if sdrmlink.regulation==2:
                if snod2==mmpathnodes[0]:
                    sconnectlinks.append(s_link)
                    sconnectnodes[s_link]= snod1
                    continue
            elif sdrmlink.regulation==3:
                if snod1==mmpathnodes[0]:
                    sconnectlinks.append(s_link)
                    sconnectnodes[s_link]= snod2
                    continue 
            elif sdrmlink.regulation==1:
                if snod2==mmpathnodes[0]:
                    sconnectlinks.append(s_link)
                    sconnectnodes[s_link]= snod1
                    continue
                elif snod1==mmpathnodes[0]:
                    sconnectlinks.append(s_link)
                    sconnectnodes[s_link]= snod2
                    continue    
        #求sconnectlinks中与起点距离最短的link，并把相应的node添加到mmpathnodes当中       
        if sconnectlinks:
            sdistp2l=100   #匹配路段必须在40m以内，此处初始值设只要大于40即可 
            saddlink=sconnectlinks[0]  # 
            for sconnectlink in sconnectlinks:
                dtemp=distp2link(strackp,linklist[sconnectlink])
                if dtemp[0]!=-1 and dtemp[0]<sdistp2l:
                   sdistp2l=dtemp[0]
                   saddlink=sconnectlink
            if sdistp2l<=40:  #如果距离起点最近路段在40以内，则把此路段添加到最短路径中
                mmpathnodes.insert(0,sconnectnodes[saddlink])
                    
    #修正止点,修正止点和修正起点的思路一样，程序略微不同
    #先排除不需要修正的情况
    etrackp=G.Point()
    etrackp.x=tracklist[trackdatetime[-1]].long
    etrackp.y=tracklist[trackdatetime[-1]].lat
    evert=vertp2l(etrackp,linklist[GLinkNode[mmpathnodes[-2]][mmpathnodes[-1]]])  #求垂足
    if not evert:    #如果垂足为空，则修正起点;否则不修正
        econnectlinks=[]   #收集止点候选link集中与当前路径终点相连通的link
        econnectnodes={}   #保存止点候选link集中与当前路径终点相连通的link的终点 
        for e_link in e_links:
            edrmlink=linklist[e_link]
            enod1=edrmlink.node1
            enod2=edrmlink.node2
            if edrmlink.regulation==2:
                if enod1==mmpathnodes[-1]:
                    econnectlinks.append(e_link)
                    econnectnodes[e_link]= enod2
                    continue
            elif edrmlink.regulation==3:
                if enod2==mmpathnodes[-1]:
                    econnectlinks.append(e_link)
                    econnectnodes[e_link]= enod1
                    continue 
            elif edrmlink.regulation==1:
                if enod2==mmpathnodes[-1]:
                    econnectlinks.append(e_link)
                    econnectnodes[e_link]= enod1
                    continue
                elif enod1==mmpathnodes[-1]:
                    econnectlinks.append(e_link)
                    econnectnodes[e_link]= enod2
                    continue
        #求econnectlinks中与止点距离最短的link，并把相应的node添加到mmpathnodes当中       
        if econnectlinks:
            edistp2l=100   #匹配路段必须在40m以内，此处初始值设只要大于40即可 
            eaddlink=econnectlinks[0]  # 
            for econnectlink in econnectlinks:
                dtemp=distp2link(etrackp,linklist[econnectlink])
                if dtemp[0]!=-1 and dtemp[0]<edistp2l:
                   edistp2l=dtemp[0]
                   eaddlink=econnectlink
            if edistp2l<=40:  #如果距离起点最近路段在40以内，则把此路段添加到最短路径中
                mmpathnodes.append(econnectnodes[eaddlink])