import pytest

from models import FileObject
from src.converter.conv import ImagetoTextConverter


@pytest.mark.asyncio
async def test_image_to_text():
    #mock_file = FileObject(name=file_name, data=file.file)
    obj = ImagetoTextConverter()
    obj.get_text_file()
    assert obj == '1'