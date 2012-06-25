module('bcode' , package.seeall)

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

Stack = {
    
    first = 0 ,
    
    last = 0,
    
    new=function(self)
        local o=utils.copy(self)
        o.new = nil
        return o
    end,
    
    push=function(self,value)
        self.last = self.last + 1
        self[self.last] = value
        return true
    end,
    
    pop=function(self)
        if self.last > self.first then
            local v = self[self.last]
            self.last = nil
            self.last = self.last - 1
            return v
        else
            return false
        end
    end
}

--[[

local _normal =                    -1
local _event_init =                 0
local _event_type_int_start =       1
local _event_type_int_end =         2
local _event_type_str_start =       3
local _event_type_str_end =         4
local _event_type_list_start =      5
local _event_type_list_end =        6
local _event_type_dict_start =      7
local _event_type_dict_end =        8
local _event_end =                  9

local state = _event_init
local stetes = Stack:new()
--]]


local curr_tb = {}
local curr_tbs = Stack:new()

local parse_handler = {
    ['0'] = str_capture, 
    ['1'] = str_capture, 
    ['2'] = str_capture, 
    ['3'] = str_capture, 
    ['4'] = str_capture, 
    ['5'] = str_capture, 
    ['6'] = str_capture, 
    ['7'] = str_capture, 
    ['8'] = str_capture, 
    ['9'] = str_capture, 
    
    ['i'] = int_capture, 
    ['l'] = list_capture, 
    ['d'] = dict_capture, 
}

getmetatable('x').__call=string.sub


function decode(s)
    if type(s) ~= 'string' then
        return nil
    end
    local res = {}
    curr_tb = res
    tokenize(s)
end


function parse(s,cur=1)
    -- 整数 i([0-9-]+)e
    -- 字符 ([0-9]+) : \1字节  
    -- 列表 l[整数|字符]+e
    -- 字典 d[(整数,字符)]+e
    --[[
    if state > 0 then
        error('wrong state')
    end
    --]]
    local bit = s(cur,1)
    if not bit:match('[ldi0-9]') then
        error('wrong format at '..cur)
    end
    parse_hanler[bit](s,cur)
end

function str_capture(s,cur)
    local num = {}
    while true do
        local bit = s(cur,1)
        if bit:match('[0-9]') then
            num[#num+1] = bit
            cur = cur + 1
        else
            cur = cur + 1 -- 此处  ＋1 因为字符串类型有个:分隔符
            break
        end
    end
    local len = table.concat(num,'')
    len = len + 0
    if len < 1 then
        error('wrong lengh value at '..cur)
    end
    local str = s(cur,len)
    curr_tb[#curr_tb+1] = str
    cur = cur + len
    parse(s,cur)
end

function int_capture(s,cur)
    cur = cur + 1
    local num = {}
    while true do
        local bit = s(cur , 1)
        if bit:match('[0-9]') then
            num[#num+1] = bit
            cur = cur + 1
        else
            cur = cur + 1 -- 此处  ＋1 因为整数类型有个e在最后面
            break
        end
    end
    local int_val = table.concat(num,'')
    int_val = int_val + 0
    curr_tb[#curr_tb+1] = int_val
    parse(s,cur)
end

function list_capture(s,cur)
    new_tb = {}
    curr_tb[#curr_tb + 1] = new_tb
    curr_tbs:push(curr_tb)
    curr_tb = new_tb

end

function dict_capture(s,cur)
    
end
