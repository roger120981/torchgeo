# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

"""Pre-trained YOLO models."""

from typing import Any, cast

import kornia.augmentation as K
import torch.nn as nn
from torchvision.models._api import Weights, WeightsEnum

from ..datasets.utils import lazy_import

# DelineateAnything's image size during training is 512x512 and uses
# multiple image sources of varying resolution. They do not detail their
# normalization method for each source.
_delineate_anything_transforms = K.AugmentationSequential(
    K.Resize(size=(512, 512)), data_keys=None
)


class YOLO_Weights(WeightsEnum):  # type: ignore[misc]
    """YOLO weights.

    For `ultralytics <https://github.com/ultralytics/ultralytics>`_
    *YOLO* implementation.

    .. versionadded:: 0.8
    """

    DELINEATE_ANYTHING = Weights(
        url='https://hf.co/torchgeo/delineate-anything-s/resolve/60bea7b2f81568d16d5c75e4b5b06289e1d7efaf/delineate_anything_rgb_yolo11x-88ede029.pt',
        transforms=_delineate_anything_transforms,
        meta={
            'dataset': 'FBIS-22M',
            'in_chans': 3,
            'num_classes': 1,
            'classes': ('field',),
            'model': 'yolo11x-seg',
            'task': 'segment',
            'encoder': None,
            'input_shape': (3, 512, 512),
            'bands': ['R', 'G', 'B'],
            'publication': 'https://arxiv.org/abs/2409.16252',
            'repo': 'https://github.com/Lavreniuk/Delineate-Anything',
            'resolution': None,
            'license': 'AGPL-3.0',
        },
    )
    DELINEATE_ANYTHING_SMALL = Weights(
        url='https://hf.co/torchgeo/delineate-anything-s/resolve/69cd440b0c5bd450ced145e68294aa9393ddae05/delineate_anything_s_rgb_yolo11n-b879d643.pt',
        transforms=_delineate_anything_transforms,
        meta={
            'dataset': 'FBIS-22M',
            'in_chans': 3,
            'num_classes': 1,
            'classes': ('field',),
            'model': 'yolo11n-seg',
            'task': 'segment',
            'encoder': None,
            'input_shape': (3, 512, 512),
            'bands': ['R', 'G', 'B'],
            'publication': 'https://arxiv.org/abs/2409.16252',
            'repo': 'https://github.com/Lavreniuk/Delineate-Anything',
            'resolution': None,
            'license': 'AGPL-3.0',
        },
    )
    CORE_DINO = Weights(
        url='https://hf.co/torchgeo/core-dino/resolve/59427e13d114cbbf02f4745e1bea7570be3e2057/core_dino_rgb_yolo11x-80ca836f.pt',
        transforms=nn.Identity(),  # transform is handled within ultralytics.YOLO model
        meta={
            'dataset': 'core-five',
            'in_chans': 3,
            'num_classes': None,
            'classes': None,
            'model': 'yolo11x',
            'task': 'bbox',
            'encoder': None,
            'input_shape': (3, -1, -1),  # trained for dynamic input shape
            'bands': ['R', 'G', 'B'],
            'publication': None,
            'repo': 'https://huggingface.co/gajeshladhar/core-dino',
            'resolution': None,
            'license': 'CC-BY-NC-3.0',
        },
    )


def yolo(weights: YOLO_Weights | None = None, *args: Any, **kwargs: Any) -> nn.Module:
    """YOLO model.

    .. versionadded:: 0.8

    Args:
        weights: Pre-trained model weights to use.
        *args: Additional arguments to pass to :class:`ultralytics.YOLO`
        **kwargs: Additional keyword arguments to pass to :class:`ultralytics.YOLO`

    Returns:
        An ultralytics.YOLO model.

    Raises:
        DependencyNotFoundError: If ultralytics is not installed.
    """
    ultralytics = lazy_import('ultralytics')

    if weights:
        kwargs['model'] = weights.url

        if 'task' not in kwargs:
            kwargs['task'] = weights.meta['task']

    model = ultralytics.YOLO(*args, **kwargs)
    return cast(nn.Module, model)
