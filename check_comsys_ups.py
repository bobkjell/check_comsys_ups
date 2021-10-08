#!/usr/bin/env python
#
# Description: Monitor Comsys UPS metrics
# Author: Robert Claesson <rclaesson@itrsgroup.com> 2021
#

# Modules
import argparse, urllib
import xml.etree.ElementTree as ET
from argparse import RawTextHelpFormatter

# Arguments
parser = argparse.ArgumentParser(description='Monitor Comsys UPS metrics using ITRS OP5 Monitor.', formatter_class=RawTextHelpFormatter)
parser.add_argument("-H","--host", help="Hostname/IP to UPS Server.", type=str, required=True)
parser.add_argument("-m","--mode", help="Possible modes are: \nsystem\nload\nbattery\ninput", type=str, required=True)
parser.add_argument("-w","--warning", help="Warning threshold.", type=str, required=False)
parser.add_argument("-c","--critical", help="Critiacl threshold.", type=str, required=False)
parser.add_argument("-s","--submode", help="Possible sub modes are:\nsystem\n\tsite\n\ttime\n\tsw_ver\n\tuptime\nload\n\tvoltage\n\tcurrent\n\tpower\n\tpercent\nbattery\n\tbattery_1\n\tbattery_2\n\tbattery_3\ninput\n\tacdc\n\tsolar\n\ttotal", type=str, required=True)
args = parser.parse_args()

# Get XML
urllib.urlretrieve("http://" + args.host + "/openxml.cgi", "/opt/plugins/custom/comsys.xml")
tree = ET.parse('/opt/plugins/custom/comsys.xml')
root = tree.getroot()

# SI units
u_voltage = "V"
u_current = "A"
u_power = "kW"
u_energy = "kWh"
u_celsius = "C"
u_percent = "%"

# Defaults
exit_code = 0
state_output = "OK: "

# Remove %l from results
def rm_chars(value):
  global s_metric
  s_metric = value.replace('%l', '')
  s_metric = s_metric.replace('%p', '') 
  return s_metric

# Check thresholds
def thresholds(metric):
  global exit_code, state_output
  if metric >= args.critical:
    exit_code = 2
    state_output = "CRITICAL: "
  elif metric >= args.warning:
    exit_code = 1
    state_output = "WARNING: "
  else:
    exit_code = 0
    state_output = "OK: "
  return (exit_code, state_output)

# Check modes and sub-modes
## System
if args.mode == 'system':
  for system in root.iter('system'):
    if args.submode == 'site':
      metric = system[0][0].text
      rm_chars(metric)
      perfdata = " | site=" + s_metric
      print ("System site is: " + s_metric + perfdata)
    elif args.submode == 'time':
      metric = system[0][1].text
      rm_chars(metric)
      perfdata = " | time=" + s_metric
      print ("System time is: " + s_metric + perfdata)
    elif args.submode == 'uptime':
      metric = system[0][3].text
      rm_chars(metric)
      perfdata = " | uptime=" + s_metric
      print ("System uptime is: " + s_metric + perfdata)
    elif args.submode == 'sw_ver':
      metric = system[0][4].text
      rm_chars(metric)
      perfdata = " | sw_ver=" + s_metric
      print ("System software version is: " + s_metric + perfdata)
    else:
      print ("UNKNOWN: Invalid sub mode \"" + args.submode + "\" for mode system.\n")
      parser.print_help()
      exit(3)

## Load
elif args.mode == 'load':
  for load in root.iter('load'):
    if args.submode == 'voltage':
      metric = load[0][0].text + u_voltage
      rm_chars(metric)
      if args.warning or args.critical:
        thresholds(s_metric)
      perfdata = " | voltage=" + s_metric
      print (state_output + "Load voltage is: " + s_metric + perfdata)
      exit(exit_code)
    elif args.submode == 'current':
      metric = load[0][1].text + u_current
      rm_chars(metric)
      if args.warning or args.critical:
        thresholds(s_metric)
      perfdata = " | current=" + s_metric
      print (state_output + "Load current is: " + s_metric + perfdata)
      exit(exit_code)
    elif args.submode == 'power':
      metric = load[0][2].text + u_power
      rm_chars(metric)
      if args.warning or args.critical:
        thresholds(s_metric)
      perfdata = " | power=" + s_metric
      print (state_output +"Load power is: " + s_metric + perfdata)
      exit(exit_code)
    elif args.submode == 'percent':
      metric = load[0][3].text + u_percent
      rm_chars(metric)
      if args.warning or args.critical:
        thresholds(s_metric)
      perfdata = " | percent=" + s_metric
      print (state_output +"Load percent is: " + s_metric + perfdata)
      exit(exit_code)
    else:
      print ("UNKNOWN: Invalid sub mode \"" + args.submode + "\" for mode load.\n")
      parser.print_help()
      exit(3)

