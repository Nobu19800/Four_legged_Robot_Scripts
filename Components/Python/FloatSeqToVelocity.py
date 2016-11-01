#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file FloatSeqToVelocity.py
 @brief AIST
 @date $Date$

 @author 宮本　信彦　n-miyamoto@aist.go.jp
 産業技術総合研究所　ロボットイノベーション研究センター
 ロボットソフトウエアプラットフォーム研究チーム

 LGPL

"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
floatseqtovelocity_spec = ["implementation_id", "FloatSeqToVelocity", 
		 "type_name",         "FloatSeqToVelocity", 
		 "description",       "AIST", 
		 "version",           "1.0.0", 
		 "vendor",            "AIST", 
		 "category",          "Converter", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 "conf.default.rotation_by_position", "-0.02",
		 "conf.default.velocity_by_position", "0.002",

		 "conf.__widget__.rotation_by_position", "text",
		 "conf.__widget__.velocity_by_position", "text",

         "conf.__type__.rotation_by_position", "double",
         "conf.__type__.velocity_by_position", "double",

		 ""]
# </rtc-template>


class DataListener(OpenRTM_aist.ConnectorDataListenerT):
  def __init__(self, outOut, out, rotation_by_position, velocity_by_position):
    self._outOut = outOut
    self._out = out
    self._rotation_by_position = rotation_by_position
    self._velocity_by_position = velocity_by_position

  def __del__(self):
    pass

  def __call__(self, info, cdrdata):
    data = OpenRTM_aist.ConnectorDataListenerT.__call__(self, info, cdrdata, RTC.TimedFloatSeq(RTC.Time(0,0),[]))
    if len(data.data) >= 2:
        self._out.data.vx = data.data[1] * self._velocity_by_position[0]
        self._out.data.vy = 0
        self._out.data.va = data.data[0] * self._rotation_by_position[0]
        OpenRTM_aist.setTimestamp(self._out)
        self._outOut.write()
    
    


##
# @class FloatSeqToVelocity
# @brief AIST
# 
# TimedFloatSeq型をTimedVelocity2D型に変換します。
# 
# 
class FloatSeqToVelocity(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		#in_arg = [None] * ((len(RTC._d_TimedFloatSeq) - 4) / 2)
		#self._d_in = RTC.TimedFloatSeq(*in_arg)
		self._d_in = RTC.TimedFloatSeq(RTC.Time(0,0),[])
		"""
		変換前のデータ
		 - Type: RTC::TimedFloatSeq
		 - Number: 2
		"""
		self._inIn = OpenRTM_aist.InPort("in", self._d_in)
		
		
		#out_arg = [None] * ((len(RTC._d_TimedVelocity2D) - 4) / 2)
		#self._d_out = RTC.TimedVelocity2D(*out_arg)
		self._d_out = RTC.TimedVelocity2D(RTC.Time(0,0),RTC.Velocity2D(0.0,0.0,0.0))
		"""
		変換後のデータ
		 - Type: RTC::TimedVelocity2D
		 - Unit: m/s, rad/s
		"""
		self._outOut = OpenRTM_aist.OutPort("out", self._d_out)


		
		

		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""
		ジョイスティックのX座標の位置に対する角速度の変化量
		 - Name: rotation_by_position rotation_by_position
		 - DefaultValue: -0.02
		"""
		self._rotation_by_position = [-0.02]
		"""
		ジョイステックのY座標に対する速度の変化量
		 - Name: velocity_by_position velocity_by_position
		 - DefaultValue: 0.002
		"""
		self._velocity_by_position = [0.002]
		
		# </rtc-template>

		self._inIn.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE,DataListener(self._outOut, self._d_out, self._rotation_by_position, self._velocity_by_position))
		 
	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry() 
	# 
	# @return RTC::ReturnCode_t
	# 
	#
	def onInitialize(self):
		# Bind variables and configuration variable
		self.bindParameter("rotation_by_position", self._rotation_by_position, "-0.02")
		self.bindParameter("velocity_by_position", self._velocity_by_position, "0.002")
		
		# Set InPort buffers
		self.addInPort("in",self._inIn)
		
		# Set OutPort buffers
		self.addOutPort("out",self._outOut)
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports
		
		return RTC.RTC_OK
	
		##
		# 
		# The finalize action (on ALIVE->END transition)
		# formaer rtc_exiting_entry()
		# 
		# @return RTC::ReturnCode_t
	
		# 
	def onFinalize(self):
	
		return RTC.RTC_OK
	
		##
		#
		# The startup action when ExecutionContext startup
		# former rtc_starting_entry()
		# 
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onStartup(self, ec_id):
	
		return RTC.RTC_OK
	
		##
		#
		# The shutdown action when ExecutionContext stop
		# former rtc_stopping_entry()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onShutdown(self, ec_id):
	
		return RTC.RTC_OK
	
		##
		#
		# The activated action (Active state entry action)
		# former rtc_active_entry()
		#
		# @param ec_id target ExecutionContext Id
		# 
		# @return RTC::ReturnCode_t
		#
		#
	def onActivated(self, ec_id):
	
		return RTC.RTC_OK
	
		##
		#
		# The deactivated action (Active state exit action)
		# former rtc_active_exit()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onDeactivated(self, ec_id):
	
		return RTC.RTC_OK
	
		##
		#
		# The execution action that is invoked periodically
		# former rtc_active_do()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onExecute(self, ec_id):
	
		return RTC.RTC_OK
	
		##
		#
		# The aborting action when main logic error occurred.
		# former rtc_aborting_entry()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onAborting(self, ec_id):
	
		return RTC.RTC_OK
	
		##
		#
		# The error action in ERROR state
		# former rtc_error_do()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onError(self, ec_id):
	
		return RTC.RTC_OK
	
		##
		#
		# The reset action that is invoked resetting
		# This is same but different the former rtc_init_entry()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onReset(self, ec_id):
	
		return RTC.RTC_OK
	
		##
		#
		# The state update action that is invoked after onExecute() action
		# no corresponding operation exists in OpenRTm-aist-0.2.0
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#

		#
	def onStateUpdate(self, ec_id):
	
		return RTC.RTC_OK
	
		##
		#
		# The action that is invoked when execution context's rate is changed
		# no corresponding operation exists in OpenRTm-aist-0.2.0
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onRateChanged(self, ec_id):
	
		return RTC.RTC_OK
	



def FloatSeqToVelocityInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=floatseqtovelocity_spec)
    manager.registerFactory(profile,
                            FloatSeqToVelocity,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    FloatSeqToVelocityInit(manager)

    # Create a component
    comp = manager.createComponent("FloatSeqToVelocity")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

