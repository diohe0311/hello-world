#!/usr/bin/env python3

import os
import unittest
from unittest import mock
from unittest.mock import patch, mock_open
import tempfile

import glob
import hashlib
import multiprocessing
import os
import random
import time

class FanMonitor:
    def __init__(self):
        self.hwmons = []
        self._fan_paths = glob.glob('/sys/class/hwmon/hwmon*/fan*_input')
        for i in self._fan_paths:
            device = os.path.join(os.path.dirname(i), 'device')
            device_path = os.path.realpath(device)
            print("1. device_path: ", device_path)
            if "pci" in device_path:
                pci_class_path = os.path.join(device, 'class')
                print("2. pci_class_path: ", pci_class_path)
                try:
                    with open(pci_class_path, 'r') as _file:
                        pci_class = _file.read().splitlines()
                        pci_device_class = (
                            int(pci_class[0], base=16) >> 16) & 0xff
                        if pci_device_class == 3:
                            continue
                except OSError:
                    print('Not able to access {}'.format(pci_class_path))
                    continue
            self.hwmons.append(i)
            print("3. self.hwmons: ", self.hwmons)
        if not self.hwmons:
            print('Fan monitoring interface not found in SysFS')
            raise SystemExit(0)

    def get_rpm(self):
        result = {}
        for p in self.hwmons:
            try:
                with open(p, 'rt') as f:
                    fan_mon_name = os.path.relpath(p, '/sys/class/hwmon')
                    result[fan_mon_name] = int(f.read())
            except OSError:
                print('Fan SysFS node disappeared ({})'.format(p))
        return result

    def get_average_rpm(self, period):
        acc = self.get_rpm()
        for i in range(period):
            time.sleep(1)
            rpms = self.get_rpm()
            for k, v in acc.items():
                acc[k] += rpms[k]
        for k, v in acc.items():
            acc[k] /= period + 1
        return acc


class FanMonitorTests(unittest.TestCase):
    @mock.patch('glob.glob')
    @mock.patch.object(os.path, 'relpath', autospec=True)
    def test_simple(self, relpath_mock, glob_mock):
        print("")
        print("")
        print("test_simple###")
        with tempfile.TemporaryDirectory() as fake_sysfs:
            fan_input_file = os.path.join(fake_sysfs, 'fan1_input')
            with open(fan_input_file, 'w') as f:
                f.write('150')
            glob_mock.return_value = [fan_input_file]
            relpath_mock.side_effect = ['hwmon4/fan1_input']
            fan_mon = FanMonitor()
            self.assertEqual(fan_mon.get_rpm(), {'hwmon4/fan1_input': 150})

    @mock.patch('glob.glob')
    @mock.patch.object(os.path, 'relpath', autospec=True)
    def test_multiple(self, relpath_mock, glob_mock):
        print("")
        print("")
        print("test_multiple###")
        with tempfile.TemporaryDirectory() as fake_sysfs:
            print("4. fake_sysfs: ", fake_sysfs)
            fan_input_file1 = os.path.join(fake_sysfs, 'fan1_input')
            print("5. fan_input_file1: ", fan_input_file1)
            with open(fan_input_file1, 'w') as f1:
                f1.write('150')
            fan_input_file2 = os.path.join(fake_sysfs, 'fan2_input')
            with open(fan_input_file2, 'w') as f2:
                f2.write('1318')
            glob_mock.return_value = [fan_input_file1, fan_input_file2]
            relpath_mock.side_effect = [
                'hwmon4/fan1_input', 'hwmon6/fan2_input']
            print("6. glob_mock.return_value: ", glob_mock.return_value)
            print("7. relpath_mock.side_effect: ", relpath_mock.side_effect)
            fan_mon = FanMonitor()
            self.assertEqual(
                fan_mon.get_rpm(),
                {'hwmon4/fan1_input': 150, 'hwmon6/fan2_input': 1318})

if __name__ == '__main__':
    unittest.main()
