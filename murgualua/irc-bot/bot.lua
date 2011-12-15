-----------------------------------------------------------------------------------
dofile("mycfg.ini")

isquit=nil
------------------------------Utils------------------------------------------------
split=function(str, pat)
   if (str==nil) then return {"", ""} end
   local t = {} -- NOTE: use {n = 0} in Lua-5.0
   local fpat = "(.-)" .. pat
   local last_end = 1
   local s, e, cap = str:find(fpat, 1)
   while s do
      if s ~= 1 or cap ~= "" then
table.insert(t,cap)
      end
      last_end = e+1
      s, e, cap = str:find(fpat, last_end)
   end
   if last_end <= #str then
      cap = str:sub(last_end)
      table.insert(t, cap)
   end
   return t
end

function sendmsg(u,p,msg)
	local http = require"socket.http"
	local req="status="..msg
	local t={}
	http.request{
		method="POST",
		url="http://api.fanfou.com/statuses/update.xml",
		user = u,
		password = p,
		headers={
			["Content-Length"] = string.len(req),
			["Content-Type"] =  "application/x-www-form-urlencoded"
		},
		source = ltn12.source.string(req),
		--sink=ltn12.sink.table(t),
		redirect=false
	}
	--print(h)
	--[[
	for k,v in pairs(h) do
		print(k.." : "..v)
	end
	--]]
end
------------------------------Irc func---------------------------------------------
function iput(skt,msg)
  skt:send("PRIVMSG "..cfg.chanel.." :"..msg.."\n")
end

function ipong(skt,msg)
	skt:send("PONG "..msg.."\n")
end

function iquit(skt)
	skt:send("QUIT")
	skt:close()
end

function ipart(skt,chanel)
	skt:send("PART "..cfg.chanel)
end

function ijoin(skt,chanel)
	skt:send("JOIN "..chanel)
	cfg.chanel=chanel
end

function onjoin(skt,hstr)
  local usr=string.match(hstr[1],":(.*)!")
  if ((isjoin==nil) and cfg.debug) then
    --cfg.debug=nil
    local chanel=string.match(hstr[3],":(.*)")
    cfg.chanel=chanel
  end
  if (usr==cfg.nick) then
    iput(skt,"Start log!you can see the log on "..cfg.furl)
  end
  print("Event :"..usr.." JOIN "..cfg.chanel)
end

function onquit(skt,hstr)
  local usr=string.match(hstr[1],":(.*)!")
  print("Event :"..usr.." QUIT "..cfg.chanel)
end

function onmsg(skt,hstr)
  local hstr=hstr
  local cmd=nil
  --local isprv=nil
  local usr=string.match(hstr[1],":(.*)!")
  --print(usr)
  if hstr[3]==cfg.nick then
	isprv=true
	--print("prvmsg\n")
  end 
  table.remove(hstr,1)
  table.remove(hstr,1)
  table.remove(hstr,1)
  local msg=table.concat(hstr,"\032")
  if isprv then
	print("!PrvMSG < "..usr.." > "..msg)
	if (msg==":out") then
		iquit(skt)
		isquit=true
	elseif string.match(msg,":%)(.*\032.*)") then
		cmd=string.match(msg,":%)(.*\032.*)")
		--print(cmd)
		skt:send(cmd.."\n")
	else
		sendmsg(cfg.fuser,cfg.fpwd,usr..msg)
		isprv=nil
	end
  else  
	print("< "..usr.." > "..msg)
	sendmsg(cfg.fuser,cfg.fpwd,"["..cfg.chanel.."]<"..usr.."> "..msg)
  end
end
-----------------------------------------------------------------------------------
rd=socket.connect(cfg.host,cfg.port)
rd:settimeout(0.03)

if (cfg.pwd and cfg.pwd~="") then
  rd:send("PASS "..cfg.pwd.."\n")
end

rd:send("USER "..cfg.user.." hi.baidu.com/jyf1987 "..cfg.host.." :"..cfg.user.."\n")

rd:send("NICK "..cfg.nick.."\n")


rd:send("JOIN "..cfg.chanel.."\n")
sendmsg(cfg.fuser,cfg.fpwd,"LOG BEGIN\nChanel: "..cfg.chanel.."\nHost: "..cfg.host.."\nPowered by jyf1987")
s=rd:receive('*l')

while 1 do
  
  if s then
	--[[
    if (string.find(s,"PING"))==1 then 
      print(s)
      ipong(rd)
      s=rd:receive('*l')
    end
    --]]
    local debug=(cfg.debug=="on") and print("Debug: "..s)
    local hstr=split(s,"%s")
    --print(#hstr[2])
---------------------hook event-----------------------------------    
    if hstr[1]=="PING" then
	print("Event :"..s)
	ipong(rd,hstr[2])
	s=rd:receive('*l')
    end
    if hstr[2]=="JOIN" then
      onjoin(rd,hstr)    
    elseif hstr[2]=="PRIVMSG" then
      onmsg(rd,hstr)    
    elseif hstr[2]=="PART" then
      onquit(rd,hstr)
    end

------------------------------------------------------------------    
  end
  if isquit then
	break
  else
	s=rd:receive('*l')
	--murgaLua.sleep(10)
  end
end
sendmsg(cfg.fuser,cfg.fpwd,"LOG END")

