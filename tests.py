import requests
import time
from concurrent.futures import ThreadPoolExecutor

unique_requests = """/show_adhan_times?timezone=Australia%2FMelbourne&longitude=144.682904&latitude=-37.84028&fajr_isha_method=2&asr_fiqh=hanafi 
/show_adhan_times?timezone=America%2FChicago&longitude=-88.1137&latitude=42.3412&fajr_isha_method=5&asr_fiqh=hanafi
/show_adhan_times?timezone=CET&longitude=4.034497505903098&latitude=49.25108864296843&fajr_isha_method=6&asr_fiqh=jomhor
/show_adhan_times?timezone=US%2FEastern&longitude=-74.2996982&latitude=40.5662568&fajr_isha_method=5&asr_fiqh=hanafi 
/show_adhan_times?timezone=CST6CDT&longitude=-87.9028&latitude=41.9986&fajr_isha_method=1&asr_fiqh=hanafi 
/show_adhan_times?timezone=EST&longitude=-82.255620&latitude=28.352520&fajr_isha_method=1&asr_fiqh=hanafi 
/show_adhan_times?timezone=America%2FChicago&longitude=-88.1137&latitude=42.3412&fajr_isha_method=5&asr_fiqh=hanafi 
/show_adhan_times?timezone=Asia/Kolkata&longitude=77.594566&latitude=12.971599&fajr_isha_method=1&asr_fiqh=hanafi 
/show_adhan_times?timezone=Europe/London&longitude=-0.96096884&latitude=53.620736&fajr_isha_method=5&asr_fiqh=hanafi 
/show_adhan_times?timezone=Asia%2FDubai&longitude=55.732413&latitude=24.235921&fajr_isha_method=1&asr_fiqh=jomhor 
/show_adhan_times?timezone=CET&longitude=4.034497505903098&latitude=49.25108864296843&fajr_isha_method=6&asr_fiqh=jomhor 
/show_adhan_times?timezone=PST8PDT&longitude=-117.6412&latitude=33.5507&fajr_isha_method=5&asr_fiqh=jomhor 
/show_adhan_times?timezone=Canada%2FEastern&longitude=-81.374417&latitude=19.2908&fajr_isha_method=1&asr_fiqh=jomhor 
/show_adhan_times?timezone=EST&longitude=-72.853171&latitude=41.386613&fajr_isha_method=1&asr_fiqh=hanafi 
/show_adhan_times?timezone=EST&longitude=-81.374417&latitude=19.2908&fajr_isha_method=1&asr_fiqh=hanafi 
/show_adhan_times?timezone=Asia%2FDubai&longitude=55.1391981&latitude=24.9641249&fajr_isha_method=1&asr_fiqh=hanafi' 
/show_adhan_times?timezone=Europe%2FBerlin&longitude=9.2368358&latitude=48.8316156&fajr_isha_method=2 
/show_adhan_times?timezone=Europe/Paris&longitude=48.8984474&latitude=2.2481411&fajr_isha_method=1&asr_fiqh=hanafi 
/show_adhan_times?timezone=GMT&longitude=-0.118092&latitude=51.509865&fajr_isha_method=2&asr_fiqh=hanafi 
/show_adhan_times?timezone=America%2FChicago&longitude=-87.883400&latitude=42.033363&fajr_isha_method=1&asr_fiqh=hanafi 
/show_adhan_times?timezone=Europe%2FParis&longitude=4.034497505903098&latitude=49.25108864296843&fajr_isha_method=6&asr_fiqh=jomhor 
/show_adhan_times?timezone=America%2FToronto&longitude=-81.374417&latitude=19.2908&fajr_isha_method=5&asr_fiqh=jomhor 
/show_adhan_times?timezone=EST&longitude=-93.089%207&latitude=44.95&fajr_isha_method=1&asr_fiqh=hanafi 
/show_adhan_times?timezone=Australia%2FSydney&longitude=150.905645&latitude=-33.795779&fajr_isha_method=1&asr_fiqh=hanafi 
/show_adhan_times?timezone=Africa%2FCasablanca&longitude=-6.805117&latitude=34.050058&fajr_isha_method=1&asr_fiqh=jomhor 
/show_adhan_times?timezone=Europe%2FBerlin&longitude=7.288430&latitude=52.786280&fajr_isha_method=2&asr_fiqh=jomhor 
/show_adhan_times?timezone=EST5EDT&longitude=-85.017270&latitude=35.009950&fajr_isha_method=1&asr_fiqh=jomhor 
/show_adhan_times?timezone=Europe/London&longitude=-0.12765&latitude=%2051.5073359%20&fajr_isha_method=5&asr_fiqh=hanafi"""

# /show_adhan_times?timezone=Etc/GMT%2B2&fajr_isha_method=1&asr_fiqh=hanafi  # user did not specify longitude and latitude so user error
# /show_adhan_times?timezone=America%2FLos_Angeles&longitude=34.0522&latitude=118.2437&fajr_isha_method=1&asr_fiqh=jomhor # this gives domain error maybe bad longitude and latitude

def print_unique_requests(content):
    get_query_params = lambda url: url.split("?")[1]
    params_to_dict = lambda params: {key: value for key, value in [param.split("=") for param in params.split("&")] if key not in ["threshold", "name"]}
    query_param_dicts = [params_to_dict(get_query_params(url)) for url in content.split("\n")]
    # now find unique dicts 
    unique_dicts = []
    for query_param_dict in query_param_dicts:
        if query_param_dict not in unique_dicts:
            unique_dicts.append(query_param_dict)
    for query_param in unique_dicts:
        # join the query params
        query_params = "&".join([f"{key}={value}" for key, value in query_param.items()])
        print(f"/show_adhan_times?{query_params}")

old_server = "https://adhantime.khancave.in"
dev_server = "http://localhost:8084"

def test_requests_match():
    old = old_server + unique_requests
    new = dev_server + unique_requests
    old = old.split("\n")
    new = new.split("\n")
    # call the old server
    old_futures = []
    new_futures = []
    get_json_res = lambda url: (url, requests.get(url).json())
    with ThreadPoolExecutor(max_workers=10) as executor:
        for path in unique_requests.split("\n"):
            path = path.strip()
            old_futures.append(executor.submit(get_json_res, old_server + path))
            new_futures.append(executor.submit(get_json_res, new_server + path))
    
    # get the responses
    old_responses = [res.result() for res in old_futures]
    new_responses = [res.result() for res in new_futures]
    

    # compare the responses
    # create a CSV file with the results
    filename = f"test_results-{time.time()}.csv"
    with open(f"{filename}.csv", "w") as f:
        f.write("url,old,new,match\n")
        for old, new in zip(old_responses, new_responses):
            match = old[1] == new[1]
            f.write(f"{old[0]},{old[1]},{new[1]},{match}\n")
# test_requests_match()
