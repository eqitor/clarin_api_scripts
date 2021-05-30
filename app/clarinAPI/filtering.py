from datetime import datetime
from dateutil.parser import parse, parserinfo
import logging
class Filtering:


    def get_list_of_files_for_filters(self,metadata:dict, boundaries:dict, filters:dict):
        result = metadata
        for filter in boundaries:
            if filters[filter]["type"] == "date":
                converted_last = self.convert_to_datetime(boundaries[filter]["last"])
                converted_first = self.convert_to_datetime(boundaries[filter]["first"])
                result = {k: v for k, v in result.items()
                          if converted_last >= v[filter] >= converted_first}
            elif filters[filter]["type"] == "string":
                result = {k: v for k, v in result.items()
                          if v[filter] in boundaries[filter]["domain"]}
            elif filters[filter]["type"] == "float":
                result = {k: v for k, v in result.items()
                          if boundaries[filter]["last"] >= v[filter] >= boundaries[filter]["first"]}
            elif filters[filter]["type"] == "integer":
                result = {k: v for k, v in result.items()
                          if boundaries[filter]["last"] >= v[filter] >= boundaries[filter]["first"]}
        return result.keys()

    def convert_all_dates_into_datetimes(self, metadata: dict, filters_schema: dict) -> dict:
        for filtr in filters_schema:
            if filters_schema[filtr]["type"] == "date":
                for data in metadata.values():
                    data[filtr] = self.convert_to_datetime(data[filtr])
        return metadata

    def get_filters_schema_from_dict_and_convert_dates(self, metadata: dict) -> dict:
        example = list(metadata.values())[0]
        filters = {}
        logging.warning(f"filtrowanie{example}")
        for key in example:
            if self._is_date(example[key]):
                filters[key] = {"type": "date",
                                "first": self.convert_to_datetime(example[key]),
                                "last": self.convert_to_datetime(example[key])
                                }
            elif self._is_string(example[key]):
                filters[key] = {"type": "string",
                                "domain": set()
                                }
            elif self._is_float(example[key]):
                filters[key] = {"type": "float",
                                "first": example[key],
                                "last": example[key]
                                }
            elif self._is_integer(example[key]):
                filters[key] = {"type": "integer",
                                "first": example[key],
                                "last": example[key]
                                }
            else:
                raise ValueError("filters must be date, string, float or integer")

        metadata = self.convert_all_dates_into_datetimes(metadata, filters)

        for file, descr in metadata.items():
            for filter in filters:
                filter_data = filters[filter]
                if filter_data["type"] == "string":
                    filter_data["domain"].add(descr[filter])
                elif filter_data["type"] == "date":
                    if filter_data["first"] > descr[filter]:
                        filter_data["first"] = descr[filter]
                    elif filter_data["last"] < descr[filter]:
                        filter_data["last"] = descr[filter]
                else:
                    if filter_data["first"] > descr[filter]:
                        filter_data["first"] = descr[filter]
                    elif filter_data["last"] < descr[filter]:
                        filter_data["last"] = descr[filter]
        return filters


    def convert_to_datetime(self,date:str) -> datetime:
        pi = parserinfo(yearfirst=True)
        return parse(date, parserinfo=pi)


    def _is_date(self, value) -> bool:
        if not isinstance(value,str):
            return False
        try:
            parse(value)
            return True
        except ValueError:
            return False

    def _is_string(self, value) -> bool:
        return isinstance(value, str)

    def _is_float(self, value) -> bool:
        return isinstance(value, float)

    def _is_integer(self, value) -> bool:
        return isinstance(value, int)
