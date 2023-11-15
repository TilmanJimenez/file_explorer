import xml.etree.ElementTree as ET

from file_explorer import mapping
import datetime
import logging


logger = logging.getLogger(__name__)


def get_parser_from_file(path, encoding=None):
    if encoding:
        with open(path, encoding=encoding) as fid:
            return ET.fromstring(fid.read())
    else:
        return ET.parse(path)


def get_parser_from_string(string):
    return ET.ElementTree(ET.fromstring(string))


def get_sensor_info(tree):
    index = {}
    sensor_info = []
    root = tree

    if tree.find('Instrument'):
        root = tree.find('Instrument').find('SensorArray')

    elif tree.find('InstrumentState'):
        root = tree.find('InstrumentState').find('HardwareData').find('InternalSensors')

    sensors = root.findall('Sensor')
    if not sensors:
        sensors = root.findall('sensor')

    ii = 0
    for i, sensor in enumerate(sensors):
        nr = ''
        par = ''
        typ = ''
        calibration_date = ''
        scale_factor = ''
        vblank = ''
        children = list(sensor)
        if not children:
            continue
        if len(children) > 1:
            par = sensor.attrib['id']
            for child in children:
                if child.tag == 'type':
                    typ = child.text
                elif child.tag == 'SerialNumber':
                    nr = child.text
        else:
            child = children[0]
            par = child.tag
            if par == 'Sensor':
                par = child.attrib['id']
            nr = child.find('SerialNumber').text or ''
            calibration_date = get_datetime_object(child.find('CalibrationDate').text or '')
            scale_factor = child.find('ScaleFactor')
            if scale_factor is not None:
                scale_factor = scale_factor.text
            vblank = child.find('Vblank')
            if vblank is not None:
                vblank = vblank.text
        index.setdefault(par, [])
        index[par].append(ii)
        data = {'parameter': par,
                'serial_number': nr,
                'name': par,
                'type': typ,
                'calibration_date': calibration_date,
                'scale_factor': scale_factor,
                'vblank': vblank,
                }
        sensor_info.append(data)
        ii += 1
    for par, index_list in index.items():
        if len(index_list) == 1:
            continue
        for nr, i in enumerate(index_list):
            sensor_info[i]['parameter'] = f'{sensor_info[i]["parameter"]}_{nr + 1}'
    return sensor_info


def get_instrument(tree):
    return mapping.get_instrument_mapping(tree.find('Instrument').find('Name').text)


def get_instrument_number(tree):
    root = tree

    if tree.find('Instrument'):
        root = tree.find('Instrument').find('SensorArray')

    sensors = root.findall('Sensor')
    if not sensors:
        sensors = root.findall('sensor')

    for sensor in sensors:
        child = list(sensor)[0]
        if child.tag == 'PressureSensor':
            return child.find('SerialNumber').text


def get_hardware_data(tree):
    item = tree.find('InstrumentState').find('HardwareData')
    if not item:
        return
    return item.attrib


def get_datetime_object(date_str):
    if not date_str:
        return ''
    if len(date_str) == 6:
        format_str = '%d%m%y'
    elif len(date_str) == 8 and '-' not in date_str:
        format_str = '%d%m%Y'
    else:
        if '-' in date_str:
            parts = date_str.split('-')
            if parts[1].isalpha():
                parts[1] = parts[1][:3]
        else:
            parts = date_str.split(' ')
        if len(parts[-1]) == 2:
            format_str = '%d-%b-%y'
        else:
            if parts[1].isalpha():
                parts[1] = parts[1][:3]
            format_str = '%d-%b-%Y'
        date_str = '-'.join(parts)
    try:
        return datetime.datetime.strptime(date_str, format_str)
    except ValueError:
        format_str = '%Y-%m-%d'
        return datetime.datetime.strptime(date_str, format_str)

