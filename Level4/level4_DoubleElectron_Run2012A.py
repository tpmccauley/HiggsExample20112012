import FWCore.ParameterSet.Config as cms
from RecoMuon.TrackingTools.MuonServiceProxy_cff import *
import FWCore.PythonUtilities.LumiList as LumiList
import FWCore.ParameterSet.Types as CfgTypes
process = cms.Process("Demo")

# intialize MessageLogger and output report
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.categories.append('Demo')
process.MessageLogger.cerr.INFO = cms.untracked.PSet(
        limit = cms.untracked.int32(-1)
        )
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
# **********************************************************************
# set the maximum number of events to be processed                     *
#    this number (argument of int32) is to be modified by the user     *
#    according to need and wish                                        *
#    default is preset to -1 (all events)                              *
# **********************************************************************
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

# set the number of events to be skipped (if any) at end of file below

# define JSON file for 2012 data
goodJSON = '../datasets/Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt'

myLumis = LumiList.LumiList(filename = goodJSON).getCMSSWString().split(',')

# ****************************************************************************
# define the input data set here by inserting the appropriate .txt file list *
# ****************************************************************************
import FWCore.Utilities.FileUtils as FileUtils
#
files = FileUtils.loadListFromFile("../datasets/CMS_Run2012A_DoubleElectron_AOD_22Jan2013-v1_20000_file_index.txt")
files.extend(FileUtils.loadListFromFile("../datasets/CMS_Run2012A_DoubleElectron_AOD_22Jan2013-v1_20008_file_index.txt"))
files.extend(FileUtils.loadListFromFile("../datasets/CMS_Run2012A_DoubleElectron_AOD_22Jan2013-v1_30000_file_index.txt"))

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(*files    
    )    
)

# apply JSON file
#   (needs to be placed *after* the process.source input file definition!)
process.source.lumisToProcess = CfgTypes.untracked(CfgTypes.VLuminosityBlockRange())
process.source.lumisToProcess.extend(myLumis)

# *************************************************
# number of events to be skipped (0 by default)   *
# *************************************************
process.source.skipEvents = cms.untracked.uint32(0)


process.demo = cms.EDAnalyzer('HiggsDemoAnalyzerGit'
)
# ***********************************************************
# output file name                                          *
# default is DoubleMuParked2012C_10000.root                 *
# change this according to your wish                        *
# ***********************************************************
process.TFileService = cms.Service("TFileService",
       fileName = cms.string('DoubleElectron2012A.root')
                                   )

process.p = cms.Path(process.demo)
