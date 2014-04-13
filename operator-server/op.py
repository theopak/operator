from telapi import rest, inboundxml
import requests
from settings import account_sid, auth_token

client  = rest.Client(account_sid, auth_token)
account = client.accounts[client.account_sid]

def place_call(phone, uid, sequence):
    call  = account.calls.create( 
        from_number = '+16176844744', 
        to_number = phone, 
        url = 'http://happyoperator.com/inbound/connected/'+str(uid)+'/'+sequence
    )
    return "success"

def press_buttons(sid, uid, sequence):
    # call  = account.calls[str(sid)]
    # call.play_dtmf = sequence
    # call.save()

    r = requests.post('https://api.telapi.com/v1/Accounts/AC6c8890845673e4b306e74e16990b475d/Calls/'+sid+'.json', auth=(account_sid, auth_token), data={'PlayDtmf': sequence})
    pause_duration = int(len(sequence) * 0.5 + 1)
    return '<?xml version="1.0"?>\n' + str(inboundxml.Response(
        inboundxml.Pause(length=pause_duration),
        inboundxml.Redirect(
            'http://happyoperator.com/inbound/waiting/'+str(uid),
            method = 'POST'
        ),
    ))

def loop_human_check(uid):
    return '<?xml version="1.0"?>\n' + str(inboundxml.Response(
        inboundxml.Gather(
            inboundxml.Play(
                "http://happyoperator.com/static/wav/press-zeroSwiftAlphaOne.wav",
            ),
            action      = 'http://happyoperator.com/inbound/complete/'+str(uid),
            method      = 'GET',
            numDigits   = 1,
            timeout     = 20,
            finishOnKey = '#',
        ),
        inboundxml.Redirect(
            'http://happyoperator.com/inbound/waiting/'+str(uid),
            method = 'POST'
        ),
    ))

def call_user(user_phone, uid):
    return '<?xml version="1.0"?>\n' + str(inboundxml.Response(
        inboundxml.Record(
            method = 'POST',
            transcribe = True,
            transcribeCallback = 'http://happyoperator.com/inbound/record-complete/'+str(uid),
        ),
        inboundxml.Dial(
            str(user_phone),
        )
    ))