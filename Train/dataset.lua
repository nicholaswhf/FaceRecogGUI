
require 'torch'
torch.setdefaulttensortype('torch.FloatTensor')
local ffi=require 'ffi'
local dir=require 'pl.dir'
local argcheck=require 'argcheck'
require 'sys'
require 'xlua'
require 'image'

local dataset=torch.class('dataLoader')
local initcheck=argcheck{
	pack=true,
	help=[[introduce]],
	{check=function(paths)
		local out=true;
		for _,v in ipairs(paths) do
			if type(v) ~='string' then
				print('paths can only be of string input');
				out=false
			end
		end
		return out
	end,
	name='paths',
	type="table",
	help="Multiple paths of directories with images"},
	{name="sampleSize",type="table",help="a consistent sample size to resize the images"},
	{name="split",type="number",help="Percentage of split to go to Trainging"},
	{name="samplingMode",type="string",help="Sample mode:random | balanced",default="balanced"},
	{name="verbose",type="boolean",help="verbose mode during initialization",default=false},
	{name="loadSize",type="table",help="a size to load the images to,initially",opt=true},
	{name="forceClasses",type="table",help="",opt=true},
	{name="sampleHookTrain",type="function",help="applied to sample during training",opt=true},
	{name="sampleHookTest",type="function",help="applied to sample during testing",opt=true},
} 

function dataset:__init(...)
	local args=initcheck(...)
	print(args)
	for k,v in pairs(args) do self[k] =v end
	if not self.sampleHookTrain then self.sampleHookTrain=self.defaultSampleHook end
	if not self.sampleHookTest then self.sampleHookTest=self.defaultSampleHook end

	self.classes={}
	local classPaths={}
	if self.forceClasses then
		for k,v in pairs(self.forceClasses) do
			self.classes[k]=v
			classPaths[k]={}
		end
	end
	local function tableFind(t,o) for k,v in pairs(t) do if v==o then return k end end end
	for _,path in ipat
			end
			if not tableFind(classPaths[idx],dirpath) then
				table.insert(classPaths[idx],dirpath);
			end
		end
	end

	self.classIndices={}
	for k,v in ipairs(self.classes) do
		self.classIndices[v]=k
	end

	local wc='wc'
	local cut='cut'
	local find='find'

	if jit.os=='OSX' then
		wc='gwc'
		cut='gcut'
		find='gfind'
	end

	local extensionList={'jpg','png','JPG','PNG','JPEG','ppm','PPM','bmp','BMP'}
	local findOptions='-iname "*.' .. extensionList[1]..'"'
	for i=2,#extensionList do
		findOptions=findOptions .. '-o -iname "*.' .. extensionList[i] .. '"'
	end
	self.imagePath=torch.CharTensor()
	self.imageClass=torch.LongTensor()
	self.classList={}
	self.classListSample=self.classList

	local classFindFiles={}
	for i=1,#self.classes do
		classFindFiles[i]=os.tmpname()
	end
	local combinedFindList=os.tmpname();
	local tmpfile=os.tmpname()
	local tmphandle=assert(io.open(tmpfile,'w'))
	for i,_ in ipairs(self.classes) do
		for _,path in ipairs(classPaths[i]) do
			local command=find .. '"'.. path ..'"'..findOptions 
				..'>>"' .. classFindFiles[i] ..'"\n'
				tmphandle:write(command)
		end
	end
	io.close(tmphandle)
	os.execute('bash'..tmpfile)
	os.execute('rm -f'..tmpfile)

	tmpfle=os.tmpname()
	tmphandle=assert(io.open(tmpfile,'w'))
	for i=1,#self.classes do
		local command='cat "'..classFindFiles[i] .. '">>'..combinedFindList ..'\n'
		tmphandle:write(command)
	end
	io.close(tmphandle)
	os.execute('bash' .. tmpfile)
	os.execute('rm -f'..tmpfile)

	local maxPathLength=tonumber(sys.fexecute(wc.."-L '" ..combinedFindList .. "' |"..cut .. "-f1 -d ' ' "))
	assert(length>0,"Could not find any image file in the given input paths")
	assert(maxPathLength>0,"paths of files are length 0?")
	self.imgaPath:resize(length,maxPathLength):fill(0)
	local s_data=self.imgaPath:data()
	local count=0
	for line in io.lines(combinedFindList) do
		ffi.copy(s_data,line)
		s_data=s_data+maxPathLength
		if self.verbose and count % 10000 == 0 then
			xlua.progress(count,length)
		end;
		count=count+1
	end

	self.numSamples=self.imagePath:size(1)
	if self.verbose then print(self.numSamples .. 'samples found.') end
	self.imageClass:resize(self.numSamples)
	local runningIndex=0
	for i=1,#self.classes do
		if self,verbose then xlua.progress(i,#(Self.classes)) end
		local clsLength =tonumber(sys.fexecute(wc.."-l '"..classFindFiles[i].."'|"..cut.." -f1 -d''"))
		if clsLength==0 then
			error('Class has zero samples:'..self.classes[i])
		else
			self.classList[i]=torch.range(runningIndex+1,runningIndex+clsLength):long()
			self.imageClass[{{runningIndex+1,runningIndex+clsLength}}]:fill(i)
		end
		runningIndex=runningIndex+clsLength
	end
	local tmpfilelistall=''
	for i=1,#(classFindFiles) do
		tmpfilelistall=tmpfilelistall .. '"' .. classFindFiles[i] .. '"'
		if i %1000==0 then
			os.excute('rm -f' .. tmpfilelistall)
			tmpfilelistall=''
		end
	end
	os.execute('rm -f' .. tmpfilelistall)
	os.execute('rm -f"'..combinedFindList..'"')

	if self.split==100 then
		self.testIndicesSize=0
	else
		print('Splitting training and test sets to a ratio of'..self.split..'/'..(100-self.split))
		



