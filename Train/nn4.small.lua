imgDim=96
function createModel()
	local net = nn.Sequential()

	net:add(nn.SpatialConvolutionMM(3,64,7,7,2,2,3,3))
	net:add(nn.SpatialBatchNormalization(64))
	net:add(nn.RelU())
	net:add(nn.SpatialMaxPooling(3,3,2,2,1,1))
	net:add(nn.SpatialCrossMapLRN(5,0.0001,0.75))

	net:add(nn.SpatialConvolutionMM(64,64,1,1))
