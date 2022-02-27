import requests
import json
import yaml
from datetime import datetime
import gmail

with open('./config.yml', 'r') as file:
    conf = yaml.safe_load(file)

lastName = conf['icbc']['drvrLastName']
licenceNumber = conf['icbc']['licenceNumber']
keyword = conf['icbc']['keyword']
expactAfterDate = conf['icbc']['expactAfterDate']
expactBeforeDate = conf['icbc']['expactBeforeDate']
expactAfterTime = conf['icbc']['expactAfterTime']
expactBeforeTime = conf['icbc']['expactBeforeTime']
examClass = str(conf['icbc']['examClass'])

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M"


def getToken():
    login_url = "https://onlinebusiness.icbc.com/deas-api/v1/webLogin/webLogin"
    headers = {'Content-type': 'application/json'}
    payload = {
        "drvrLastName": lastName,
        "licenceNumber": licenceNumber,
        "keyword": keyword
    }
    response = requests.put(login_url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        return response.headers["Authorization"]
    return ""


def getAppointments(token):
    appointment_url = "https://onlinebusiness.icbc.com/deas-api/v1/web/getAvailableAppointments"
    headers = {
        'Content-type': 'application/json',
        'Authorization': token
    }
    point_grey = {
        "aPosID": 9,
        "examType": examClass+"-R-1",
        "examDate": expactAfterDate,
        "ignoreReserveTime": "false",
        "prfDaysOfWeek": "[0,1,2,3,4,5,6]",
        "prfPartsOfDay": "[0,1]",
        "lastName": lastName,
        "licenseNumber": licenceNumber
    }
    response = requests.post(appointment_url, data=json.dumps(point_grey), headers=headers)

    if response.status_code == 200:
        return response.json()
    print('Authorization Error')
    return []


def getAppointmentDate(appointment):
    return appointment["appointmentDt"]["date"]


def appointmentMatchRequirement(appointment):
    appointmentDate = getAppointmentDate(appointment)
    thatDate = datetime.strptime(appointmentDate, DATE_FORMAT)
    beforeDate = datetime.strptime(expactBeforeDate, DATE_FORMAT)

    appointmentTime = appointment["startTm"]
    thatTime = datetime.strptime(appointmentTime, TIME_FORMAT)
    afterTime = datetime.strptime(expactAfterTime, TIME_FORMAT)
    beforeTime = datetime.strptime(expactBeforeTime, TIME_FORMAT)

    return thatDate <= beforeDate and afterTime <= thatTime <= beforeTime


if __name__ == "__main__":
    token = getToken()
    appointments = getAppointments(token)

    mail_header = "Available Dates and Times:"
    mail_content = ""
    prevDate = ""

    for appointment in appointments:
        if (appointmentMatchRequirement(appointment)):
            appointmentDate = getAppointmentDate(appointment)
            appointmentTime = appointment["startTm"]
            if prevDate != appointmentDate:
                mail_content += '\n\n' + appointmentDate + ':'
                prevDate = appointmentDate
            mail_content += '\n\t' + appointmentTime

    if mail_content != "":
        sender_address = conf['gmail']['sender_address']
        sender_pass = conf['gmail']['sender_pass']
        receiver_address = conf['gmail']['receiver_address']
        print(gmail.sendEmail(mail_header+mail_content, sender_address, sender_pass, receiver_address))
    else:
        print('No appointment match the date: '+expactAfterDate+' - ' +
              expactBeforeDate+' at '+expactAfterTime+' - '+expactBeforeTime)
