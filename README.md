# Step-by-step guide to configure Splunk with APIsec.

## Approach 1: Using a Scripted Input (With Splunk Enterprise):
1.	Copy and place the script and config file developed by APIsec into the Splunk accessible folder.
2.	Update the config file with the Service Account username/password (I have used a token for testing) and update the logs settings to enable which logs to fetch:

![image](https://github.com/user-attachments/assets/2e7b61e9-676b-4d87-8dad-2af5db6ee708)
4.	From Splunk Enterprise Go to **Settings**-> **Data inputs** -> **Scripts** -> **New Local Script**
Select the script provided by APISec and then select the interval for periodic execution, it could be a CRON job also.

![image](https://github.com/user-attachments/assets/3a08f984-619d-4f77-9a16-ba9584d88e0f)
5.	Next Provide the Source Type to JSON.

![image](https://github.com/user-attachments/assets/94c6db8c-05cf-4c1d-83eb-3aeb6dbde706)
6.	This will be the final settings:

![image](https://github.com/user-attachments/assets/016132de-bbff-4854-b503-8b2dca8dc7a3)
7.	You should be able to see the logs in Splunk:

![image](https://github.com/user-attachments/assets/2ec88c1e-f799-425d-b3a0-30a0e001132d)

## Approach 2: Using Splunk Universal Forwarder:
To receive data from Splunk UF we need to enable the receiving port on **Splunk Indexer** (Default port is **9997**)  (**Settings**->**Forwarding and receiving** -> **Configuring receiving**)

![image](https://github.com/user-attachments/assets/61a487c9-555c-4165-91c8-c3eea4e63b4c)

![image](https://github.com/user-attachments/assets/7142ee73-6a5e-4996-bb0e-c8cd8082e1e5)
Install **Universal Forwarder** on the machine from where the user wants to send the data to the indexer, and while installing provide the IP address and port of the Splunk Indexer:

![image](https://github.com/user-attachments/assets/a005e497-2722-4b55-b791-7fdfc7d61f7d)
Here select data from Splunk forwarder (**Settings**-> **Add Data** )

![image](https://github.com/user-attachments/assets/60351ce1-b5ba-424a-8848-035cf4a4a4a1)
We should see the **configured forwarder** on Splunk, here in my case, it shows my **laptop hostname**. Next, the user needs to provide a class name, this will create an app in Splunk Forwarder

![image](https://github.com/user-attachments/assets/02e12e60-2497-433f-8d33-47eb4bb6bc91)

![image](https://github.com/user-attachments/assets/bdb3f8bb-e079-4453-b6f8-28f6ad130f76)
Next, we need to select “``Scripts``” as a source:

![image](https://github.com/user-attachments/assets/4bae8a1d-cded-4497-8d6d-c00355892cd0)
IMP Note: One of the catches here is that the script that we have developed needs to be available in the Splunk directory only if you see in the image below we have only two options to select the script from: “``bin\scripts``” and “``\etc\system\bin``”.  Another thing is Splunk UF doesn’t support Python script, so we need to write another wrapper script in “.bat” or “.sh” depending on OS. From this wrapper script, we need to call our Python script. So for this Python and our required scripts libraries must be installed on the client machine.

![image](https://github.com/user-attachments/assets/55a39f50-3450-4968-86ce-2dbd36b23566)
Here we can configure the interval in seconds or as a CRON job:

![image](https://github.com/user-attachments/assets/368f6f3e-b9af-44d5-baf5-f3c480ae37d8)
Our APIs are providing output in JSON, so I selected the source type as JSON:

![image](https://github.com/user-attachments/assets/4d8008de-c9ea-40f0-9762-f830941156c5)
Summary of config:

![image](https://github.com/user-attachments/assets/f194b1c8-322c-42ad-b57f-0e577717bd03)
Lastly, we can see the output here, I have written wrapper script “``wrapper_script2.bat``”:

![image](https://github.com/user-attachments/assets/fd410da3-1adc-47b7-b141-6de59049d2a3)










