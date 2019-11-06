local Threads=require 'threads'

do --
	if opt.nDonkeys>0 then
		local options=opt
		donkeys=Threads(
			opt.nDonkeys,
			function()
				require 'torch'
			end,
			function( idx )
				-- body
				opt=options
				tid=idx
				local seed=opt.manualSeed+idx
				torch.manualSeed(seed)
				paths.dofile('donkey.lua')
			end
		);
	else
		paths.dofile('donkey.lua')
		donkeys={}
		function donkeys:addjob(f1,f2) f2(f1()) end
		function donkeys:synchronize() end
	end
end

nClasses=nil
classes=nil
donkeys:addjob(
	function() return trainLoader.classes end,
	function(c) classes=c end)
donkeys:synchronize()
for key,value in pairs(classes) do
	print(value)
end
nClasses=#classes
assert(nClasses,"Faile to get")
torch.save(paths.concat(opt.save,'classes.t7'),classes)