## Battery
elif args.mode == 'battery':
  for battery in root.iter('battery'):
    if args.submode == 'battery_1':
      metric_top = battery[0][1].text.replace('%p', '') + u_voltage
      metric_mid = battery[0][2].text.replace('%p', '') + u_voltage
      metric_symm = battery[0][3].text.replace('%p', '')
      metric_temp = battery[0][4].text.replace('%p', '') + u_celsius
      perfdata = " | top=" + metric_top + " mid=" + metric_mid + " symm=" + metric_symm + " temp=" + metric_temp
      print ("Battery 1 is: Top: " + metric_top + " Mid: " + metric_mid + " Symm: " + metric_symm + " Temp: " + metric_temp + perfdata)
      exit(exit_code)
    elif args.submode == 'battery_2':
      metric_top = battery[1][1].text.replace('%p', '') + u_voltage
      metric_mid = battery[1][2].text.replace('%p', '') + u_voltage
      metric_symm = battery[1][3].text.replace('%p', '')
      metric_temp = battery[1][4].text.replace('%p', '') + u_celsius
      perfdata = " | top=" + metric_top + " mid=" + metric_mid + " symm=" + metric_symm + " temp=" + metric_temp
      print ("Battery 2 is: Top: " + metric_top + " Mid: " + metric_mid + " Symm: " + metric_symm + " Temp: " + metric_temp + perfdata)
      exit(exit_code)
    elif args.submode == 'battery_3':
      metric_top = battery[2][1].text.replace('%p', '') + u_voltage
      metric_mid = battery[2][2].text.replace('%p', '') + u_voltage
      metric_symm = battery[2][3].text.replace('%p', '')
      perfdata = " | top=" + metric_top + " mid=" + metric_mid + " symm=" + metric_symm
      print ("Battery 1 is: Top: " + metric_top + " Mid: " + metric_mid + " Symm: " + metric_symm + perfdata)
      exit(exit_code)
    else:
      print ("UNKNOWN: Invalid sub mode \"" + args.submode + "\" for mode battery.\n")
      parser.print_help()
      exit(3)

## Input
elif args.mode == 'input':
  for input in root.iter('input'):
    if args.submode == 'acdc':
      metric_voltage = input[0][1].text.replace('%p', '') + u_voltage
      metric_current = input[0][2].text.replace('%p', '') + u_current
      metric_power = input[0][3].text.replace('%p', '') + u_power
      metric_energy = input[0][4].text.replace('%p', '') + u_energy
      perfdata = " | voltage=" + metric_voltage + " current=" + metric_current + " power=" + metric_power + " energy=" + metric_energy
      print ("Input AC/DC is: Voltage: " + metric_voltage + " Current: " + metric_current + " Power: " + metric_power + " Energy: " + metric_energy + perfdata)
      exit(exit_code)
    elif args.submode == 'solar':
      metric_voltage = input[1][1].text.replace('%p', '') + u_voltage
      metric_current = input[1][2].text.replace('%p', '') + u_current
      metric_power = input[1][3].text.replace('%p', '') + u_power
      metric_energy = input[1][4].text.replace('%p', '') + u_energy
      perfdata = " | voltage=" + metric_voltage + " current=" + metric_current + " power=" + metric_power + " energy=" + metric_energy
      print ("Input solar is: Voltage: " + metric_voltage + " Current: " + metric_current + " Power: " + metric_power + " Energy: " + metric_energy + perfdata)
      exit(exit_code)
    elif args.submode == 'total':
      metric_current = input[2][1].text.replace('%p', '') + u_current
      metric_power = input[2][2].text.replace('%p', '') + u_power
      metric_energy = input[2][3].text.replace('%p', '') + u_energy
      perfdata = " | current=" + metric_current + " power=" + metric_power + " energy=" + metric_energy
      print ("Input total is: Current: " + metric_current + " Power: " + metric_power + " Energy: " + metric_energy + perfdata)
      exit(exit_code)
    else:
      print ("UNKNOWN: Invalid sub mode \"" + args.submode + "\" for mode battery.\n")
      parser.print_help()
      exit(3)

else:
  print ("UNKNOWN: Invalid mode \"" + args.mode + "\"" + "\n")
  parser.print_help()
  exit(3)
