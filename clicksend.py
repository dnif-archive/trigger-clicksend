import requests
import json
import yaml
import logging
import time
import os
import re

path = os.environ["WORKDIR"]
try:
    with open(path + "/trigger_plugins/clicksend/dnifconfig.yml", 'r') as ymlfile:
        CFG = yaml.load(ymlfile)
        USERNAME = CFG['trigger_plugin']['CS_USERNAME']
        API_KEY = CFG['trigger_plugin']['CS_API_KEY']
        SOURCE = CFG['trigger_plugin']['CS_SOURCE']
        LANG = CFG['trigger_plugin']['CS_LANG']
        VOICE = CFG['trigger_plugin']['CS_VOICE']
        REQ_INPUT = CFG['trigger_plugin']['CS_REQUIRE_INPUT']
        MACH_DETECT = CFG['trigger_plugin']['CS_MACHINE_DETECTION']
except Exception,e:
    logging.warning()


def clicksend_call(cno,msg):
    logging.debug("In clicksend_call")
    logging.debug("Call place to >>{}<< with message >>{}<<".format(cno,msg))
    messg = str("<speak><prosody volume='x-loud' rate='medium'>" + msg + "</prosody></speak>")
    url = "https://rest.clicksend.com/v3/voice/send"
    headers = {"Content-Type": "application/json"}
    body = {"messages":
        [
            {
                "source": SOURCE,
                "body": messg,
                "to": cno,
                "lang": LANG,
                "voice": VOICE,
                "require_input": REQ_INPUT,
                "machine_detection": MACH_DETECT
            }
        ]
    }
    try:
        i = {}
        response = requests.post(url, auth=(USERNAME, API_KEY), data=json.dumps(body), headers=headers)
    except Exception as e:
        logging.error("Clicksend API Error >>{}<<".format(e))
        i['$ClickSendError'] = str(e)

    json_response = response.json()

    if json_response['data']['messages'][0]['status'] == 'SUCCESS':
        logging.info('Call placed to' + str(cno) + 'with cost of' + str(
            json_response['data']['_currency']['currency_name_short'] + str(json_response['data']['total_price'])))
    else:
        logging.error('Call ' + str(json_response['data']['messages'][0]['status']))
    try:
        messages = json_response['data']['messages'][0]
    except Exception:
        pass
    try:
        i['$CSCarrier'] = messages['carrier']
        i['$CSCountry'] = messages['country']
        i['$CSMEssageID'] = messages['message_id']
        i['$CSTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(1347517370))
        i['$CSFrom'] = messages['from']
        i['$CSStatus'] = messages['status']
    except Exception as e:
        pass
    try:
        i['$CSTotalPrice'] = json_response['data']['total_price']
    except Exception:
        pass

    url = "https://rest.clicksend.com/v3/account"

    response = requests.get(url, auth=(USERNAME, API_KEY))
    json_response = response.json()

    try:
        i['$CSBalance'] = json_response['data']['balance']
    except Exception:
        pass
    return i


def clicksend_sms(cno,msg):
    logging.debug("in clicksend_sms")
    logging.debug("SMS sent to >>{}<< with message >>{}<<".format(cno,msg))
    url = "https://rest.clicksend.com/v3/sms/send"
    headers = {"Content-Type": "application/json"}
    body = {"messages":
        [
            {
                "source": SOURCE,
                "from": SOURCE,
                "body": msg,
                "to": cno
            }
        ]
    }
    try:
        i = {}
        response = requests.post(url, auth=(USERNAME, API_KEY), data=json.dumps(body), headers=headers)
    except Exception as e:
        logging.error("Clicksend API Error >>{}<<".format(e))
        i['$ClickSendError'] = str(e)
    json_response = response.json()

    if json_response['data']['messages'][0]['status'] == 'SUCCESS':
        logging.info('SMS sent to' + cno + 'with cost of' + str(
            json_response['data']['_currency']['currency_name_short'] + str(json_response['data']['total_price'])))
    else:
        logging.error('Call ' + str(json_response['data']['messages'][0]['status']))
    try:
        messages = json_response['data']['messages'][0]
    except Exception:
        pass
    try:
        i['$CSCarrier'] = messages['carrier']
        i['$CSCountry'] = messages['country']
        i['$CSMEssageID'] = messages['message_id']
        i['$CSTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(1347517370))
        i['$CSFrom'] = messages['from']
        i['$CSStatus'] = messages['status']
    except Exception as e:
        pass
    try:
        i['$CSTotalPrice'] = json_response['data']['total_price']
    except Exception:
        pass

    url = "https://rest.clicksend.com/v3/account"

    response = requests.get(url, auth=(USERNAME, API_KEY))
    json_response = response.json()

    try:
        i['$CSBalance'] = json_response['data']['balance']
    except Exception:
        pass
    return i


def call(inward_array, var_array):
    """Place a call."""
    logging.debug("in call")
    tmp_lst = []
    if len(inward_array) == 0:
        var_array[0] = str(var_array[0]).strip()
        s1 = var_array[0].split('"')
        cno = str(s1[0]).strip()
        msg = str(s1[1]).strip()
        tmp_dct = {}
        fn = clicksend_call(cno,msg)
        tmp_dct.update(fn)
        inward_array.append(tmp_dct)
        return inward_array
    else:
        for i in inward_array:
            # if var_array[2]:
            var_array[0] = str(var_array[0]).strip()
            s1 = var_array[0].split('"')
            s = str(s1[1]).strip()
            d = re.findall('\s*_(.*?)_\s*', s)
            nt = s
            for di in d:
                nt = re.sub("_{}_".format(di), '{$' + di + '}', nt)
            d = dict((x[1], '~~') for x in nt._formatter_parser())
            d.update(i)
            cno = str(s1[0]).strip()
            msg = nt.format(**d)
            fn= clicksend_call(cno,msg)
            i.update(fn)
            tmp_lst.append(i)
        return tmp_lst


def sms(inward_array, var_array):
    """Place a sms."""
    logging.debug("In sms")
    tmp_lst = []
    if len(inward_array) == 0:
        var_array[0] = str(var_array[0]).strip()
        s1 = var_array[0].split('"')
        cno = str(s1[0]).strip()
        msg = str(s1[1]).strip()
        tmp_dct = {}
        fn = clicksend_sms(cno, msg)
        tmp_dct.update(fn)
        inward_array.append(tmp_dct)
        return inward_array
    else:
        for i in inward_array:
            # if var_array[2]:
            logging.warning("To number is : {}".format(var_array[0]))
            var_array[0] = str(var_array[0]).strip()
            s1 = var_array[0].split('"')
            s = str(s1[1]).strip()
            d = re.findall('\s*_(.*?)_\s*', s)
            nt = s
            for di in d:
                nt = re.sub("_{}_".format(di), '{$' + di + '}', nt)
            d = dict((x[1], '~~') for x in nt._formatter_parser())
            d.update(i)
            cno = str(s1[0]).strip()
            msg = nt.format(**d)
            fn = clicksend_sms(cno, msg)
            i.update(fn)
            tmp_lst.append(i)
        return tmp_lst
