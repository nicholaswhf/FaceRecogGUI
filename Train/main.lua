--#!/usr/bin/env th

require 'torch'
require 'optim'
require 'paths'
require 'xlua'


local opts=paths.dofile('opt.lua')
opt=opts.parse(arg)

if opt.cuda then
	require 'cutorch'
	cutorch.setDevice(opt.device)
end

torch.save(paths.concat(opt.save,'opts.t7'),opt,'ascii')

torch.setdefaulttensortype('torch.FloatTensor')
torch.manualSeed(opt.manualSeed)
paths.dofile('data.lua')
paths.dofile('util.lua')
model=nil
criterion=nil

paths.dofile('train.lua')
paths.dofile('test.lua')

if opt.peoplePerBatch > nClasses then
	print('people per batch > classes')
	os.exit(-1)
end

epoch=opt.epochNumber

for _=1,opt.nEpochs do
	train()
	model=saveModel(model)
	if opt.testing then
		test()
	end
	epoch =epoch+1
end