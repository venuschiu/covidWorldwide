from configparser import ConfigParser
from datetime import datetime, timedelta
import json
import urllib.parse

def get_api_url(date_filter = None, date_value = None):

    configure = ConfigParser()
    configure.read('config.ini')
    base_url = configure.get("api_params", "base_url")
    params_dic = {}
    params_dic['resource'] = configure.get('api_params','resource')
    params_dic['section'] = configure.get('api_params','section')
    params_dic['format'] = configure.get('api_params','format')


    filter_list = []
    filter_date_col = []
    filter_date_col.append(configure.get('api_params','date_col_index')) 

    if date_filter is None and date_value is None:
        filter_date_col.append(configure.get('api_params','date_col_filter')) 
        filter_date_col.append([ (datetime.now()- timedelta( days= int(configure.get('api_params', 'date_col_time_delta') )))\
                    .strftime("%d/%m/%Y") ])     
    else:
        filter_date_col.append(date_filter) 
        filter_date_col.append([ date_value.strftime("%d/%m/%Y") ])     

    
    filter_list.append(filter_date_col)
    params_dic['filters'] = filter_list 

    json_param = json.dumps(params_dic)
    print(json_param)

    url = base_url + urllib.parse.quote_plus(json_param)
    #print(urllib.parse.quote_plus(params2))
    # print(url)

    return url


print(get_api_url())
print(get_api_url("lt", datetime.now()))

