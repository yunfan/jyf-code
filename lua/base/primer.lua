
primers = {
    ["value"] = 2 ,
    ["next"] =  nil
}

primer_end = primers

count = 0

function is_primer(num)
    local pcount = 0 ;
    --print("\n\nis_primer begin: " , num)
    local current = _G["primers"]
    local stopnum = math.ceil(math.sqrt(num))
    --print("while begin: " , stopnum)
    while current do
	pcount = pcount + 1
	--print("num: ",num,"| count: ",count)
	if current.value > stopnum then
	    --print(current.value , " > " , stopnum)
	    break
	else
	    if (math.fmod(num,current.value) == 0) then
		--print(num , " mod " , current.value , " = " , 0)
		_G['count'] = _G['count'] + pcount
		print(num.."|0|"..pcount)
		return false
	    else
		--print(num , " mod " , current.value , " = " , math.fmod(num,current.value))
		current = current.next
	    end
	end
    end
    
    _G["primer_end"].next = {
	["value"] = num,
	["next"] = nil
    }

    _G["primer_end"] = _G["primer_end"].next
    _G['count'] = _G['count'] + pcount
    print(num.."|1|"..pcount)
    return true
end

local pp = 0
for i = 2,99999999 do
    if is_primer(i) then
	--print(ia)
	pp = pp + 1
    end
end

print("count:",count,"\nall primers:",pp)