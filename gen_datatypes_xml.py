import xml.etree.ElementTree as ET
from astropy.table import Table
from lxml import etree
from xml.dom import minidom
import argparse



def get_data(filename):
    table = Table.read(filename, format="fits")
    table = table.as_array()

    return table

def lxml_generateXML(filepath, name):
    datatypes = etree.Element("datatypes")
    datatype = etree.Element("datatype", id="test1", id_field="PAKTNUMB", time_field="TIME", desc="")
    datatypes.append(datatype)

    table = get_data(filepath)

    names = table.dtype.names

    for i in names:
        if str(table.dtype[i]) == "uint8" or str(table.dtype[i]) == "uint32" or str(table.dtype[i]) or "uint16" or str(table.dtype[i]) == ">i4" or str(table.dtype[i]) == ">i8":
            field = etree.Element("field", name=i, data_shape="scalar", data_type="int")
            datatype.append(field)
        elif str(table.dtype[i]) == ">f8":
            field = etree.Element("field", name=i, data_shape="scalar", data_type="float")
            datatype.append(field)
    xml = etree.tostring(datatypes, pretty_print=True)
    f = open(name, "w")
    f.write(str(xml))
    f.close()

def generateXML(filepath, name):
    datatypes = ET.Element("datatypes")
    datatype = ET.SubElement(datatypes,"datatype", id="test1", id_field="PAKTNUMB", time_field="TIME", desc="")

    table = get_data(filepath)

    names = table.dtype.names

    for i in names:
        if str(table.dtype[i]) == "uint8" or str(table.dtype[i]) == "uint32" or str(table.dtype[i]) or "uint16" or str(table.dtype[i]) == ">i4" or str(table.dtype[i]) == ">i8":
            field = ET.SubElement(datatype, "field", name=i, data_shape="scalar", data_type="int")
        elif str(table.dtype[i]) == ">f8":
            field = ET.SubElement(datatype, "field", name=i, data_shape="scalar", data_type="float")

    rough_string = ET.tostring(datatypes)
    reparsed = minidom.parseString(rough_string)
    f = open(name, "w")
    f.write(reparsed.toprettyxml(indent="  "))
    f.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--filepath", type=str, help="FITS filepath", required=True)
    parser.add_argument("--name", type=str, help="Filename XML", required=True)
    args = parser.parse_args()

    generateXML(args.filepath, args.name)
