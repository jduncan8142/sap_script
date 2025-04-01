import os
from pathlib import Path
from typing import Optional
import xml.etree.ElementTree as ET


class Systems:
    def __init__(self, landscape_file: Optional[str | Path] = None) -> None:
        self._landscape_file: str | Path | None = (
            landscape_file
            if landscape_file is not None
            else Path(
                f"C:/Users/{os.getlogin()}/AppData/Roaming/SAP/Common/SAPUILandscape.xml"
            )
        )
        self._available_systems: list[str] = []
        self._landscape_xml: ET.ElementTree | None = None
        self.landscape_xml_root: ET.Element | None = None
        self._includes: list[str] = []
        self.load_landscape_file()
        self.parse_landscape_file()

    def __repr__(self) -> str:
        if isinstance(self.landscape_xml_root, ET.ElementTree):
            return ET.tostring(element=self.landscape_xml_root, encoding="unicode")
        return "No landscape file loaded"

    def __str__(self) -> str:
        if isinstance(self.landscape_xml_root, ET.ElementTree):
            return ET.tostring(element=self.landscape_xml_root, encoding="unicode")
        return "No landscape file loaded"

    def load_landscape_file(self) -> None:
        if not self._landscape_file.exists():
            raise ValueError(
                f"No landscape specified and no file found, at default location: {self._landscape_file}, please specify a valid landscape file."
            )
        try:
            self._landscape_xml = ET.parse(source=self._landscape_file.open(mode="r"))
        except Exception as _:
            raise ValueError(
                f"Error parsing landscape file, at path: {self._landscape_file}"
            )

    def parse_landscape_file(self) -> None:
        if not isinstance(self._landscape_xml, ET.ElementTree):
            raise ValueError(
                "No landscape file loaded, run load_landscape(value='path/to/landscape.xml') first."
            )
        self.landscape_xml_root = self._landscape_xml.getroot()
        for child in self.landscape_xml_root:
            if child.tag == "Services":
                self._available_systems = [gc.attrib["name"] for gc in child]
            elif child.tag == "Includes":
                for include in child:
                    self._includes.append(include.attrib["url"])
        if self._includes is not None:
            for include in self._includes:
                if include.startswith("file://"):
                    include = include[5:]
                    try:
                        include = open(file=include, mode="r")
                    except Exception as _:
                        raise ValueError(f"Error opening include file: {include}")
                try:
                    include_xml = ET.parse(source=include)
                    include_root = include_xml.getroot()
                    for child in include_root:
                        if child.tag == "Services":
                            self._available_systems.extend(
                                [gc.attrib["name"] for gc in child]
                            )
                except Exception as _:
                    raise ValueError(f"Error parsing include file: {include}")

    def available_systems(self) -> list[str]:
        if isinstance(self._available_systems, list):
            return self._available_systems
        elif isinstance(self._landscape_xml, ET.ElementTree):
            self.parse_landscape_file()
            return self._available_systems
        else:
            try:
                self.load_landscape_file()
                self.parse_landscape_file()
                return self._available_systems
            except Exception as _:
                raise ValueError(
                    "No landscape file loaded, run load_landscape(value='path/to/landscape.xml') first."
                )
