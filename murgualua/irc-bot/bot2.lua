require("socket")

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

local IRCclient={
	nick = nil,
	user = nil,
	pwd = nil,
	is_go = true,
	debug_mode = nil,
	conn = nil,
	raw_data = nil,
	msg = {},
	
	chanel = {},
	svrhook = {
		["433"] = function(self)
			self.nick = self.nick .. "_"
			self:send("NICK  "..self.nick.."\n")
		end
	},
	prvhook = {},
	
	new = function(self)
		local o = utils.copy(self)
		o.new = nil
		return o
	end,
	 
	send = function(self , raw_data)
		if (self.debug and raw_data) then print(raw_data) end
		if (self.conn) then
			self.conn:send(raw_data)
		else
			error("couldn't send data to a none exists place\n")
		end
	end,
	
	connect = function(self , cfg)
		if cfg.host and cfg.nick then
			if cfg.user == nil then
				cfg.user = cfg.nick
			end
			
			if cfg.port == nil then
				cfg.port = 6667
			end			
			
			self.conn = socket.connect(cfg.host , cfg.port)
			self.conn:settimeout(0.03)
			
			if (cfg.pwd and cfg.pwd ~= "") then
				self.conn:send("PASS  "..cfg.pwd.."\n")
			end
			
			self.nick = cfg.nick
			self.user = cfg.user
			self.pwd =cfg.pwd
			
			self:send("NICK  " .. cfg.nick .. "\n")
			self:send("USER " .. cfg.user .. "  jyf-host-not-real  none none\n")
			
			self.raw_data = self.conn:receive("*l")
		else
			error("you need to set host and nick\n")
		end
	end,
	
	join = function(self,chanel)
		self:send("JOIN "..chanel.."\n")
	end,
	
	part = function(self,chanel)
		self:send("PART "..chanel.."\n")
	end,
	
	run = function(self)
		while self.is_go do
			if (self.debug and self.raw_data) then print(self.raw_data) end
			if self.raw_data then
				self.msg.prefix,self.msg.cmd,self.msg.param = string.match(self.raw_data , "^:(.-)%s+(.-)%s+(.*)")
				if self.msg.prefix then
					if (string.match(self.msg.prefix , "!n=")) then
						self.msg.type = "prv"
						local user = {}
						user.nick,user.user,user.host = string.match(self.msg.prefix , "(.-)!n=(.-)@(.*)")
						self.msg.user = user
						for i in ipairs(self.prvhook) do
							self.prvhook[i](self)
						end
					else
						self.msg.type = "svr"
						if self.svrhook[self.msg.cmd] then
							self.svrhook[self.msg.cmd](self)
						end
					end
				else
					if (string.match(self.raw_data , "^PING")) then
						self:send(string.gsub(self.raw_data , "^PING" , "PONG"))
					end
				end
			end
			self.raw_data = nill
			self.msg={}
			self.raw_data = self.conn:receive("*l")
		end
	end
}

local mycfg = {
	host = 'irc.freenode.net' ,
	nick = 'ymanbot',
	user = 'administor'
}
local mybot = IRCclient:new()
mybot.sapwd = "wuxian"
mybot.debug = true

local admin = {
}

local botcmd = {
	["auth"] = function(self,msg)
		if msg == self.sapwd then
			admin[self.msg.user.nick] = self.msg.user.nick
			self:send("PRIVMSG "..self.msg.user.nick.." :now you are admin\n")
		else
			self:send("PRIVMSG "..self.msg.user.nick.." :sorry,try to auth again?\n")
		end
	end,
	
	["out"] = function(self,msg)
		local nick = self.msg.user.nick
		if admin[nick] then
			self:send("PART "..msg.."\n")
			self:send("PRIVMSG "..nick.." :cmd has sent\n")
		end
	end,
	
	["del"] = function(self,msg)
		local nick = self.msg.user.nick
		if admin[nick] then
			if admin[msg] then
				self:send("PRIVMSG "..nick.." :the user has been deleted!\n")
			else
				self:send("PRIVMSG "..nick.." :this user is not a admin\n")
			end
		end
	end,
	
	["user"] = function(self,msg)
		local nick = self.msg.user.nick
		
		if admin[nick] then
			local users = ''
			for k in pairs(admin) do
				users = users .. k .. ","
			end
			self:send("PRIVMSG "..nick.."  :".. users .."\n")
		end
	end,
	
	["join"] = function(self,msg)
		local nick = self.msg.user.nick
		if admin[nick] then
			self:join(msg)
			self:send("PRIVMSG "..nick.." :cmd has sent\n")
		end
	end,
	
	["raw"] = function(self,msg)
		local nick = self.msg.user.nick
		if admin[nick] then
			self:send(msg.."\n")
			self:send("PRIVMSG "..nick.." :cmd has sent\n")
		end
	end,
	
	["debug"] = function(self,msg)
		local nick = self.msg.user.nick
		if admin[nick] then
			do
				local iobuffer={}
				local raw_print = print
				print = function(p)
					
				end
			end
		end
	end,
	
	["run"] = function(self,msg)
		local nick = self.msg.user.nick
		if admin[nick] then
			local strlen = 0
			local buffer = {}
			
			for k in io.popen(msg):lines() do
				
				if (string.len(k) + strlen) > 490 then
					self:send("PRIVMSG "..nick.." :"..table.concat(buffer ,' | ').."\n")
					strlen = string.len(k)
					buffer = {k}
				else
					strlen = strlen + string.len(k)
					buffer[#buffer+1] = k
				end
			end	
			if buffer then
				print(table.concat(buffer , " | "))
				self:send("PRIVMSG "..nick.." :"..table.concat(buffer , ' | ').."\n")
			end
		end
	end,
}



mybot:connect(mycfg)

table.insert(mybot.prvhook,function(self)
	local msg = self.msg
	local user = msg.user
	if msg.cmd == "JOIN" then
		if user.nick == self.nick then
			self.chanel[string.match(msg.param , "^:(.*)")] = true
		else
			--nothing to do
		end
	end
	
	if msg.cmd == "PART" then
		if user.nick == self.nick then
			self.chanel[string.match(msg.param , "^:(.*)")] = nil
		else
			--nothing to do
		end
	end
	
	if msg.cmd == "PRIVMSG" then
		local target,msg2 = string.match(msg.param , "^(.-)%s-:(.*)")
		--print(target,msg2)
		if target == self.nick then
			local cmd,msg3 = string.match(msg2 , "^(.-)%s(.*)")
			
			if msg3 == nil then
				msg3 = 'NULL'
			end
			
			if cmd == nil then
				cmd = 'NULL'
			end
			

			print(msg2.."\n"..cmd.."\n"..msg3)
			
			if botcmd[cmd] then
				botcmd[cmd](self,msg3)
			end
		else
			if botcmd[msg2] then
				botcmd[msg2](self,'')
			end
			--nothing to do
		end
	end
end)

mybot:join("#bottest")
mybot:join("#ubuntu-cn")

mybot:run()
