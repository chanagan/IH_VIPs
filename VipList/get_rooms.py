import time
import requests

from operator import itemgetter

from VipList.credentials import *

PROPERTY_ID = PROP_ID
BASE_URL = CB_URL
API_KEY = X_API_KEY

CB_GET_RESERVATION = "getReservation"

HEADERS = {"x-api-key": API_KEY,
           "Accept": "application/json",
           "x-property-id": PROPERTY_ID,
           }

def get_rooms(vip_reservations):
    # for each of the reservations, get the guests and rooms
    workingReservations = []
    for reservation in vip_reservations:
        reservationID = reservation["reservationID"]
        start = time.perf_counter()
        response = requests.get(
            f"{BASE_URL}/{CB_GET_RESERVATION}",
            headers=HEADERS,
            params={
                "propertyID": PROPERTY_ID,
                "reservationID": reservationID,
            }
        )
        response.raise_for_status()
        end = time.perf_counter()
        print(f"self.get_rooms: {end - start:.3f} seconds")

        guestRecord = response.json()['data']
        # print(guestRecord)
        guests = guestRecord['guestList']
        tmpGuests = []
        for guest in guests:
            tmpGuest = {}
            tmpGuest['guestID'] = guests[guest]['guestID']
            tmpGuest['guestFirstName'] = guests[guest]['guestFirstName']
            tmpGuest['guestLastName'] = guests[guest]['guestLastName']
            tmpGuest['isMainGuest'] = guests[guest]['isMainGuest']
            # print(tmpGuest)
            tmpGuests.append(tmpGuest)

        # this bit should put the primary guest first in list
        guests_srted = sorted(tmpGuests,
                            key=itemgetter('isMainGuest'),reverse=True)
        assigned = guestRecord['assigned']
        tmpRooms = []
        for rooms in assigned:
            tmpRoom = {}
            tmpRoom['startDate'] = rooms['startDate']
            tmpRoom['roomName'] = rooms['roomName']
            tmpRooms.append(tmpRoom)
            # print(tmpRooms)
        rooms_srted = sorted(tmpRooms,key=itemgetter('startDate'))
        reservation['guests'] = guests_srted
        reservation['rooms'] = rooms_srted

        workingReservations.append(reservation)

    return workingReservations

#         "reservationID": "8176082119429",

if __name__ == '__main__':
    guestList = get_rooms('8176082119429')
    # print(guestList)

