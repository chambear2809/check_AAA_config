#!/usr/bin/env python
'''
Python 2.7.x only
check_for_AAA


Copyright (C) 2015 Cisco Systems Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
__appname__ = 'check_for_AAA'
__version__ = '1.0.0'
__license__ = '?'

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings() 
import sys
from cobra.mit.session import LoginSession
from cobra.mit.access import MoDirectory

###-------------------------------------------------------------------------------------------------------------------###
def login(apicUrl, user, password):
    try:
        loginSession = LoginSession(apicUrl,user,password)
        moDir = MoDirectory(loginSession)
        moDir.login()
    except:
        print "the username and/or password you entered is incorrect"
    return moDir
###-------------------------------------------------------------------------------------------------------------------###
def close_device(Master):
    Master.destroy()

###-------------------------------------------------------------------------------------------------------------------###

def Check_MO(moDir):
    LDAP_server = ""
    TACACS_server = ""
    RADIUS_server = ""
    forHtmlString = ""

    parent_A = moDir.lookupByClass('aaaLoginDomain',parentDn='uni/userext')
    for i in parent_A:
        print '  LoginDomain server:  {:20} Dn:  {:10} '.format(i.name,i.dn)
        linez = '  LoginDomain server:  {:20} Dn:  {:10} '.format(i.name,i.dn)
        forHtmlString += linez+"<br>"
    print '\n  ----------------------------------------------------------------------------------------------------\n'
    linez = '\n  ----------------------------------------------------------------------------------------------------\n'
    forHtmlString += "<br>"+linez+"<br>"

    ###-----------------------------------------------------------------------------------------------------------------###

    parent_A = moDir.lookupByClass('aaaLdapProvider',parentDn='uni/userext/ldapext')
    for i in parent_A:
        LDAP_server =  i.name

    ###------------------------------------------ RADIUS ----------------------------------------------------------------###

    parent_A = moDir.lookupByClass('aaaRadiusProvider',parentDn='uni/userext/radiusext')
    for i in parent_A:
        RADIUS_server = i.name

    ###------------------------------------------ TacacsPlus ------------------------------------------------------------###

    parent_A = moDir.lookupByClass('aaaTacacsPlusProvider',parentDn='uni/userext/tacacsext')
    for i in parent_A:
        TACACS_server = i.name


    return LDAP_server, TACACS_server, RADIUS_server, forHtmlString

###-----------------------------------------------------------------------------------------------------------------###
def main(hostIP, userID, pw):
    HtmldomainInfo = []

    forHtmlString = ""
    forHtmlString += '<pre>'
    forHtmlString += '<!DOCTYPE>'
    forHtmlString += '<html>'
    forHtmlString += '<head>'
    forHtmlString += '<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js"></script>'
    forHtmlString += '<link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon">'
    forHtmlString += '<link rel="icon" href="/static/favicon.ico" type="image/x-icon">'
    forHtmlString += '<link href="/static/style.css" rel="stylesheet">'
    forHtmlString += '</head>'
    forHtmlString += '<body>'
    forHtmlString += '<a href="/select_script"><img src="/static/cisco-logo.png" alt="Cisco Logo" width="10%" height="10%" ></a>'
    print '\n APIC OOB IP : ' + hostIP
    linez = '<b> APIC OOB IP : ' + hostIP
    forHtmlString += "<br>"+"<br>"+linez+"<br>"
    print   '\n              Check for login Domains (LDAP, RADIUS, and TACACS services) on the APIC'
    linez = '              Check for login Domains (LDAP, RADIUS, and TACACS services) on the APIC'
    forHtmlString += linez+"<br>"
    print   '\n======================================================================================================\n'
    linez = '======================================================================================================'
    forHtmlString += linez+"<br>"
    HtmldomainInfo.append(forHtmlString)
    forHtmlString = ""

    LDAP_server, TACACS_server, RADIUS_server, forHtmlString = Check_MO(login("https://"+hostIP,userID,pw,))
    HtmldomainInfo.append(forHtmlString)
    forHtmlString = ""

    if LDAP_server != "":
        print "  LDAP   :  Received update on status of %s (DN uni/userext/ldapext/ldapprovider-%s) - status is ALIVE " % (LDAP_server,LDAP_server)
        linez = "  LDAP   :  Received update on status of %s (DN uni/userext/ldapext/ldapprovider-%s) - status is ALIVE " % (LDAP_server,LDAP_server)
        forHtmlString += linez+"<br>"
    else:
        print '\n  LDAP   :  LDAP_server has not been configured '
        linez = '\n  LDAP   :  LDAP_server has not been configured '
        forHtmlString += linez+"<br>"

    if RADIUS_server != "":
        print "  RADIUS :  Received update on status of %s (DN uni/userext/radiusext/radiusprovider-%s) - status is ALIVE " % (RADIUS_server,RADIUS_server)
        linez =  "  RADIUS :  Received update on status of %s (DN uni/userext/radiusext/radiusprovider-%s) - status is ALIVE " % (RADIUS_server,RADIUS_server)
        forHtmlString += linez+"<br>"
    else:
        print '\n  RADIUS :  RADIUS_server has not been configured '
        linez = '\n  RADIUS :  RADIUS_server has not been configured '
        forHtmlString += linez+"<br>"

    if TACACS_server != "":
        print "  TACACS :  Received update on status of %s (DN uni/userext/tacacsext/tacacsplusprovider-%s) - status is ALIVE " % (TACACS_server,TACACS_server)
        linez = "  TACACS :  Received update on status of %s (DN uni/userext/tacacsext/tacacsplusprovider-%s) - status is ALIVE " % (TACACS_server,TACACS_server)
        forHtmlString += linez+"<br>"
    else:
        print '\n  TACACS :  TACACS_server has not been configured '
        linez = '\n  TACACS :  TACACS_server has not been configured '
        forHtmlString += linez+"<br>"

    forHtmlString += '<div id="power">'
    forHtmlString += 'Powered By'
    forHtmlString += '<img src="/static/cisco-tac.jpg" alt="Cisco TAC" width="25%" height="25%" >'
    forHtmlString += '</div>'

    forHtmlString += '</body>'
    forHtmlString += '</html>'
    forHtmlString += '</pre>'
    HtmldomainInfo.append(forHtmlString)

    return HtmldomainInfo

###------------------------------------------------------------------------------------------------------------------------###
if __name__ == "__main__":
    apicIP, userID, pw = '', '',''
    main(sys.argv[1],sys.argv[2],sys.argv[3])

