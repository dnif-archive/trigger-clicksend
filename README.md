# ClickSend
https://www.clicksend.com/in/voice/

### Overview
ClickSend is a global leader in business communication solutions.
From bulk marketing to mission-critical solutions, email marketing tools through to Fax, Post and Geolocation services, are used by some of the largest and most trusted brands in India and around the world.  

#### PRE-REQUISITES to use ClickSend and DNIF  
Outbound access required for github to clone the plugin

| Protocol   | Source IP  | Source Port  | Direction	 | Destination Domain | Destination Port  |  
|:------------- |:-------------|:-------------|:-------------|:-------------|:-------------|  
| TCP | DS,CR,A10 | Any | Egress	| github.com | 443 | 
| TCP | DS,CR,A10 | Any | Egress	| clicksend.com | 443 |  

**Note** The above rule assumes both request and response in enabled  

### ClickSend trigger plugin functions
Details of the function that can be used with the ClickSend trigger is given in this section.  
[call](#call)  
[sms](#sms)

### call 
This function allows for a call to be placed to a specified number with a custom message against an observerd event .

#### Input  
- Contact person's mobile number 
- The custom message to be sent for the event  
#### Example
```
_fetch $SrcIP, $ViolationField , $IntelRef from event where $Intel=True limit 1
>> _trigger api clicksend call +918xxxxxxxxx "Source IP _SrcIP_ found positive in Intel check against Intel feed _IntelRef_"
```
  
#### Output  
  ![call](https://user-images.githubusercontent.com/37173181/50265069-d981e780-0443-11e9-9116-0e4e36c79e1e.jpg)
    
The output of the lookup call has the following structure (for the available data)
    
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

### sms 
This function allows for a sms to be sent to a specified number with a custom message against an observerd event .

#### Input  
- Contact person's mobile number 
- The custom message to be sent for the event  
#### Example
```
_fetch $SrcIP, $ViolationField , $IntelRef from event where $Intel=True limit 1
>> _trigger api clicksend sms +918xxxxxxxxx "Source IP _SrcIP_ found positive in Intel check against Intel feed _IntelRef_"
```  
#### Output  
  ![sms](https://user-images.githubusercontent.com/37173181/50265121-2960ae80-0444-11e9-8069-6bfc5f8dca27.jpg)
    
The output of the lookup call has the following structure (for the available data)
    
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
https://github.com/dnif/trigger-clicksend
### Getting started with ClickSend API and DNIF

1. ####    Login to your Data Store, Correlator, and A10 containers.  
   [ACCESS DNIF CONTAINER VIA SSH](https://dnif.it/docs/guides/tutorials/access-dnif-container-via-ssh.html)
2. ####    Move to the `‘/dnif/<Deployment-key>/trigger_plugins’` folder path.
```
$cd /dnif/CnxxxxxxxxxxxxV8/trigger_plugins/
```
3. ####   Clone using the following command  
```  
git clone https://github.com/dnif/trigger-clicksend.git clicksend
```
4. ####   Move to the `‘/dnif/<Deployment-key>/trigger_plugins/clicksend/’` folder path and open dnifconfig.yml configuration file     
    
   Replace the tag: <Add_your_api_key_here> with your ClickSend API key
```
trigger_plugin:
  CS_USERNAME: <Add_your_ClickSend_username_here>
  CS_API_KEY:  <Add_your_api_key_here>
  CS_SOURCE: <Add_the_name_of_source_here>
  CS_LANG: <Add_language_here>
  CS_VOICE: <Add_voice_gender_here>
  CS_REQUIRE_INPUT: <Add_1_for_true,Add_0_for_false>
  CS_MACHINE_DETECTION: 0 
```
