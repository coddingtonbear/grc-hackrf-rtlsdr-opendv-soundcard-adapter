#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Thu Nov  5 08:00:29 2015
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr
import sys
import time

from distutils.version import StrictVersion
class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        try:
             self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
             pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.rtl_rate = rtl_rate = int(2.4e6)
        self.in_frequency_offset = in_frequency_offset = 0
        self.in_frequency = in_frequency = 145.551e6
        self.in_final_gain = in_final_gain = 4
        self.in_audio_inverted = in_audio_inverted = True
        self.dstar_bandwidth = dstar_bandwidth = 6.5e3
        self.audio_rate = audio_rate = int(48e3)

        ##################################################
        # Blocks
        ##################################################
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.rtlsdr_source_0.set_sample_rate(rtl_rate)
        self.rtlsdr_source_0.set_center_freq(in_frequency+in_frequency_offset, 0)
        self.rtlsdr_source_0.set_freq_corr(77, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(10, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna("", 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
          
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=audio_rate*5,
                decimation=rtl_rate,
                taps=None,
                fractional_bw=None,
        )
        self.low_pass_filter_1 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, audio_rate*5, dstar_bandwidth*2, 200, firdes.WIN_HAMMING, 6.76))
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((0-in_final_gain if in_audio_inverted else in_final_gain, ))
        self.audio_sink_0 = audio.sink(audio_rate, "hw:11,0", True)
        self.analog_fm_demod_cf_0 = analog.fm_demod_cf(
        	channel_rate=audio_rate*5,
        	audio_decim=5,
        	deviation=dstar_bandwidth,
        	audio_pass=dstar_bandwidth,
        	audio_stop=dstar_bandwidth+1e3,
        	gain=1,
        	tau=0,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fm_demod_cf_0, 0), (self.blocks_multiply_const_vxx_1, 0))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.audio_sink_0, 0))    
        self.connect((self.low_pass_filter_1, 0), (self.analog_fm_demod_cf_0, 0))    
        self.connect((self.rational_resampler_xxx_1, 0), (self.low_pass_filter_1, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.rational_resampler_xxx_1, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_rtl_rate(self):
        return self.rtl_rate

    def set_rtl_rate(self, rtl_rate):
        self.rtl_rate = rtl_rate
        self.rtlsdr_source_0.set_sample_rate(self.rtl_rate)

    def get_in_frequency_offset(self):
        return self.in_frequency_offset

    def set_in_frequency_offset(self, in_frequency_offset):
        self.in_frequency_offset = in_frequency_offset
        self.rtlsdr_source_0.set_center_freq(self.in_frequency+self.in_frequency_offset, 0)

    def get_in_frequency(self):
        return self.in_frequency

    def set_in_frequency(self, in_frequency):
        self.in_frequency = in_frequency
        self.rtlsdr_source_0.set_center_freq(self.in_frequency+self.in_frequency_offset, 0)

    def get_in_final_gain(self):
        return self.in_final_gain

    def set_in_final_gain(self, in_final_gain):
        self.in_final_gain = in_final_gain
        self.blocks_multiply_const_vxx_1.set_k((0-self.in_final_gain if self.in_audio_inverted else self.in_final_gain, ))

    def get_in_audio_inverted(self):
        return self.in_audio_inverted

    def set_in_audio_inverted(self, in_audio_inverted):
        self.in_audio_inverted = in_audio_inverted
        self.blocks_multiply_const_vxx_1.set_k((0-self.in_final_gain if self.in_audio_inverted else self.in_final_gain, ))

    def get_dstar_bandwidth(self):
        return self.dstar_bandwidth

    def set_dstar_bandwidth(self, dstar_bandwidth):
        self.dstar_bandwidth = dstar_bandwidth
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.audio_rate*5, self.dstar_bandwidth*2, 200, firdes.WIN_HAMMING, 6.76))

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.audio_rate*5, self.dstar_bandwidth*2, 200, firdes.WIN_HAMMING, 6.76))


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    if(StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0")):
        Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)
    tb = top_block()
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None #to clean up Qt widgets
