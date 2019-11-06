require 'nn'
require 'dpnn'
require 'optim'

if opt.cuda then
	require 'cunn'
	if opt.cudnn then 
		cudnn.benchmark -opt.cudnn_bench
		cudnn.fastest=true
		cudnn.verbose=false
	end
end

paths.dofile('torch-TripletEmbedding/TripletEmbedding.lua')

local M={}

function M.modelSetup(continue)
	if continue then
		model=continue
	elseif opt.retrain~='none' then
		assert(path.filep(opt.retrain),'file not found:'..opt.retrain)
		model=torch.load(opt.retrain)
	else
		paths.dofile(opt.modelDef)
		model=createModel()
	end

	if torch.type(model)=='nn.DataParallelTable' then
		model=model:get(1)
	end

	criterion=nn.TripletEmbeddingCriterion(opt.alpha)

	optimizeNet(model,opt.imgDim)
	if opt.cuda and opt.nGPU >1 then
		model=makeDataParallel(model,opt.nGPU)
	end

	collectgarbage()
	return model,criterion
end
return M