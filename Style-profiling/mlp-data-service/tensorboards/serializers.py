import collections.abc
from typing import Sequence, Mapping, Any
from numpy import isin

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class LaunchTensorboardSerializer(serializers.Serializer):
    experiment_ids = serializers.JSONField()

    def validate_experiment_ids(self, experiment_ids):

        #
        if isinstance(experiment_ids, str):
            experiment_ids = [experiment_ids, ]
        if not isinstance(experiment_ids, collections.abc.Sequence):
            raise ValidationError(f'experiment_ids should be Sequence, but {experiment_ids}')

        #
        experiment_ids = list(set(experiment_ids))
        if len(experiment_ids) == 0:
            raise ValidationError(f'experiment_ids should not be empty, but {experiment_ids}')

        #
        for experiment_id in experiment_ids:
            if not isinstance(experiment_id, str):
                raise ValidationError(f'experiment_ids should be str of Sequence, but {experiment_ids}')

        return experiment_ids
