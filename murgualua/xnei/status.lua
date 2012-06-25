#!/home/jyf/bin/murgaLua
-- File: status.lua
-- Date: 2009-10-17
-- Author: jyf
-- Comment: i use it to update my xnei status quickly
--[[
    LICENSE: do what the fuck you want to do to it!
    CONTACT: jyf1987@gmail.com or 80288196@talk.xiaonei.com
--]]

require("socket")
require("mime")

-- get params
-----------------------------------------------------

dofile("cfg.ini")

--print(#arg)

if 0 == #arg then
    print("need at least one params")
    os.exit()
end

if 3 ==  #arg then
    cfg.user = arg[1]
    cfg.pwd = arg[2]
    status = arg[3]
end

if 2 == #arg then
    cfg.pwd = arg[1]
    status = arg[2]
end

if 1 == #arg then
    status = arg[1]
end

-- define some libs
-----------------------------------------------------

function sock_get(sock)
    re = {}
    l = sock:receive(1)
    while l do
        re[#re+1] = l
        l = sock:receive(1)
    end
    return table.concat(re,"")
end

-- define request TPL
-----------------------------------------------------

-- connect request
conn_req = [==[<?xml version="1.0"?>
<stream:stream xmlns:stream="http://etherx.jabber.org/streams"
xmlns="jabber:client" to="talk.xiaonei.com" >
]==]

-- autherization request
auth_str = mime.b64(cfg.user.."@talk.xiaonei.com\000"..cfg.user.."\000"..cfg.pwd)
auth_req = '<auth xmlns="urn:ietf:params:xml:ns:xmpp-sasl" mechanism="PLAIN">'..auth_str..'</auth>'

-- send status 
presence_req = [==[
<presence from="80288196@talk.xiaonei.com" to="80288196@talk.xiaonei.com">
    <status>]==]..status..[==[</status>
</presence>
]==]

-- now working
-----------------------------------------------------

print("connect to server...")
s = socket.connect("talk.xiaonei.com",5222)
s:settimeout(1)

print("server connected!now send hello request")
s:send(conn_req)
--print("conn_req: "..conn_req.."\n")
conn_res = sock_get(s)
--print("conn_res: "..conn_res.."\n")

print("now send login request")
s:send(auth_req)
--print("auth_req: "..auth_req.."\n")
conn_res = sock_get(s)
if conn_res:find("success") then
    print('login success!')
else
    print('login failed!\nplease check your username and password')
    print(cfg.user..':'..cfg.pwd)
    os.exit()
end
--print("conn_res: "..conn_res.."\n")

s:send(presence_req)
print('status has already been sent')
--print("presence_req: "..presence_req.."\n")
--conn_res = sock_get(s)
--print("conn_res: "..conn_res.."\n")
