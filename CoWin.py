#This code uses the Co-Win public API to fetch data based on districts and data and serach 
# if there is any avaiballe slot for 45+ people to take Dose 1 of Covishoeld vaccine. Written in Python 3.x

#Function to define districts for which centers needs to be fetched

def defineDistricts():
    dist_list = [725, 730]
    return dist_list

# End of function 

#Function to define the age category for which centers needs to be fetched
#Currently this function is not been used in the code and age is hard coded as 45+

def defineAge():
    age_list=[45, 18]
    return age_list

# End of function

#Function to define data range for which centers needs to be fetched. 
# it will be 10 days from current date + 1

def defineDateRange():
    import datetime
    base = datetime.datetime.today() + datetime.timedelta(days=1) #get tomorrows date
    date_list = [base + datetime.timedelta(days=x) for x in range(10)]
    date_str = [x.strftime("%d-%m-%Y") for x in date_list]
    return date_str

# End of function

# Function to get slot availability

def findSlot():
    import requests
    import json
    from fake_useragent import UserAgent
    temp_user_agent = UserAgent()
    browser_header = {'User-Agent': temp_user_agent.random}

    center_count = 0

    for slotdate in defineDateRange():
        for distid in defineDistricts():
            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}".format(distid, slotdate)
            response = requests.get(URL, headers=browser_header)
            resp_json = response.json()

            data_dict=json.loads(json.dumps(resp_json))
            no_of_items = (len(data_dict['sessions']))

            for i in range(0, no_of_items):
                if data_dict['sessions'][i]['fee_type'] == 'Paid' and data_dict['sessions'][i]['vaccine'] == 'COVISHIELD' and data_dict['sessions'][i]['min_age_limit'] == 45 and data_dict['sessions'][i]['available_capacity_dose1']>0:
                    print(data_dict['sessions'][i]['district_name'], '-', data_dict['sessions'][i]['name'],'-',data_dict['sessions'][i]['date'],'-',data_dict['sessions'][i]['available_capacity_dose1'])
                    center_count += 1
    if center_count > 0:
        print(center_count, " center(s) found")
    else:
        print("None Found. Try again")


#End of Function

#Calling the main Function

findSlot()
