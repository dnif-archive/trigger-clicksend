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

def call(inward_array, var_array):
    """Place a call."""
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
        c = nt.format(**d)
        messg = str("<speak><prosody volume='x-loud' rate='medium'>" + c + "</prosody></speak>")
        url = "https://rest.clicksend.com/v3/voice/send"
        headers = {"Content-Type": "application/json"}
        body = {"messages":
            [
                {
                    "source": SOURCE,
                    "body": messg,
                    "to": s1[0],
                    "lang": LANG,
                    "voice": VOICE,
                    "require_input": REQ_INPUT,
                    "machine_detection": MACH_DETECT
                }
            ]
        }

        try:
            response = requests.post(url, auth=(USERNAME, API_KEY), data=json.dumps(body), headers=headers)
        except Exception as e:
            logging.error("Clicksend API Error >>{}<<".format(e))
            i['$ClickSendError'] = str(e)

        json_response = response.json()

        if json_response['data']['messages'][0]['status'] == 'SUCCESS':
            logging.info('Call placed to' + str(s1[0]) + 'with cost of' + str(
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
    return inward_array


def sms(inward_array, var_array):
    """Place a call."""
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
        c = nt.format(**d)
        url = "https://rest.clicksend.com/v3/sms/send"
        headers = {"Content-Type": "application/json"}
        body ={"messages":
                   [
                      {
                        "source": SOURCE,
                        "from": SOURCE,
                        "body": c,
                        "to": s1[0],
                        "custom_string": "this is a test",
                        "from_email" : "karthik.subramanian@net-mon.net"
                      }
                   ]
                }
        try:
            response = requests.post(url, auth=(USERNAME, API_KEY), data=json.dumps(body), headers=headers)
        except Exception as e:
            logging.error("Clicksend API Error >>{}<<".format(e))
            i['$ClickSendError'] = str(e)
        json_response = response.json()

        if json_response['data']['messages'][0]['status'] == 'SUCCESS':
            logging.info('Call placed to' + s1[0] + 'with cost of' + str(
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

    return inward_array

