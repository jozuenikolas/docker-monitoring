import subprocess
import requests

def run_process(exec):
    return subprocess.check_output(exec, shell=True, text=True).rstrip('\n')

def request_dparadig(message, service, criticality):
    bodyParams = {
        "access_token": "7QCZkbrnCqfIJIMkqyLsJd8J2gFuUVmsO9eYtZq2qQQbWQbL==",
        "message":  message,
        "servicio": service,
        "criticidad": criticality,
        "external_id": "test_id"
    }
    url = "https://sni.dparadig.com/api/clientapi/sendNotification"

    resp = requests.post(url,
                    headers = {'Accept': 'application/json'},
                     json = bodyParams)

    print("status_code", resp.status_code)
    print("text", resp.text, "\n")

while True:

    services = run_process('docker container ls --format "{{.Names}}" -a').split('\n')

    for service in services:
        cpu_usage = run_process('docker stats '+ service +' --format "{{.CPUPerc}}" --no-stream').replace('%', '')
        memory_usage = run_process('docker stats '+ service +' --format "{{.MemPerc}}" --no-stream').replace('%', '')
        status = run_process('docker inspect --format="{{.State.Status}}" '+ service)
        message = "El servicio " + service + " se encuentra en estado: " + status + ", uso de CPU: " + cpu_usage + " y uso de memoria: " + memory_usage  
        
        print("Current service:", service)
        print("CPU usage:", cpu_usage)
        print("Memory usage:", memory_usage)
        print("Status:", status)

        criticality = ""

        if status != 'running':
            criticality = "critical"
        else:
            if float(memory_usage) > 66 or float(cpu_usage) > 66:
                criticality = "critical"

            elif float(memory_usage) > 33 or float(cpu_usage) > 33:
                criticality = "major"

            elif float(memory_usage) >= 0 or float(cpu_usage) >= 0:
                criticality = "minor"
                
        print("Criticality:", criticality)
        print("Message", message)

        request_dparadig(message, service, criticality)
    
            


    
