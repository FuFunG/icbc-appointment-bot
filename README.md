# ICBC Appointment Bot

Robot for checking ICBC road test appointments.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependences.

```bash
pip install PyYAML requests
```

## Config

Create the yaml file `./config.yml`
```yaml
icbc:
  drvrLastName: "YOUR_LAST_NAME"
  licenceNumber: "YOUR_LICENCE_NUMBER"
  keyword: "KEYWORD"
  expactAfterDate: "2022-02-01" #YYYY-MM-DD
  expactBeforeDate: "2022-04-01" #YYYY-MM-DD
  expactAfterTime: "09:00" #HH:MM
  expactBeforeTime: "11:30" #HH:MM
  examClass: 5 #5/7
gmail:
  sender_address: "SENDER_EMAIL@gmail.com"
  sender_pass: "YOUR_EMAIL_PASSWORD"
  receiver_address: "RECEIVER_EMAIL@gmail.com"
```

## Usage

For now, it only support getting the appointments in **Point Grey**
```python
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
```

## Contributing
Feel free to contribute.

1. Able to change location (Now: only Point Grey)
2. Able to choose Day of week