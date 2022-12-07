import pytest
from experiments_runner.pipeline import Pipeline

def test_pipeline():

    # constructor
    with pytest.raises(TypeError):
        Pipeline('pipeline_name', './pipeline_root', 'components')

    # method
    pipeline = Pipeline(
        name= 'pipeline_name',
        root= './pipeline_root',
        components= [
            lambda: min(1, 2, 3, 4),
            lambda: max(1, 2, 3, 4),
            list
        ]
    )

    #
    assert len(pipeline) == 3

    # 1st component
    func = pipeline.pop()
    assert callable(func)
    assert func() == 1      # min(1, 2, 3, 4)

    # 2nd component
    func = pipeline.pop()
    assert callable(func)
    assert func() == 4      # max(1, 2, 3, 4)

    # 3rd component
    func = pipeline.pop()
    assert callable(func)
    assert func() == []     # list

    # empty
    assert len(pipeline) == 0
    with pytest.raises(IndexError):
        pipeline.pop()
