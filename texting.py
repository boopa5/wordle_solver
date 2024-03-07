from twilio.rest import Client

account_sid = 'AC524d3def2bd907b0aced5510c90ec9a8'
auth_token = '07ff83e4087b1ffc35466c193d1e1255'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='+18552478118',
  body='Hello from Twilio',
  to='+18777804236'
)

print(message.sid)