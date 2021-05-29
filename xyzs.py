import urllib2, urllib
import socket
import re
import os, inspect
import a_cf
import s_c
import r_q
from r_q import rqs
import rs_p
from l_g import lgt
from o_n import onh
from r_p import f_p
import sys
import time
import signal
from termcolor import colored
import colorama

colorama.init()
options = onh()
def signal_handler(signal, frame):    
    print colored("\n---------------------------------------------------------------",'cyan')
    print colored("\nScanning interrupted",'red')
    print colored("Scan result observed till now is stored in reflected.txt file\n",'yellow')
    if options.shreflected ==True:
        print colored("-----------------------Scan Results------------------------",'white','on_green')
        ref_file = open(path+'/'+'reflected.txt','r')
        print colored(ref_file.read(),'green')
        ref_file.close()
    sys.exit(0)
signal.signal(signal.SIGINT,signal_handler)

class xss:
    def xssrun(self,postdata,mode,log):
        reload(s_c)
        CRLF = '\r\n\r\n'
        path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        try:
            scr_file = open(path+'/'+'script.txt','r')
        except IOError:
            print colored("Cannot read the script file script.txt",'white','on_red')
            print colored("Exiting...",'red')
            sys.exit(0)
        counter = scr_file.read()
        try:
            resp_file = open(path+'/'+'response.txt','r') 
        except IOError:
            print colored("Cannot read the file response.txt",'white','on_red')
            print colored("Exiting...",'red')
            sys.exit(0)
        scr_file.seek(0)
        count = counter.count('\n')
        cr = 0
        dr = 0
        param = None
        print colored("payload count: %d" %(count),'yellow')
        c_l = f_p()
        postdata = c_l.c_l(postdata)
        ba = s_c.cscr()
        csrfprint = a_cf.p_cf()
        cc = rqs()
        response_data = rs_p.resp()
        checklogout = lgt()
        data,respcode,requrl,respurl = cc.send_req(postdata,options.ssl,options.contimeout,options.shreflected,mode,log)
        for a in range(0,count+1):
            if options.scanone == True:
                cnt = 0
                checklogout.cklgt(data,options.logout,options.logoutcode,respcode,requrl,respurl,options.shreflected)
                if options.timedelay !=None:
                    time.sleep(options.timedelay)
                resp = resp_file.readline()
                resp = resp.rstrip()
                postdata1, bb= ba.a_scr(postdata,options.urlencode)
                if bb == '' or bb == None:
                    continue
                if options.blacklist !='' and options.blacklist !=None:
                    try:
                        for dd in options.blacklist.split(','):
                            de = urllib.unquote(bb)
                            if de.upper().lower().find(dd.upper().lower()) >=0:
                                cnt = cnt+1
                    except:
                        print colored('Black list data not provided in proper format.\nPlease include the characters within "" and separate each character using comma.\nEg:"$,@,!"','white','on_red')
                        sys.exit(0)
                if cnt >0:
                    continue
                if options.csrftoken != None and log == False:
                    postdata1 = csrfprint.da_cf(postdata1,data,options.csrftoken,options.shreflected)
                postdata1 = c_l.c_l(postdata1)
                print colored("-----------------------------------------------------------",'cyan')
                if options.verbose == True:
                    print "Request:\n",postdata1
                print "Trying payload: '%s'" %(bb.replace('+',' '))
                data,respcode,requrl,respurl = cc.send_req(postdata1,options.ssl,options.contimeout,options.shreflected,mode,log)
                print "Response status code observed: %s" %(respcode)
                rp,fl = response_data.resp1(data,resp,bb,None,options.strip)
                cr +=rp
            else:
                resp = resp_file.readline()
                resp = resp.rstrip()
                for postdata1,bc,bd in ba.scr_iter(postdata,options.csrftoken,options.skipparam,options.urlencode,options.increferer,param):
                    cnt = 0
                    checklogout.cklgt(data,options.logout,options.logoutcode,respcode,requrl,respurl,options.shreflected)
                    if options.timedelay !=None:
                        time.sleep(options.timedelay)
                    if bc == '' or bc ==None:
                        continue
                    if options.blacklist !='' and options.blacklist !=None:
                        try:
                            for dd in options.blacklist.split(','):
                                de = urllib.unquote(bc)
                                if de.upper().lower().find(dd.upper().lower()) >=0:
                                    cnt = cnt+1
                        except:
                            print colored('Black list data not provided in proper format.\nPlease include the characters within "" and separate each character using comma.\nEg:"$,@,!"','white','on_red')
                    if cnt >0:
                        continue
                    if options.csrftoken != None and log == False:
                        postdata1 = csrfprint.da_cf(postdata1,data,options.csrftoken,options.shreflected)
                    postdata1 = c_l.c_l(postdata1)
                    print colored("-----------------------------------------------------------",'cyan')
                    if options.verbose == True:
                        print "Request:\n",postdata1
                    print "Trying payload: '%s' on parameter '%s'" %(bc.replace('+',' '),bd)
                    data,respcode,requrl,respurl = cc.send_req(postdata1,options.ssl,options.contimeout,options.shreflected,mode,log)
                    print "Response status code observed: %s" %(respcode)
                    rp,fl = response_data.resp1(data,resp,bc,bd,options.strip)
                    cr +=rp
                    dr +=fl
                    if dr ==1 and log == False:
                        dr +=1
                        print colored("\n-------------------------------------------------------------\n",'cyan')
                        print colored("Reflection was found on parameter '%s'" %(bd),'white','on_green')
                        print colored("Press 'y' to continue scanning all parameters, 't' to scan only this parameter for other payloads and 'n' to exit",'yellow')
                        while True:
                            try:
                                input = raw_input(colored("Press 'y' or 't' or 'n'...\n",'yellow'))
                            except KeyboardInterrupt, e:
                                print colored("\n---------------------------------------------------------------\nScanning interrupted",'yellow')
                                print colored("Scan result observed till now is stored in reflected.txt file\n",'yellow')
                                sys.exit(0)
                            if input.lower() == 'y':
                                break
                            if input.lower() == 't':
                                param = bd
                                break
                            if input.lower() == 'n':
                                print colored("Exiting...",'red')
                                print colored("The reflection results are stored in reflected.txt file",'green')
                                scr_file.close()
                                resp_file.close()
                                sys.exit(0)
        scr_file.close()
        resp_file.close()
        return cr

    
    