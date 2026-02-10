import time
import requests
from operator import itemgetter
from datetime import datetime, date
from VipList.credentials import *

PROPERTY_ID = PROP_ID
BASE_URL = CB_URL
API_KEY = X_API_KEY

CB_GET_RESERVATIONS = 'getReservations'

HEADERS = {"x-api-key": API_KEY,
           "Accept": "application/json",
           "x-property-id": PROPERTY_ID,
           }
days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
VIP_DAYS = 6

def computeNights(from_date, to_date):
    from_date = datetime.strptime(from_date, '%Y-%m-%d')
    to_date = datetime.strptime(to_date, '%Y-%m-%d')
    diffDays = (to_date - from_date).days
    return diffDays

def computeDow(from_date):
    from_date = datetime.strptime(from_date, '%Y-%m-%d')
    day_index = from_date.weekday()
    dow = days_of_week[day_index]
    return dow

def get_reservations(from_date, to_date):
    start = time.perf_counter()
    response = requests.get(
        f"{BASE_URL}/{CB_GET_RESERVATIONS}",
        headers=HEADERS,
        params={
            "propertyID": PROP_ID,
            "checkInFrom": from_date,
            "checkInTo": to_date,
        }
    )
    response.raise_for_status()
    end = time.perf_counter()
    print(f"self.get_reservations: {end - start:.3f} seconds")

    vips = []
    reservations = response.json()['data']
    print(f"get_reservations #: {len(reservations)}")
    for reservation in reservations:
        if reservation['status'] == 'canceled':
            # print(reservation)
            continue
        resNights = computeNights(reservation['startDate'], reservation['endDate'])
        if resNights < VIP_DAYS:
            # print(reservation)
            continue
        resDow = computeDow(reservation['startDate'])
        tmpReservation = {}
        tmpReservation['reservationID'] = reservation['reservationID']
        tmpReservation['startDate'] = reservation['startDate']
        tmpReservation['endDate'] = reservation['endDate']
        tmpReservation['guestName'] = reservation['guestName']
        tmpReservation['adults'] = reservation['adults']
        tmpReservation['dow'] = resDow
        tmpReservation['nights'] = resNights
        vips.append(tmpReservation)
    print(f"get_reservations VIP #: {len(vips)}")
    vips_srted = sorted(vips,
                        key=itemgetter('startDate'))
        # vips.append(reservation)
        # print (reservation['guestName'])
    return vips_srted


if __name__ == '__main__':
    vipList = get_reservations()
    print(vipList)

# "data": [
#         {
#             "propertyID": "310046",
#             "reservationID": "8176082119429",
#             "dateCreated": "2026-01-19 18:11:31",
#             "dateModified": "2026-01-20 08:12:53",
#             "status": "confirmed",
#             "guestID": "163192582",
#             "profileID": "190355873050823",
#             "guestName": "Mark Johnston",
#             "startDate": "2026-02-04",
#             "endDate": "2026-02-10",
#             "adults": "2",
#             "children": "0",
#             "balance": 1954.14,
#             "sourceID": "s-3",
#             "sourceName": "Phone",
#             "thirdPartyIdentifier": null,
#             "allotmentBlockCode": null,
#             "groupCode": null,
#             "origin": ""
#         },
#
