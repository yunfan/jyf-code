socket = require('socket')
http = require('socket.http')
mime = require('mime')

utils={
	copy = function(obj)
		if type(obj)~="table" then
			return obj
		else
			local o={}
			for k,v in pairs(obj) do
				o[k]=utils.copy(v)
			end
			return o
		end
	end,
	
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
}

fanfou = {
	id = '' ,
	pwd = '' ,
	debug = 'off',

	new = function(self , me)
		local o = utils.copy(self)
		o.id = me.id
		o.pwd = me.pwd
		o.new = nil
		return o
	end,

	post = function(self ,url ,msg)
		if self.id and self.pwd then
			qstr = msg
			req = "POST " .. url .. " HTTP/1.1\r\n"
			req = req .. "Host: api.fanfou.com\r\n"
			req = req .. "Authorization: Basic "..mime.b64(self.id .. ":" .. self.pwd ).."\r\n"
			req = req .. "Content-Type: application/x-www-form-urlencoded\r\n"
			req = req .. "Content-Length: "..string.len(qstr).."\r\n\r\n"
			req = req .. qstr

			cl = socket.connect('api.fanfou.com' , 80)
			
			cl:send(req)
			
			if self.debug == 'on' then
				print(req)
				print("\r\n")
			end

			l = cl:receive("*l")
			h = l
			if self.debug == "on" then
				while l do
					print(l)
					if l == '' then
						l = nil
					else
						l = cl:receive("*l")
					end
				end
			end
			cl:close()
			if string.match("200" , h) then
				return true
			else
				return false
			end
		else
			return false
		end
	end,

	update = function(self,msg)
		url = "/statuses/update.json"
		data = 'status='..msg
		r = self:post(url,data)
		return r
	end,

	sendsm = function(self,id,text)
		url = "/direct_messages/new.json"
		data = 'user='..id..'&text='..text
		r = self:post(url,data)
		return r
	end,

	addfrd = function(self,id)
		url = "/friendships/create.json"
		data = "id="..id
		r = self:post(url,data)
		return r
	end
}


yf = fanfou:new({id = 'xxxx' , pwd = 'xxxxx'})
yf:addfrd('chuanye')


--[[
fp = assert(io.open("100.db" , "r"))
l = fp:read("*l")
ct = 0
while l do
	local id = string.match(l , "^id:(.+)%|")
	yf:addfrd(id)
	print(ct)
	ct = ct+1
	l = fp:read("*l")
end
--]]

