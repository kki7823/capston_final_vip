
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import vip1
import paramiko
import time
import datetime as d


class XDialog(QDialog, vip1.Ui_Dialog):

    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setup1()
        self.button6clicked()
        self.button5clicked()
	

    def setup1(self):

        global table1
        table1 = self.tableWidget
        global table2
        table2 = self.tableWidget_2
        global table3
        table3 = self.tableWidget_3
        global table5
        table5 = self.tableWidget_5
        global table6
        table6 = self.tableWidget_6
        global table7
        table7 = self.tableWidget_7
        global table8
        table8 = self.tableWidget_8
        global tr1
        tr1 = self.treeWidget
        global tr2
        tr2 = self.treeWidget_2
        global tr3
        tr3 = self.treeWidget_3
        global tr4
        tr4 = self.treeWidget_4
        global tr5
        tr5 = self.treeWidget_5
        global prog
        prog = self.progressBar
        global btn6
        
        label11 = self.label_11
        pixmap = QPixmap("back5.jpg")
        pixmap = pixmap.scaledToHeight(520)
        pixmap = pixmap.scaledToWidth(580)
        label11.setPixmap(pixmap)

        label12 = self.label_12
        pixmap2 = QPixmap("smu2.jpg")
        pixmap2 = pixmap2.scaledToHeight(90)
        pixmap2 = pixmap2.scaledToWidth(80)
        label12.setPixmap(pixmap2)
        
        le1 = self.lineEdit                       
        self.groupBox_2.close()

        prog.setValue(0)
        le3 = self.lineEdit_3
        le3.displayText()

        #test
        
    def button6clicked(self):
        btn6 = self.pushButton_6
        btn6.clicked.connect(self.btn6click)

    def btn6click(self):
        self.Authentication()


    def button5clicked(self):
        btn5 = self.pushButton_5
        btn5.clicked.connect(self.btn5click)

    def btn5click(self):
        QMessageBox.about(self,"제작팀","지도교수 : 오 선 진 교수님\n조장: 김 경 일\n조원: 문 진 영, 이 시 후, 조 건 희")
     
        
    def Authentication(self):

        le1 = self.lineEdit
        le2 = self.lineEdit_2
        le3 = self.lineEdit_3
        lb5 = self.label_5
        prog = self.progressBar
        tb1 = self.textBrowser
        
        #

        #userinfo
        tb5 = self.textBrowser_5
        tb6 = self.textBrowser_6
        tb7 = self.textBrowser_7
        tb8 = self.textBrowser_8

        #VERSION info
        tb9 = self.textBrowser_9
        tb10 = self.textBrowser_10
        tb11 = self.textBrowser_11
        tb12 = self.textBrowser_12

        #cpuinfo
        tb13 = self.textBrowser_13
        tb14 = self.textBrowser_14
        tb15 = self.textBrowser_15
        tb16 = self.textBrowser_16
        
        global client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      
        host = str(le1.text())
        port_num= 22
        user = str(le2.text())
        pw = str(le3.text())

        def con():
            try:
                client.connect(hostname=host, port=port_num, username=user, password=pw)
                return True
            except:
                return False
            
        def exec_cmd(cmd) :
            (stdin, stdout, stderr) = client.exec_command(cmd)
            if stderr.read().strip() != "" :
                return invoke_shell(cmd)
            return stdout.read().strip()
        
        def invoke_shell(cmd) :
            channel = client.invoke_shell()
            response = channel.recv(9999)
            channel.send(cmd+"\n")
            while not channel.recv_ready():
                time.sleep(3)
            response = channel.recv(9999)
            out = response.decode("utf-8")
            first_enter_index = min(out.find("/r"), out.find("\n"))
            out = out.replace("\r\n", "\n")
            return out.strip()

        con1 = con()

        if con1 == True :

            global route1
            global ospf1
            global ospfarea1
            global memory1
            global user1
            global cpu1
            global version1
            global eth0cmd
            global eth1cmd
            global eth2cmd
            global eth3cmd
            
            route1 = exec_cmd('show ip route')
            ospf1 = exec_cmd('show ip ospf neighbor')
            ospfarea1 = exec_cmd('show ip ospf | no-more')
            memory1 = exec_cmd('show system memory')
            user1 = exec_cmd('show system login user')
            cpu1 = exec_cmd('show hardware cpu')
            version1 = exec_cmd('show version')
            eth0cmd = exec_cmd('show interface ethernet eth0')
            eth1cmd = exec_cmd('show interface ethernet eth1')
            eth2cmd = exec_cmd('show interface ethernet eth2')
            eth3cmd = exec_cmd('show interface ethernet eth3')
            noshutdown1 = exec_cmd('/home/vyos/')

            QMessageBox.about(self,"notice","Login successful")
            #
            self.groupBox.close()
            self.groupBox_2.show()
            time1 = d.datetime.now()
            lb5.setText("Device : {}\nIP Address: {}\nroot id: {}\n\n\n\n{}".format('vyos',host,user,time1))

            #라우팅 테이블
            rownum = route1[188:].count('\x1b[m\n')
            table1.setRowCount(rownum)
            RoutingTableList = self.routeseparate(route1)
            cnt1 = 0
            cnt2 = 0
            for i in range(0,rownum):
                if RoutingTableList[i][0] == 'O':
                    cnt1 = cnt1 + 1
            table3.setRowCount(cnt1)
            
            for i in range(0,rownum):
                for j in range(0,4):
                    table1.setItem(i,j, QTableWidgetItem(self.makeroutelist(RoutingTableList[i])[j]))
                if self.makeroutelist(RoutingTableList[i])[0][0] == 'O':
                    for k in range(0,4):
                        table3.setItem(cnt2,k, QTableWidgetItem(table1.item(i,k).text()))
                    cnt2 += 1
                    
            #ospf테이블 
            ospfrownum = ospf1[176:].count('\x1b[m \x08')
            table2.setRowCount(ospfrownum)
            ospfTableList = self.ospfTable(ospf1)

            for i in range(0,ospfrownum):
                for j in range(0,4):
                    table2.setItem(i,j, QTableWidgetItem(self.makeospflist(ospfTableList[i])[j]))

            #ospf 에어리어 분류
            oal = self.ospfArealist(ospfarea1)
            tr1.topLevelItem(0).setText(1, oal[0])
            tr1.topLevelItem(0).child(0).child(0).setText(1, oal[1])
            tr1.topLevelItem(0).child(0).child(1).setText(1, oal[2])
            tr1.topLevelItem(0).child(1).setText(1, oal[3])
            tr1.topLevelItem(0).child(2).setText(1, oal[4])
            tr1.topLevelItem(0).child(3).setText(1, oal[5])

            #메모리 관리
            mvalue = self.memorylist(memory1)
            prog.setValue(mvalue[1]/mvalue[0]*100)

            tb1.setText("총 용량(Mb): "+str(mvalue[0])+"\n잔여 용량(Mb): "
                        +str(mvalue[0]-mvalue[1])+"\n사용된 용량(Mb): "+str(mvalue[1]))

            #user정보
            us = user1.split()
            tb5.setText(us[16])
            tb6.setText(us[17])
            tb7.setText(us[19])
            tb8.setText(str(time1))

            #버전 정보 
            verinfo = self.verlist(version1)
            tb9.setText(verinfo[0])
            tb10.setText(verinfo[1])
            tb11.setText(verinfo[2])
            tb12.setText(verinfo[3])

            #cpu정보 
            cpuinfo = self.cpulist(cpu1)
            tb13.setText(cpuinfo[0])
            tb14.setText(cpuinfo[1])
            tb15.setText(cpuinfo[2])
            tb16.setText(cpuinfo[3])

            #Interface
            for (ethXcmd,tableX) in [(eth0cmd,table5),(eth1cmd,table6),(eth2cmd,table7),(eth3cmd,table8)]:
                for n in range(0,2):
                    for m in range(0,6):
                        tableX.setItem(n,m, QTableWidgetItem(self.etherlist(ethXcmd)[m+(6*n)]))

            #address
            for (ethXcmd, trX) in [(eth0cmd,tr2),(eth1cmd,tr3),(eth2cmd,tr4),(eth3cmd,tr5)] :
                ad = self.addrlist(ethXcmd)
                trX.topLevelItem(0).child(0).setText(1, ad[0])
                trX.topLevelItem(0).child(1).setText(1, ad[1])
                trX.topLevelItem(1).child(0).setText(1, ad[2])
                trX.topLevelItem(2).child(0).setText(1, ad[3])
                trX.topLevelItem(2).child(1).setText(1, ad[4])
                                   
                
            
        else :
            QMessageBox.about(self,"notice","Login failed")

            
    def routeseparate(self,route):
        routex = route[188:]
        x = route[188:].count('\x1b[m\n')
        j = 0
        routelist = []
        for i in range(0,x):
            temp = routex.index('\n',j,-1) + 1
            routelist.append(routex[j:temp])
            j= temp
        return routelist

    def makeroutelist(self, route):
        if route[0]=='S':
            protocol = 'Static'
            addr = route[4:route.index('[')-1]
            nexthop = route[route.index('via')+4:route.index(',')]
            nexthopif = route[route.index(',')+2:route.index('\x1b')]

        elif route[0]=='C':
            protocol = 'Direct'
            addr = route[4:route.index('is')-1]
            nexthop = '-'
            nexthopif = route[route.index(',')+2:route.index('\x1b')]

        elif route[0]=='O':
            addr = route[4:route.index('[')-1]
            try:
                nexthop = route[route.index('via')+4:route.index(',')]
                nexthopif = route[route.index(',')+2:route.index('\x1b')-10]
                protocol = 'OSPF'
            except:
                nexthop = '-'
                nexthopif = route[route.index(',')+2:route.index('\x1b')-10]
                protocol = 'OSPF(Direct)'

        elif route[0]=='B':
            protocol = 'BGP'
            addr = route[4:route.index('[')-1]
            nexthop = route[route.index('via')+4:route.index('(')-1]
            nexthopif = '-'
            
        else :
            protocol='x'
            addr='x'
            nexthop='x'
            nexthopif='x'
            
                
        return [protocol,addr,nexthop,nexthopif]

    def ospfTable (self, route):
        routex = route[176:]
        x = routex.count('\x1b[m \x08')
        j=0
        routelist = []
        for i in range(0,x):
            temp = routex.index('\n',j,-1) + 1
            routelist.append(routex[j:temp])
            j= temp
        return routelist

    def makeospflist (self, route):
        o = route.split()
        return [o[0],o[3],o[4],o[5]]

    def ospfArealist(self,ospfroute):
        area1 = ospfroute[ospfroute.index("Area ID"):]
        ospf_area = area1[9:area1.index('\n')]

        intnum1 = ospfroute[ospfroute.index("Number of interfaces in this area"):]
        ospf_intmumT = intnum1[intnum1.index('Total')+7:intnum1.index(',')]
        ospf_intmumA = intnum1[intnum1.index('Active')+8:intnum1.index('\n')]

        adj1 = ospfroute[ospfroute.index("Number of fully adjacent neighbors in this area"):]
        ospf_adj = adj1[48:adj1.index('\n')]

        if(ospfroute.count('no authentication') == 1):
            ospf_auth = 'N'
        else:
            ospf_auth = 'Y'

        lsa1 = ospfroute[ospfroute.index("Number of LSA"):]
        ospf_lsa = lsa1[14:lsa1.index('\n')]
                        
        return [ospf_area,ospf_intmumT,ospf_intmumA,ospf_adj,ospf_auth,ospf_lsa]

    def memorylist(self,memorycmd):
        total1 = memorycmd[memorycmd.index("Total"):]
        totalmemory = total1[6:total1.index('\x1b[m\n')]

        used1 = memorycmd[memorycmd.index("Used"):]
        usedmemory = used1[6:used1.index('\x1b[m\n')]

        return [int(totalmemory), int(usedmemory)]

    def cpulist(self, cpucmd):
        mhz1 = cpucmd[cpucmd.index("CPU MHz"):]
        cpu_mhz = mhz1[23:mhz1.index('\x1b[m\n')]

        arc1 = cpucmd[cpucmd.index("Architecture"):]
        cpu_arc = arc1[23:arc1.index('\x1b[m\n')]

        mod1 = cpucmd[cpucmd.index("CPU op-mode(s)"):]
        cpu_mod = mod1[23:mod1.index('\x1b[m\n')]

        vendor1 = cpucmd[cpucmd.index("Vendor ID"):]
        cpu_vendor = vendor1[23:vendor1.index('\x1b[m\n')]

        return [cpu_mhz, cpu_arc, cpu_mod, cpu_vendor]
    
    def verlist(self, vercmd):
        ver1 = vercmd[vercmd.index("Version"):]
        ver = ver1[14:ver1.index('\x1b[m\n')]

        hv1 = vercmd[vercmd.index("Hypervisor"):]
        hv = hv1[14:hv1.index('\x1b[m\n')]

        hwm1 = vercmd[vercmd.index("HW model"):]
        hwm = hwm1[14:hwm1.index('\x1b[m\n')]

        boot1 = vercmd[vercmd.index("Boot via"):]
        boot = boot1[14:boot1.index('\x1b[m\n')]

        return [ver, hv, hwm, boot]

    def etherlist(self, ethcmd):
        RX = ethcmd[ethcmd.index('RX'):ethcmd.index('TX')-5]
        TX = ethcmd[ethcmd.index('TX'):]
        RX1 = RX.split()
        TX1 = TX.split()
        def rateform(x,y):
            return str(float(x)/float(y)*100)
                
        return  [RX1[7], RX1[8], RX1[9], RX1[10], rateform(RX1[9],RX1[8]), rateform(RX1[10],RX1[8]) ,TX1[7], TX1[8], TX1[9], TX1[10], rateform(TX1[9],TX1[8]), rateform(TX1[10],TX1[8])]

    def addrlist(self, ethcmd):
        mac1 = ethcmd[ethcmd.index('link/ether'):ethcmd.index('\x1b[m\n    inet')]
        try:
            ip41= ethcmd[ethcmd.index('inet '):ethcmd.index('scope global')]
            ip4 = ip41.split()
        except:
            ip4=['None','None','None','None']
        ip61 = ethcmd[ethcmd.index('inet6'):ethcmd.index('scope link')]
        mac = mac1.split()
        ip6 = ip61.split()

        return [ ip4[1], ip4[3], ip6[1], mac[1], mac[3] ]
    
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = XDialog()
    dlg.show()
    app.exec_()



