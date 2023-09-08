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

# ****************************************************************************
# define the input data set here by inserting the appropriate .txt file list *
# ****************************************************************************
import FWCore.Utilities.FileUtils as FileUtils

files = FileUtils.loadListFromFile("../datasets/mc_lists/CMS_MonteCarlo2012_Summer12_DR53X_ZZTo4mu_8TeV-powheg-pythia6_AODSIM_PU_RD1_START53_V7N-v1_20000_file_index.txt")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(*files    
    )
)
#
# *************************************************
# number of events to be skipped (0 by default)   *
# *************************************************
process.source.skipEvents = cms.untracked.uint32(0)


process.demo = cms.EDAnalyzer('HiggsDemoAnalyzerGit'
)

process.TFileService = cms.Service("TFileService",
       fileName = cms.string('ZZto4mu_2012.root')
                                   )

process.p = cms.Path(process.demo)
