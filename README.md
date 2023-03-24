#### Azan Helper
how to make echo device your muadhan (The person who performs the adhan)

Requirements
1 - echo device and connected Amazon account
2 - Alexa skill "virtual routine trigger"
2 - account at https://www.virtualsmarthome.xyz/virtual_routine_trigger/
3 - a webservice that can tell virtualsmarthome if its azan time
4 - Alexa skill "Azan (ALP Enabled)" that just plays Azan

On virtualsmarthome you can create 5 triggers that will be added to your Alexa apps as doorbells.

virtualsmarthome polls our endpoint and and compare the result to what we have set, if the condition matches a trigger is fired.

In Alexa app we can configure 5 routines 1 for each prayer time, that should  

this server was build to provide APIs that can be used by virtualsmarthome 
https://www.virtualsmarthome.xyz/virtual_routine_trigger/
