import re
from PIL import Image
from fastapi import UploadFile
import aiofiles
import pytesseract
from abc import ABC, abstractmethod
from .convert_exception import ConvertException
from models import FileObject, TextFileObject
from pdf2image.pdf2image import convert_from_bytes
from config import TMP_DIR_PATH


class BaseConverter(ABC):
    lang = "rus+eng"
    config = f"--oem 3 --psm 6 -l {lang}"
    storage_path = TMP_DIR_PATH

    @abstractmethod
    async def get_text_file(self, file: FileObject) -> TextFileObject:
        pass


class PDFtoTextConverter(BaseConverter):
    async def get_text_file(self, file: FileObject) -> TextFileObject:
        tmp_images = convert_from_bytes(file.data.read())
        file_name = re.sub(r"\.[^.]+$", ".txt", file.name)
        async with aiofiles.open(self.storage_path + "/" + file_name, "a") as tmp_file:
            for _ in tmp_images:
                text = pytesseract.image_to_string(_, config=self.config)
                await tmp_file.write(text)
        text_obj = TextFileObject(
            name=file_name, path=self.storage_path + "/" + file_name
        )
        return text_obj


class ImagetoTextConverter(BaseConverter):

    async def get_text_file(self, file: FileObject) -> TextFileObject:
        file_name = re.sub(r"\.[^.]+$", ".txt", file.name)
        pil_image = Image.open(file.data)
        async with aiofiles.open(self.storage_path + "/" + file_name, "a") as tmp_file:
            text = pytesseract.image_to_string(pil_image, config=self.config)
            await tmp_file.write(text)
        text_obj = TextFileObject(
            name=file_name, path=self.storage_path + "/" + file_name
        )
        return text_obj


class BaseConverterFactory(ABC):
    @abstractmethod
    def get_converter(self) -> BaseConverter:
        pass


class PDFtoTextConverterFactory(BaseConverterFactory):
    def get_converter(self) -> PDFtoTextConverter:
        return PDFtoTextConverter()


class ImagetoTextConverterFactory(BaseConverterFactory):
    def get_converter(self) -> ImagetoTextConverter:
        return ImagetoTextConverter()


async def entry(file: UploadFile) -> TextFileObject:
    file_name = file.filename
    converter = None
    file_obj = None
    if file_name.endswith("pdf"):
        converter = PDFtoTextConverterFactory().get_converter()
        file_obj = FileObject(name=file_name, data=file.file)
    elif file_name.endswith(("png", "jpeg", "gif", "svg", "psd", "tiff")):
        converter = ImagetoTextConverterFactory().get_converter()
        file_obj = FileObject(name=file_name, data=file.file)
    else:
        raise ConvertException(file_name.split(".")[-1])
    converted_file = await converter.get_text_file(file_obj)
    return converted_file


if __name__ == "__main__":
    print(os.path.abspath("tempor_files"))
    buffer = io.BytesIO()
    with open("../40.pdf", "rb") as file:
        buffer.write(file.read())
    buffer.seek(0)
    file = UploadFile(file=buffer, filename="40.pdf")
    res = asyncio.run(entry(file))
    print(res)