# {
#     "success": true,
#     "data": {
#         "propertyID": "310046",
#         "guestName": "Mark Johnston",
#         "guestEmail": "markjohnston693@gmail.com",
#         "isAnonymized": false,
#         "guestList": {
#             "163192582": {
#                 "guestID": "163192582",
#                 "guestFirstName": "Mark",
#                 "guestLastName": "Johnston",
#                 "guestGender": "N/A",
#                 "guestEmail": "markjohnston693@gmail.com",
#                 "guestPhone": "",
#                 "guestCellPhone": "5403253993",
#                 "guestCountry": "US",
#                 "guestAddress": "1276 N Wayne street",
#                 "guestAddress2": "Apt#1007",
#                 "guestCity": "Arlington",
#                 "guestZip": "22201",
#                 "guestState": "Virginia",
#                 "guestStatus": "not_checked_in",
#                 "guestBirthdate": "",
#                 "guestDocumentType": "",
#                 "guestDocumentNumber": "",
#                 "guestDocumentIssueDate": "",
#                 "guestDocumentIssuingCountry": "",
#                 "guestDocumentExpirationDate": "",
#                 "assignedRoom": true,
#                 "roomID": "601917-0",
#                 "roomName": "418 AP1",
#                 "roomTypeName": "AP1 - Lux 1BR Apt, King",
#                 "isMainGuest": true,
#                 "isAnonymized": false,
#                 "taxID": "",
#                 "companyTaxID": "",
#                 "companyName": "",
#                 "customFields": [],
#                 "unassignedRooms": [],
#                 "rooms": [
#                     {
#                         "reservationRoomID": "213187937",
#                         "roomTypeID": "601917",
#                         "roomTypeName": "AP1 - Lux 1BR Apt, King",
#                         "roomTypeIsVirtual": false,
#                         "roomID": "601917-0",
#                         "roomName": "418 AP1",
#                         "subReservationID": "8176082119429"
#                     }
#                 ]
#             },
#             "163192583": {
#                 "guestID": "163192583",
#                 "guestFirstName": "Thomas",
#                 "guestLastName": "Lawson",
#                 "guestGender": "N/A",
#                 "guestEmail": "",
#                 "guestPhone": "",
#                 "guestCellPhone": "",
#                 "guestCountry": "US",
#                 "guestAddress": "",
#                 "guestAddress2": "",
#                 "guestCity": "",
#                 "guestZip": "",
#                 "guestState": "",
#                 "guestStatus": "not_checked_in",
#                 "guestBirthdate": "",
#                 "guestDocumentType": "",
#                 "guestDocumentNumber": "",
#                 "guestDocumentIssueDate": "",
#                 "guestDocumentIssuingCountry": "",
#                 "guestDocumentExpirationDate": "",
#                 "assignedRoom": true,
#                 "roomID": "601917-0",
#                 "roomName": "418 AP1",
#                 "roomTypeName": "AP1 - Lux 1BR Apt, King",
#                 "isMainGuest": false,
#                 "isAnonymized": false,
#                 "taxID": "",
#                 "companyTaxID": "",
#                 "companyName": "",
#                 "customFields": [],
#                 "unassignedRooms": [],
#                 "rooms": [
#                     {
#                         "reservationRoomID": "213187937",
#                         "roomTypeID": "601917",
#                         "roomTypeName": "AP1 - Lux 1BR Apt, King",
#                         "roomTypeIsVirtual": false,
#                         "roomID": "601917-0",
#                         "roomName": "418 AP1",
#                         "subReservationID": "8176082119429"
#                     }
#                 ]
#             }
#         },
#         "reservationID": "8176082119429",
#         "dateCreated": "2026-01-19 18:11:31",
#         "dateModified": "2026-01-20 08:12:53",
#         "source": "Phone",
#         "sourceID": "s-3",
#         "thirdPartyIdentifier": "",
#         "status": "confirmed",
#         "total": 3908.28,
#         "balance": 1954.14,
#         "balanceDetailed": {
#             "suggestedDeposit": "1954.14",
#             "subTotal": 3474,
#             "additionalItems": 0,
#             "taxesFees": 434.28,
#             "grandTotal": 3908.28,
#             "paid": 1954.14
#         },
#         "assigned": [
#             {
#                 "reservationRoomID": "213187937",
#                 "roomTypeName": "AP1 - Lux 1BR Apt, King",
#                 "roomTypeNameShort": "AP1",
#                 "roomTypeIsVirtual": false,
#                 "roomTypeID": "601917",
#                 "subReservationID": "8176082119429",
#                 "startDate": "2026-02-04",
#                 "endDate": "2026-02-10",
#                 "adults": "2",
#                 "children": "0",
#                 "dailyRates": [
#                     {
#                         "date": "2026-02-04",
#                         "rate": 579
#                     },
#                     {
#                         "date": "2026-02-05",
#                         "rate": 579
#                     },
#                     {
#                         "date": "2026-02-06",
#                         "rate": 579
#                     },
#                     {
#                         "date": "2026-02-07",
#                         "rate": 579
#                     },
#                     {
#                         "date": "2026-02-08",
#                         "rate": 579
#                     },
#                     {
#                         "date": "2026-02-09",
#                         "rate": 579
#                     }
#                 ],
#                 "roomTotal": "3474.00",
#                 "marketName": "Retail",
#                 "marketCode": "RTL",
#                 "roomName": "418 AP1",
#                 "roomID": "601917-0"
#             }
#         ],
#         "unassigned": [],
#         "cardsOnFile": [
#             {
#                 "cardID": "87559501",
#                 "cardNumber": "9723",
#                 "cardType": "master"
#             }
#         ],
#         "customFields": [
#             {
#                 "customFieldName": "Returning Guest",
#                 "customFieldValue": "N"
#             }
#         ],
#         "startDate": "2026-02-04",
#         "endDate": "2026-02-10",
#         "allotmentBlockCode": null,
#         "orderId": "",
#         "origin": ""
#     }
# }
