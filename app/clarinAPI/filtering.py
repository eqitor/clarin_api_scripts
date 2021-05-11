

class Filtering:

    def get_filters_schema_from_dict(self, metadata: dict) -> dict:
        example = list(metadata.values())[0]
        filters = {}
        for key in example:
            if self._is_date(example[key]):
                filters[key] = {"type": "date",
                                "first": None,
                                "last": None
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

        for file, descr in metadata.items():
            for filter in filters:
                filter_data = filters[filter]
                if filter_data["type"] == "string":
                    filter_data["domain"].add(descr[filter])
                else:
                    if filter_data["first"] > descr[filter]:
                        filter_data["first"] = descr[filter]
                    elif filter_data["last"] < descr[filter]:
                        filter_data["last"] = descr[filter]
        return filters

    def get_files_for_filters(self, filters: dict, filters_schema: dict) -> dict:
        pass

    def _is_date(self, value) -> bool:
        # TODO dates are not implemented yet
        return False

    def _is_string(self, value) -> bool:
        return isinstance(value, str)

    def _is_float(self, value) -> bool:
        return isinstance(value, float)

    def _is_integer(self, value) -> bool:
        return isinstance(value, int)
