require 'optim'
require 'image'
require 'torchx'
local optnet_loaded,optnet=pcall(require,'optnet')
local models=require 'model'
local openFaceOptim=require 'openFaceOptim'

local optimMethod = optim.adam
local optimState={}
local optimator=nil

trainLogger=optim.Logger(paths.concat(opt.save,'train.log'))

local batchNumber
local triplet_loss

function train()
	print('==>doing epoch on training data:')
	print("==>online epoch #" ..epoch)
	batchNumber =0
	model,criterion=models.modelSetup(model)
	optimator=openFaceOptim:__init(model,optimState)
	if opt.cuda then
		cutorch.synchronize()
	end
	model:training()

	local tm=torch.Timer()
	triplet_loss=0

	local i=1
	while batchNumber<opt.epochSize do
		donkeys:addjob(
			function()
				local inputs,numPerClass=trainLoader:samplePeople(opt.peoplePerBatch,opt.imagesPerPerson)
				inputs=inputs:float()
				numPerClass=numPerClass:float()
				return sendTensor(inputs),sendTensor(numPerClass)
			end,
			trainBatch
		)
		if i %5 ==0 then
			donkeys:synchronize()
		end
		i=i+1
	end

	donkeys:synchronize()
	if opt.cuda then
		cutorch.synchronize()
	end

	triplet_loss=triplet_loss/batchNumber

	trainLogger:add{
		['avg triplet loss (train set)']=triplet_loss,
	}
	collectgarbage()
end

function saveModel(model)
	local function checkNans(x,tag)
		local I=torch.ne(x,x)
		if torch.any(I) then
			print("train.lua:Error:NaNs found in:",tag)
			os.exit(-1)
		end
	end

	for j,mod in ipairs(model:listModules()) do
		if torch.typename(mod)=='nn.SpatialBatchNormalization' then
			checkNans(mod.running_mean,string.format("%d-%s-%s",j,mod,'running_mean'))
			checkNans(mod.running_var,string.format("%d-%s-%s",j.mod,'running_var'))
		end
	end
	if opt.cuda then
		if opt.cudnn then
			cudnn.convert(model,nn)
		end
	end

	local dpt
	if torch.type(model)=='nn.DataParallelTable' then
		dpt=model
		model=model:get(1)
	end

	if optnet_loaded then
		optnet.removeOptimization(model)
	end

	torch.save(paths.concat(opt.save,'model_'..epoch..'.t7'),model:float():clearState())
	torch.save(path.concat(opt.save,'optimState_'..epoch..'.t7'),optimState)

	if dpt then
		dpt:clearState()
	end

	collectgarbage()

	return model
end

local inputsCPU=torch.FloatTensor()
local numPerClass=torch.FloatTensor()

local  timer = torch.Timer()

function trainBatch(inputsThread,numPerClassThread)
	collectgarbage()
	if batchNumber>=opt.epochSize then
		return
	end
	if opt.cuda then
		cutorch.synchronize()
	end
	time:reset()

	receiveTensor(inputsThread,inputsCPU)
	receiveTensor(numPerClassThread,numPerClass)

	local inputs
	if opt.cuda then
		inputs=inputsCPU:cuda()
	else
		inputs=inputsCPU
	end

	local numImages=inputs:size(1)
	local embeddings=model:forward(inputs):float()

	local as_table={}
	local ps_table={}
	local ns_table={}

	local triplet_idx={}
	local num_example_per_idx=torch.Tensor(embeddings:size(1))
	num_example_per_idx:zero()

	local tripIdx=1
	local embStartIdx=1
	local numTrips=0`
	for i =1,opt.peoplePerBatch do
		local n=numPerClass[i]
		for j=1,n-1 do
			local aIdx=embStartIdx+j-1
			local diff=embeddings-embeddings[{{aIdx}}]:expandAs(embeddings)
			local norms=diff:norm(2,2):pow(2):squeeze()
			for pair=j,n-1 do
				local pIdx=embStartIdx+pair
				local fff=(embeddings[aIdx]-embeddings[pIdx]):norm(2)
				local normsP=norms-torch.Tensor(embeddings:size(1)):fill(fff*fff)

				normsP[{{embStartIdx,embStartIdx+n-1}}]=normsP:max()
				local in_margin=normsP:lt(opt.alpha)
				local allNeg=torch.find(in_margin,1)
				if table.getn(allNeg)~=0 then
					selNegIdx=allNeg[math.random(table.getn(allNeg))]
					table.insert(as_table,embeddings[aIdx])
					table.insert(ps_table,embeddings[pIdx])
					table.insert(ns_table,embeddings[selNegIdx])

					table.insert(triplet_idx,{aIdx,pIdx,selNegIdx})

					num_example_per_idx[aIdx]=num_example_per_idx[aIdx]+1
					num_example_per_idx[pIdx]=num_example_per_idx[pIdx]+1
					num_example_per_idx[selNegIdx]=num_example_per_idx[selNegIdx]+1
					tripIdx=tripIdx+1
				end
				numTrips=numTrips+1
			end
		end
		embStartIdx=embStartIdx+n
	end
	assert(embStartIdx-1==numImages)
	local nTripsFound = table.getn(as_table)
	if nTripsFound==0 then
		return
	end

	local as=torch.concat(as_table):view(table.getn(as_table),opt.embSize)

