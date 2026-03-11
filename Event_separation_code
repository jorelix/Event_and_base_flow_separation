
import streamlit as st
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
import os
from io import BytesIO, StringIO
import base64
from contextlib import redirect_stdout
import uuid
import json
from datetime import datetime
from pathlib import Path
from botocore.exceptions import ClientError
import boto3
import math


# Set page config for a wide layout and custom title
st.set_page_config(page_title="Event Analysis Dashboard", layout="wide")


# Function to convert plot to base64 for display and download
def get_image_download_link(img_path):
    with open(img_path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode()
    return f'<a href="data:image/png;base64,{b64_string}" download="plot.png">Download Plot</a>'

# Function to convert text file to download link
def get_text_download_link(txt_path):
    with open(txt_path, "r") as txt_file:
        content = txt_file.read()
    b64_string = base64.b64encode(content.encode()).decode()
    return f'<a href="data:text/plain;base64,{b64_string}" download="events.txt">Download Event Data</a>'

# Function to validate CSV with enhanced error handling

def validate_csv(file):
    try:
        # Reset file pointer
        file.seek(0)
        # Read first few bytes to check content
        sample = file.read(1024).decode('utf-8', errors='ignore')
        if not sample.strip():
            return False, "CSV file is empty."
        
        # Try different delimiters and encodings
        for encoding in ['utf-8', 'latin1', 'iso-8859-1']:
            for delimiter in [',', ';', '\t']:
                try:
                    file.seek(0)
                    df = pd.read_csv(file, encoding=encoding, sep=delimiter, nrows=5)
                    if df.empty or len(df.columns) < 3:
                        continue
                    required_columns = ['Date', 'Flow', 'Concentration']
                    # if all(col in df.columns for col in required_columns):
                    if all(col.lower() in [c.lower() for c in df.columns] for col in required_columns):
                        return True, ""
                    return False, "CSV must have 'Date', 'Flow', and 'Concentration' columns (check spelling and case)."
                except Exception as e:
                    continue
        return False, "Unable to parse CSV. Check delimiter (should be comma, semicolon, or tab) and ensure valid data."
    except Exception as e:
        return False, f"Invalid CSV: {str(e)}"


def daily_events(data_file, heading, water_table, water_temp, winterr, springg, summerr, falll, season_deli, field_area):

##############################################################################################################################################################
##############################################################################################################################################################
##############################################################################################################################################################                
# You can reset the values by either deleting the run_metadata.json file or using the reset button or manually setting the values int the run_metadata.json file.

        # S3 bucket and file details
    bucket_name = 'runmetadata.json'
    file_key = 'runmetadatafile.json'

    def read_json_from_s3(display=False):
        """Read JSON from S3 and optionally display the content in a single-column dashboard layout."""
        try:
            # Retrieve AWS credentials from Streamlit secrets
            aws_access_key_id = st.secrets["AWS_ACCESS_KEY_ID"]
            aws_secret_access_key = st.secrets["AWS_SECRET_ACCESS_KEY"]
            aws_region = st.secrets.get("AWS_DEFAULT_REGION", "us-east-1")  # Default to us-east-1 if not provided

            # Initialize the S3 client with the credentials
            s3_client = boto3.client(
                's3',
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=aws_region
            )

            # Read the file from S3
            response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
            # Read the content and decode it
            file_content = response['Body'].read().decode('utf-8')
            # Parse JSON content
            json_content = json.loads(file_content)
            
            return json_content
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                st.write(f"File {file_key} not found in bucket {bucket_name}")
            else:
                st.write(f"Error reading from S3: {e}")
            return None
        except json.JSONDecodeError as e:
            st.write(f"Error decoding JSON: {e}")
            return None
        except KeyError as e:
            st.error(f"Missing AWS credentials in Streamlit secrets: {e}")
            return None

    def write_json_to_s3(data, display=False):
        """Write JSON to S3 and optionally display the written content."""
        try:
            # Retrieve AWS credentials from Streamlit secrets
            aws_access_key_id = st.secrets["AWS_ACCESS_KEY_ID"]
            aws_secret_access_key = st.secrets["AWS_SECRET_ACCESS_KEY"]
            aws_region = st.secrets.get("AWS_DEFAULT_REGION", "us-east-1")  # Default to us-east-1 if not provided

            # Initialize the S3 client with the credentials
            s3_client = boto3.client(
                's3',
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=aws_region
            )

            # Convert data to JSON string
            json_content = json.dumps(data, indent=2)
            # Write the file to S3
            s3_client.put_object(
                Bucket=bucket_name,
                Key=file_key,
                Body=json_content.encode('utf-8'),
                ContentType='application/json'
            )
            # if display:
            #     st.write("Updated file content:", data)
            #     st.write(f"Successfully wrote to {file_key} in bucket {bucket_name}")
        except ClientError as e:
            st.write(f"Error writing to S3: {e}")
        except Exception as e:
            st.write(f"Error: {e}")

    def update_selected_fields(prev_data, fields_to_increment):
        """Update only the specified fields by incrementing their values by 1."""
        updated_data = prev_data.copy()
        updated_data["timestamp"] = datetime.now().isoformat()
        
        for field in fields_to_increment:
            if field in updated_data and isinstance(updated_data[field], (int, float)):
                updated_data[field] += 1
            else:
                st.write(f"Warning: Field {field} not found or not numeric, skipping.")
        
        return updated_data

###############################################################################################################################################################
    # Example usage - This is the writer
    if __name__ == "__main__":
        # Read and display the current file content in dashboard layout
        content = read_json_from_s3(display=True)
        
        if content:
            # Specify which fields to increment
            fields_to_increment = [
                "Total_Analysis_Performed",
                # "Hourly_Data_Analysis",
                "Daily_Data_Analysis",
                # "Seasonal_Delineation_Method_A",
                # "Seasonal_Delineation_Method_B"
            ]
            
            # Update selected fields
            updated_data = update_selected_fields(content, fields_to_increment)
            
            # Write and display the updated content
            write_json_to_s3(updated_data, display=True)
        else:
            # If no file exists, create new data
            new_data = {
                "timestamp": datetime.now().isoformat(),
                "Total_Analysis_Performed": 4,
                "Seasonal_Delineation_Method_A": 2,
                "Seasonal_Delineation_Method_B": 2,
                "Daily_Data_Analysis": 2,
                "Hourly_Data_Analysis": 2
            }
            st.write("No file found. Creating new file with default data.")
            write_json_to_s3(new_data, display=True)
###############################################################################################################################################################

#############################################################################################################################################################
############################################################################################################################################################# 


    df = pd.read_csv(data_file)
    st.write('\n')
    st.header('This is the first 50 lines')
    st.write('\n')
    st.write(df.head(51))
    st.write('\n')
    
    Date = []
    Discharge = []
    concentration = []
    with open(data_file, 'r', newline='') as file:
        reader = csv.reader(file)
        valid = 1
        valid_used = False
        instate = 0
        for row in reader:
            if row[0] == '':
                if instate == 0:
                    instate = valid
                elif valid > instate:
                    st.write(f'You have a missing date on line {instate} - Kindly check line {instate} on your csv file')
                    valid_used = True
                    break
            else:
                valid += 1
                Date.append(row[0])
                if row[1] == '':
                    Discharge.append(0.0)
                else:
                    Discharge.append((row[1]))
                    
                if row[2] == '':
                    concentration.append(0.0)
                else:
                    concentration.append((row[2]))


                    
    if valid_used == False:
        if water_table == 'Yes':
            water_level = []
            with open(data_file, 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == '':
                        break
                    else:
                        if row[3] == '':
                            water_level.append(0.0)
                        else:
                            water_level.append((row[3]))

        st.write('\n')
        if water_temp == 'Yes':
            water_chill = []
            with open(data_file, 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == '':
                        break
                    else:
                        if row[4] == '':
                            water_chill.append(0.0)
                        else:
                            water_chill.append((row[4]))
                    
        st.write('\n')
        if heading == 'Yes':
            Date.remove(Date[0])
            Discharge.remove(Discharge[0])
            concentration.remove(concentration[0])
            if water_table == 'Yes':
                water_level.remove(water_level[0])
            if water_temp == 'Yes':
                water_chill.remove(water_chill[0])
            
    #         st.write(Date)
            for elements in range(0, len(Discharge)):
                Discharge[elements] = float(Discharge[elements])
                concentration[elements] = float(concentration[elements])
                if water_table == 'Yes':
                    water_level[elements] = float(water_level[elements])
                if water_temp == 'Yes':
                    water_chill[elements] = float(water_chill[elements])
                    
            Dates = []
            for elements in Date:
                spliter = []
                collector = ''
                y = list(elements)
                for elem in y:
                    collector += elem
                spliter.append(collector)
                Dates.append(spliter)
        else:
            for elements in range(0, len(Discharge)):
                # st.write(Discharge[elements])
                Discharge[elements] = float(Discharge[elements])
                concentration[elements] = float(concentration[elements])
                if water_table == 'Yes':
                    water_level[elements] = float(water_level[elements])
                if water_temp == 'Yes':
                    water_chill[elements] = float(water_chill[elements])
                    
            Dates = []
            for elements in Date:
                spliter = []
                collector = ''
                y = list(elements)
                for elem in y:
                    collector += elem
                spliter.append(collector)
                Dates.append(spliter)
    #   
        
        percentage_discharge_change = ['event']
        for elements in range(1, len(Discharge)):
            y = Discharge[elements]
            change = y - Discharge[elements - 1]
            if Discharge[elements - 1 ] == 0:
                percentage_discharge_change.append('no flow')
            else:
                percent_change = (change/Discharge[elements - 1]) * 100
                percentage_discharge_change.append(percent_change)
        
        for elements in range(0, len(percentage_discharge_change)):
            c = f'{elements + 1} - {percentage_discharge_change[elements]}'
    #         st.write(c)
        high_compound_flow = []
        low_compound_flow = []
        combine_compound_flow = []
        events = []
        event_dates = []
        baseflow = []
        baseflow_dates = []
        event_endpoint = 0
        event_bunch = []
        catch_no = 0
        packer = 0
        caught_events = {}
        event_occuring = False
        switch = False
        winter = 0
        spring = 0
        summer  = 0
        fall = 0
        seasons = 0
        all_varient = []
        
        
        event_point = winterr
        winter = event_point
        all_varient.append(float(event_point))

        event_point = springg
        spring = event_point
        all_varient.append(float(event_point))

        event_point = summerr
        summer = event_point
        all_varient.append(float(event_point))

        event_point = falll
        fall = event_point
        all_varient.append(float(event_point))
        
        mean_jump = sum(all_varient)/len(all_varient)
    #     st.write(mean_jump)
        
        season_delineation = season_deli
        st.write('\n') 
        searching = True

        month = ''
        if season_delineation == 'B':
###############################################################################################################################################################
            # Example usage - This is the writer
            if __name__ == "__main__":
                # Read and display the current file content in dashboard layout
                content = read_json_from_s3(display=True)
                
                if content:
                    # Specify which fields to increment
                    fields_to_increment = [
                        # "Total_Analysis_Performed",
                        # "Hourly_Data_Analysis",
                        # "Daily_Data_Analysis",
                        # "Seasonal_Delineation_Method_A",
                        "Seasonal_Delineation_Method_B"
                    ]
                    
                    # Update selected fields
                    updated_data = update_selected_fields(content, fields_to_increment)
                    
                    # Write and display the updated content
                    write_json_to_s3(updated_data, display=True)
                else:
                    # If no file exists, create new data
                    new_data = {
                        "timestamp": datetime.now().isoformat(),
                        "Total_Analysis_Performed": 4,
                        "Seasonal_Delineation_Method_A": 2,
                        "Seasonal_Delineation_Method_B": 2,
                        "Daily_Data_Analysis": 2,
                        "Hourly_Data_Analysis": 2
                    }
                    st.write("No file found. Creating new file with default data.")
                    write_json_to_s3(new_data, display=True)
###############################################################################################################################################################
#####################################################################################################################################
            # Text file reading and writing above json file below
            
#####################################################################################################################################

            # st.write(Dates[0])
            step = 0
            while searching == True:
                #This does not loop in any list it is to tell you what the starter is
                day = list(Dates[0][0])
    #             st.write(day)
                member = day[step]
    #             st.write(member)
                try:
                    member = int(member)
                    month +=  f'{member}'
                    step += 1
                except:
                    searching = False
                    if float(month) == 12 or float(month) < 3:
                        event_point = winter
                        st.subheader('Analysis starting in Winter')
                    elif float(month) > 2 and float(month) < 6:
                        event_point = spring
                        st.subheader('Analysis starting in spring')
                    elif float(month) > 5 and float(month) < 9:
                        event_point = summer                    
                        st.subheader('Analysis starting in summer')
                    elif float(month) > 8 and float(month) < 12:
                        event_point = fall                    
                        st.subheader('Analysis starting in fall')
        elif season_delineation == 'A':
###############################################################################################################################################################
            # Example usage - This is the writer
            if __name__ == "__main__":
                # Read and display the current file content in dashboard layout
                content = read_json_from_s3(display=True)
                
                if content:
                    # Specify which fields to increment
                    fields_to_increment = [
                        # "Total_Analysis_Performed",
                        # "Hourly_Data_Analysis",
                        # "Daily_Data_Analysis",
                        "Seasonal_Delineation_Method_A",
                        # "Seasonal_Delineation_Method_B"
                    ]
                    
                    # Update selected fields
                    updated_data = update_selected_fields(content, fields_to_increment)
                    
                    # Write and display the updated content
                    write_json_to_s3(updated_data, display=True)
                else:
                    # If no file exists, create new data
                    new_data = {
                        "timestamp": datetime.now().isoformat(),
                        "Total_Analysis_Performed": 4,
                        "Seasonal_Delineation_Method_A": 2,
                        "Seasonal_Delineation_Method_B": 2,
                        "Daily_Data_Analysis": 2,
                        "Hourly_Data_Analysis": 2
                    }
                    st.write("No file found. Creating new file with default data.")
                    write_json_to_s3(new_data, display=True)
###############################################################################################################################################################

#####################################################################################################################################
            # Text file reading and writing above json file below
            
#####################################################################################################################################
            
            # st.write(Dates[0])
            step = 0
            while searching == True:
                day = list(Dates[0][0])
                member = day[step]
    #             st.write(member)
                try:
    #                 st.write(member)
                    member = int(member)
                    month +=  f'{member}'
                    step += 1
                except:
                    searching = False
    #                 st.write(month)
                    if float(month) < 4:
                        event_point = winter
                        st.subheader('Analysis starting in Winter')
                    elif float(month) > 3 and float(month) < 7:
                        event_point = spring
                        st.subheader('Analysis starting in spring')
                    elif float(month) > 6 and float(month) < 10:
                        event_point = summer                    
                        st.subheader('Analysis starting in summer')
                    elif float(month) > 9:
                        event_point = fall                    
                        st.subheader('Analysis starting in fall')
        st.write('\n')
        
        if Discharge[0] > event_point:
            event_occuring = True
            ## this part supplies the whole data for the analysis
        event_ends = 0
        base_compound = 0
        high_compound = 0
    #     st.write(len(Discharge))
        for elements in range(0, len(Discharge)):
            searching = True
            month = ''
            if season_delineation == 'B':
    #             st.write(Dates[0])
                step = 0
                while searching == True:
    #                 st.write(Dates)
    #                 st.write(Dates[elements])
                    day = list(Dates[elements][0])
    #                 st.write(day)
    #                 st.write(step)
    #                 st.write(member)
                    member = day[step]
        #             st.write(member)
                    try:
                        member = int(member)
                        month +=  f'{member}'
                        step += 1
                    except:
                        searching = False
                        if float(month) == 12 or float(month) < 3:
                            event_point = winter
                        elif float(month) > 2 and float(month) < 6:
                            event_point = spring
                        elif float(month) > 5 and float(month) < 9:
                            event_point = summer                 
                        elif float(month) > 8 and float(month) < 12:
                            event_point = fall                 
            elif season_delineation == 'A':
                # st.write(Dates[0])
                step = 0
                while searching == True:
    #                 st.write(Dates[elements])
                    day = list(Dates[elements][0])
        #             st.write(day)
                    member = day[step]
        #             st.write(member)
                    try:
                        member = int(member)
                        month +=  f'{member}'
                        step += 1
                    except:
                        searching = False
                        if float(month) < 4:
                            event_point = winter
                        elif float(month) > 3 and float(month) < 7:
                            event_point = spring
                        elif float(month) > 6 and float(month) < 10:
                            event_point = summer
                        elif float(month) > 9:
                            event_point = fall
            
    #         st.write(f'you have passed there emeka {event_point}')
            last_slope = -1
            if event_occuring and elements >= len(events):
                truncated_list = Discharge[elements:]
                section_dates = Dates[elements:]
                changing_flow = percentage_discharge_change[elements:]
                ## this part sections the whole data at event point and works on it until the event ends
                for elements1 in range(0, len(truncated_list)):
    #                 the part logs the event
                    if event_occuring:
                        if truncated_list[elements1] > event_point:
                            event_ends = 0
                            if elements1 > 0:
                                if changing_flow[elements1] == 'no flow':
                                    changing_flow[elements1] = 0.0000000001
                                if changing_flow[elements1] < 0:
                                    events.append(truncated_list[elements1])
                                    event_dates.append(section_dates[elements1])
                                    last_slope = changing_flow[elements1]
                                    baseflow.append('')
                                else:
                                    if last_slope < 0:
                                        high_compound += 1
                                        events.append(truncated_list[elements1])
                                        event_dates.append(section_dates[elements1])
                                        last_slope = changing_flow[elements1]
                                        baseflow.append('')
                                    else:
                                        events.append(truncated_list[elements1])
                                        event_dates.append(section_dates[elements1])
                                        last_slope = changing_flow[elements1]
                                        baseflow.append('')
                            else:
                                event_ends = 0
                                events.append(truncated_list[elements1])
                                event_dates.append(section_dates[elements1])
                                baseflow.append('')
    #                         the part chech if the event is ended and if base flow as begun
                        else:                        
                            event_ends += 1
                            if event_ends < 2:
                                events.append(truncated_list[elements1])
                                event_dates.append(section_dates[elements1])
                                drop_1 = truncated_list[elements1]
                                baseflow.append('')
                            #this part checks if a compount event begins after reaching baseflow treshold
                            else:
                                if truncated_list[elements1] <= drop_1:
                                    baseflow.append(truncated_list[elements1])
                                    baseflow_dates.append(section_dates[elements1])
                                    event_occuring = False
                                    switch = True
                                    event_endpoint = elements1
                                    events.append('')
                                else:
    #                             This part check if it is a slight bump, is significant to creat compound event
                                    if truncated_list[elements1] <= event_point:
                                        baseflow.append(truncated_list[elements1])
                                        baseflow_dates.append(section_dates[elements1])
                                        events.append('')
                                        event_occuring = False
                                        switch = True
                                        event_endpoint = elements1
                                    else:
                                        base_compound += 1
                                        events.append(truncated_list[elements1])
                                        event_dates.append(section_dates[elements1])
                                        baseflow.append('')
            else:
                if len(events) > 0 and len(events) >= packer and switch == True:
                    catch_no += 1
                    event_bunch.append(events)
                    packer = len(events)
                    caught_events[f'{catch_no} event '] = f'{event_dates[0]} - {event_dates[-1]}'
                    switch = False
                    if high_compound > 1:
                        if base_compound > 1:
                            combine_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
                        else:
                            high_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
                    elif base_compound > 1:
                        low_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
                        
                if elements >= len(events):
                    if Discharge[elements] >= event_point:
                        event_ends = 0
                        event_dates = []
                        event_occuring = True
                        if event_occuring and elements >= len(events):
                            truncated_list = Discharge[elements:]
                            section_dates = Dates[elements:]
                            changing_flow = percentage_discharge_change[elements:]
                            ## this part sections the whole data at event point and works on it until the event ends
                            for elements1 in range(0, len(truncated_list)):
                #                 the part logs the event
                                if event_occuring:
                                    if truncated_list[elements1] > event_point:
                                        event_ends = 0
                                        if elements1 > 0:
                                            if changing_flow[elements1] == 'no flow':
                                                changing_flow[elements1] = 0.0000000001
                                            if changing_flow[elements1] < 0:
                                                events.append(truncated_list[elements1])
                                                event_dates.append(section_dates[elements1])
                                                last_slope = changing_flow[elements1]
                                                baseflow.append('')
                                            else:
                                                if last_slope < 0:
                                                    high_compound += 1
                                                    events.append(truncated_list[elements1])
                                                    event_dates.append(section_dates[elements1])
                                                    last_slope = changing_flow[elements1]
                                                    baseflow.append('')
                                                else:
                                                    events.append(truncated_list[elements1])
                                                    event_dates.append(section_dates[elements1])
                                                    last_slope = changing_flow[elements1]
                                                    baseflow.append('')
                                        else:
                                            event_ends = 0
                                            events.append(truncated_list[elements1])
                                            event_dates.append(section_dates[elements1])
                                            baseflow.append('')
                #                         the part chech if the event is ended and if base flow as begun
                                    else:                           
                                        event_ends += 1
                                        if event_ends < 2:
                                            events.append(truncated_list[elements1])
                                            event_dates.append(section_dates[elements1])
                                            drop_1 = truncated_list[elements1]
                                            baseflow.append('')
                                        #this part checks if a compount event begins after reaching baseflow treshold
                                        else:
                                            if truncated_list[elements1] <= drop_1:
                                                baseflow.append(truncated_list[elements1])
                                                baseflow_dates.append(section_dates[elements1])
                                                event_occuring = False
                                                switch = True
                                                event_endpoint = elements1
                                                events.append('')
                                            else:
                #                             This part check if it is a slight bump, is significant to creat compound event
                                                if truncated_list[elements1] <= event_point:
                                                    baseflow.append(truncated_list[elements1])
                                                    baseflow_dates.append(section_dates[elements1])
                                                    events.append('')
                                                    event_occuring = False
                                                    switch = True
                                                    event_endpoint = elements1
                                                else:
                                                    base_compound += 1
                                                    events.append(truncated_list[elements1])
                                                    event_dates.append(section_dates[elements1])
                                                    baseflow.append('')
                        else:
                            if len(events) > 0 and len(events) >= packer and switch == True:
                                catch_no += 1
                                event_bunch.append(events)
                                packer = len(events)
                                caught_events[f'{catch_no} event '] = f'{event_dates[0]} - {event_dates[-1]}'
                                switch = False
                                if high_compound > 1:
                                    if base_compound > 1:
                                        combine_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
                                    else:
                                        high_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
                                elif base_compound > 1:
                                    low_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
            
                    else:
                        baseflow.append(Discharge[elements])
                        baseflow_dates.append(Dates[elements])
                        events.append('')                        
        
        
        
        valid_drop = mean_jump 
        pack = 0
        blocks = 0
        pairs = 1
        event_kickout = []
        for elements in range(0,len(events)):
            if type(events[elements]) == float:
                pack += 1
            elif elements > pack - 1 and pack > 0 and pack < 3:
                look_max = []
                blocks += 1
                reductions = 0
                for members in range (0, pack):
                    look_max.append(events[elements - pack])
                    pairs += 1
    #             st.write(look_max)
                max_look = max(look_max)
    #             st.write(max_look)
    #             st.write(look_max)
    #             st.write(type(max_look))
                if max_look < 1.25 * event_point:
                    event_kickout.append(f'{blocks} event ')
                    for kit in range (0, pack):
                        events[elements - 1 - pack + reductions] = ''
                        reductions += 1
                pack = 0
            else:
                if pack > 0:
                    blocks += 1
                pack = 0
                
        # st.write(f'blocks (representing the amount of events left) = {blocks}')
    #     st.write(f'These are the event kickout - {event_kickout}')
        for elements in range(0, len(event_kickout)):
            del caught_events[event_kickout[elements]]
        
        
        # st.write('These are the modified events')
        
        # numbering = 0
        # for elements in caught_events:
        #     numbering += 1
        #     if elements != f'{numbering} event ':
        #         caught_events[f'{numbering} event '] = caught_events.pop(elements)
        #     st.write(caught_events[elements])

        # st.write('\n')
        # st.header('These are the Caught events')
        # st.write(caught_events)
        # st.write(len(caught_events))
        # st.write('\n')
        # st.write(f'There are {len(caught_events)} events')
        # st.write('\n')
        
        for elements in range (0, len(events)):
            if type(events[elements]) == float:
                if elements > 0 and events[elements] > valid_drop:
                    events[elements - 1] = Discharge[elements - 1]
                    
        file_name = "Daily_flow_event_data.txt"
            # Write to file (small predicted data)
        with open(file_name, "w") as file:
            for number in events:
                file.write(f"{number}\n")
        st.write(f"Numbers successfully written to {file_name}")
                
        
        y2 = events
        y1 = Discharge
        
        x = []
        for elements in range(0, len(y1)):
            x.append(Dates[elements][0])

        # Convert empty strings to np.nan and the rest to float for y2
        y2_clean = [float(val) if val != '' else np.nan for val in y2]

        # Create stacked subplots with shared x-axis
        fig, axs = plt.subplots(2, 1, figsize=(6, 6), sharex=True)

        # First plot (y1)
        axs[0].plot(x, y1, marker='', color='green')
        axs[0].set_title('Plot of Discharge Data')
        axs[0].set_ylabel('Drainage (cm or mm)')
        axs[0].grid(False)

        # Second plot (y2 with missing)
        axs[1].plot(x, y2_clean, marker='', linestyle='-', color='blue')
        axs[1].set_title('Plot of Events')
        axs[1].set_xlabel('Dates')
        axs[1].set_ylabel('Drainage (cm or mm)')
        axs[1].grid(False)
        points = 30
        if len(x) < points:
            points = len(x)
        axs[1].xaxis.set_major_locator(plt.MaxNLocator(nbins=points))
        fig.autofmt_xdate(rotation=45)

        # Optional: Set same y-axis limits (uncomment if needed)
        y_min = min(min(y1, default=np.nan), min(y2_clean, default=np.nan))
        y_max = max(max(y1, default=np.nan), max(y2_clean, default=np.nan))
        if not np.isnan(y_min) and not np.isnan(y_max):
            axs[0].set_ylim(y_min, y_max)
            axs[1].set_ylim(y_min, y_max)

        # Adjust layout and show
        plt.tight_layout()
        # plt.show()
        st.pyplot(plt)

        
        for elements in range(0, len(Discharge)):
            if type(events[elements]) == float and type(baseflow[elements]) == float:
                baseflow[elements] = ''
            elif type(events[elements]) == str and type(baseflow[elements]) == str and Discharge[elements] > 0:
                baseflow[elements] = Discharge[elements]
        
        file_name = "Daily_flow_base_data.txt"
            # Write to file (small predicted data)
        with open(file_name, "w") as file:
            for number in baseflow:
                file.write(f"{number}\n")
        st.write(f"Numbers successfully written to {file_name}")
        
        st.write('\n Flow weighted Concentration for event\n')
        
        start_date = False
        end_date = False
        hit = 0
        full_hit = 0
        flow_weighted_concentration = []
        label = 0
        average_water_table_depth = []
        average_water_table_temp = []
        # st.write(caught_events)
        
        for key in caught_events:
            label += 1
            good_break_point = False
    #         st.write(list(caught_events[key]))
            matcher = list(caught_events[key])
            matcher = [item for item in matcher if item != '[']
            matcher = [item for item in matcher if item != ']']
            matcher = [item for item in matcher if item != "'"]
    #         st.write(f'This is the matcher {matcher}')
            for elementss in range(0, len(Dates)):
    #             st.write(elementss)
                if good_break_point == True:
                    break
                if start_date == False:
                    mini_conc = []
                    mini_flow = []
                    mini_table = []
                    mini_temp = []
                    plucks = 0
                    plucks1 = 0
                    starter = list(Dates[elementss][0])
                    hit = 0
                    for elements in range(0, len(starter)):
    #                     st.write(f'This is the starter elements {starter[elements]}')
                        if starter[elements] == matcher[elements]:
                            hit += 1
                        if hit == len(starter):
                            start_date = True
                            starter.append(' ')
                            starter.append('-')
                            starter.append(' ')
                            half_band = starter
                            mini_conc.append(concentration[elementss])
                            mini_flow.append(events[elementss])
                            if water_table == 'Yes':
                                mini_table.append(water_level[elementss])
                                plucks += 1
                                
                            if water_temp == 'Yes':
                                mini_temp.append(water_chill[elementss])
                                plucks1 += 1
                else:
                    full_band_unsure = []
                    for elemennt in (half_band):
                        full_band_unsure.append(elemennt)
    #                 st.write('This is the static half band')
    #                 st.write(half_band)
                    ender = list(Dates[elementss][0])
                    hit = 0
                    for elements in ender:
                        full_band_unsure.append(elements)
                    for elements in range(0, len(full_band_unsure)):
                        if full_band_unsure[elements] == matcher[elements]:
                            hit += 1
                        if hit == len(full_band_unsure):
    #                         st.write('I got the full hit')
    #                         st.write(full_band_unsure)
                            full_hit += 1
                            start_date = False
                            good_break_point = True
                    mini_conc.append(concentration[elementss])
                    mini_flow.append(events[elementss])
                    if water_table == 'Yes':
                        mini_table.append(water_level[elementss])
                        plucks += 1
                        
                    if water_temp == 'Yes':
                        mini_temp.append(water_chill[elementss])
                        plucks1 += 1
                        
                    if start_date == False:
                        conc_flow_sum = 0
                        flow_sum = 0
                        level_sum = 0
                        temp_sum = 0
                        for elements in range(0, len(mini_conc)):
                            try:
                                y = float(mini_conc[elements])
                                b = float(mini_flow[elements])
                                
                                if water_table == 'Yes':
                                    level = float(mini_table[elements])
                                    
                                if water_temp == 'Yes':
                                    temp = float(mini_temp[elements])
                                    
                                if y > 0:
                                    conc_flow_sum += (float(mini_conc[elements] * float(mini_flow[elements])))
                                    flow_sum += float(mini_flow[elements])
                                    
                                if water_table == 'Yes':
                                    if level > 0:
                                        level_sum += float(mini_table[elements])
                                        
                                if water_temp == 'Yes':
                                    if temp > 0:
                                        temp_sum += float(mini_temp[elements])
                                        
                            except:
                                toool = 'not usable becuase is it a string'
                        if flow_sum == 0:
                            st.write('Make sure all of your flow has corresponding concentrations or input \'1\' in concentration column')
                            st.stop()
                            # flow_sum = 1
                        F_W_C = conc_flow_sum / flow_sum    
                        flow_weighted_concentration.append(f'{label}_event - {F_W_C}')
                        
                        if water_table == 'Yes':
                            A_W_T_D = level_sum/plucks
                            average_water_table_depth.append(f'{label}_event - {A_W_T_D}')
                        
                        if water_temp == 'Yes':
                            A_W_T_T = temp_sum/plucks1
                            average_water_table_temp.append(f'{label}_event - {A_W_T_T}')


        
        st.download_button(label='Download Daily Event data.txt', data=open('Daily_flow_event_data.txt', 'rb'), file_name='Daily Event data.txt')
        st.download_button(label='Download Base Data.txt', data=open('Daily_flow_base_data.txt', 'rb'), file_name='Base Flow data.txt')
        # st.download_button(label='Download Full Base Data.txt', data=open('Daily_flow_base_full_data.txt', 'rb'), file_name='Full Base Flow data.txt')
        buffer = BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)

        # Create download button
        # st.download_button(
        #     label="Download Daily Event Plot",
        #     data=buffer,
        #     file_name="daily_discharge_events_plot.png",
        #     mime="image/png"
        # )

        # Close the figure to free memory
        plt.close(fig)

        refined_base = []
        for elements in baseflow:
            refined_base.append(elements)
            
        # print('\n')
#         print(refined_base)
#         print('\n')
        
        eventing = False
        for elements in range (1, len(events)):
            if events[elements] != '':
                if events[elements - 1] == '':
                    eventing = True
                    refined_base[elements] = events[elements]
            else:
                if events[elements - 1] != '':
                    eventing = False
                    refined_base[elements - 1] = events[elements - 1]
        
#         print(events)
#         print(refined_base)

        no_data = True

        for elements in range(0, len(refined_base)):
            if refined_base[elements] == '' and no_data == True:
                a = 'keep_searching'
            else:
                no_data = False
                if refined_base[elements] == '':
                    boarder = False
                    steps = 1
                    span = 0
                    jump = 0
                    while boarder == False:
                        nex = elements + steps
                        if nex != len(refined_base):
                            if refined_base[nex] != '':
                                boarder = True
                                span = refined_base[nex] - refined_base[elements - 1]
                                jump = span/(steps + 1)
                                pair1 = 0
                                pair2 = 1
                                for element in range (0, steps):
                                    refined_base[elements - 1 + pair2] = refined_base[elements - 1 + pair1] + jump
                                    pair1 += 1
                                    pair2 += 1
        #                             print(refined_base)
        #                             print('\n')
                            else:
                                steps += 1
                        else:
                            break
        

        for elements in range(0, len(events)):
            if events[elements] != '' and refined_base[elements] != '':
                if refined_base[elements] > events[elements]:
                    refined_base[elements] = events[elements]

        # print(refined_base)
        off_colony = []
        colony = 0
        passes = 0
        door = 0
        single_colony = False
        for elements in range(0, len(events)):
            if events[elements] == '' and elements > 0:
                door += 1
                if colony == 1:
                    single_colony = True
                elif colony > 1:
                    passes += 1
                    colony = 0
            else:
                if colony == 1 and door == 1:
                    off_colony.append(passes + 1)
                colony += 1
                door = 0
        
        # print('This is the off colony')
        # print(off_colony)

        start_off = False
        first_base = 0
        parse = 0
        for elemen in range(0, len(refined_base)):
            if refined_base[elemen] == '':
                start_off = True
            elif start_off == True and parse == 0:
                first_base = refined_base[elemen]
                parse += 1
            
        if start_off == True:
            for elements in range(0, len(refined_base)):
                if refined_base[elements] == '':
                    refined_base[elements] = first_base
#         print(refined_base)

        sides = []
        hold_trapezoid = []
        flow_vol = 0
        event_vols = []
        too_low = False
        eventon = False
        for elements in range(0, len(events)):
            if events[0] == '':
                if elements > 1:
                    if events[elements] != '':
                        if events[elements - 1] != '':
                            eventon = True
                    
                    elif events[elements - 1] != '':
                        eventon = False
                        if len(sides) != 0:
                            side = events[elements - 1] - refined_base[elements - 1]
                            sides.append(side)
                            if len(sides) == 2:
                                flow_vol += 0.5 *(sides[0] + sides[1])
                                hold_trapezoid.append(0.5 *(sides[0] + sides[1]))
                        
                        if flow_vol > 0:       
                            event_vols.append(flow_vol)
#                             print(event_vols)
                        sides = []
                        flow_vol = 0
                    
                    if eventon:
                        side = events[elements - 1] - refined_base[elements - 1]
                        sides.append(side)
                        if len(sides) == 2:
                            flow_vol += 0.5 *(sides[0] + sides[1])
                            hold_trapezoid.append(0.5 *(sides[0] + sides[1]))
                            sides.remove(sides[0])
                        
            else:
                if elements > 0:
#                     print(Date)
#                     print(winter)
#                     print(spring)
#                     print(summer)
#                     print(fall)
#                     print('\n')
                    day_list = list(Date[elements])
#                     print(day_list)
                    check_month = f'{day_list[0]}{day_list[1]}'
#                     print(check_month)
                    if season_delineation == 'A':
                        if int(check_month) == 1 or int(check_month) == 2 or int(check_month) == 3:
                            shoulder = winter
                        elif int(check_month) == 4 or int(check_month) == 5 or int(check_month) == 6:
                            shoulder = spring
                        elif int(check_month) == 7 or int(check_month) == 8 or int(check_month) == 9:
                            shoulder = summer
                        else:
                            shoulder = fall
                    else:
                        if int(check_month) == 12 or int(check_month) == 2 or int(check_month) == 1:
                            shoulder = winter
                        elif int(check_month) == 4 or int(check_month) == 5 or int(check_month) == 3:
                            shoulder = spring
                        elif int(check_month) == 7 or int(check_month) == 8 or int(check_month) == 6:
                            shoulder = summer
                        else:
                            shoulder = fall
                            
                    if events[elements] != '':
                        if events[elements - 1] != '':
                            eventon = True
                    if events[elements] != '' and events[elements - 1] != '':
                        if events[elements] < shoulder and events[elements - 1] < shoulder:
                            too_low = True
                            eventon = False
                            if len(sides) != 0:
                                side = events[elements - 1] - refined_base[elements - 1]
                                sides.append(side)
                                if len(sides) == 2:
                                    flow_vol += 0.5 *(sides[0] + sides[1])
                                    hold_trapezoid.append(0.5 *(sides[0] + sides[1]))
                            
                            if flow_vol > 0:       
                                event_vols.append(flow_vol)
    #                             print(event_vols)
                            sides = []
                            flow_vol = 0
                        
                    elif events[elements - 1] != '' and too_low == False:
                        eventon = False
                        if len(sides) != 0:
                            side = events[elements - 1] - refined_base[elements - 1]
                            sides.append(side)
                            if len(sides) == 2:
                                flow_vol += 0.5 *(sides[0] + sides[1])
                                hold_trapezoid.append(0.5 *(sides[0] + sides[1]))
                        
                        if flow_vol > 0:       
                            event_vols.append(flow_vol)
#                             print(event_vols)
                        sides = []
                        flow_vol = 0
                    
                    if eventon:
                        side = events[elements - 1] - refined_base[elements - 1]
                        sides.append(side)
                        if len(sides) == 2:
                            flow_vol += 0.5 *(sides[0] + sides[1])
                            hold_trapezoid.append(0.5 *(sides[0] + sides[1]))
                            sides.remove(sides[0])
                    too_low = False

############################################################################################################################################################################
####################################### tell the singles event point in the data set ####################################################################################         
#         skipped_events = []
#         chain = 0
#         chaining = False
#         block = 0
#         for elements in events:
#             if elements !=  '':
#                 chaining = True
#                 chain += 1
#             elif chaining == True:
#                 block += 1
#                 chaining = False
#                 if chain == 1:
#                     skipped_events.append(block)
#                 chain = 0

# this looks to catch the high and low in aims to split compounded events
#         print(f'This are you unsplited event volumes {event_vols}')
#         season_delineation = 'A'
        
        row = 0
        chain = 0
        chaining = False
        block = 0
        last_high = 0
        half_chain = False
        split_detail = []
        down = False
        for elements in range(0, len(events)):
            if events[elements] !=  '':
                chaining = True
                new = events[elements]
                if new > last_high and down == False:
                    last_high = new
                                
                elif new > last_high and down != False:
                    last_high = events[elements]
                    if season_delineation == 'A':
                        split = list(Date[elements])
                        day = split[0] + split[1]
                        wi = ['01', '02', '03']
                        sp = ['04', '05', '06']
                        su = ['07', '08', '09']
                        fa =  ['10', '11', '12']
                        for ements in wi:
                            if day == ements:
#                                 print('it winter')
                                if events[elements - 1] < winter:
                                    row += 1
                                    if row == 2:
                                        half_chain = True
                                        half = chain - 1
#                                         print(Date[elements - 1])
#                                         print(block)
                        for ements in sp:
                            if day == ements:
#                                 print('it spring')
                                if events[elements - 1] < spring:
                                    row += 1
                                    if row == 2:
                                        half_chain = True
                                        half = chain - 1
#                                         print(Date[elements - 1])
#                                         print(block)
                        for ements in su:
                            if day == ements:
#                                 print('it summer')
                                if events[elements - 1] < summer:
                                    row += 1
                                    if row == 2:
                                        half_chain = True
                                        half = chain - 1
#                                         print(Date[elements - 1])
#                                         print(block)
                        for ements in fa:
                            if day == ements:
#                                 print('it fall')
                                if events[elements - 1] < fall:
                                    row += 1
                                    if row == 2:
                                        half_chain = True
                                        half = chain - 1
#                                         print(Date[elements - 1])
#                                         print(block)
                    else:
                        split = list(Date[elements])
                        day = split[0] + split[1]
                        wi = ['12', '01', '02']
                        sp = ['03', '04', '05']
                        su = ['06', '07', '08']
                        fa =  ['09', '10', '11']
                        for ements in wi:
                            if day == ements:
#                                 print('it winter')
                                if events[elements - 1] < winter:
                                    row += 1
                                    if row == 2:
                                        half_chain = True
                                        half = chain - 1
#                                         print(Date[elements - 1])
#                                         print(block)
                        for ements in sp:
                            if day == ements:
#                                 print('it spring')
                                if events[elements - 1] < spring:
                                    row += 1
                                    if row == 2:
                                        half_chain = True
                                        half = chain - 1
#                                         print(Date[elements - 1])
#                                         print(block)
                        for ements in su:
                            if day == ements:
#                                 print('it summer')
                                if events[elements - 1] < summer:
                                    row += 1
                                    if row == 2:
                                        half_chain = True
                                        half = chain - 1
#                                         print(Date[elements - 1])
#                                         print(block)
                        for ements in fa:
                            if day == ements:
#                                 print('it fall')
                                if events[elements - 1] < fall:
                                    row += 1
                                    if row == 2:
                                        half_chain = True
                                        half = chain - 1
#                                         print(Date[elements - 1])
#                                         print(block)
                    
                else:
                    down = True
                    row = 0
                    last_high = events[elements]
                    
                chain += 1
            elif chaining == True:
                down = False
                last_high = 0
                chaining = False
                if half_chain == True:
                    portion = half/chain
#                     print(portion)
                    split_detail.append(block + portion)
                chain = 0
                half_chain = False
                split_detail.append(block)
                block += 1
#                 print(split_detail)
#         print(f'wave Events - {wave_events}')
        
#         print('split_detail')
#         print(split_detail)
        refine = []
        if len(split_detail) > 0:
            refine.append(0)
        for elements in range (1, len(split_detail)):
            if split_detail[elements] > split_detail[elements - 1]:
                refine.append(split_detail[elements])
        split_detail = refine
        
        
#         print(event_vols)
#         print(len(event_vols))
#         print('split_detail')
#         print(split_detail)
#         print(len(split_detail))
#         print('First look Emeka')
        move = 0
        split_vols = []
                
        while move < len(split_detail) - 1:
            for elements in range(0, len(event_vols)):
                if move < len(split_detail):
                    if elements < float(split_detail[move]):
            #                         print(elements)
                        portion = split_detail[move] - math.floor(split_detail[move])
                        split_vols.append(portion * event_vols[elements])
                        split_vols.append(event_vols[elements] - (portion * event_vols[elements]))
                        move += 1
                        # print('came through')
            #                         print(split_vols)
                                      
                    else:
                        split_vols.append(event_vols[elements])
            #                         print(split_vols)
                        move += 1
                        
                else:
                    split_vols.append(event_vols[elements])
            #                     print(split_vols)
                                      
#         print(event_vols)
#         print(split_vols)
#         print(len(split_vols))
###########################################################################################################################
        # st.write('got here')
        event_trapezoid = []
#         print(hold_trapezoid)
        through = 0
        paired = 0
        for elements in range(0, len(events)):
            if events[elements] == '':
                paired = 0
                event_trapezoid.append(events[elements])
            elif paired > 1 and through < len(hold_trapezoid):
                event_trapezoid.append(hold_trapezoid[through])
                through += 1
            else:
                event_trapezoid.append(0)
                paired += 1
                if elements == 0 and events[0] != '':
                    paired += 1

        st.write('\n')
        st.header('These are the Caught events')
        if len(off_colony) > 0:
            for elements in off_colony:
                key_to_remove = list(caught_events.keys())[elements]
                del caught_events[key_to_remove]

#################################################################################################################################################################################################################
# refininin the way the concentration is presented
        leap = [1904, 1908, 1912, 1916, 1920, 1924, 1928, 1932, 1936, 1940, 1944, 1948, 1952, 1956, 1960, 1964, 1968,
1972, 1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020, 2024, 2028, 2032, 2036,
2040, 2044, 2048, 2052, 2056, 2060, 2064, 2068, 2072, 2076, 2080, 2084, 2088, 2092, 2096, 2104, 2108,
2112, 2116, 2120, 2124, 2128, 2132, 2136, 2140, 2144, 2148, 2152, 2156, 2160, 2164, 2168, 2172, 2176,
2180, 2184, 2188, 2192, 2196, 2204, 2208, 2212, 2216, 2220, 2224, 2228, 2232, 2236, 2240, 2244, 2248,
2252, 2256, 2260, 2264, 2268, 2272, 2276, 2280, 2284, 2288, 2292, 2296, 2304, 2308, 2312, 2316, 2320,
2324, 2328, 2332, 2336, 2340, 2344, 2348, 2352, 2356, 2360, 2364, 2368, 2372, 2376, 2380, 2384, 2388,
2392, 2396, 2400, 2404, 2408, 2412, 2416, 2420, 2424, 2428, 2432, 2436, 2440, 2444, 2448, 2452, 2456,
2460, 2464, 2468, 2472, 2476, 2480, 2484, 2488, 2492, 2496, 2504, 2508, 2512, 2516, 2520, 2524, 2528,
2532, 2536, 2540, 2544, 2548, 2552, 2556, 2560, 2564, 2568, 2572, 2576, 2580, 2584, 2588, 2592, 2596,
2604, 2608, 2612, 2616, 2620, 2624, 2628, 2632, 2636, 2640, 2644, 2648, 2652, 2656, 2660, 2664, 2668,
2672, 2676, 2680, 2684, 2688, 2692, 2696, 2704, 2708, 2712, 2716, 2720, 2724, 2728, 2732, 2736, 2740,
2744, 2748, 2752, 2756, 2760, 2764, 2768, 2772, 2776, 2780, 2784, 2788, 2792, 2796, 2800, 2804, 2808,
2812, 2816, 2820, 2824, 2828, 2832, 2836, 2840, 2844, 2848, 2852, 2856, 2860, 2864, 2868, 2872, 2876,
2880, 2884, 2888, 2892, 2896, 2904, 2908, 2912, 2916, 2920, 2924, 2928, 2932, 2936, 2940, 2944, 2948,
2952, 2956, 2960, 2964, 2968, 2972, 2976, 2980, 2984, 2988, 2992, 2996]

        months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        monthsl = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        span = []
        new_year = False
        for element in caught_events:
            event = (caught_events[element])
            event_list = list(event)
        #     print(event_list)
            start = []
            start1 = ''
            end = []
            end1 = ''
            for elem in range(0, 10):
                start.append(event_list[elem + 2])
                start1 += event_list[elem + 2]
                end.append(event_list[elem + 19])
                end1 += event_list[elem + 19]
                # print(end)
            year = int(f'{start[6]}{start[7]}{start[8]}{start[9]}')
            year1 = int(f'{end[6]}{end[7]}{end[8]}{end[9]}')
            caught_events[element] = f'{start1} - {end1}'
        #     print(year)
            if year == year1:
                inleap = False
                for elements in leap:
                    if year == elements:
                        inleap = True
                day_start = int(f'{start[3]}{start[4]}')
            #     print(day_start)
                month_start = int(f'{start[0]}{start[1]}')
            #     (print(month_start))
                day_end = int(f'{end[3]}{end[4]}')
                month_end = int(f'{end[0]}{end[1]}')
                if month_start > 12:
                    st.write('Make sure Your date is in the format mm/dd/yyyy - currently is not, please corrrect it')
                    st.stop()
            #     print(month_end)
            #     print(day_end)
                ending = 0
                starting = 0
                if inleap == False:
                    for eleme in range(0, month_start):
                        starting += months[eleme]
                    starting += day_start
            #         print(starting)
                    
                    for eleme in range(0, month_end):
                        ending += months[eleme]
                    ending += day_end
            #         print(ending)
                else:
                    for eleme in range(0, month_start):
                        starting += monthsl[eleme]
                    starting += day_start
                    
                    for eleme in range(0, month_end):
                        ending += monthsl[eleme]
                    ending += day_end
                    
                span.append(ending - starting)
            
            else:
                span1 = []
                split_list = {
                    '*1 event ': f"['{start1}'] - ['12/31/{year}']",
                    '*2 event ': f"['01/01/{year1}'] - ['{end1}']"                      
                              }
                for element in split_list:
                    event = (split_list[element])
                    event_list = list(event)
                #     print(event_list)
                    start = []
                    start1 = ''
                    end = []
                    end1 = ''
                    for elem in range(0, 10):
                        start.append(event_list[elem + 2])
                        start1 += event_list[elem + 2]
                        end.append(event_list[elem + 19])
                        end1 += event_list[elem + 19]
                    year = int(f'{start[6]}{start[7]}{start[8]}{start[9]}')
                    year1 = int(f'{end[6]}{end[7]}{end[8]}{end[9]}')
                #     print(year)
                    if year == year1:
                        inleap = False
                        for elements in leap:
                            if year == elements:
                                inleap = True
                        day_start = int(f'{start[3]}{start[4]}')
                    #     print(day_start)
                        month_start = int(f'{start[0]}{start[1]}')
                    #     (print(month_start))
                        day_end = int(f'{end[3]}{end[4]}')
                        month_end = int(f'{end[0]}{end[1]}')
        #                 print('month_end')
        #                 print(month_end)
        #                 print('day_end')
        #                 print(day_end)
                        ending = 0
                        starting = 0
                        if inleap == False:
                            for eleme in range(0, month_start):
                                starting += months[eleme]
                            starting += day_start
                    #         print(starting)
                            
                            for eleme in range(0, month_end):
                                ending += months[eleme]
                            ending += day_end
                    #         print(ending)
                        else:
                            for eleme in range(0, month_start):
                                starting += monthsl[eleme]
                            starting += day_start
                            
                            for eleme in range(0, month_end):
                                ending += monthsl[eleme]
                            ending += day_end
                            
                        span1.append(ending - starting)
                
                totes = 1
                for elementy in span1:
                    totes += elementy
                span.append(totes)
        #         print(totes)
        #         print(split_list)
        #         print(len(split_list))
        #         print(type(split_list))
        #         print(span1)
    
#################################################################################################################################################################################################################

                # print(caught_events)
        with st.expander("📅 Drainage Events"):
            event_dict = caught_events
            # Convert dictionary to a format suitable for dataframe
            events_data = {
                "Event": list(event_dict.keys()),
                "Date-Time Range": list(event_dict.values()),
                "Duration (Days)": span
            }
            st.dataframe(events_data, use_container_width=True)
        # st.write(caught_events)
        st.write(len(caught_events))
        st.write('\n')
        st.write(f'There are {len(caught_events)} events')
        st.write('\n')
        
        if len(split_vols) > len(caught_events):
            if split_vols[len(caught_events) - 1] == 0:
                cut_list = split_vols[:len(caught_events) - 1]
                split_vols = cut_list
        
        under_pass = split_vols
        if len(under_pass) < len(caught_events):
        #             print(events)
            colony = 0
            shreaded = []
            event_bulk = []
            passes = 0
            eventing = False
            batch_load = 0
            under_jump = 0
            for elements in range(0, len(event_trapezoid)):
                if events[elements] != '' and colony >= 1:
                    eventing = True
                    event_bulk.append(event_trapezoid[elements])
        #             print(Date)
                    split = list(Date[elements])
        #             print(split)
                    month = split[0] + split[1]
                    if season_delineation == 'A':                        
                        wi = ['01', '02', '03']
                        sp = ['04', '05', '06']
                        su = ['07', '08', '09']
                        fa =  ['10', '11', '12']
                        for ements in wi:
                            if month == ements:
                                if events[elements] < winter:
                                    colony += 1
                                    under_jump += 1
                                    if under_jump == 2:
                                        shreaded.append(sum(event_bulk) - event_trapezoid[elements])
                                        passes += 1
                                        under_jump = 0
                                        event_bulk = []
                                        colony = 1
                                        event_bulk.append(event_trapezoid[elements])
        #                                         print(passes)
                                else:
                                    under_jump = 0
                                    colony += 1
                                                
                        for ements in sp:
                            if month == ements:
                                if events[elements] < summer:
                                    colony += 1
                                    under_jump += 1
                                    if under_jump == 2:
                                        shreaded.append(sum(event_bulk) - event_trapezoid[elements])
                                        passes += 1
                                        under_jump = 0
                                        event_bulk = []
                                        colony = 1
                                        event_bulk.append(event_trapezoid[elements])
        #                                         print(passes)
                                else:
                                    under_jump = 0
                                    colony += 1
                                                
                        for ements in su:
                            if month == ements:
                                if events[elements] < spring:
                                    colony += 1
                                    under_jump += 1
                                    if under_jump == 2:
                                        shreaded.append(sum(event_bulk) - event_trapezoid[elements])
                                        passes += 1
                                        under_jump = 0
                                        event_bulk = []
                                        colony = 1
                                        event_bulk.append(event_trapezoid[elements])
        #                                         print(passes)
                                else:
                                    under_jump = 0
                                    colony += 1
                                                
                        for ements in fa:
                            if month == ements:
                                if events[elements] < fall:
                                    colony += 1
                                    under_jump += 1
                                    if under_jump == 2:
                                        shreaded.append(sum(event_bulk) - event_trapezoid[elements])
                                        passes += 1
                                        under_jump = 0
                                        event_bulk = []
                                        colony = 1
                                        event_bulk.append(event_trapezoid[elements])
        #                                         print(passes)
                                else:
                                    under_jump = 0
                                    colony += 1
                                                
                    else:
                        wi = ['12', '01', '02']
                        sp = ['03', '04', '05']
                        su = ['06', '07', '08']
                        fa =  ['09', '10', '11']
                        for ements in wi:
                            if month == ements:
                                if events[elements] < winter:
                                    colony += 1
                                    under_jump += 1
                                    if under_jump == 2:
                                        shreaded.append(sum(event_bulk) - event_trapezoid[elements])
                                        passes += 1
                                        under_jump = 0
                                        event_bulk = []
                                        colony = 1
                                        event_bulk.append(event_trapezoid[elements])
        #                                         print(passes)
                                else:
                                    under_jump = 0
                                    colony += 1
                                                
                        for ements in sp:
                            if month == ements:
                                if events[elements] < spring:
                                    colony += 1
                                    under_jump += 1
                                    if under_jump == 2:
                                        shreaded.append(sum(event_bulk) - event_trapezoid[elements])
                                        passes += 1
                                        under_jump = 0
                                        event_bulk = []
                                        colony = 1
                                        event_bulk.append(event_trapezoid[elements])
        #                                         print(passes)
                                else:
                                    under_jump = 0
                                    colony += 1
                                                
                        for ements in su:
                            if month == ements:
                                if events[elements] < summer:
                                    colony += 1
                                    under_jump += 1
                                    if under_jump == 2:
                                        shreaded.append(sum(event_bulk) - event_trapezoid[elements])
                                        passes += 1
                                        under_jump = 0
                                        event_bulk = []
                                        colony = 1
                                        event_bulk.append(event_trapezoid[elements])
        #                                         print(passes)
                                else:
                                    under_jump = 0
                                    colony += 1
                                                
                        for ements in fa:
                            if month == ements:
                                if events[elements] < fall:
                                    colony += 1
                                    under_jump += 1
                                    if under_jump == 2:
                                        shreaded.append(sum(event_bulk) - event_trapezoid[elements])
                                        passes += 1
                                        under_jump = 0
                                        event_bulk = []
                                        colony = 1
                                        event_bulk.append(event_trapezoid[elements])
        #                                         print(passes)
                                else:
                                    under_jump = 0
                                    colony += 1
                                                                    
                    
                elif events[elements] != '' and colony < 2:
                    colony += 1
                    event_bulk.append(event_trapezoid[elements])
                elif events[elements] == '' or eventing == True:
                    colony = 0
                    eventing = False
                    if len(event_bulk) > 1:
                        shreaded.append(sum(event_bulk))
                        passes += 1
#                         print(event_bulk)
#                         print(passes)
                    event_bulk = []
                
            split_vols = shreaded

        st.write('These are the daily discharge volumes per event (Flow Units * Area Units)')
        field_vol = []
        passes = 0
        # st.write('split_vols')
        # st.write(split_vols)
        for elements in split_vols:
            passes += 1
            field_vol.append(f'Event-{passes} - {field_area * elements}')
        
        field_vol1 = []   
        if len(off_colony) > 0 or len(field_vol) > len(caught_events):
            for element in range(0, len(caught_events)):
                field_vol1.append(field_vol[element])
        
        if len(off_colony) > 0 or len(field_vol) > len(caught_events):
             # st.write(field_vol1)
            with st.expander("📈 field_vol1"):
                event_list = field_vol1
                events_data = {
                "Event": [event.split(" - ")[0] for event in event_list],
                "Value": [float(event.split(" - ")[1]) for event in event_list]
                }
            st.dataframe(events_data, use_container_width=True)
            st.write(len(field_vol1))
        else:
            with st.expander("📈 field_vol"):
                event_list = field_vol
                events_data = {
                "Event": [event.split(" - ")[0] for event in event_list],
                "Value": [float(event.split(" - ")[1]) for event in event_list]
                }
            st.dataframe(events_data, use_container_width=True)
            st.write(len(field_vol))
#         print(split_vols)
#         print(split_vols)
    #     st.write(full_hit)
        st.write('\n')
        # st.write('got here')
        # print(flow_weighted_concentration)
        for elements in flow_weighted_concentration:
            y = list(elements)
        st.write('The flow weighted concentration for the events are:')
        if len(off_colony) > 0:
            for elements in off_colony:
                flow_weighted_concentration.remove(flow_weighted_concentration[elements])
        
        conc_teller = []
        for elements in flow_weighted_concentration:
            y = list(elements)
            number = float(f'{y[len(y) - 3]}{y[len(y) - 2]}{y[len(y) - 1]}')
            conc_teller.append(number)
            # print(conc_teller)
        mode_conc = max(set(conc_teller), key=conc_teller.count)
        if mode_conc == 1.0:
            st.markdown(
                    "<p style='color:red; font-weight:bold;'>"
                    "Warning: The concentration shown here may not represent the actual concentration because the cell was likely populated with placeholder values of 1."
                    "</p>",
                    unsafe_allow_html=True
                )
            with st.expander("📈 flow_weighted_concentration"):
                event_list = flow_weighted_concentration
                events_data = {
                "Event": [event.split(" - ")[0] for event in event_list],
                "Value": [float(event.split(" - ")[1]) for event in event_list]
                }
        else:
            with st.expander("📈 flow_weighted_concentration"):
                event_list = flow_weighted_concentration
                events_data = {
                "Event": [event.split(" - ")[0] for event in event_list],
                "Value": [float(event.split(" - ")[1]) for event in event_list]
                }
        st.dataframe(events_data, use_container_width=True)
        st.write(len(flow_weighted_concentration))
        
        if water_table == 'Yes':
            st.write('\n')
            st.write('These are the average water table depths for the events')
            if len(off_colony) > 0:
                for elements in off_colony:
                    average_water_table_depth.remove(average_water_table_depth[elements])
            with st.expander("📈 average_water_table_depth"):
                event_list = average_water_table_depth
                events_data = {
                "Event": [event.split(" - ")[0] for event in event_list],
                "Value": [float(event.split(" - ")[1]) for event in event_list]
            }
            st.dataframe(events_data, use_container_width=True)
            st.write(len(average_water_table_depth))
            
        if water_temp == 'Yes':
            st.write('\n')
            st.write('These are the average water temperatures for the events')
            if len(off_colony) > 0:
                for elements in off_colony:
                    average_water_table_temp.remove(average_water_table_temp[elements])
            with st.expander("📈 Average Water Table Temperature"):
                event_list = average_water_table_temp
                events_data = {
                "Event": [event.split(" - ")[0] for event in event_list],
                "Value": [float(event.split(" - ")[1]) for event in event_list]
            }
            st.dataframe(events_data, use_container_width=True)
            st.write(len(average_water_table_temp))


        file_name = "Daily_flow_base_full_data.txt"
            # Write to file (small predicted data)
        with open(file_name, "w") as file:
            for number in refined_base:
                file.write(f"{number}\n")
        st.write(f"Numbers successfully written to {file_name}")

        st.download_button(label='Download Full Base Data.txt', data=open('Daily_flow_base_full_data.txt', 'rb'), file_name='Full Base Flow data.txt')

        st.download_button(
            label="Download Daily Event Plot",
            data=buffer,
            file_name="daily_discharge_events_plot.png",
            mime="image/png"
        )
##################################################################################################################################################################################################################################
        # Convert data to numpy arrays, replacing '' with np.nan
        events = np.array([float(x) if x != '' else np.nan for x in events])
        base_flow = np.array([float(x) if x != '' else np.nan for x in refined_base])

        # Create time index
        x = np.arange(1, len(events) + 1)

        # Interpolate base flow to fill gaps for continuous shading
        # Get indices where base_flow is not NaN
        valid_indices = np.where(~np.isnan(base_flow))[0]
        valid_values = base_flow[valid_indices]
        # Interpolate over all indices
        base_flow_interpolated = np.interp(x - 1, valid_indices, valid_values)

        # Create the plot
        plt.figure(figsize=(12, 6))
        
        plt.plot(x, events, color='red', linewidth=2, label='Event Flow')

        # Plot base flow with continuous blue shading
        plt.fill_between(x, base_flow_interpolated, color='blue', alpha=0.3, label='Base Flow')
        # Plot original base flow points with black trace (only where data exists)
#         plt.plot(x, base_flow, color='black', linewidth=2, linestyle='dotted', label='_Base Flow Trace')
        plt.plot(x, base_flow, color='black', linewidth=2, linestyle=':', label='_Base Flow Trace')  # Hidden label

        # Plot event flow with red trace

        # Customize the plot
        plt.xlabel('Time Index')
        plt.ylabel('Flow')
        plt.title('Event and Base Flow Trends')
        plt.legend()
        plt.grid(True, linestyle=':')

        # Show the plot
        plt.tight_layout()
        plt.show()
        st.pyplot(plt)


        os.remove("temp.csv")


#################################################################################################################################################################################################################################    
#################################################################################################################################################################################################################################
#################################################################################################################################################################################################################################    
#################################################################################################################################################################################################################################
#################################################################################################################################################################################################################################    
#################################################################################################################################################################################################################################
#################################################################################################################################################################################################################################    
#################################################################################################################################################################################################################################
#################################################################################################################################################################################################################################    
#################################################################################################################################################################################################################################
#################################################################################################################################################################################################################################    
#################################################################################################################################################################################################################################
#################################################################################################################################################################################################################################    
#################################################################################################################################################################################################################################
#################################################################################################################################################################################################################################    
#################################################################################################################################################################################################################################
#################################################################################################################################################################################################################################    
#################################################################################################################################################################################################################################
#################################################################################################################################################################################################################################    
#################################################################################################################################################################################################################################


def hourly_events(data_file, heading, water_table, water_temp, winterr, springg, summerr, falll, season_deli, field_area):

##############################################################################################################################################################
##############################################################################################################################################################
##############################################################################################################################################################                
# You can reset the values by either deleting the run_metadata.json file or using the reset button or manually setting the values int the run_metadata.json file.

        # S3 bucket and file details
    bucket_name = 'runmetadata.json'
    file_key = 'runmetadatafile.json'

    def read_json_from_s3(display=False):
        """Read JSON from S3 and optionally display the content in a single-column dashboard layout."""
        try:
            # Retrieve AWS credentials from Streamlit secrets
            aws_access_key_id = st.secrets["AWS_ACCESS_KEY_ID"]
            aws_secret_access_key = st.secrets["AWS_SECRET_ACCESS_KEY"]
            aws_region = st.secrets.get("AWS_DEFAULT_REGION", "us-east-1")  # Default to us-east-1 if not provided

            # Initialize the S3 client with the credentials
            s3_client = boto3.client(
                's3',
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=aws_region
            )

            # Read the file from S3
            response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
            # Read the content and decode it
            file_content = response['Body'].read().decode('utf-8')
            # Parse JSON content
            json_content = json.loads(file_content)
            
            return json_content
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                st.write(f"File {file_key} not found in bucket {bucket_name}")
            else:
                st.write(f"Error reading from S3: {e}")
            return None
        except json.JSONDecodeError as e:
            st.write(f"Error decoding JSON: {e}")
            return None
        except KeyError as e:
            st.error(f"Missing AWS credentials in Streamlit secrets: {e}")
            return None

    def write_json_to_s3(data, display=False):
        """Write JSON to S3 and optionally display the written content."""
        try:
            # Retrieve AWS credentials from Streamlit secrets
            aws_access_key_id = st.secrets["AWS_ACCESS_KEY_ID"]
            aws_secret_access_key = st.secrets["AWS_SECRET_ACCESS_KEY"]
            aws_region = st.secrets.get("AWS_DEFAULT_REGION", "us-east-1")  # Default to us-east-1 if not provided

            # Initialize the S3 client with the credentials
            s3_client = boto3.client(
                's3',###
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=aws_region
            )

            # Convert data to JSON string
            json_content = json.dumps(data, indent=2)
            # Write the file to S3
            s3_client.put_object(
                Bucket=bucket_name,
                Key=file_key,
                Body=json_content.encode('utf-8'),
                ContentType='application/json'
            )
            # if display:
            #     st.write("Updated file content:", data)
            #     st.write(f"Successfully wrote to {file_key} in bucket {bucket_name}")
        except ClientError as e:
            st.write(f"Error writing to S3: {e}")
        except Exception as e:
            st.write(f"Error: {e}")

    def update_selected_fields(prev_data, fields_to_increment):
        """Update only the specified fields by incrementing their values by 1."""
        updated_data = prev_data.copy()
        updated_data["timestamp"] = datetime.now().isoformat()
        
        for field in fields_to_increment:
            if field in updated_data and isinstance(updated_data[field], (int, float)):
                updated_data[field] += 1
            else:
                st.write(f"Warning: Field {field} not found or not numeric, skipping.")
        
        return updated_data
###############################################################################################################################################################
    # Example usage - This is the writer
    if __name__ == "__main__":
        # Read and display the current file content in dashboard layout
        content = read_json_from_s3(display=True)
        
        if content:
            # Specify which fields to increment
            fields_to_increment = [
                "Total_Analysis_Performed",
                "Hourly_Data_Analysis",
                # "Daily_Data_Analysis",
                # "Seasonal_Delineation_Method_A",
                # "Seasonal_Delineation_Method_B"
            ]
            
            # Update selected fields
            updated_data = update_selected_fields(content, fields_to_increment)
            
            # Write and display the updated content
            write_json_to_s3(updated_data, display=True)
        else:
            # If no file exists, create new data
            new_data = {
                "timestamp": datetime.now().isoformat(),
                "Total_Analysis_Performed": 4,
                "Seasonal_Delineation_Method_A": 2,
                "Seasonal_Delineation_Method_B": 2,
                "Daily_Data_Analysis": 2,
                "Hourly_Data_Analysis": 2
            }
            st.write("No file found. Creating new file with default data.")
            write_json_to_s3(new_data, display=True)
###############################################################################################################################################################

#############################################################################################################################################################
############################################################################################################################################################# 



    df = pd.read_csv(data_file)
    st.write('\n')
    st.write('This is the first 50 lines')
    st.write('\n')
    st.write(df.head(51))
    st.write('\n')
    
    Date = []
    Discharge = []
    concentration = []
    with open(data_file, 'r', newline='') as file:
        reader = csv.reader(file)
        valid = 1
        valid_used = False
        instate = 0
        for row in reader:
            if row[0] == '':
                if instate == 0:
                    instate = valid
                elif valid > instate:
                    st.write(f'You have a missing date on line {instate} - Kindly check line {instate} on your csv file')
                    valid_used = True
                    break
            else:
                valid += 1
                Date.append(row[0])
                if row[1] == '':
                    Discharge.append(0.0)
                else:
                    Discharge.append((row[1]))
                    
                if row[2] == '':
                    concentration.append(0.0)
                else:
                    concentration.append((row[2]))
    if valid_used == False:
        if water_table == 'Yes':
            water_level = []
            with open(data_file, 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == '':
                        break
                    else:
                        if row[3] == '':
                            water_level.append(0.0)
                        else:
                            water_level.append((row[3]))

        st.write('\n')
        if water_temp == 'Yes':
            water_chill = []
            with open(data_file, 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == '':
                        break
                    else:
                        if row[4] == '':
                            water_chill.append(0.0)
                        else:
                            water_chill.append((row[4]))
                    
        st.write('\n')
        if heading == 'Yes':
            Date.remove(Date[0])
            Discharge.remove(Discharge[0])
            concentration.remove(concentration[0])
            if water_table == 'Yes':
                water_level.remove(water_level[0])
            if water_temp == 'Yes':
                water_chill.remove(water_chill[0])
            
    #         st.write(Date)
            for elements in range(0, len(Discharge)):
                Discharge[elements] = float(Discharge[elements])
                concentration[elements] = float(concentration[elements])
                if water_table == 'Yes':
                    water_level[elements] = float(water_level[elements])
                if water_temp == 'Yes':
                    water_chill[elements] = float(water_chill[elements])
                    
            Dates = []
            for elements in Date:
                spliter = []
                collector = ''
                y = list(elements)
                for elem in y:
                    collector += elem
                spliter.append(collector)
                Dates.append(spliter)
        else:
            for elements in range(0, len(Discharge)):
                Discharge[elements] = float(Discharge[elements])
                concentration[elements] = float(concentration[elements])
                if water_table == 'Yes':
                    water_level[elements] = float(water_level[elements])
                if water_temp == 'Yes':
                    water_chill[elements] = float(water_chill[elements])
                    
            Dates = []
            for elements in Date:
                spliter = []
                collector = ''
                y = list(elements)
                for elem in y:
                    collector += elem
                spliter.append(collector)
                Dates.append(spliter)
   
        percentage_discharge_change = ['event']
        for elements in range(1, len(Discharge)):
            y = Discharge[elements]
            change = y - Discharge[elements - 1]
            if Discharge[elements - 1 ] == 0:
                percentage_discharge_change.append('no flow')
            else:
                percent_change = (change/Discharge[elements - 1]) * 100
                percentage_discharge_change.append(percent_change)
            
  
        for elements in range(0, len(percentage_discharge_change)):
            c = f'{elements + 1} - {percentage_discharge_change[elements]}'
    #         st.write(c)
        high_compound_flow = []
        low_compound_flow = []
        combine_compound_flow = []
        events = []
        event_dates = []
        baseflow = []
        baseflow_dates = []
        event_endpoint = 0
        event_bunch = []
        catch_no = 0
        packer = 0
        caught_events = {}
        event_occuring = False
        switch = False
        winter = 0
        spring = 0
        summer  = 0
        fall = 0
        seasons = 0
        all_varient = []
        
        
        event_point = winterr
        winter = event_point
        all_varient.append(float(event_point))

        event_point = springg
        spring = event_point
        all_varient.append(float(event_point))

        event_point = summerr
        summer = event_point
        all_varient.append(float(event_point))

        event_point = falll
        fall = event_point
        all_varient.append(float(event_point))
        
        mean_jump = sum(all_varient)/len(all_varient)
    #     st.write(mean_jump)
        
        season_delineation = season_deli
        st.write('\n') 
        searching = True

        month = ''
        if season_delineation == 'B':
###############################################################################################################################################################
            # Example usage - This is the writer
            if __name__ == "__main__":
                # Read and display the current file content in dashboard layout
                content = read_json_from_s3(display=True)
                
                if content:
                    # Specify which fields to increment
                    fields_to_increment = [
                        # "Total_Analysis_Performed",
                        # "Hourly_Data_Analysis",
                        # "Daily_Data_Analysis",
                        # "Seasonal_Delineation_Method_A",
                        "Seasonal_Delineation_Method_B"
                    ]
                    
                    # Update selected fields
                    updated_data = update_selected_fields(content, fields_to_increment)
                    
                    # Write and display the updated content
                    write_json_to_s3(updated_data, display=True)
                else:
                    # If no file exists, create new data
                    new_data = {
                        "timestamp": datetime.now().isoformat(),
                        "Total_Analysis_Performed": 4,
                        "Seasonal_Delineation_Method_A": 2,
                        "Seasonal_Delineation_Method_B": 2,
                        "Daily_Data_Analysis": 2,
                        "Hourly_Data_Analysis": 2
                    }
                    st.write("No file found. Creating new file with default data.")
                    write_json_to_s3(new_data, display=True)
###############################################################################################################################################################
            # st.write(Dates[0])
#####################################################################################################################################
            # Text file reading and writing above json file below
            
#####################################################################################################################################

            step = 0
            while searching == True:
                #This does not loop in any list it is to tell you what the starter is
                day = list(Dates[0][0])
    #             st.write(day)
                member = day[step]
    #             st.write(member)
                try:
                    member = int(member)
                    month +=  f'{member}'
                    step += 1
                except:
                    searching = False
                    if float(month) == 12 or float(month) < 3:
                        event_point = winter
                        st.write('Analysis starting in Winter')
                    elif float(month) > 2 and float(month) < 6:
                        event_point = spring
                        st.write('Analysis starting in spring')
                    elif float(month) > 5 and float(month) < 9:
                        event_point = summer                    
                        st.write('Analysis starting in summer')
                    elif float(month) > 8 and float(month) < 12:
                        event_point = fall                    
                        st.write('Analysis starting in fall')
        elif season_delineation == 'A':
###############################################################################################################################################################
            # Example usage - This is the writer
            if __name__ == "__main__":
                # Read and display the current file content in dashboard layout
                content = read_json_from_s3(display=True)
                
                if content:
                    # Specify which fields to increment
                    fields_to_increment = [
                        # "Total_Analysis_Performed",
                        # "Hourly_Data_Analysis",
                        # "Daily_Data_Analysis",
                        "Seasonal_Delineation_Method_A",
                        # "Seasonal_Delineation_Method_B"
                    ]
                    
                    # Update selected fields
                    updated_data = update_selected_fields(content, fields_to_increment)
                    
                    # Write and display the updated content
                    write_json_to_s3(updated_data, display=True)
                else:
                    # If no file exists, create new data
                    new_data = {
                        "timestamp": datetime.now().isoformat(),
                        "Total_Analysis_Performed": 4,
                        "Seasonal_Delineation_Method_A": 2,
                        "Seasonal_Delineation_Method_B": 2,
                        "Daily_Data_Analysis": 2,
                        "Hourly_Data_Analysis": 2
                    }
                    st.write("No file found. Creating new file with default data.")
                    write_json_to_s3(new_data, display=True)
###############################################################################################################################################################
            
#####################################################################################################################################
            # Text file reading and writing above json file below            
            
#####################################################################################################################################
            
            # st.write(Dates[0])
            step = 0
            while searching == True:
                day = list(Dates[0][0])
                member = day[step]
    #             st.write(member)
                try:
    #                 st.write(member)
                    member = int(member)
                    month +=  f'{member}'
                    step += 1
                except:
                    searching = False
    #                 st.write(month)
                    if float(month) < 4:
                        event_point = winter
                        st.write('Analysis starting in Winter')
                    elif float(month) > 3 and float(month) < 7:
                        event_point = spring
                        st.write('Analysis starting in spring')
                    elif float(month) > 6 and float(month) < 10:
                        event_point = summer                    
                        st.write('Analysis starting in summer')
                    elif float(month) > 9:
                        event_point = fall                    
                        st.write('Analysis starting in fall')
        st.write('\n')
        
        if Discharge[0] > event_point:
            event_occuring = True
            ## this part supplies the whole data for the analysis
        event_ends = 0
        base_compound = 0
        high_compound = 0
    #     st.write(len(Discharge))
        for elements in range(0, len(Discharge)):
            searching = True
            month = ''
            if season_delineation == 'B':
    #             st.write(Dates[0])
                step = 0
                while searching == True:
    #                 st.write(Dates)
    #                 st.write(Dates[elements])
                    day = list(Dates[elements][0])
    #                 st.write(day)
    #                 st.write(step)
    #                 st.write(member)
                    member = day[step]
        #             st.write(member)
                    try:
                        member = int(member)
                        month +=  f'{member}'
                        step += 1
                    except:
                        searching = False
                        if float(month) == 12 or float(month) < 3:
                            event_point = winter
                        elif float(month) > 2 and float(month) < 6:
                            event_point = spring
                        elif float(month) > 5 and float(month) < 9:
                            event_point = summer                 
                        elif float(month) > 8 and float(month) < 12:
                            event_point = fall      

            elif season_delineation == 'A':
                # st.write(Dates[0])
                step = 0
                while searching == True:
    #                 st.write(Dates[elements])
                    day = list(Dates[elements][0])
        #             st.write(day)
                    member = day[step]
        #             st.write(member)
                    try:
                        member = int(member)
                        month +=  f'{member}'
                        step += 1
                    except:
                        searching = False
                        if float(month) < 4:
                            event_point = winter
                        elif float(month) > 3 and float(month) < 7:
                            event_point = spring
                        elif float(month) > 6 and float(month) < 10:
                            event_point = summer
                        elif float(month) > 9:
                            event_point = fall
            
    #         st.write(f'you have passed there emeka {event_point}')
            last_slope = -1
            if event_occuring and elements >= len(events):
                truncated_list = Discharge[elements:]
                section_dates = Dates[elements:]
                changing_flow = percentage_discharge_change[elements:]
                ## this part sections the whole data at event point and works on it until the event ends
                for elements1 in range(0, len(truncated_list)):
    #                 the part logs the event
                    if event_occuring:
                        if truncated_list[elements1] > event_point:
                            event_ends = 0
                            if elements1 > 0:
                                if changing_flow[elements1] == 'no flow':
                                    changing_flow[elements1] = 0.0000000001
                                if changing_flow[elements1] < 0:
                                    events.append(truncated_list[elements1])
                                    event_dates.append(section_dates[elements1])
                                    last_slope = changing_flow[elements1]
                                    baseflow.append('')
                                else:
                                    if last_slope < 0:
                                        high_compound += 1
                                        events.append(truncated_list[elements1])
                                        event_dates.append(section_dates[elements1])
                                        last_slope = changing_flow[elements1]
                                        baseflow.append('')
                                    else:
                                        events.append(truncated_list[elements1])
                                        event_dates.append(section_dates[elements1])
                                        last_slope = changing_flow[elements1]
                                        baseflow.append('')
                            else:
                                event_ends = 0
                                events.append(truncated_list[elements1])
                                event_dates.append(section_dates[elements1])
                                baseflow.append('')
    #                         the part chech if the event is ended and if base flow as begun
                        else:                        
                            event_ends += 1
                            if event_ends < 2:
                                events.append(truncated_list[elements1])
                                event_dates.append(section_dates[elements1])
                                drop_1 = truncated_list[elements1]
                                baseflow.append('')
                            #this part checks if a compount event begins after reaching baseflow treshold
                            else:
                                if truncated_list[elements1] <= drop_1:
                                    baseflow.append(truncated_list[elements1])
                                    baseflow_dates.append(section_dates[elements1])
                                    event_occuring = False
                                    switch = True
                                    event_endpoint = elements1
                                    events.append('')
                                else:
    #                             This part check if it is a slight bump, is significant to creat compound event
                                    if truncated_list[elements1] <= event_point:
                                        baseflow.append(truncated_list[elements1])
                                        baseflow_dates.append(section_dates[elements1])
                                        events.append('')
                                        event_occuring = False
                                        switch = True
                                        event_endpoint = elements1
                                    else:
                                        base_compound += 1
                                        events.append(truncated_list[elements1])
                                        event_dates.append(section_dates[elements1])
                                        baseflow.append('')
            else:
                if len(events) > 0 and len(events) >= packer and switch == True:
                    catch_no += 1
                    event_bunch.append(events)
                    packer = len(events)
                    caught_events[f'{catch_no} event '] = f'{event_dates[0]} - {event_dates[-1]}'
                    switch = False
                    if high_compound > 1:
                        if base_compound > 1:
                            combine_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
                        else:
                            high_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
                    elif base_compound > 1:
                        low_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
                        
                if elements >= len(events):
                    if Discharge[elements] >= event_point:
                        event_ends = 0
                        event_dates = []
                        event_occuring = True
                        if event_occuring and elements >= len(events):
                            truncated_list = Discharge[elements:]
                            section_dates = Dates[elements:]
                            changing_flow = percentage_discharge_change[elements:]
                            ## this part sections the whole data at event point and works on it until the event ends
                            for elements1 in range(0, len(truncated_list)):
                #                 the part logs the event
                                if event_occuring:
                                    if truncated_list[elements1] > event_point:
                                        event_ends = 0
                                        if elements1 > 0:
                                            if changing_flow[elements1] == 'no flow':
                                                changing_flow[elements1] = 0.0000000001
                                            if changing_flow[elements1] < 0:
                                                events.append(truncated_list[elements1])
                                                event_dates.append(section_dates[elements1])
                                                last_slope = changing_flow[elements1]
                                                baseflow.append('')
                                            else:
                                                if last_slope < 0:
                                                    high_compound += 1
                                                    events.append(truncated_list[elements1])
                                                    event_dates.append(section_dates[elements1])
                                                    last_slope = changing_flow[elements1]
                                                    baseflow.append('')
                                                else:
                                                    events.append(truncated_list[elements1])
                                                    event_dates.append(section_dates[elements1])
                                                    last_slope = changing_flow[elements1]
                                                    baseflow.append('')
                                        else:
                                            event_ends = 0
                                            events.append(truncated_list[elements1])
                                            event_dates.append(section_dates[elements1])
                                            baseflow.append('')
                #                         the part chech if the event is ended and if base flow as begun
                                    else:                           
                                        event_ends += 1
                                        if event_ends < 2:
                                            events.append(truncated_list[elements1])
                                            event_dates.append(section_dates[elements1])
                                            drop_1 = truncated_list[elements1]
                                            baseflow.append('')
                                        #this part checks if a compount event begins after reaching baseflow treshold
                                        else:
                                            if truncated_list[elements1] <= drop_1:
                                                baseflow.append(truncated_list[elements1])
                                                baseflow_dates.append(section_dates[elements1])
                                                event_occuring = False
                                                switch = True
                                                event_endpoint = elements1
                                                events.append('')
                                            else:
                #                             This part check if it is a slight bump, is significant to creat compound event
                                                if truncated_list[elements1] <= event_point:
                                                    baseflow.append(truncated_list[elements1])
                                                    baseflow_dates.append(section_dates[elements1])
                                                    events.append('')
                                                    event_occuring = False
                                                    switch = True
                                                    event_endpoint = elements1
                                                else:
                                                    base_compound += 1
                                                    events.append(truncated_list[elements1])
                                                    event_dates.append(section_dates[elements1])
                                                    baseflow.append('')
                        else:
                            if len(events) > 0 and len(events) >= packer and switch == True:
                                catch_no += 1
                                event_bunch.append(events)
                                packer = len(events)
                                caught_events[f'{catch_no} event '] = f'{event_dates[0]} - {event_dates[-1]}'
                                switch = False
                                if high_compound > 1:
                                    if base_compound > 1:
                                        combine_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
                                    else:
                                        high_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
                                elif base_compound > 1:
                                    low_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
             
                    else:
                        baseflow.append(Discharge[elements])
                        baseflow_dates.append(Dates[elements])
                        events.append('')                        
                
        valid_drop = mean_jump 
        pack = 0
        blocks = 0
        pairs = 1
        event_kickout = []
        for elements in range(0,len(events)):
            if type(events[elements]) == float:
                pack += 1
            elif elements > pack - 1 and pack > 0 and pack < 3:
                look_max = []
                blocks += 1
                reductions = 0
                for members in range (0, pack):
                    look_max.append(events[elements - pack])
                    pairs += 1
    #             st.write(look_max)
                max_look = max(look_max)
    #             st.write(max_look)
    #             st.write(look_max)
    #             st.write(type(max_look))
                if max_look < 1.25 * event_point:
                    event_kickout.append(f'{blocks} event ')
                    for kit in range (0, pack):
                        events[elements - 1 - pack + reductions] = ''
                        reductions += 1
                pack = 0
            else:
                if pack > 0:
                    blocks += 1
                pack = 0
                
        # st.write(f'blocks (representing the amount of events left) = {blocks}')
    #     st.write(f'These are the event kickout - {event_kickout}')
        for elements in range(0, len(event_kickout)):
            del caught_events[event_kickout[elements]]
        
        # st.write('\n')
        # st.write('These are the modified events')
        # st.write(caught_events)
        # st.write(len(caught_events))
        # st.write('\n')
        # st.write(f'There are {len(caught_events)} events')
        # st.write('\n')
        
        for elements in range (0, len(events)):
            if type(events[elements]) == float:
                if elements > 0 and events[elements] > valid_drop:
                    events[elements - 1] = Discharge[elements - 1]
                    
        file_name = "Hourly_flow_event_data.txt"
            # Write to file (small predicted data)
        with open(file_name, "w") as file:
            for number in events:
                file.write(f"{number}\n")
        st.write(f"Numbers successfully written to {file_name}")
        # st.write('BaseFlow')
        # for elements in baseflow:
        #     if elements == 0.0:
        #         st.write('')
        #     else:
        #         st.write(elements)
    #     st.write('end')
        
        
        y2 = events
        y1 = Discharge
        
        x = []
        for elements in range(0, len(y1)):
            x.append(Dates[elements][0])

        # Convert empty strings to np.nan and the rest to float for y2
        y2_clean = [float(val) if val != '' else np.nan for val in y2]

        # Create stacked subplots with shared x-axis
        fig, axs = plt.subplots(2, 1, figsize=(6, 6), sharex=True)

        # First plot (y1)
        axs[0].plot(x, y1, marker='', color='green')
        axs[0].set_title('Plot of Discharge Data')
        axs[0].set_ylabel('Drainage (cm or mm)')
        axs[0].grid(False)

        # Second plot (y2 with missing)
        axs[1].plot(x, y2_clean, marker='', linestyle='-', color='blue')
        axs[1].set_title('Plot of Events')
        axs[1].set_xlabel('Dates')
        axs[1].set_ylabel('Drainage (cm or mm)')
        axs[1].grid(False)
        points = 30
        if len(x) < points:
            points = len(x)
        axs[1].xaxis.set_major_locator(plt.MaxNLocator(nbins=points))
        fig.autofmt_xdate(rotation=45)

        # Optional: Set same y-axis limits (uncomment if needed)
        y_min = min(min(y1, default=np.nan), min(y2_clean, default=np.nan))
        y_max = max(max(y1, default=np.nan), max(y2_clean, default=np.nan))
        if not np.isnan(y_min) and not np.isnan(y_max):
            axs[0].set_ylim(y_min, y_max)
            axs[1].set_ylim(y_min, y_max)

        # Adjust layout and show
        plt.tight_layout()
        # plt.show()
        st.pyplot(plt)
        
    #     st.write(Discharge)
    #     st.write(events)
        
        
        for elements in range(0, len(Discharge)):
            if type(events[elements]) == float and type(baseflow[elements]) == float:
                baseflow[elements] = ''
            elif type(events[elements]) == str and type(baseflow[elements]) == str and Discharge[elements] > 0:
                baseflow[elements] = Discharge[elements]
        
        file_name = "hourly_flow_base_data.txt"
            # Write to file (small predicted data)
        with open(file_name, "w") as file:
            for number in baseflow:
                file.write(f"{number}\n")
        st.write(f"Numbers successfully written to {file_name}")
        
        st.write('\n Flow weighted Concentration for event\n')
        
        start_date = False
        end_date = False
        hit = 0
        full_hit = 0
        flow_weighted_concentration = []
        label = 0
        average_water_table_depth = []
        average_water_table_temp = []
        # st.write(caught_events)
        
        for key in caught_events:
            label += 1
            good_break_point = False
    #         st.write(list(caught_events[key]))
            matcher = list(caught_events[key])
            matcher = [item for item in matcher if item != '[']
            matcher = [item for item in matcher if item != ']']
            matcher = [item for item in matcher if item != "'"]
    #         st.write(f'This is the matcher {matcher}')
            for elementss in range(0, len(Dates)):
    #             st.write(elementss)
                if good_break_point == True:
                    break
                if start_date == False:
                    mini_conc = []
                    mini_flow = []
                    mini_table = []
                    mini_temp = []
                    plucks = 0
                    plucks1 = 0
                    starter = list(Dates[elementss][0])
                    hit = 0
                    for elements in range(0, len(starter)):
    #                     st.write(f'This is the starter elements {starter[elements]}')
                        if starter[elements] == matcher[elements]:
                            hit += 1
                        if hit == len(starter):
                            start_date = True
                            starter.append(' ')
                            starter.append('-')
                            starter.append(' ')
                            half_band = starter
                            mini_conc.append(concentration[elementss])
                            mini_flow.append(events[elementss])
                            if water_table == 'Yes':
                                mini_table.append(water_level[elementss])
                                plucks += 1
                                
                            if water_temp == 'Yes':
                                mini_temp.append(water_chill[elementss])
                                plucks1 += 1
                else:
                    full_band_unsure = []
                    for elemennt in (half_band):
                        full_band_unsure.append(elemennt)
    #                 st.write('This is the static half band')
    #                 st.write(half_band)
                    ender = list(Dates[elementss][0])
                    hit = 0
                    for elements in ender:
                        full_band_unsure.append(elements)
                    for elements in range(0, len(full_band_unsure)):
                        if full_band_unsure[elements] == matcher[elements]:
                            hit += 1
                        if hit == len(full_band_unsure):
    #                         st.write('I got the full hit')
    #                         st.write(full_band_unsure)
                            full_hit += 1
                            start_date = False
                            good_break_point = True
                    mini_conc.append(concentration[elementss])
                    mini_flow.append(events[elementss])
                    if water_table == 'Yes':
                        mini_table.append(water_level[elementss])
                        plucks += 1
                        
                    if water_temp == 'Yes':
                        mini_temp.append(water_chill[elementss])
                        plucks1 += 1
                        
                    if start_date == False:
                        conc_flow_sum = 0
                        flow_sum = 0
                        level_sum = 0
                        temp_sum = 0
                        for elements in range(0, len(mini_conc)):
                            try:
                                y = float(mini_conc[elements])
                                b = float(mini_flow[elements])
                                
                                if water_table == 'Yes':
                                    level = float(mini_table[elements])
                                    
                                if water_temp == 'Yes':
                                    temp = float(mini_temp[elements])
                                    
                                if y > 0:
                                    conc_flow_sum += (float(mini_conc[elements] * float(mini_flow[elements])))
                                    flow_sum += float(mini_flow[elements])
                                    
                                if water_table == 'Yes':
                                    if level > 0:
                                        level_sum += float(mini_table[elements])
                                        
                                if water_temp == 'Yes':
                                    if temp > 0:
                                        temp_sum += float(mini_temp[elements])
                                        
                            except:
                                toool = 'not usable becuase is it a string'
                        if flow_sum == 0:
                            st.write('Make sure all of your flow has corresponding concentrations or input \'1\' in concentration column')
                            st.stop()
                            # flow_sum = 1
                        F_W_C = conc_flow_sum / flow_sum    
                        flow_weighted_concentration.append(f'{label}_event - {F_W_C}')
                        
                        if water_table == 'Yes':
                            A_W_T_D = level_sum/plucks
                            average_water_table_depth.append(f'{label}_event - {A_W_T_D}')
                        
                        if water_temp == 'Yes':
                            A_W_T_T = temp_sum/plucks1
                            average_water_table_temp.append(f'{label}_event - {A_W_T_T}')

        
        st.download_button(label='Download Hourly Event Data.txt', data=open('Hourly_flow_event_data.txt', 'rb'), file_name='Hourly Event data.txt')
        st.download_button(label='Download Base Data.txt', data=open('hourly_flow_base_data.txt', 'rb'), file_name='Base Flow data.txt')
        # st.download_button(label='Download Full Base Data.txt', data=open('hourly_flow_base_full_data.txt', 'rb'), file_name='Full Base Flow data.txt')
        buffer = BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)

        # Create download button
        # st.download_button(
        #     label="Download Hourly Event Plot",
        #     data=buffer,
        #     file_name="hourly_discharge_events_plot.png",
        #     mime="image/png"
        # )

        # Close the figure to free memory
        plt.close(fig)
    
        refined_base = []
        for elements in baseflow:
            refined_base.append(elements)
            
        # print('\n')
#         print(refined_base)
#         print('\n')
        
        eventing = False
        for elements in range (1, len(events)):
            if events[elements] != '':
                if events[elements - 1] == '':
                    eventing = True
                    refined_base[elements] = events[elements]
            else:
                if events[elements - 1] != '':
                    eventing = False
                    refined_base[elements - 1] = events[elements - 1]
        
#         print(events)
#         print(refined_base)
        
        no_data = True

        for elements in range(0, len(refined_base)):
            if refined_base[elements] == '' and no_data == True:
                a = 'keep_searching'
            else:
                no_data = False
                if refined_base[elements] == '':
                    boarder = False
                    steps = 1
                    span = 0
                    jump = 0
                    while boarder == False:
                        nex = elements + steps
                        if nex != len(refined_base):
                            if refined_base[nex] != '':
                                boarder = True
                                span = refined_base[nex] - refined_base[elements - 1]
                                jump = span/(steps + 1)
                                pair1 = 0
                                pair2 = 1
                                for element in range (0, steps):
                                    refined_base[elements - 1 + pair2] = refined_base[elements - 1 + pair1] + jump
                                    pair1 += 1
                                    pair2 += 1
        #                             print(refined_base)
        #                             print('\n')
                            else:
                                steps += 1
                        else:
                            break
        

        for elements in range(0, len(events)):
            if events[elements] != '' and refined_base[elements] != '':
                if refined_base[elements] > events[elements]:
                    refined_base[elements] = events[elements]

        # print(refined_base)
        # the colonly is to catch the error of some certain false events that can occur
        off_colony = []
        colony = 0
        passes = 0
        door = 0
        single_colony = False
        for elements in range(0, len(events)):
            if events[elements] == '' and elements > 0:
                door += 1
                if colony == 1:
                    single_colony = True
                elif colony > 1:
                    passes += 1
                    colony = 0
            else:
                if colony == 1 and door == 1:
                    off_colony.append(passes + 1)
                colony += 1
                door = 0
        
        # print('This is the off colony')
        # print(off_colony)

        start_off = False
        first_base = 0
        parse = 0
        for elemen in range(0, len(refined_base)):
            if refined_base[elemen] == '':
                start_off = True
            elif start_off == True and parse == 0:
                first_base = refined_base[elemen]
                parse += 1
            
        if start_off == True:
            for elements in range(0, len(refined_base)):
                if refined_base[elements] == '':
                    refined_base[elements] = first_base
#         print(refined_base)

        sides = []
        hold_trapezoid = []
        flow_vol = 0
        event_vols = []
        too_low = False
        eventon = False
        for elements in range(0, len(events)):
            if events[0] == '':
                if elements > 1:
                    if events[elements] != '':
                        if events[elements - 1] != '':
                            eventon = True
                    
                    elif events[elements - 1] != '':
                        eventon = False
                        if len(sides) != 0:
                            side = events[elements - 1] - refined_base[elements - 1]
                            sides.append(side)
                            if len(sides) == 2:
                                flow_vol += 0.5 *(sides[0] + sides[1])
                                hold_trapezoid.append(0.5 *(sides[0] + sides[1]))
                        
                        if flow_vol > 0:       
                            event_vols.append(flow_vol)
                        sides = []
                        flow_vol = 0
                    
                    if eventon:
                        side = events[elements - 1] - refined_base[elements - 1]
                        sides.append(side)
                        if len(sides) == 2:
                            flow_vol += 0.5 *(sides[0] + sides[1])
                            hold_trapezoid.append(0.5 *(sides[0] + sides[1]))
                            sides.remove(sides[0])
                        
            else:
                if elements > 0:
#                     print(Date)
#                     print(winter)
#                     print(spring)
#                     print(summer)
#                     print(fall)
#                     print('\n')
                    day_list = list(Date[elements])
#                     print(day_list)
                    check_month = f'{day_list[0]}{day_list[1]}'
#                     print(check_month)
                    if season_delineation == 'A':
                        if int(check_month) == 1 or int(check_month) == 2 or int(check_month) == 3:
                            shoulder = winter
                        elif int(check_month) == 4 or int(check_month) == 5 or int(check_month) == 6:
                            shoulder = spring
                        elif int(check_month) == 7 or int(check_month) == 8 or int(check_month) == 9:
                            shoulder = summer
                        else:
                            shoulder = fall
                    else:
                        if int(check_month) == 12 or int(check_month) == 2 or int(check_month) == 1:
                            shoulder = winter
                        elif int(check_month) == 4 or int(check_month) == 5 or int(check_month) == 3:
                            shoulder = spring
                        elif int(check_month) == 7 or int(check_month) == 8 or int(check_month) == 6:
                            shoulder = summer
                        else:
                            shoulder = fall
                            
                    if events[elements] != '':
                        if events[elements - 1] != '':
                            eventon = True
                    if events[elements] != '' and events[elements - 1] != '':
                        if events[elements] < shoulder and events[elements - 1] < shoulder:
                            too_low = True
                            eventon = False
                            if len(sides) != 0:
                                side = events[elements - 1] - refined_base[elements - 1]
                                sides.append(side)
                                if len(sides) == 2:
                                    flow_vol += 0.5 *(sides[0] + sides[1])
                                    hold_trapezoid.append(0.5 *(sides[0] + sides[1]))
                            
                            if flow_vol > 0:       
                                event_vols.append(flow_vol)
    #                             print(event_vols)
                            sides = []
                            flow_vol = 0
                    
                    elif events[elements - 1] != '' and too_low == False:
                        eventon = False
                        if len(sides) != 0:
                            side = events[elements - 1] - refined_base[elements - 1]
                            sides.append(side)
                            if len(sides) == 2:
                                flow_vol += 0.5 *(sides[0] + sides[1])
                                hold_trapezoid.append(0.5 *(sides[0] + sides[1]))
                        
                        if flow_vol > 0:       
                            event_vols.append(flow_vol)
                        sides = []
                        flow_vol = 0
                    
                    if eventon:
                        side = events[elements - 1] - refined_base[elements - 1]
                        sides.append(side)
                        if len(sides) == 2:
                            flow_vol += 0.5 *(sides[0] + sides[1])
                            hold_trapezoid.append(0.5 *(sides[0] + sides[1]))
                            sides.remove(sides[0])

                    too_low = False
##################################################################################################################################################################################################################################
####################################### tell the singles event point in the data set ####################################################################################         
#         skipped_events = []
#         chain = 0
#         chaining = False
#         block = 0
#         for elements in events:
#             if elements !=  '':
#                 chaining = True
#                 chain += 1
#             elif chaining == True:
#                 block += 1
#                 chaining = False
#                 if chain == 1:
#                     skipped_events.append(block)
#                 chain = 0

# this looks to catch the high and low in aims to split compounded events
        # season_delineation = 'A'
        
        row = 0
        chain = 0
        chaining = False
        block = 0
        last_high = 0
        half_chain = False
        split_detail = []
        down = False
        for elements in range(0, len(events)):
            if events[elements] !=  '':
                chaining = True
                new = events[elements]
                if new > last_high and down == False:
                    last_high = new
                                
                elif new > last_high and down != False:
                    last_high = events[elements]
                    if season_delineation == 'A':
                        split = list(Date[elements])
                        day = split[0] + split[1]
                        wi = ['01', '02', '03']
                        sp = ['04', '05', '06']
                        su = ['07', '08', '09']
                        fa =  ['10', '11', '12']
                        for ements in wi:
                            if day == ements:
#                                 print('it winter')
                                if events[elements - 1] < winter:
                                    row += 1
                                    if row == 2:
                                        half_chain = True
                                        half = chain - 1
#                                         print(Date[elements - 1])
#                                         print(block)
                        for ements in sp:
                            if day == ements:
#                                 print('it spring')
                                if events[elements - 1] < spring:
                                    row += 1
                                    if row == 2:
                                        half_chain = True
                                        half = chain - 1
#                                         print(Date[elements - 1])
#                                         print(block)
                        for ements in su:
                            if day == ements:
#                                 print('it summer')
                                if events[elements - 1] < summer:
                                    row += 1
                                    if row == 2:
                                        half_chain = True
                                        half = chain - 1
#                                         print(Date[elements - 1])
#                                         print(block)
                        for ements in fa:
                            if day == ements:
#                                 print('it fall')
                                if events[elements - 1] < fall:
                                    row += 1
                                    if row == 2:
                                        half_chain = True
                                        half = chain - 1
#                                         print(Date[elements - 1])
#                                         print(block)
                    else:
                        split = list(Date[elements])
                        day = split[0] + split[1]
                        wi = ['12', '01', '02']
                        sp = ['03', '04', '05']
                        su = ['06', '07', '08']
                        fa =  ['09', '10', '11']
                        for ements in wi:
                            if day == ements:
#                                 print('it winter')
                                if events[elements - 1] < winter:
                                    row += 1
                                    if row == 2:
                                        half_chain = True
                                        half = chain - 1
#                                         print(Date[elements - 1])
#                                         print(block)
                        for ements in sp:
                            if day == ements:
#                                 print('it spring')
                                if events[elements - 1] < spring:
                                    row += 1
                                    if row == 2:
                                        half_chain = True
                                        half = chain - 1
#                                         print(Date[elements - 1])
#                                         print(block)
                        for ements in su:
                            if day == ements:
#                                 print('it summer')
                                if events[elements - 1] < summer:
                                    row += 1
                                    if row == 2:
                                        half_chain = True
                                        half = chain - 1
#                                         print(Date[elements - 1])
#                                         print(block)
                        for ements in fa:
                            if day == ements:
#                                 print('it fall')
                                if events[elements - 1] < fall:
                                    row += 1
                                    if row == 2:
                                        half_chain = True
                                        half = chain - 1
#                                         print(Date[elements - 1])
#                                         print(block)
                    
                else:
                    down = True
                    row = 0
                    last_high = events[elements]
                    
                chain += 1
            elif chaining == True:
                down = False
                last_high = 0
                chaining = False
                if half_chain == True:
                    portion = half/chain
#                     print(portion)
                    split_detail.append(block + portion)
                chain = 0
                half_chain = False
                split_detail.append(block)
                block += 1
#                 print(split_detail)
#         print(f'wave Events - {wave_events}')
        
        # st.write('split_detail')
        # st.write(split_detail)
        
        refine = []
        if len(split_detail) > 0:
            refine.append(0)
        for elements in range (1, len(split_detail)):
            if split_detail[elements] > split_detail[elements - 1]:
                refine.append(split_detail[elements])
        split_detail = refine
        # print(split_detail)
        # print(len(split_detail))
        move = 0
        split_vols = []
                
        while move < len(split_detail) - 1:
            for elements in range(0, len(event_vols)):
                if move < len(split_detail):
                    if elements < float(split_detail[move]):
            #                         print(elements)
                        portion = split_detail[move] - math.floor(split_detail[move])
                        split_vols.append(portion * event_vols[elements])
                        split_vols.append(event_vols[elements] - (portion * event_vols[elements]))
                        move += 1
                        # print('came through')
            #                         print(split_vols)
                                      
                    else:
                        split_vols.append(event_vols[elements])
            #                         print(split_vols)
                        move += 1
                        
                else:
                    split_vols.append(event_vols[elements])
            #                     print(split_vols)
                                      
        # print(event_vols)
        # print(split_vols)
###########################################################################################################################
        
        event_trapezoid = []
        # print(len(events))
        # print(len(hold_trapezoid))
        through = 0
        paired = 0
        for elements in range(0, len(events)):
            if events[elements] == '':
                paired = 0
                event_trapezoid.append(events[elements])
            elif paired > 1 and through < len(hold_trapezoid):
                event_trapezoid.append(hold_trapezoid[through])
                through += 1
            else:
                event_trapezoid.append(0)
                paired += 1
                if elements == 0 and events[0] != '':
                    paired += 1

        
        st.write('\n')
        # st.write('These are the modified events')
        st.write('These are the caught events')
        if len(off_colony) > 0:
            for elements in off_colony:
                key_to_remove = list(caught_events.keys())[elements]
                del caught_events[key_to_remove]
               
############################################################################################################################################################################
        # print(caught_events)
        leap = [1904, 1908, 1912, 1916, 1920, 1924, 1928, 1932, 1936, 1940, 1944, 1948, 1952, 1956, 1960, 1964, 1968,
1972, 1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020, 2024, 2028, 2032, 2036,
2040, 2044, 2048, 2052, 2056, 2060, 2064, 2068, 2072, 2076, 2080, 2084, 2088, 2092, 2096, 2104, 2108,
2112, 2116, 2120, 2124, 2128, 2132, 2136, 2140, 2144, 2148, 2152, 2156, 2160, 2164, 2168, 2172, 2176,
2180, 2184, 2188, 2192, 2196, 2204, 2208, 2212, 2216, 2220, 2224, 2228, 2232, 2236, 2240, 2244, 2248,
2252, 2256, 2260, 2264, 2268, 2272, 2276, 2280, 2284, 2288, 2292, 2296, 2304, 2308, 2312, 2316, 2320,
2324, 2328, 2332, 2336, 2340, 2344, 2348, 2352, 2356, 2360, 2364, 2368, 2372, 2376, 2380, 2384, 2388,
2392, 2396, 2400, 2404, 2408, 2412, 2416, 2420, 2424, 2428, 2432, 2436, 2440, 2444, 2448, 2452, 2456,
2460, 2464, 2468, 2472, 2476, 2480, 2484, 2488, 2492, 2496, 2504, 2508, 2512, 2516, 2520, 2524, 2528,
2532, 2536, 2540, 2544, 2548, 2552, 2556, 2560, 2564, 2568, 2572, 2576, 2580, 2584, 2588, 2592, 2596,
2604, 2608, 2612, 2616, 2620, 2624, 2628, 2632, 2636, 2640, 2644, 2648, 2652, 2656, 2660, 2664, 2668,
2672, 2676, 2680, 2684, 2688, 2692, 2696, 2704, 2708, 2712, 2716, 2720, 2724, 2728, 2732, 2736, 2740,
2744, 2748, 2752, 2756, 2760, 2764, 2768, 2772, 2776, 2780, 2784, 2788, 2792, 2796, 2800, 2804, 2808,
2812, 2816, 2820, 2824, 2828, 2832, 2836, 2840, 2844, 2848, 2852, 2856, 2860, 2864, 2868, 2872, 2876,
2880, 2884, 2888, 2892, 2896, 2904, 2908, 2912, 2916, 2920, 2924, 2928, 2932, 2936, 2940, 2944, 2948,
2952, 2956, 2960, 2964, 2968, 2972, 2976, 2980, 2984, 2988, 2992, 2996]

        months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        monthsl = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        span = []
        hours = []

        for element in caught_events:
            event = (caught_events[element])
            event_list = list(event)
        #     print(event_list)
        # print(caught_events)
            start = []
            start1 = ''
            end = []
            end1 = ''
            for elem in range(2, 18):
                start.append(event_list[elem])
                start1 += event_list[elem]
                end.append(event_list[elem + 23])
                end1 += event_list[elem + 23]
        #     print(start)
        #     print(end)
            year = int(f'{start[6]}{start[7]}{start[8]}{start[9]}')
            year1 = int(f'{end[6]}{end[7]}{end[8]}{end[9]}')
            caught_events[element] = f'{start1} - {end1}'
        #     print(year)
            if year == year1:
                inleap = False
                for elements in leap:
                    if year == elements:
                        inleap = True
                day_start = int(f'{start[3]}{start[4]}')
            #     print(day_start)
                month_start = int(f'{start[0]}{start[1]}')
            #     (print(month_start))
                day_end = int(f'{end[3]}{end[4]}')
                month_end = int(f'{end[0]}{end[1]}')
                if month_start > 12:
                    st.write('Make sure Your date is in the format mm/dd/yyyy hh:mm - currently is not, please corrrect it')
                    st.stop()
            #     print(month_end)
            #     print(day_end)
                ending = 0
                starting = 0
                if inleap == False:
                    for eleme in range(0, month_start):
                        starting += months[eleme]
                    starting += day_start
            #         print(starting)
                    
                    for eleme in range(0, month_end):
                        ending += months[eleme]
                    ending += day_end
            #         print(ending)
                else:
                    for eleme in range(0, month_start):
                        starting += months[eleme]
                    starting += day_start
                    
                    for eleme in range(0, month_end):
                        ending += months[eleme]
                    ending += day_end
                
                day_span = ending - starting
                span.append(day_span)
                if day_span < 1:
                    first = int(f'{end[11]}{end[12]}') - int(f'{start[11]}{start[12]}')
            #         print(first)
                    hours.append(first)
                else:
                    days_hours = 24 * (day_span - 1)
                    lead = 24 - int(f'{start[11]}{start[12]}')
                    total_bridge = int(f'{end[11]}{end[12]}') + lead
                    total_hours = total_bridge + days_hours
            #         print(total_hours)
                    hours.append(total_hours)
                
            else:
                hours1 = []
        #         print(end1)
                # split_list = {
                #     '*1 event': f'{start1}:00 - 12/31/{year} 24:00',
                #     '*2 event': f'01/01/{year1} 00:00 - {end1}:00'                      
                #             }
                split_list = {
                    '*1 event': f'{start1}- 12/31/{year} 24:00',
                    '*2 event': f'01/01/{year1} 00:00 - {end1}'                      
                            }
                # print(split_list)
                print('I got here March 10 2026')
                for element in split_list:
                    event = (split_list[element])
                    event_list = list(event)
                #     print(event_list)
                # print(caught_events)
                    start = []
                    start1 = ''
                    end = []
                    end1 = ''
                    for elem in range(0, 13):
                        start.append(event_list[elem])
                        start1 += event_list[elem]
                        end.append(event_list[elem + 19])
                        end1 += event_list[elem + 19]
                #     print(start)
                #     print(end)
                    year = int(f'{start[6]}{start[7]}{start[8]}{start[9]}')
                    year1 = int(f'{end[6]}{end[7]}{end[8]}{end[9]}')
                #     print(year)
                    if year == year1:
                        inleap = False
                        for elements in leap:
                            if year == elements:
                                inleap = True
                        day_start = int(f'{start[3]}{start[4]}')
                    #     print(day_start)
                        month_start = int(f'{start[0]}{start[1]}')
                    #     (print(month_start))
                        day_end = int(f'{end[3]}{end[4]}')
                        month_end = int(f'{end[0]}{end[1]}')
                    #     print(month_end)
                    #     print(day_end)
                        ending = 0
                        starting = 0
                        if inleap == False:
                            for eleme in range(0, month_start):
                                starting += months[eleme]
                            starting += day_start
                    #         print(starting)
                            
                            for eleme in range(0, month_end):
                                ending += months[eleme]
                            ending += day_end
                    #         print(ending)
                        else:
                            for eleme in range(0, month_start):
                                starting += monthsl[eleme]
                            starting += day_start
                            
                            for eleme in range(0, month_end):
                                ending += monthsl[eleme]
                            ending += day_end
                        
                        day_span = ending - starting
                        span.append(day_span)
                        if day_span < 1:
                            first = int(f'{end[11]}{end[12]}') - int(f'{start[11]}{start[12]}')
                    #         print(first)
                            hours1.append(first)
                        else:
                            days_hours = 24 * (day_span - 1)
                            lead = 24 - int(f'{start[11]}{start[12]}')
                            total_bridge = int(f'{end[11]}{end[12]}') + lead
                            total_hours = total_bridge + days_hours
                    #         print(total_hours)
                            hours1.append(total_hours)
                    
                    
                    
                
                totes = 0
                for elementy in hours1:
                    totes += elementy
                hours.append(totes)
        #         print(totes)
        #         print(split_list)
        #         print(len(split_list))
        #         print(type(split_list))
        #         print(span1)
############################################################################################################################################################################
        # print(caught_events)
         
        with st.expander("📅 Drainage Events"):
            event_dict = caught_events
            # Convert dictionary to a format suitable for dataframe
            events_data = {
                "Event": list(event_dict.keys()),
                "Date-Time Range": list(event_dict.values()),
                "Duration (hours)": hours
            }
            st.dataframe(events_data, use_container_width=True)
        # st.write(caught_events)
        st.write(len(caught_events))
        st.write('\n')
        st.write(f'There are {len(caught_events)} events')
        st.write('\n')
        


        if len(split_vols) > len(caught_events):
            if split_vols[len(caught_events) - 1] == 0:
                cut_list = split_vols[:len(caught_events) - 1]
                split_vols = cut_list
        
        under_pass = split_vols
        if len(under_pass) < len(caught_events):
        #             print(events)
            colony = 0
            shreaded = []
            event_bulk = []
            passes = 0
            eventing = False
            batch_load = 0
            under_jump = 0
            for elements in range(0, len(event_trapezoid)):
                if events[elements] != '' and colony >= 1:
                    eventing = True
                    event_bulk.append(event_trapezoid[elements])
        #             print(Date)
                    split = list(Date[elements])
        #             print(split)
                    month = split[0] + split[1]
                    if season_delineation == 'A':                        
                        wi = ['01', '02', '03']
                        sp = ['04', '05', '06']
                        su = ['07', '08', '09']
                        fa =  ['10', '11', '12']
                        for ements in wi:
                            if month == ements:
                                if events[elements] < winterr:
                                    colony += 1
                                    under_jump += 1
                                    if under_jump == 2:
                                        shreaded.append(sum(event_bulk) - event_trapezoid[elements])
                                        passes += 1
                                        under_jump = 0
                                        event_bulk = []
                                        colony = 1
                                        event_bulk.append(event_trapezoid[elements])
        #                                         print(passes)
                                else:
                                    under_jump = 0
                                    colony += 1
                                                
                        for ements in sp:
                            if month == ements:
                                if events[elements] < springg:
                                    colony += 1
                                    under_jump += 1
                                    if under_jump == 2:
                                        shreaded.append(sum(event_bulk) - event_trapezoid[elements])
                                        passes += 1
                                        under_jump = 0
                                        event_bulk = []
                                        colony = 1
                                        event_bulk.append(event_trapezoid[elements])
        #                                         print(passes)
                                else:
                                    under_jump = 0
                                    colony += 1
                                                
                        for ements in su:
                            if month == ements:
                                if events[elements] < summerr:
                                    colony += 1
                                    under_jump += 1
                                    if under_jump == 2:
                                        shreaded.append(sum(event_bulk) - event_trapezoid[elements])
                                        passes += 1
                                        under_jump = 0
                                        event_bulk = []
                                        colony = 1
                                        event_bulk.append(event_trapezoid[elements])
        #                                         print(passes)
                                else:
                                    under_jump = 0
                                    colony += 1
                                                
                        for ements in fa:
                            if month == ements:
                                if events[elements] < falll:
                                    colony += 1
                                    under_jump += 1
                                    if under_jump == 2:
                                        shreaded.append(sum(event_bulk) - event_trapezoid[elements])
                                        passes += 1
                                        under_jump = 0
                                        event_bulk = []
                                        colony = 1
                                        event_bulk.append(event_trapezoid[elements])
        #                                         print(passes)
                                else:
                                    under_jump = 0
                                    colony += 1
                                                
                    else:
                        wi = ['12', '01', '02']
                        sp = ['03', '04', '05']
                        su = ['06', '07', '08']
                        fa =  ['09', '10', '11']
                        for ements in wi:
                            if month == ements:
                                if events[elements] < winterr:
                                    colony += 1
                                    under_jump += 1
                                    if under_jump == 2:
                                        shreaded.append(sum(event_bulk) - event_trapezoid[elements])
                                        passes += 1
                                        under_jump = 0
                                        event_bulk = []
                                        colony = 1
                                        event_bulk.append(event_trapezoid[elements])
        #                                         print(passes)
                                else:
                                    under_jump = 0
                                    colony += 1
                                                
                        for ements in sp:
                            if month == ements:
                                if events[elements] < springg:
                                    colony += 1
                                    under_jump += 1
                                    if under_jump == 2:
                                        shreaded.append(sum(event_bulk) - event_trapezoid[elements])
                                        passes += 1
                                        under_jump = 0
                                        event_bulk = []
                                        colony = 1
                                        event_bulk.append(event_trapezoid[elements])
        #                                         print(passes)
                                else:
                                    under_jump = 0
                                    colony += 1
                                                
                        for ements in su:
                            if month == ements:
                                if events[elements] < summerr:
                                    colony += 1
                                    under_jump += 1
                                    if under_jump == 2:
                                        shreaded.append(sum(event_bulk) - event_trapezoid[elements])
                                        passes += 1
                                        under_jump = 0
                                        event_bulk = []
                                        colony = 1
                                        event_bulk.append(event_trapezoid[elements])
        #                                         print(passes)
                                else:
                                    under_jump = 0
                                    colony += 1
                                                
                        for ements in fa:
                            if month == ements:
                                if events[elements] < falll:
                                    colony += 1
                                    under_jump += 1
                                    if under_jump == 2:
                                        shreaded.append(sum(event_bulk) - event_trapezoid[elements])
                                        passes += 1
                                        under_jump = 0
                                        event_bulk = []
                                        colony = 1
                                        event_bulk.append(event_trapezoid[elements])
        #                                         print(passes)
                                else:
                                    under_jump = 0
                                    colony += 1
                                                                    
                    
                elif events[elements] != '' and colony < 2:
                    colony += 1
                    event_bulk.append(event_trapezoid[elements])
                elif events[elements] == '' or eventing == True:
                    colony = 0
                    eventing = False
                    if len(event_bulk) > 1:
                        shreaded.append(sum(event_bulk))
                        passes += 1
                        # print(event_bulk)
                        # print(passes)
                    event_bulk = []
                
            split_vols = shreaded

##############################################################################################################################
        st.write('These are the hourly discharge volumes per event')
        field_vol = []
        passes = 0
        # st.write('split_vols')
        # st.write(split_vols)
        for elements in split_vols:
            passes += 1
            field_vol.append(f'Event-{passes} - {field_area * elements}')
        
        field_vol1 = []   
        if len(off_colony) > 0 or len(field_vol) > len(caught_events):
            for element in range(0, len(caught_events)):
                field_vol1.append(field_vol[element])
        
        if len(off_colony) > 0 or len(field_vol) > len(caught_events):
            # st.write(field_vol1)
            with st.expander("📈 field_vol1"):
                event_list = field_vol1
                events_data = {
                "Event": [event.split(" - ")[0] for event in event_list],
                "Value": [float(event.split(" - ")[1]) for event in event_list]
                }
            st.dataframe(events_data, use_container_width=True)
            st.write(len(field_vol1))
        else:
            # st.write(field_vol)
            with st.expander("📈 field_vol"):
                event_list = field_vol
                events_data = {
                "Event": [event.split(" - ")[0] for event in event_list],
                "Value": [float(event.split(" - ")[1]) for event in event_list]
                }
            st.dataframe(events_data, use_container_width=True)
            st.write(len(field_vol))
        
    #     st.write(full_hit)
        st.write('\n')
        
        st.write('The flow weighted concentration for the events are: ')
        if len(off_colony) > 0:
            for elements in off_colony:
                flow_weighted_concentration.remove(flow_weighted_concentration[elements])
        # st.write(flow_weighted_concentration)
        
        conc_teller = []
        for elements in flow_weighted_concentration:
            y = list(elements)
            number = float(f'{y[len(y) - 3]}{y[len(y) - 2]}{y[len(y) - 1]}')
            conc_teller.append(number)
            # print(conc_teller)
        mode_conc = max(set(conc_teller), key=conc_teller.count)
        if mode_conc == 1.0:
            st.markdown(
                    "<p style='color:red; font-weight:bold;'>"
                    "Warning: The concentration shown here may not represent the actual concentration because the cell was likely populated with placeholder values of 1."
                    "</p>",
                    unsafe_allow_html=True
                )
            with st.expander("📈 flow_weighted_concentration"):                
                event_list = flow_weighted_concentration
                events_data = {
                "Event": [event.split(" - ")[0] for event in event_list],
                "Value": [float(event.split(" - ")[1]) for event in event_list]
                }
        else:
            with st.expander("📈 flow_weighted_concentration"):
                event_list = flow_weighted_concentration
                events_data = {
                "Event": [event.split(" - ")[0] for event in event_list],
                "Value": [float(event.split(" - ")[1]) for event in event_list]
                }
        st.dataframe(events_data, use_container_width=True)
        st.write(len(flow_weighted_concentration))
        
        if water_table == 'Yes':
            st.write('\n')
            st.write('These are the average water table depths for the events')
            if len(off_colony) > 0:
                for elements in off_colony:
                    average_water_table_depth.remove(average_water_table_depth[elements])
            # st.write(average_water_table_depth)
            with st.expander("📈 average_water_table_depth"):
                event_list = average_water_table_depth
                events_data = {
                "Event": [event.split(" - ")[0] for event in event_list],
                "Value": [float(event.split(" - ")[1]) for event in event_list]
            }
            st.dataframe(events_data, use_container_width=True)
            st.write(len(average_water_table_depth))
            
        if water_temp == 'Yes':
            st.write('\n')
            st.write('These are the average water temperatures for the events')
            if len(off_colony) > 0:
                for elements in off_colony:
                    average_water_table_temp.remove(average_water_table_temp[elements])
            # st.write(average_water_table_temp)
            with st.expander("📈 Average Water Table Temperature"):
                event_list = average_water_table_temp
                events_data = {
                "Event": [event.split(" - ")[0] for event in event_list],
                "Value": [float(event.split(" - ")[1]) for event in event_list]
            }
            st.dataframe(events_data, use_container_width=True)
            st.write(len(average_water_table_temp))


        file_name = "hourly_flow_base_full_data.txt"
            # Write to file (small predicted data)
        with open(file_name, "w") as file:
            for number in refined_base:
                file.write(f"{number}\n")
        st.write(f"Numbers successfully written to {file_name}")

        st.download_button(label='Download Full Base Data.txt', data=open('hourly_flow_base_full_data.txt', 'rb'), file_name='Full Base Flow data.txt')

        st.download_button(
            label="Download Hourly Event Plot",
            data=buffer,
            file_name="hourly_discharge_events_plot.png",
            mime="image/png"
        )
##################################################################################################################################################################################################################################

        # Convert data to numpy arrays, replacing '' with np.nan
        events = np.array([float(x) if x != '' else np.nan for x in events])
        base_flow = np.array([float(x) if x != '' else np.nan for x in refined_base])

        # Create time index
        x = np.arange(1, len(events) + 1)

        # Interpolate base flow to fill gaps for continuous shading
        # Get indices where base_flow is not NaN
        valid_indices = np.where(~np.isnan(base_flow))[0]
        valid_values = base_flow[valid_indices]
        # Interpolate over all indices
        base_flow_interpolated = np.interp(x - 1, valid_indices, valid_values)

        # Create the plot
        plt.figure(figsize=(12, 6))
        
        plt.plot(x, events, color='red', linewidth=2, label='Event Flow')

        # Plot base flow with continuous blue shading
        plt.fill_between(x, base_flow_interpolated, color='blue', alpha=0.3, label='Base Flow')
        # Plot original base flow points with black trace (only where data exists)
#         plt.plot(x, base_flow, color='black', linewidth=2, linestyle='dotted', label='_Base Flow Trace')
        plt.plot(x, base_flow, color='black', linewidth=2, linestyle=':', label='_Base Flow Trace')  # Hidden label

        # Plot event flow with red trace

        # Customize the plot
        plt.xlabel('Time Index')
        plt.ylabel('Flow')
        plt.title('Event and Base Flow Trends')
        plt.legend()
        plt.grid(True, linestyle=':')

        # Show the plot
        plt.tight_layout()
        plt.show()
        st.pyplot(plt)

        os.remove("temp.csv")
# Main app
def main():
    st.write('Making Drainage Events Easy')
    st.title("📊 Event Analysis Dashboard - Version 1.0")
    st.markdown("Upload your data and configure analysis parameters to detect events in discharge data.")
    st.markdown("Please make sure your date is formatted correctly, most errors are due to incorrect date formatting.")
    st.header("Event & Baseflow Definitions")

    with st.expander("Click to view details"):
        st.markdown("""
    **Event Flow** \n
        Event Flow is the portion of subsurface drainage discharge associated with rapid hydrologic responses to rainfall or snowmelt. 
        
        In this framework, an event is defined using a seasonally derived event threshold (Qx)computed as the product of the mean 
        baseflow obtained from the Lyne–Hollick recursive filter and a dimensionless scaling factor (λ) that incorporates drainage 
        induced flashiness and baseflow amplification effects. Seasonal thresholds are computed separately to account for intra-annual
        hydrologic variability.

    **Base Flow** \n
        Base Flow is the sustained, low-intensity component of subsurface drainage that represents delayed soil water and shallow
        groundwater release outside of rapid drainage activation periods.

        Flows at or below the seasonally derived event threshold (Qx) are classified as base flow. During identified events, base flow
        is estimated by linear interpolation between the event start and end points to represent the underlying slow-response
        contribution within the composite signal.
                    
    **Event Start and End Points** \n
        An event is initiated when the drainage discharge (a) exceeds the seasonal event threshold (Qx) and (b) increases by at least 20%
        relative to the preceding time step, ensuring that the identified signal represents a hydrologically meaningful activation rather 
        than noise.
        """)
    st.markdown(
    "[see Help interface for date formatting](https://event-package-website.web.app/help)",
    unsafe_allow_html=True
)

    # File uploader
    with st.expander("📂 Upload Data", expanded=True):
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file:
            is_valid, message = validate_csv(uploaded_file)
            if is_valid:
                st.success("File uploaded successfully!")
            else:
                st.markdown(f'<div class="error">{message}</div>', unsafe_allow_html=True)

    # Data configuration
    st.markdown("")
    st.markdown("If your dataset does not contain Temperature or Water Table columns, please turn off those options to prevent errors..")
    with st.expander("⚙️ Data Configuration"):
        col1, col2, col3 = st.columns(3)
        # col1, col2 = st.columns(2)
        with col1:
            heading = st.radio("Does your data have a header?", ('Yes', 'No'), format_func=lambda x: 'Yes' if x == 'Yes' else 'No')
        with col2:
            water_table = st.radio("Has water table data?", ('Yes', 'No'), format_func=lambda x: 'Yes' if x == 'Yes' else 'No')
        with col3:
            water_temp = st.radio("Has water temperature data?", ('Yes', 'No'), format_func=lambda x: 'Yes' if x == 'Yes' else 'No')

    # Analysis settings
    st.markdown("")
    st.markdown("Remember to use the recommendations from the event threshold analysis")
    with st.expander("🔍 Analysis Settings"):
        col1, col2 = st.columns(2)
        with col1:
            Analysis = st.radio("Analysis Type", ('Daily', 'Hourly'), format_func=lambda x: x.lower())
        with col2:
            season_deli = st.radio("Season Delineation Method", ('A', 'B'))

        st.subheader("Seasonal Thresholds (cm/day or mm/day)")
        col3, col4, col5, col6 = st.columns(4)
        with col3:
            winterr = st.number_input("Winter Threshold", min_value=0.0, step=0.1, value=0.2, format="%.3f")
        with col4:
            springg = st.number_input("Spring Threshold", min_value=0.0, step=0.1, value=0.3, format="%.3f")
        with col5:
            summerr = st.number_input("Summer Threshold", min_value=0.0, step=0.1, value=0.1, format="%.3f")
        with col6:
            falll = st.number_input("Fall Threshold", min_value=0.0, step=0.1, value=0.2, format="%.3f")

        st.subheader("Field Area")
        col7 = st.columns(1)[0]
        with col7:
            field_area = st.number_input("Field Area (Units for Events: m²/ha/acre/km²)", min_value=0.0, step=0.1, value=1.0, format="%.3f")
    # Run analysis button
    if st.button("🚀 Run Analysis"):
        if not uploaded_file:
            st.markdown('<div class="error">Please upload a CSV file.</div>', unsafe_allow_html=True)
        else:
            is_valid, message = validate_csv(uploaded_file)
            if not is_valid:
                st.markdown(f'<div class="error">{message}</div>', unsafe_allow_html=True)
                return
            
            try:
                # Debug: Inspect uploaded file content
                uploaded_file.seek(0)
                file_content = uploaded_file.read().decode('utf-8', errors='ignore')
                if not file_content.strip():
                    st.markdown('<div class="error">Uploaded file is empty.</div>', unsafe_allow_html=True)
                    return
                
                # Save uploaded file
                with open("temp.csv", "wb") as f:
                    uploaded_file.seek(0)
                    f.write(uploaded_file.getbuffer())
                
                # Debug: Verify temp.csv content
                with open("temp.csv", "r") as f:
                    temp_content = f.read()
                    if not temp_content.strip():
                        st.markdown('<div class="error">Temporary CSV file is empty.</div>', unsafe_allow_html=True)
                        return

                ID = ''
                if Analysis == 'Daily':
                    result = daily_events("temp.csv", heading, water_table, water_temp, winterr, springg, summerr, falll, season_deli, field_area)
                    ID += f'Res-D_'
                    ID += f'Sea-{season_deli}_'
                    ID += f'Win-{winterr}_'
                    ID += f'Spr-{springg}_'
                    ID += f'Sum-{summerr}_'
                    ID += f'Fal-{falll}'
                    st.write(f'Your Analysis Configuration ID is: {ID}')
                else:
                    result = hourly_events("temp.csv", heading, water_table, water_temp, winterr, springg, summerr, falll, season_deli, field_area)
                    ID += f'Res-H_'
                    ID += f'Sea-{season_deli}_'
                    ID += f'Win-{winterr}_'
                    ID += f'Spr-{springg}_'
                    ID += f'Sum-{summerr}_'
                    ID += f'Fal-{falll}'
                    st.write(f'Your Analysis Configuration ID is: {ID}')
               
            except Exception as e:
                st.markdown(f'<div class="error">Error: {str(e)}</div>', unsafe_allow_html=True)



if __name__ == "__main__":
    main() 
