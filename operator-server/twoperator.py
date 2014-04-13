from telapi import rest, inboundxml

account_sid = 'AC6c8890845673e4b306e74e16990b475d'
auth_token  = 'fc1d521995724225a4d58f661aa732fc'
client      = rest.Client(account_sid, auth_token)
account     = client.accounts[client.account_sid]

def place_call(phone, sequence):
    call  = account.calls.create( 
        from_number = '+16176844744', 
        to_number = phone, 
        url = 'http://happyoperator.com/inbound/connected/'+sequence 
    )
    return "success"

def push_buttons(sid, sequence):
    # sid = request.form['sid']
    return inboundxml.Response(
        inboundxml.Say(
            "sid",
            voice = 'man',
            loop  = 3
        ),
        inboundxml.Say(
            'Hello, My name is Jane.',
            voice = 'woman'
        ),
        inboundxml.Say(
            'Now I will not stop talking.',
            loop = 3
        )
    )
    