# -*- coding: utf-8 -*-
class VolumeBasedCondition(object):

    def __init__(self, period, nr_of_periods, volume):
        self.period = period
        self.nr_of_periods = nr_of_periods
        self.volume = volume

    @classmethod
    def from_dict(cls, json_dict):
        return VolumeBasedCondition(
#     def to_dict(obj):
            json_dict['period'],
            json_dict['nr_of_periods'],
            json_dict['volume'],
        )


        return obj.__dict__

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"VolumeBasedCondition.from_dict({self.to_dict()})"
