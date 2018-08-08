# ClickSend
https://clicksend.docs.apiary.io/

The trigger directive allows for a call to be placed with a custom message.

## Trigger functions incorporated with ClickSend

### Call
 
Allows for placing a call to a specified number with0 a message, error, warning etc.

- input : the custom message to be sent

```
_fetch * from event where $Intel=True limit 1
>> _trigger api clicksend call +9183xxxxxxxx, Source found positive in Intel check , $SrcIP
```

|     Field     |             Description              |
|---------------|--------------------------------------|
| $CSCarrier    | The carrier ClickSend is calling to  |
| $CSCountry    | The country ClickSend is calling to  |
| $CSMEssageID  | The ID of the call placed            |
| $CSTime       | Time the call was placed             |
| $CSFrom       | Number the call is being placed from |
| $CSStatus     | Status of the call placed            |
| $CSTotalPrice | Cost of the call placed              |
| $CSBalance    | Remaining balance in the account     |    

### Using the ClickSend API and DNIF  
The ClickSend API is found on github at 

#### Getting started with ClickSend API and DNIF

1. #####    Login to your Data Store, Correlator, and A10 containers.  
   [ACCESS DNIF CONTAINER VIA SSH](https://dnif.it/docs/guides/tutorials/access-dnif-container-via-ssh.html)
2. #####    Move to the `‘/dnif/<Deployment-key>/trigger_plugins’` folder path.
```
$cd /dnif/CnxxxxxxxxxxxxV8/lookup_plugins/
```
3. #####   Clone using the following command  
```  
git clone https://github.com/dnif/trigger-clicksend.git clicksend
```
4. #####   Move to the `‘/dnif/<Deployment-key>/trigger_plugins/clicksend/’` folder path and open dnifconfig.yml configuration file     
    
   Replace the tag: <Add_your_api_key_here> with your ClickSend api key
```
trigger_plugin:
  CS_USERNAME: <Add_your_ClickSend_username_here>
  CS_API_KEY:  <Add_your_api_key_here>
  CS_NUMBER: <Add_your_number_here>
  CS_SOURCE: <Add_the_name_of_source_here>
  CS_LANG: <Add_language_here>
  CS_VOICE: <Add_voice_gender_here>
  CS_REQUIRE_INPUT: <Add_1_for t
  CS_MACHINE_DETECTION: 0 

```
