# pip.ai
pip.ai is a Currency Exchange Monitor & Alert Agent. It is a Python-based tool that allows users to track and receive alerts on currency exchange rate fluctuations. This project uses the uAgent library to create a user-friendly interface and to interact with a currency exchange API to provide real-time exchange rate data.

## Features
* **Base Currency Selection**: Users can choose their preferred base currency, which serves as the reference currency for exchange rate comparisons.
* **Monitor Multiple Foreign Currencies**: Users can select one or more foreign currencies they wish to monitor against their chosen base currency.
* **Real-Time Exchange Rate Data**: The application connects to a currency exchange API to fetch up-to-date exchange rates.
* **Threshold Alerts**: Users can set custom threshold values for each monitored currency pair. The system will notify them when the exchange rate crosses these thresholds.
* **Notification Alerts**: The tool sends alerts or notifications to users through emails.

## Getting Started
Follow these steps to set up and run the Currency Exchange Monitor & Alert Agent:
1. **Clone the Repository**: Clone this project's Git repository to your local machine.
2. **Prerequisites**
   * Python (3.10 is required)
   * Poetry (a packaging and dependency management tool for Python)

  
  3. Run index.py as
     ```
     poetry run streamlit run index.py
     ```
  4. You'll be redirected to local host.
     * Click on Create Page
     * Fill the form
     * Click on Submit
       
  5. To update user preferences:
     * Click on Update Page
     * Update pref and Submit
    
  6. **Setup for .env File**:<br>
     Update the values of placeholders in .env.example and **rename the file to .env**(.env.example is included in the directory for sample)
     * **API Access**: Obtain an API key from (https://app.currencyapi.com/register) by signing in with your emailID
       (Note that if you’ve run out of your request limit, you will not be able to get results for this project.)
     * **Obtain APP_PASSWORD**: Follow the steps in the [link](https://support.google.com/accounts/answer/185833?hl=en) to setup APP_PASSWORD for your email account<br>
     
      To use the environment variables from .env and install the project:
      ```
      cd src
      poetry install
      ```
      * **For AGENT_SEED**: Add any random pass phrase
      * **For AGENT_ADDRESS**(For Exchange and Notify Agents Address): Run the main.py file, you need to look for the following output in the logs:
         ```
         Adding Exchange agent to Bureau : {exchange_agent.address}
         Adding Notify agent to Bureau : {notify_agent.address}
         ```
         Copy the {agent_name_agent.address} value, this is your AGENT's ADDRESS<br>

     Once you have all the keys, update the .env file
7. 
      
  
## Special Considerations

     




