--#!/usr/bin/ th

local gm=assert(require 'graphicsmagick')
paths.dofile('dataset.lua')
paths.dofile('util.lua')
ffi=require 'ffi'

local trainCache =paths.concat(opt.cache,'trainCache.t7')
if not os.execute('cd' .. opt.data) then
	error(("could not chdir to '%s'"):format(opt.data))
end

local loadSize ={3,opt.imgDim,opt.imgDim}
local sampleSize={3,opt.imgDim,opt.imgDim}

local trainHook =function(self,path)
	local input = gm.Image():load(path,self.loadSize[3],self.loadSize[2])
	input:size(self.sampleSize[3],sampleSize[2])
	local out=input

	if torch.uniform() >0.5 then 
		out:flop()
	end
	out=out:toTensor('float','RGB','DHW')
	return out
end

if paths.filep(trainCache) then
	trainLoader=torch.load(trainCache)
	trainLoader.sampleHookTrain=trainHook
else
	trainLoader=dataLoader{
		paths={paths.concat(opt.data)},
		loadSize=loadSize,
		sampleSize=sampleSize,
		split=100,
		verbose=true
	}
	torch.save(trainCache,trainLoader)
	trainLoader.sampleHookTrain=trainHook
end

collectgarbage()

do
	local class=trainLoader.imageClass
	local nClasses=#trainLoader.Classes
	assert(class:max() <=nClasses,"class logic has error")
	assert(class:min()>=1,"class has logic error")
end

