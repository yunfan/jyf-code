--[[

	April 22, 2009

	public domain lua-module for bittorrent-bencoded data
	thanks to Kristofer Karlsson (krka) from #lua on freenode for writing the decoder-functions, islist and isdictionary
	(he obviously did the main part :D)
	encoder written by Moritz Wilhelmy (n0nsense)
	feel free to send your complaints to n0nsense@xinutec.org ;-)
	We don't take responsibility for this code possibly being harmful, incorrect and probably being not the fastest possible implementation.

]]--

module("bencode", package.seeall)

local function islist(t) 
	local n = #t 
	for k, v in pairs(t) do 
		if type(k) ~= "number" or math.floor(k) ~= k or k < 1 or k > n then 
			return false 
		end 
	end 
	for i = 1, n do 
		if t[i] == nil then 
			return false 
		end 
	end 
	return true
end 

local function isdictionary(t) 
	return not islist(t)
end  

function encode(x) -- bencode the value x
	if type(x) == "string" then
		return string.len(x) .. ":" .. x
	elseif type(x) == "number" then
		local x = tostring(math.floor(x)) -- maybe the number is not an integer. we cut the part after the comma
		return "i" .. x .. "e"
	elseif type(x) == "table" then
		local result  -- temporary variable for the result
		if islist(x) then
			result = "l"
			for k, v in ipairs(x) do
				result = result .. encode(v)
			end
			result = result .. "e"
		else -- x is a dictionary
			result = "d"
			-- bittorrent requires the keys to be sorted.
			local sortedkeys = {}
			for k, v in pairs(x) do
				assert(type(k) == "string", "dictionary keys of dictionaries passed to bencode.encode must be strings.")
				sortedkeys[#sortedkeys + 1] = k
			end
			table.sort(sortedkeys)

			for k, v in ipairs(sortedkeys) do
				result = result .. encode(v) .. encode(x[v])
			end
			result = result .. "e"
		end
		return result
	else
		error("Value passed to bencode.encode is of invalid type: " .. type(x))
	end
end

local function decode_integer(s, index) 
	local a, b, int = s:find("^([0-9]+)e", index) 
	assert(int, "not a number: nil") 
	int = tonumber(int) 
	assert(int, "not a number: " .. int) 
	return int, b + 1 
end 
	 
local function decode_list(s, index) 
	local t = {} 
	while s:sub(index, index) ~= "e" do 
		local obj 
		obj, index = decode(s, index) 
		t[#t + 1] = obj 
	end 
	index = index + 1 
	return t, index 
end 
	 
local function decode_dictionary(s, index) 
	local t = {} 
	while s:sub(index, index) ~= "e" do 
		local obj1 
		obj1, index = decode(s, index) 
		local obj2 
		obj2, index = decode(s, index) 
		t[obj1] = obj2 
	end 
	index = index + 1 
	return t, index 
end 
	 
local function decode_string(s, index) 
	local a, b, len = s:find("^([0-9]+):", index) 
	assert(len, "not a length") 
	index = b + 1 
	 
	local v = s:sub(index, index + len - 1) 
	index = index + len 
	return v, index 
end 
	 
	 
function decode(s, index) 
	index = index or 1 
	local t = s:sub(index, index) 
	assert(t) 
	if t == "i" then 
		return decode_integer(s, index + 1) 
	elseif t == "l" then 
		return decode_list(s, index + 1) 
	elseif t == "d" then 
		return decode_dictionary(s, index + 1) 
	elseif t >= '0' and t <= '9' then 
		return decode_string(s, index) 
	else 
		error"invalid type" 
	end 
end

